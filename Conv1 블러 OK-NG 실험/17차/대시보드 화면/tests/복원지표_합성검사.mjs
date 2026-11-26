import {createServer} from '../server.mjs';
import {promises as fs} from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import assert from 'node:assert/strict';
const root=await fs.mkdtemp(path.join(os.tmpdir(),'ct17-privacy-synthetic-'));const id='sigma_000_블러만';let server;
try{const dir=path.join(root,'conditions',id);await fs.mkdir(dir,{recursive:true});await fs.writeFile(path.join(root,'status.json'),JSON.stringify({schema:'stage17-v1',run_id:'synthetic-run',conditions:[{id}]}));
const one={mse:.2,ssim:.7,psnr:null,count:4,mean_baseline_mse:.1,privacy_error_ratio_raw:2,privacy_error_ratio_clipped:1,privacy_error_score:100,privacy_error_clipping_applied:true,privacy_structure_ratio_raw:.3,privacy_structure_ratio_clipped:.3,privacy_structure_score:30,privacy_structure_clipping_applied:false,undefined_reason:null,psnr_infinite_count:1};
const two={...one,mse:.4,privacy_error_ratio_raw:4,privacy_error_score:95,count:2};
await fs.writeFile(path.join(dir,'dashboard.json'),JSON.stringify({run_id:'synthetic-run',attack:{selected_family:'copy_decoded',validation_mse:.12,privacy_ratio_raw:2,privacy_ratio_clipped:1,undefined_reason:null,test:one,candidate_metrics:{copy_decoded:{validation:two,validation_by_class:{OK:one,NG:two},test:one,test_by_class:{OK:two,NG:one}},mean_train:{test:two,test_by_class:{OK:one,NG:two}}},posthoc_strongest_observed:{overall:{family:'mean_train',privacy_error_score:95}}}}));
server=createServer({work:root});await new Promise(r=>server.listen(0,'127.0.0.1',r));const r=await fetch(`http://127.0.0.1:${server.address().port}/api/condition?id=`+encodeURIComponent(id));assert.equal(r.status,200);const x=(await r.json()).result.attack;assert.equal(x.selected_family,'copy_decoded');assert.equal(x.candidate_metrics.copy_decoded.validation.mse,.4);assert.equal(x.candidate_metrics.copy_decoded.validation_by_class.OK.mse,.2);assert.equal(x.candidate_metrics.copy_decoded.test.psnr_infinite_count,1);assert.equal(x.candidate_metrics.copy_decoded.test.privacy_error_ratio_raw,2);assert.equal(x.candidate_metrics.copy_decoded.test.privacy_error_clipping_applied,true);assert.equal(x.candidate_metrics.copy_decoded.test_by_class.OK.mse,.4);assert.equal(x.candidate_metrics.mean_train.test.mse,.4);assert.equal(x.candidate_metrics.mean_train.test_by_class.OK.mse,.2);assert.equal(x.posthoc_strongest_observed.overall.family,'mean_train');console.log('합성 복원 자료: 공격별·분류별 독립값, 원비율·제한·무한 PSNR·시험 후 탐색 전달 통과');
}finally{if(server)await new Promise(r=>server.close(r));await fs.rm(root,{recursive:true,force:true})}

