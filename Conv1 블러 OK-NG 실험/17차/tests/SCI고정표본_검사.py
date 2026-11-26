"""작은 CPU fixture로 고정 사본과 실제 소비 경계를 검사합니다."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tempfile
import unittest
import json
import numpy as np
from PIL import Image
import torch
from 실행 import digest
from SCI고정표본 import prepare_fixed,prepare_sigma,read_raw,read_observed,epoch_rows
from legacy.model import GaussianDCTBlur

class FixedTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.config={'input_policy':'fixed-copies-v1','fixed_samples_root':str(self.root/'fixed'),'samples_per_class':3,
            'validation_samples_per_class':2,'test_samples_per_class':2,'seed':42,'image_size':8,'fixed_blur_batch_size':2}
        self.manifest={'protocol':'stage17-luna25-2d-patient-v2','splits':{},'external':{}}
        for split in ('train','validation','test'):
            rows=[]
            for label in (0,1):
                p=self.root/f'{split}_{label}.png'
                Image.fromarray((np.arange(64).reshape(8,8)*3+label*20).astype('uint8')).save(p)
                rows.append({'id':split+str(label),'patient_id':split,'global_patient_id':split,'label':label,'cohort':'LUNA25',
                    'image_path':str(p),'image_sha256':digest(p),'metadata':{}})
            self.manifest['splits'][split]=rows
    def tearDown(self): self.tmp.cleanup()
    def test_counts_lineage_original_first_and_real_copy(self):
        result=prepare_fixed(self.manifest,self.config)
        self.assertEqual([len(result['splits'][s]) for s in ('train','validation','test')],[6,4,4])
        for split,rows in result['splits'].items():
            self.assertEqual({r['patient_id'] for r in rows},{split})
            for label in (0,1):
                row=next(r for r in rows if r['label']==label)
                source=self.manifest['splits'][split][label]
                self.assertEqual(Path(row['image_path']).read_bytes(),Path(source['image_path']).read_bytes())
                self.assertNotEqual(Path(row['image_path']).stat().st_ino,Path(source['image_path']).stat().st_ino)
                self.assertTrue(row['materialized']);self.assertNotIn('augmentation',row)
    def test_deterministic_base_idempotence_and_tamper_rejection(self):
        first=prepare_fixed(self.manifest,self.config)
        times={r['image_path']:Path(r['image_path']).stat().st_mtime_ns for r in first['splits']['train']}
        self.assertEqual(first,prepare_fixed(self.manifest,self.config))
        self.assertEqual(times,{p:Path(p).stat().st_mtime_ns for p in times})
        self.config['fixed_samples_root']=str(self.root/'other')
        second=prepare_fixed(self.manifest,self.config)
        self.assertEqual([r['image_sha256'] for r in first['splits']['train']],[r['image_sha256'] for r in second['splits']['train']])
        Path(second['splits']['train'][0]['image_path']).write_bytes(b'tampered')
        with self.assertRaises(ValueError): prepare_fixed(self.manifest,self.config)
    def test_changed_input_and_partial_cache_rejected(self):
        prepare_fixed(self.manifest,self.config)
        self.config['seed']=43
        with self.assertRaises(ValueError): prepare_fixed(self.manifest,self.config)
    def test_partial_resume_and_original_observed_identity(self):
        from SCI고정표본 import original_rows
        base=prepare_fixed(self.manifest,self.config)
        (self.root/'fixed/base/complete.json').unlink()
        self.assertEqual(base,prepare_fixed(self.manifest,self.config))
        cached=prepare_sigma(base,self.config,1)
        for row in original_rows(cached['test']):
            fixed=next(r for r in cached['test'] if r['source_id']==row['id'] and r['canonical'])
            self.assertEqual(row['observed_path'],fixed['observed_path'])
    def test_completed_metadata_tamper_rejected(self):
        base=prepare_fixed(self.manifest,self.config)
        prepare_sigma(base,self.config,1)
        sigma=self.root/'fixed/sigmas/sigma_1/complete.json'
        record=json.loads(sigma.read_text(encoding='utf-8'));record['rows']['train'].pop()
        sigma.write_text(json.dumps(record),encoding='utf-8')
        with self.assertRaises(ValueError): prepare_sigma(base,self.config,1)
        index=self.root/'fixed/base/complete.json'
        record=json.loads(index.read_text(encoding='utf-8'));record['splits']['test'].pop()
        index.write_text(json.dumps(record),encoding='utf-8')
        with self.assertRaises(ValueError): prepare_fixed(self.manifest,self.config)
    def test_production_root_rejects_fixture_before_writing(self):
        from unittest.mock import patch
        import SCI고정표본 as fixed
        with patch.object(fixed,'ROOT',self.root),patch.object(fixed,'_sources',return_value={'fixture':'fixed'}):
            self.config['fixed_samples_root']=str(self.root/'work/data/fixed_samples')
            with self.assertRaises(ValueError): prepare_fixed(self.manifest,self.config)
            self.assertFalse(Path(self.config['fixed_samples_root']).exists())
    def test_sigma_float32_matches_reference_and_reuses(self):
        base=prepare_fixed(self.manifest,self.config);result=prepare_sigma(base,self.config,2)
        row=result['train'][0];raw=read_raw(row);observed=read_observed(row)
        expected=GaussianDCTBlur(2)(torch.from_numpy(raw)[None,None])[0,0].numpy()
        np.testing.assert_array_equal(observed,expected)
        self.assertEqual(observed.dtype,np.float32)
        self.assertNotEqual(Path(row['image_path']).stat().st_ino,Path(base['splits']['train'][0]['image_path']).stat().st_ino)
        stamp=Path(row['observed_path']).stat().st_mtime_ns
        self.assertEqual(result,prepare_sigma(base,self.config,2));self.assertEqual(stamp,Path(row['observed_path']).stat().st_mtime_ns)
        Path(row['observed_path']).write_bytes(b'tampered')
        with self.assertRaises(ValueError): prepare_sigma(base,self.config,2)
    def test_epoch_order_only_and_no_online_flip(self):
        from SCI실행 import Dataset
        rows=prepare_fixed(self.manifest,self.config)['splits']['train']
        self.assertEqual(sorted(r['id'] for r in epoch_rows(rows,45)),sorted(r['id'] for r in rows))
        dataset=Dataset(rows,True)
        for _ in range(8): np.testing.assert_array_equal(dataset[0][0][0].numpy(),read_raw(rows[0]))
    def test_model_bypass_and_attack_share_observed(self):
        from SCI모델 import SCIResNet
        from SCI공격 import _source,FeatureCodec
        from SCI실행 import image
        row=prepare_sigma(prepare_fixed(self.manifest,self.config),self.config,2)['train'][0]
        model=SCIResNet('resnet18',2,pretrained=False,preblurred=True)
        def forbidden(*args): raise AssertionError('중복 블러')
        model.blur.forward=forbidden
        target=torch.from_numpy(read_raw(row))[None,None]
        cached=torch.from_numpy(image(row))[None,None]
        np.testing.assert_array_equal(model.observed(cached).numpy(),cached.numpy())
        source,actual,observed=_source(row,model,'photo',FeatureCodec('f32'),False)
        self.assertTrue(torch.equal(actual,target));self.assertTrue(torch.equal(source,cached));self.assertTrue(torch.equal(observed,cached))

if __name__=='__main__': unittest.main(verbosity=2)
