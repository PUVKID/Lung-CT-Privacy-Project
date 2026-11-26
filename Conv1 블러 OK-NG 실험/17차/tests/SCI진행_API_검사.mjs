import {createServer} from '../대시보드 화면/server.mjs';
import {promises as fs} from 'node:fs';import os from 'node:os';import path from 'node:path';import assert from 'node:assert/strict';import vm from 'node:vm';
const root=await fs.mkdtemp(path.join(os.tmpdir(),'sci-progress-'));const server=createServer({work:root,dataRoot:root});
const progress={phase:'reconstruction',layer:'conv1',dtype:'f16',split:'test',processed:7,total:20,patient_id:'secret'};
await fs.writeFile(path.join(root,'status.json'),JSON.stringify({schema:'stage17-sci-v2',protocol:'stage17-luna25-2d-patient-v2',run_id:'r',attack_progress:progress,conditions:[]}));
await new Promise(r=>server.listen(0,'127.0.0.1',r));try{
const data=await (await fetch(`http://127.0.0.1:${server.address().port}/api/status`)).json();assert.equal(data.attack_progress.processed,7);assert.equal(data.attack_progress.total,20);assert.doesNotMatch(JSON.stringify(data),/secret/);
const src=await fs.readFile(new URL('../대시보드 화면/app.js',import.meta.url),'utf8');const line=src.split('\n').find(x=>x.startsWith('function attackProgressText('));const ctx=vm.createContext({});vm.runInContext(line+';globalThis.format=attackProgressText',ctx);assert.match(ctx.format(data.attack_progress),/원본 복원 평가.*conv1.*f16.*7 \/ 20/);assert.equal(ctx.format(null),'');console.log('공격 진행 API·한국어 표시 검사 통과');
}finally{await new Promise(r=>server.close(r));await fs.rm(root,{recursive:true,force:true});}
