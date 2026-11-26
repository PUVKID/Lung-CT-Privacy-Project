"""SCI 변경 경로만 확인하는 CPU 전용 축소 검사입니다. 실제 실험 결과가 아닙니다."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import torch
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import SCI실행 as engine
from SCI모델 import SCIResNet,freeze_running_stats
from SCI공격 import FeatureCodec,membership
from 실행 import read_json,save_json,digest
ROOT=Path(__file__).resolve().parents[1]
torch.set_num_threads(2)

class Tiny(torch.nn.Module):
    def __init__(self,*args,**kwargs):
        super().__init__();self.conv=torch.nn.Conv2d(1,1,1);self.fc=torch.nn.Linear(1,1)
    def forward(self,x): return self.fc(self.conv(x).mean((2,3))).squeeze(1)

class SCI검사(unittest.TestCase):
    def test_01_plan_patient_and_fixed_samples(self):
        config=read_json(ROOT/'SCIconfig.json');plan=engine.experiment_plan(config)
        self.assertEqual(len(plan),45);self.assertEqual(sum(r['kind']=='main' for r in plan),40)
        self.assertEqual(len({r['id'] for r in plan}),45);self.assertEqual(config['samples_per_class'],5000)
        manifest={'splits':{s:[{'id':s+str(y),'patient_id':s+str(y),'label':y,'cohort':'LUNA25'} for y in (0,1)] for s in ('train','validation','test')}}
        self.assertEqual(engine.validate_patient_separation(manifest)['patient_overlap'],0)
        fixed=engine.fixed_test_plan(manifest,{**config,'test_samples_per_class':3})
        self.assertEqual(len(fixed['rows']),6);self.assertEqual(fixed,engine.fixed_test_plan(manifest,{**config,'test_samples_per_class':3}))
        self.assertTrue(all(r['augmentation']=={'hflip':False,'contrast':1.,'brightness':0.} for r in fixed['rows'] if r['canonical']))
        manifest['splits']['test'][0]['patient_id']='train0'
        with self.assertRaisesRegex(ValueError,'중복'): engine.validate_patient_separation(manifest)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'old.json';save_json(path,{'protocol':'stage17-v1'})
            with self.assertRaisesRegex(ValueError,'기존12차'): engine.load_manifest({'manifest':str(path)})

    def test_02_actual_split_gradient(self):
        torch.manual_seed(42);raw=torch.rand(2,1,32,32);labels=torch.tensor([0.,1.])
        for boundary in ('conv1','stem','layer1'):
            whole=SCIResNet('resnet18',0,boundary,pretrained=False);split=copy.deepcopy(whole)
            whole.train();split.train();freeze_running_stats(whole);freeze_running_stats(split)
            output=whole(raw);torch.nn.functional.binary_cross_entropy_with_logits(output,labels).backward()
            actual,_,audit=split.split_loss_backward(raw,labels)
            torch.testing.assert_close(actual,output.detach(),atol=1e-6,rtol=1e-5)
            self.assertTrue(audit['detached']);self.assertGreater(audit['returned_gradient_norm'],0)
            for (name,a),(_,b) in zip(whole.named_parameters(),split.named_parameters()):
                self.assertIsNotNone(a.grad,name);torch.testing.assert_close(a.grad,b.grad,atol=1e-6,rtol=1e-4)
            self.assertEqual(whole.backbone.fc.in_features,512)

    def test_03_actual_rust_feature_packet(self):
        before=torch.cuda.is_initialized();value=torch.linspace(-3,3,256).reshape(1,4,8,8)
        for dtype in ('f32','f16','i8'):
            codec=FeatureCodec(dtype);restored=codec.transfer(value)
            if dtype=='f32': self.assertTrue(torch.equal(value,restored))
            else: self.assertLessEqual(float((value-restored).abs().max()),.013)
            report=codec.report();self.assertEqual(report['count'],1)
            self.assertEqual(report['packet_bytes'],9+value.numel()*{'f32':4,'f16':2,'i8':1}[dtype])
            self.assertGreater(report['sidecar_bytes'],0)
            with self.assertRaises(ValueError): codec.transfer(torch.tensor([float('nan')]))
        self.assertEqual(torch.cuda.is_initialized(),before);self.assertFalse(before)

    def test_04_epoch_resume_and_prediction_trace(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime=Path(tmp);config=read_json(ROOT/'SCIconfig.json')
            config.update(runtime=str(runtime),fixed_samples_root=str(runtime/'fixed'),validation_samples_per_class=1,epochs=2,min_epochs=2,samples_per_class=1,test_samples_per_class=2,batch_size=2,accumulation=1,reserve_gib=0)
            rows={}
            for split in ('train','validation','test'):
                rows[split]=[]
                for label in (0,1):
                    path=runtime/f'{split}_{label}.png';Image.fromarray(np.full((512,512),40+label*160,dtype=np.uint8)).save(path)
                    rows[split].append({'id':split+str(label),'patient_id':split+str(label),'cohort':'LUNA25','label':label,'image_path':str(path),'image_sha256':digest(path),'metadata':{}})
            manifest={'splits':rows,'external':{},'external_status':{}}
            save_json(runtime/'test_plan.json',engine.fixed_test_plan(manifest,config))
            condition=engine.experiment_plan(config)[20];folder=runtime/'conditions'/condition['id']
            original=engine.save_json
            def stop_after_epoch(path,value):
                original(path,value)
                if Path(path).name=='current.json' and value.get('epoch')==1: raise RuntimeError('의도한 epoch 경계 중단')
            protection={'attack':{'privacy_score':None},'examples':[]}
            with patch('SCI모델.SCIResNet',Tiny),patch('SCI공격.run_protection',return_value=protection),patch('SCI공격.run_diagnostics',return_value={'fixture':True}):
                with patch.object(engine,'save_json',side_effect=stop_after_epoch):
                    with self.assertRaisesRegex(RuntimeError,'의도한'): engine.train_condition(config,manifest,condition,'fixture','cpu')
                engine.train_condition(config,manifest,condition,'fixture','cpu',True)
            paths=sorted((folder/'epochs').glob('*.pth'));self.assertEqual(len(paths),2)
            checkpoint=torch.load(paths[-1],weights_only=False)
            for key in ('model','optimizer','scheduler','rng','patience_best','history'): self.assertIn(key,checkpoint)
            result=read_json(folder/'result.json');self.assertEqual(result['classifier']['test']['total'],2);self.assertEqual(result['classifier']['test_generated']['total'],4)
            from 지표 import binary_report
            for name in ('test','test_generated'):
                ref=result['classifier'][name]['predictions'];path=runtime/ref['path'];self.assertEqual(digest(path),ref['sha256'])
                saved=read_json(path)['rows'];report=binary_report([r['label'] for r in saved],[r['rawlogit'] for r in saved])
                for key in ('loss','accuracy','correct','total','confusion_matrix','undefined_reasons'): self.assertEqual(report[key],result['classifier'][name][key])
                self.assertEqual(result['classifier'][name]['n_patients'],2)
            self.assertEqual(read_json(folder/'current.json')['run_id'],'fixture')

    def test_05_membership_patient_label_matching(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows={split:[{'patient_id':split+str(i),'label':label,'value':.2+.6*label} for i in range(count) for label in (0,1)] for split,count in (('train',4),('validation',2),('test',2))}
            rows['external']={}
            with patch.object(engine,'image',side_effect=lambda row:np.full((8,8),row['value'],dtype=np.float32)):
                result=membership(Tiny(),rows,Path(tmp))
            self.assertEqual(result['selection_final_patient_overlap'],0)
            self.assertIsNotNone(result['test_auc']);self.assertEqual(set(result['by_class']),{'OK','NG'})
            self.assertTrue((Path(tmp)/'membership_raw.json').exists());self.assertIsNone(result['external']['CSTL']['auc'])

    def test_06_attack_paths_and_actual_downstream(self):
        import SCI공격 as attacks
        class Exposed(Tiny):
            def __init__(self):
                super().__init__();self.blur=type('Blur',(),{'sigma':0})()
            def observed(self,x): return x*.9
            def features_from_observed(self,x,layer): return torch.nn.functional.avg_pool2d(x,4).repeat(1,3,1,1)
            def logits_from_layer(self,x,layer): return x.mean((1,2,3))*self.conv.weight.flatten()[0]
        class Decoder(torch.nn.Module):
            def forward(self,x): return torch.nn.functional.interpolate(x.mean(1,keepdim=True),size=(32,32),mode='nearest')
        with tempfile.TemporaryDirectory() as tmp:
            runtime=Path(tmp);condition=runtime/'conditions'/'fixture';config=read_json(ROOT/'SCIconfig.json');config['image_size']=32
            rows={split:[{'id':split+str(label),'patient_id':split+str(label),'label':label,'value':.2+.6*label} for label in (0,1)] for split in ('train','validation','test','test_generated')}
            rows['external']={};model=Exposed()
            with patch.object(engine,'image',side_effect=lambda row:np.full((32,32),row['value'],dtype=np.float32)),patch.object(attacks,'_fit',return_value=Decoder()),patch.object(attacks,'_gradient_inverse',return_value=np.full((32,32),.5,dtype=np.float32)),patch.object(attacks,'_raw_gradient_inverse',return_value=(np.full((32,32),.5,dtype=np.float32),{'selected_initialization':'fixture'})):
                photo=attacks.attack_exposure(model,rows,config,condition/'attacks'/'photo','fixture')
                before=digest(condition/'attacks'/'photo'/'result.json')
                feature=attacks.attack_exposure(model,rows,config,condition/'attacks'/'stem'/'f16','fixture','stem','f16')
            self.assertEqual(len(photo['candidate_metrics']),9);self.assertEqual(len(feature['candidate_metrics']),6)
            self.assertEqual(before,digest(condition/'attacks'/'photo'/'result.json'))
            self.assertEqual(feature['classification_from_transmitted_features']['test']['total'],2)
            self.assertGreater(feature['transmission']['packet_bytes'],0)
            for result in (photo,feature):
                for example in result['examples']:
                    self.assertTrue(example['reconstructed'].startswith('conditions/fixture/attacks/'))
                    self.assertTrue((runtime/example['reconstructed']).is_file())

    def test_07_previous_run_complete_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);save_json(root/'config.json',{'regimes':['split_trainable','full_finetune'],'sigmas':[0,32]})
            status={'run_id':'old','experiment_instance_id':'instance','config_sha256':digest(root/'config.json'),'conditions':[]}
            for regime in ('split_trainable','full_finetune'):
                for sigma in (0,32):
                    relative=f'work/results/{regime}_{sigma}.json'
                    save_json(root/relative,{'run_id':'old','experiment_instance_id':'instance','regime':regime,'sigma':sigma,'completed_at':'fixture'})
                    status['conditions'].append({'regime':regime,'sigma':sigma,'status':'completed','result_path':relative})
            path=root/'work/runtime/status.json';save_json(path,status)
            self.assertEqual(engine.require_previous_experiment_complete(root)['conditions'],4)
            unchanged=digest(path);status['conditions'][-1]['status']='pending';save_json(path,status)
            with self.assertRaisesRegex(RuntimeError,'미완료'): engine.require_previous_experiment_complete(root)
            status['conditions'][-1]['status']='completed';save_json(path,status)
            target=root/status['conditions'][0]['result_path'];value=read_json(target);value['run_id']='wrong';save_json(target,value)
            with self.assertRaisesRegex(RuntimeError,'식별자'): engine.require_previous_experiment_complete(root)
            self.assertEqual(digest(path),unchanged)
            path.unlink()
            with self.assertRaises(RuntimeError): engine.require_previous_experiment_complete(root)

    def test_08_compact_and_source_dependencies(self):
        from 실행 import dashboard_projection
        detailed={'run_id':'fixture','linear_inverse_diagnostics_per_source':[{'rank':49,'residual':.0001,'observed_input_mse':.00001}]*150000,'linear_inverse_summary':{'count':150000}}
        compact=dashboard_projection(detailed)
        raw_nested={'feature':{'raw_inverse_diagnostics_per_source':[{'candidates':[{'objective':.01}]}]*2000,'raw_inverse_summary':{'count':2000}}}
        projected=dashboard_projection(raw_nested)
        self.assertNotIn('raw_inverse_diagnostics_per_source',projected['feature']);self.assertEqual(projected['feature']['raw_inverse_summary']['count'],2000)
        self.assertNotIn('linear_inverse_diagnostics_per_source',compact);self.assertEqual(compact['linear_inverse_summary']['count'],150000)
        self.assertGreater(len(json.dumps(detailed)),4*1024**2);self.assertLess(len(json.dumps(compact)),1024)
        with tempfile.TemporaryDirectory() as tmp:
            runtime=Path(tmp);config=read_json(ROOT/'SCIconfig.json');manifest={'splits':{'test':[{'id':str(y),'label':y,'patient_id':str(y)} for y in (0,1)]}}
            manifest={'splits':{split:[{'id':split+str(y),'patient_id':split+str(y),'label':y,'cohort':'LUNA25','metadata':{}} for y in (0,1)] for split in ('train','validation','test')}}
            for split,records in manifest['splits'].items():
                for row in records:
                    image_path=runtime/(row['id']+'.png');Image.fromarray(np.full((32,32),40+row['label']*160,dtype=np.uint8)).save(image_path)
                    row.update(image_path=str(image_path),image_sha256=digest(image_path))
            path=runtime/'manifest.json';save_json(path,manifest);config.update(manifest=str(path),fixed_samples_root=str(runtime/'fixed'),samples_per_class=1,validation_samples_per_class=1,test_samples_per_class=1,image_size=32)
            with patch.object(engine,'runtime_context',return_value={'device':'cpu'}): engine.bind(config,manifest,runtime,'cpu')
            binding=read_json(runtime/'run.json')['binding'];sources=binding['sources']
            for name in ('legacy/model.py','legacy/identity.py','legacy/__init__.py','SCI고정표본.py'): self.assertEqual(sources[name],digest(ROOT/name))
            self.assertEqual(binding['input_policy'],'fixed-copies-v1')
            self.assertEqual(binding['fixed_base_sha256'],digest(runtime/'fixed/base/complete.json'))
            self.assertTrue(all(r['materialized'] and Path(r['image_path']).is_file() and 'augmentation' not in r for r in read_json(runtime/'test_plan.json')['rows']))

    def test_09_feature_decoder_and_diagnostics_few_steps(self):
        import SCI공격 as attacks
        class Exposed(Tiny):
            def observed(self,x): return x
            def features_from_observed(self,x,layer): return torch.nn.functional.avg_pool2d(x,4).repeat(1,3,1,1)
        with tempfile.TemporaryDirectory() as tmp:
            runtime=Path(tmp);config=read_json(ROOT/'SCIconfig.json');config.update(runtime=str(runtime),fixed_samples_root=str(runtime/'fixed'),validation_samples_per_class=1,test_samples_per_class=1,image_size=32,reserve_gib=0,samples_per_class=1,accumulation=1)
            config['reconstruction']={**config['reconstruction'],'epochs':1,'min_epochs':1};config['diagnostics']={**config['diagnostics'],'shuffle_epochs':1}
            rows={split:[{'id':split+str(label),'patient_id':split+str(label),'label':label,'value':.2+.6*label} for label in (0,1)] for split in ('train','validation','test')}
            for split,records in rows.items():
                for row in records:
                    image_path=runtime/(row['id']+'.png');Image.fromarray(np.full((32,32),round(row['value']*255),dtype=np.uint8)).save(image_path)
                    row.update(image_path=str(image_path),image_sha256=digest(image_path),cohort='LUNA25',metadata={})
            def pixels(row): return np.full((32,32),row['value'],dtype=np.float32)
            decoder_folder=runtime/'decoder'
            with patch.object(engine,'image',side_effect=pixels),patch('SCI모델.SCIResNet',Tiny):
                model=attacks._fit(Exposed(),rows,'stem',FeatureCodec('i8'),config,decoder_folder,'fixture',False)
                restored=attacks._fit(Exposed(),rows,'stem',FeatureCodec('i8'),config,decoder_folder,'fixture',True)
                for a,b in zip(model.parameters(),restored.parameters()): self.assertTrue(torch.equal(a,b))
                result=attacks.run_diagnostics({'splits':rows},config,'fixture','cpu',False)
            self.assertEqual(len(list((decoder_folder/'epochs').glob('*.pth'))),1)
            state=torch.load(decoder_folder/'epochs/epoch_0001.pth',weights_only=False)
            for key in ('model','optimizer','scheduler','rng'): self.assertIn(key,state)
            self.assertEqual(set(result['coarse']),{'coarse_full','coarse_center','coarse_outer'})
            self.assertFalse(result['used_for_model_or_attack_selection']);self.assertEqual(result['label_shuffle']['epochs'],1)
            self.assertTrue((runtime/'diagnostics/shuffle_epochs/epoch_0001.pth').exists())
            shuffle=read_json(runtime/'diagnostics/label_shuffle_mapping.json')
            self.assertEqual(shuffle['source_counts_before'],shuffle['source_counts_after'])
            self.assertEqual(shuffle['main_training_labels_changed'],0);self.assertEqual(shuffle['validation_test_labels_changed'],0)
            self.assertNotIn('mapping',result['label_shuffle']['source_label_shuffle'])
            self.assertEqual(result['label_shuffle']['mapping_count'],len(shuffle['mapping']))
            self.assertEqual(result['label_shuffle']['mapping_sha256'],digest(runtime/'diagnostics/label_shuffle_mapping.json'))
            self.assertEqual([[row['label'] for row in rows[split]] for split in ('train','validation','test')],[[0,1],[0,1],[0,1]])

if __name__=='__main__': unittest.main(verbosity=2)
