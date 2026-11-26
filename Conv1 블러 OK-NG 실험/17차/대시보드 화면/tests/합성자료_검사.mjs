import {createServer} from '../server.mjs';
import {promises as fs} from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import assert from 'node:assert/strict';
const root=await fs.mkdtemp(path.join(os.tmpdir(),'ct17-synthetic-'));const id='resnet50_split_trainable_conv1_sigma_000';let server;
try{
 const dir=path.join(root,'conditions',id,'examples');await fs.mkdir(dir,{recursive:true});
 await fs.writeFile(path.join(root,'status.json'),JSON.stringify({schema:'stage17-sci-v2',protocol:'stage17-luna25-2d-patient-v2',run_id:'synthetic-run',state:'synthetic',conditions:[{id,sigma:0,profile:'블러만'}]}));
 await fs.writeFile(path.join(root,'conditions',id,'dashboard.json'),JSON.stringify({protocol:'stage17-luna25-2d-patient-v2',run_id:'synthetic-run',classifier:{test:{accuracy:.75,correct:3,total:4,auc:.5}},examples:[{label:'OK',source:'validation',original:`conditions/${id}/examples/OK_original.png`,transmitted:'../../secret.png',settings:{sigma:0}}]}));
 await fs.writeFile(path.join(dir,'OK_original.png'),Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVR4nGNoAAAAggCBd81ytgAAAABJRU5ErkJggg==','base64'));
 server=createServer({work:root});await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}`;
 let r=await fetch(base+'/api/comparison');let x=await r.json();assert.equal(x.rows[0].test.correct,3);
 r=await fetch(base+'/api/condition?id='+encodeURIComponent(id));x=await r.json();assert.equal(x.result.classifier.test.auc,.5);assert.deepEqual(x.examples[0].available,['original']);
 r=await fetch(base+'/api/image?id='+encodeURIComponent(id)+'&index=0&kind=original');assert.equal(r.status,200);assert.equal(r.headers.get('content-type'),'image/png');
 r=await fetch(base+'/api/image?id='+encodeURIComponent(id)+'&index=0&kind=transmitted');assert.equal(r.status,404);
 r=await fetch(base+'/api/image?id='+encodeURIComponent(id)+'&index=1&kind=original');assert.equal(r.status,404);
 r=await fetch(base+'/server.mjs');assert.equal(r.status,404);
 r=await fetch(base+'/',{method:'POST'});assert.equal(r.status,405);
 console.log('합성 자료: 결과·분모·지표·등록 사진·경로 차단·조회 전용 통과');
}finally{if(server)await new Promise(r=>server.close(r));await fs.rm(root,{recursive:true,force:true})}

