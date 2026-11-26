"""공식 주석과 합성 물리 CT로 자료 계약을 검사한다."""
import collections
import copy
import hashlib
import io
import json
import pickle
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch
from pathlib import Path
import numpy as np
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import SCI데이터 as d

class DataTests(unittest.TestCase):
    def test_official(self):
        p = ROOT / 'work/data/official/LUNA25_Public_Training_Development_Data.csv'
        if not p.exists():
            self.skipTest('공식 주석은 배포에 포함하지 않음')
        rows = d.read_luna_annotations(p)
        self.assertEqual(len(rows), 6163)
        self.assertEqual(len({r['PatientID'] for r in rows}), 2120)
        self.assertEqual(collections.Counter(r['label'] for r in rows), {'0': 5608, '1': 555})

    def test_physical(self):
        z,y,x = np.indices((21,31,41))
        v = (3*x+5*y+7*z).astype(np.float32)
        a = np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]]) @ np.diag([2.,3.,4.])
        origin = np.array([10.,20.,30.])
        center = origin + a @ [20.,15.,10.]
        patch,g = d.extract_physical_patch(v,origin_xyz=origin,index_to_world_xyz=a,center_xyz=center,fov_mm=8,output_size=5)
        self.assertAlmostEqual(float(patch[2,2]),205,places=4)
        self.assertAlmostEqual(float(patch[2,3]),205-5*1.6/3,places=4)
        self.assertEqual(g['outside_fraction'],0)
        with self.assertRaises(d.DataBlocked):
            d.extract_physical_patch(v,origin_xyz=origin,index_to_world_xyz=a,center_xyz=center,fov_mm=256)

    def test_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'meta.npy'
            spacing=np.array([4.,3.,2.])
            direction=np.array([[1.,0.,0.],[0.,0.,1.],[0.,-1.,0.]])
            a=direction@np.diag(spacing)
            np.save(p,{'origin':np.array([30.,20.,10.]),'spacing':spacing,'transform':a.T@np.diag(1/spacing)})
            meta=d.load_block_metadata(p)
            ori,actual=d.block_geometry(meta)
            np.testing.assert_allclose(actual,a[::-1,::-1])
            np.testing.assert_allclose(ori,[10.,20.,30.])
            with self.assertRaises(d.DataBlocked):
                d._MetadataUnpickler(io.BytesIO(pickle.dumps(Path('x')))).load()

    def test_split(self):
        rows=[{'id':f'{l}-{p}-{n}','patient_id':f'p{l}-{p}','label':l} for l in (0,1) for p in range(20) for n in range(2)]
        a=d.patient_split(rows)
        self.assertEqual(a,d.patient_split(rows[::-1]))
        own={}
        for s,rs in a.items():
            for r in rs:
                self.assertEqual(own.setdefault(r['patient_id'],s),s)
        self.assertEqual([len({r['patient_id'] for r in a[s]}) for s in ('train','validation','test')],[28,6,6])

    def test_zip(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            raw=io.BytesIO()
            with zipfile.ZipFile(raw,'w') as z:
                z.writestr('folder/a.txt','검사')
            b=raw.getvalue()
            (p/'one').write_bytes(b[:31]); (p/'two').write_bytes(b[31:])
            receipt=d.safe_extract([p/'one',p/'two'],p/'out')
            self.assertEqual((p/'out/folder/a.txt').read_text(),'검사')
            self.assertEqual(receipt['files'][0]['sha256'],hashlib.sha256('검사'.encode()).hexdigest())
            with zipfile.ZipFile(p/'bad.zip','w') as z:
                z.writestr('../escape','x')
            with self.assertRaises(d.DataBlocked):
                d.safe_extract([p/'bad.zip'],p/'badout')
            self.assertFalse((p/'escape').exists())

    def test_download_guard(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'guard'
            with d._download_guard(p):
                with self.assertRaises(d.DataBlocked):
                    with d._download_guard(p):
                        pass
            with d._download_guard(p):
                self.assertTrue(p.exists())

    def test_fail_closed(self):
        with self.assertRaises(d.DataBlocked):
            d.validate_manifest({'protocol':'stage12'})
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'mapping.json'
            p.write_text(json.dumps({'cohort':'Histo','reviewed':True}),encoding='utf-8')
            with self.assertRaises(d.DataBlocked):
                d.prepare_external(p,Path(td)/'out')

    def test_manifest_main_ready_external_pending(self):
        with tempfile.TemporaryDirectory() as td:
            rows=[]
            for label in (0,1):
                for i in range(10):
                    name=f'p{label}-{i}'
                    pixels=np.random.default_rng(label*100+i).integers(0,256,(512,512),dtype=np.uint8)
                    path=Path(td)/(name+'.png')
                    Image.fromarray(pixels).save(path)
                    rows.append({'id':name,'patient_id':name,'cohort':'LUNA25','label':label,'split':'unassigned',
                        'image_path':str(path),'image_sha256':d.digest(path),'source_sha256':hashlib.sha256(name.encode()).hexdigest(),
                        'metadata':{'global_patient_id':'LUNA25:'+name,'pixel_sha256':hashlib.sha256(pixels.tobytes()).hexdigest(),'label_evidence':'합성 검사용'}})
            manifest=d.build_manifest(rows)
            self.assertEqual(manifest['status'],'ready')
            self.assertEqual(manifest['summary']['Histo']['status'],'blocked')
            bad=copy.deepcopy(manifest)
            bad['splits']['test'][0]['metadata']['global_patient_id']=bad['splits']['train'][0]['metadata']['global_patient_id']
            with self.assertRaises(d.DataBlocked):
                d.validate_manifest(bad)
            bad=copy.deepcopy(manifest)
            bad['splits']['test'][0]['image_sha256']=bad['splits']['train'][0]['image_sha256']
            with self.assertRaises(d.DataBlocked):
                d.validate_manifest(bad,verify_files=False)
            Image.fromarray(np.zeros((512,512),dtype=np.uint8)).save(Path(manifest['splits']['train'][0]['image_path']))
            with self.assertRaises(d.DataBlocked):
                d.validate_manifest(manifest)

    def test_external_roi_and_raw_contract(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            image=root/'image.bmp'
            Image.fromarray(np.full((128,128),127,dtype=np.uint8)).save(image)
            annotation=root/'official.csv'
            annotation.write_text('fixture',encoding='utf-8')
            row={'id':'case','patient_id':'patient','global_patient_id':'Histo:patient','label':0,
                'label_evidence':'검사용 공식 라벨 대조','source_path':str(image),'source_sha256':d.digest(image),
                'policy':'legacy-2d-intensity','physical_geometry_unavailable':True,'nodule_center_evidence':'검사용 중심 좌표'}
            mapping={'reviewed':True,'cohort':'Histo','patient_identity_evidence':'검사용','institution_overlap_review':'검사용',
                'annotation_file':str(annotation),'annotation_sha256':d.digest(annotation),'label_definition_url':'https://zenodo.org/records/8422229','rows':[row]}
            path=root/'mapping.json'
            d.atomic_json(path,mapping)
            with self.assertRaises(d.DataBlocked):
                d.prepare_external(path,root/'prepared')

            row['center_xy_px']=[64,64]
            d.atomic_json(path,mapping)
            result=d.prepare_external(path,root/'prepared')
            self.assertEqual(len(result),1)
            self.assertTrue(result[0]['metadata']['geometry_unavailable'])
            self.assertIsNone(result[0]['metadata']['hu_window'])
            raw=root/'image.mhd'
            raw.write_text('ElementDataFile = image.raw\n',encoding='ascii')
            row.update(policy='physical-volume',source_path=str(raw),source_sha256=d.digest(raw))
            d.atomic_json(path,mapping)
            with self.assertRaises(d.DataBlocked):
                d.prepare_external(path,root/'prepared')

    def test_geometry_qc_before_split(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); blocks=root/'blocks'
            (blocks/'image').mkdir(parents=True);(blocks/'metadata').mkdir()
            annotations=[]; receipt={'files':[]}
            for i,(label,center) in enumerate(((0,64),(1,64),(1,2))):
                key=f'{i+1}_1_20200101'
                image=blocks/'image'/(key+'.npy'); meta=blocks/'metadata'/(key+'.npy')
                np.save(image,np.full((64,128,128),-500+i,dtype=np.int16))
                np.save(meta,{'origin':np.zeros(3),'spacing':np.ones(3),'transform':np.eye(3)})
                for p in (image,meta):receipt['files'].append({'path':p.relative_to(blocks).as_posix(),'sha256':d.digest(p)})
                annotations.append({'AnnotationID':key,'PatientID':str(i+1),'label':str(label),'CoordX':str(center),'CoordY':'64','CoordZ':'32','SeriesInstanceUID':str(i),'NoduleID':f'{i+1}_1'})
            d.atomic_json(blocks/'압축해제_무결성.json',receipt)
            annotation=root/'ann.csv';annotation.write_text('fixture',encoding='utf8')
            with patch.object(d,'read_luna_annotations',return_value=annotations):
                rows=d.prepare_luna(blocks,annotation,root/'prepared')
            self.assertEqual(len(rows),2)
            report=d.load_json(root/'prepared/LUNA25_입력적격성_비공개.json')
            self.assertEqual(report['rejected_annotations'],1)
            self.assertEqual(report['accepted_labels'],{'0':1,'1':1})
            self.assertEqual(report['rejected_labels'],{'1':1})
            self.assertEqual(report['policy_sha256'],d.ELIGIBILITY_SHA256)

if __name__=='__main__':
    unittest.main(verbosity=2)
