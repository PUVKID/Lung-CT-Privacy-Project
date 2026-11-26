import http from 'node:http';
import {promises as fs} from 'node:fs';
import path from 'node:path';
import {inflateSync} from 'node:zlib';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const defaultWork='D:/2026/폐암 논문/Conv1 블러 OK-NG 실험/17차/work/SCI-v2';
const protocol='stage17-luna25-2d-patient-v2';
const defaultData='E:/2026/폐암 논문/Conv1 블러 OK-NG 실험/17차/work/data';
const validId=id=>typeof id==='string'&&/^[A-Za-z0-9_-]{1,120}$/.test(id);
const asset=new Map([['/','index.html'],['/app.js','app.js'],['/16.css','16차-화면.css'],['/astryx-neutral.css','astryx-neutral.css'],['/astryx-tokens.css','astryx-tokens.css'],['/astryx-research.css','astryx-research.css']]);
function validPng(b){
 try{
  if(!b||b.length<57||!b.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))return false;
  let offset=8,header=null,end=false;const data=[];
  while(offset+12<=b.length){
   const n=b.readUInt32BE(offset);if(n>b.length-offset-12)return false;
   const type=b.toString('ascii',offset+4,offset+8),payload=b.subarray(offset+8,offset+8+n);
   let crc=0xffffffff;for(const value of b.subarray(offset+4,offset+8+n)){crc^=value;for(let i=0;i<8;i++)crc=(crc>>>1)^((crc&1)?0xedb88320:0)}
   if(((crc^0xffffffff)>>>0)!==b.readUInt32BE(offset+8+n))return false;
   if(offset===8 && (type!=='IHDR'||n!==13))return false;
   if(type==='IHDR'){if(header)return false;header=payload}
   if(type==='IDAT')data.push(payload);
   offset+=12+n;if(type==='IEND'){end=n===0&&offset===b.length;break}
  }
  if(!header||!end||!data.length)return false;
  const w=header.readUInt32BE(0),h=header.readUInt32BE(4),depth=header[8],color=header[9],channels={0:1,2:3,4:2,6:4}[color];
  if(!w||!h||w>4096||h>4096||depth!==8||!channels||header[10]!==0||header[11]!==0||header[12]!==0)return false;
  const row=1+w*channels,expected=row*h,decoded=inflateSync(Buffer.concat(data),{maxOutputLength:expected});
  if(decoded.length!==expected)return false;for(let i=0;i<h;i++)if(decoded[i*row]>4)return false;
  return true;
 }catch{return false}
}
export function createServer({work=defaultWork,dataRoot=defaultData}={}){
async function safeFile(parts,limit=4*1024*1024){let p=path.resolve(work);try{if((await fs.lstat(p)).isSymbolicLink())throw Error('연결 경로 금지');for(const part of parts){if(!part||part==='.'||part==='..'||part.includes('/')||part.includes('\\'))throw Error('경로 오류');p=path.join(p,part);if((await fs.lstat(p)).isSymbolicLink())throw Error('연결 경로 금지');}const s=await fs.stat(p);if(!s.isFile()||s.size>limit)throw Error('파일 오류');return await fs.readFile(p)}catch(e){if(e.code==='ENOENT')return null;throw e}}
async function json(parts){const b=await safeFile(parts);return b?JSON.parse(b.toString('utf8')):null}
async function status(){const x=await json(['status.json']);if(!x)return null;if(x.schema!=='stage17-sci-v2'||x.protocol!==protocol)throw Error('형식 오류');return x}
const cleanAccuracy=x=>x&&Object.fromEntries(['accuracy','correct','total','ok_accuracy','ng_accuracy','sensitivity','specificity','balanced_accuracy','auc','pr_auc','precision','npv','f1','mcc','brier_score','ece_10_bins','confusion_matrix','wilson95','accuracy_ci95_group','n_similarity_groups','patient_ci95','n_patients','group_bootstrap_draws','interval_note','interval_degenerate','interval_degenerate_reason','undefined_reasons'].filter(k=>Object.hasOwn(x,k)).map(k=>[k,x[k]]));
const cleanEpoch=x=>x&&({epoch:x.epoch,training:cleanAccuracy(x.training),validation:cleanAccuracy(x.validation)});
const sameRun=(value,runId)=>typeof runId==='string'&&runId.trim()!==''&&value?.run_id===runId;
async function condition(id,runId){const [current,history,result]=await Promise.all(['current.json','history.json','dashboard.json'].map(n=>json(['conditions',id,n])));return {current:sameRun(current,runId)?cleanEpoch(current):null,history:Array.isArray(history)?history.filter(h=>sameRun(h,runId)).map(cleanEpoch):[],result:sameRun(result,runId)&&result?.protocol===protocol?result:null}}
const cleanReport=x=>x&&Object.fromEntries(['mse','ssim','psnr','count','mean_baseline_mse','privacy_error_ratio_raw','privacy_error_ratio_clipped','privacy_error_score','privacy_error_clipping_applied','privacy_structure_ratio_raw','privacy_structure_ratio_clipped','privacy_structure_score','privacy_structure_clipping_applied','undefined_reason','psnr_infinite_count'].filter(k=>Object.hasOwn(x,k)).map(k=>[k,x[k]]));
const cleanAttack=(a,withExternal=true)=>{if(!a)return null;const candidates={};for(const [family,x] of Object.entries(a.candidate_metrics||{})){if(!/^[A-Za-z0-9_.:-]+$/.test(family))continue;candidates[family]={validation_original:cleanReport(x.validation_original),validation_original_by_class:{OK:cleanReport(x.validation_original_by_class?.OK),NG:cleanReport(x.validation_original_by_class?.NG)},validation:cleanReport(x.validation),validation_by_class:{OK:cleanReport(x.validation_by_class?.OK),NG:cleanReport(x.validation_by_class?.NG)},test_generated:cleanReport(x.test_generated),test_generated_by_class:{OK:cleanReport(x.test_generated_by_class?.OK),NG:cleanReport(x.test_generated_by_class?.NG)},test:cleanReport(x.test),test_by_class:{OK:cleanReport(x.test_by_class?.OK),NG:cleanReport(x.test_by_class?.NG)}}}const observed={};for(const k of ['overall','OK','NG']){const x=a.posthoc_strongest_observed?.[k];if(x)observed[k]={family:x.family,privacy_error_score:x.privacy_error_score}}return {selected_family:a.selected_family,validation_mse:a.validation_mse,privacy_ratio_raw:a.privacy_ratio_raw,privacy_ratio_clipped:a.privacy_ratio_clipped,undefined_reason:a.undefined_reason,test:cleanReport(a.test),candidate_metrics:candidates,posthoc_strongest_observed:observed,external:withExternal?Object.fromEntries(['CSTL','Histo'].map(k=>[k,cleanAttack(a.external?.[k],false)])):undefined,state:a.state,reason:typeof a.reason==='string'&&!/[\\/]/.test(a.reason)?a.reason:null}};
const safeExamples=(result,id)=>{
 if(!Array.isArray(result?.examples))return [];
 return result.examples.map((e,i)=>{
  const settings={};
  if(e.settings && typeof e.settings==='object')for(const [k,v] of Object.entries(e.settings)){
   if(/^[a-zA-Z0-9_]{1,40}$/.test(k) && (typeof v==='number' || typeof v==='boolean' || (typeof v==='string' && v.length<100 && !/[\\/]/.test(v))))settings[k]=v;
  }
  const available=['original','transmitted','reconstructed','feature_map','feature_reconstructed'].filter(k=>{
   if(typeof e[k]!=='string')return false;
   if(k==='feature_reconstructed')return ['OK','NG'].some(label=>e[k]===`conditions/${id}/attacks/conv1/f32/examples/${label}_reconstructed.png`);
   if(k==='reconstructed')return ['OK','NG'].some(label=>e[k]===`conditions/${id}/attacks/photo/examples/${label}_reconstructed.png`);
   return e[k].startsWith(`conditions/${id}/examples/`) && /^conditions\/[^/]+\/examples\/[A-Za-z0-9_.-]+\.png$/.test(e[k]);
  });
  if(e.settings?.feature_reconstruction && typeof e.settings.feature_reconstruction==='object'){
   const f=e.settings.feature_reconstruction,clean={};
   if(typeof f.selected_attack==='string'&&/^[A-Za-z0-9_.:-]{1,120}$/.test(f.selected_attack))clean.selected_attack=f.selected_attack;
   if(typeof f.checkpoint_sha256==='string'&&/^[a-fA-F0-9]{64}$/.test(f.checkpoint_sha256))clean.checkpoint_sha256=f.checkpoint_sha256;
   if(f.exposure_layer==='front.conv1')clean.exposure_layer=f.exposure_layer;
   if(f.layer==='conv1')clean.layer=f.layer;
   if(f.dtype==='f32')clean.dtype=f.dtype;
   if(f.precision==='fp32')clean.precision=f.precision;
   if(typeof f.photo_decoder_reused==='boolean')clean.photo_decoder_reused=f.photo_decoder_reused;
   if(typeof f.threat_model==='string'&&f.threat_model.length<=200&&!/[\\/]/.test(f.threat_model))clean.threat_model=f.threat_model;
   settings.feature_reconstruction=clean;
  }
  if(typeof result.attack?.selected_family==='string'&&/^[A-Za-z0-9_.:-]{1,120}$/.test(result.attack.selected_family))settings.photo_selected_attack=result.attack.selected_family;
  if(e.settings?.feature_map){const f=e.settings.feature_map,parts=[f.layer,f.aggregation,f.normalization].filter(v=>typeof v==='string');if(Number.isFinite(f.raw_min)&&Number.isFinite(f.raw_max))parts.push(`원값 범위 ${f.raw_min} ~ ${f.raw_max}`);const epoch=Number.isInteger(f.best_epoch)?f.best_epoch:result.classifier?.best_epoch;if(Number.isInteger(epoch))parts.push(`최적 회차 ${epoch}`);settings.feature_map=parts.join(' · ')}
  const g=e.settings?.source_metadata;if(g&&typeof g==='object'){const geometry={};for(const k of ['fov_mm','pixel_spacing_mm','output_size'])if(typeof g[k]==='number'&&Number.isFinite(g[k])&&g[k]>0)geometry[k]=g[k];if(Object.keys(geometry).length)settings.geometry=geometry;}
  return {index:i,label:typeof e.label==='string'?e.label.slice(0,100):'저장 사진',source:e.source==='validation'?'validation':'기록 없음',settings,available};
 });
};
return http.createServer(async(req,res)=>{res.setHeader('Cache-Control','no-store');res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','no-referrer');const send=(code,data,type='application/json; charset=utf-8')=>{res.writeHead(code,{'Content-Type':type});res.end(req.method==='HEAD'?undefined:typeof data==='string'||Buffer.isBuffer(data)?data:JSON.stringify(data));};try{
if(!/^(127\.0\.0\.1|localhost)(:\d+)?$/.test(req.headers.host||''))return send(403,{error:'로컬 전용'});if(!['GET','HEAD'].includes(req.method))return send(405,{error:'조회 전용'});const u=new URL(req.url,'http://127.0.0.1');
if(u.pathname==='/api/data'){try{const root=path.resolve(dataRoot),file=path.join(root,'SCI_준비상태.json');if((await fs.lstat(root)).isSymbolicLink()||(await fs.lstat(file)).isSymbolicLink())throw Error('연결 경로');const info=await fs.stat(file);if(!info.isFile()||info.size>1024*1024)throw Error('크기 오류');const d=JSON.parse((await fs.readFile(file)).toString('utf8'));if(d.protocol!==protocol)throw Error('형식 오류');const cleanReason=x=>typeof x==='string'&&!/[\\/]/.test(x)?x:'상세 확인 필요';const summary={};for(const k of ['train','validation','test','CSTL','Histo']){const v=d.summary?.[k];if(v)summary[k]={nodules:v.nodules,patients:v.patients,labels:v.labels}}return send(200,{status:d.status,updated_at:d.updated_at,reasons:Array.isArray(d.reasons)?d.reasons.map(cleanReason):[],summary,bytes:d.bytes,expected_bytes:d.expected_bytes,download_completed:Array.isArray(d.download_completed)?d.download_completed.filter(x=>['annotations','nodule-blocks','external-classification','full-ct'].includes(x)):[]});}catch(e){if(e.code==='ENOENT')return send(200,{status:'waiting',reasons:[]});return send(500,{error:'데이터 준비 상태를 읽지 못했습니다.'})}}
if(u.pathname==='/api/status'){const x=await status();if(!x)return send(200,{state:'준비 대기',message:'공식 데이터와 주석 준비 대기',conditions:[]});return send(200,{run_id:x.run_id,state:x.state,message:({blocked:'데이터 준비 차단',prepared:'데이터 준비 완료',running:'실험 진행 중',idle:'실험 대기'})[x.state]||'상태 확인 중',detail:typeof x.reason==='string'&&!/[\\/]/.test(x.reason)?x.reason:'실제 데이터·주석·학습 상태를 확인합니다.',updated_at:x.updated_at,completed_conditions:x.completed_conditions,total_conditions:x.total_conditions,conditions:Array.isArray(x.conditions)?x.conditions.filter(c=>validId(c.id)).map(({id,sigma,model,regime,split_boundary,cohort,kind,state,epoch})=>({id,sigma,model,regime,split_boundary,cohort,kind,state,epoch})):[]});}
if(u.pathname==='/api/comparison'){const x=await status();const list=Array.isArray(x?.conditions)?x.conditions.filter(c=>validId(c.id)):[];const rows=[];for(const c of list){const candidate=await json(['conditions',c.id,'dashboard.json']);const r=sameRun(candidate,x?.run_id)&&candidate?.protocol===protocol?candidate:null;rows.push({id:c.id,sigma:c.sigma,profile:c.profile,test:cleanAccuracy(r?.classifier?.test)??null,test_generated:cleanAccuracy(r?.classifier?.test_generated)??null})}const finalStatus=await status();if(typeof x?.run_id==='string'&&x.run_id.trim()!==''&&!sameRun({run_id:finalStatus?.run_id},x.run_id))return send(200,{rows:[]});return send(200,{rows});}
if(u.pathname==='/api/condition'||u.pathname==='/api/image'){const id=u.searchParams.get('id');if(!validId(id))return send(400,{error:'조건 오류'});const x=await status();if(!x?.conditions?.some(c=>c.id===id))return u.pathname==='/api/condition'?send(200,{current:null,history:[],result:null,examples:[]}):send(404,{error:'등록되지 않은 조건'});const {current,history,result}=await condition(id,x.run_id);const examples=safeExamples(result,id);
if(u.pathname==='/api/image'){const i=Number(u.searchParams.get('index')),kind=u.searchParams.get('kind');if(!Number.isInteger(i)||i<0||!examples[i]?.available.includes(kind))return send(404,{error:'등록되지 않은 사진'});const parts=result.examples[i][kind].split('/');const b=await safeFile(parts,16*1024*1024);if(!validPng(b))return send(404,{error:'PNG 사진을 확인할 수 없습니다.'});const latest=await status();if(!sameRun({run_id:latest?.run_id},x.run_id))return send(404,{error:'실행이 변경되었습니다.'});return send(200,b,'image/png');}
const latest=await status();if(!sameRun({run_id:latest?.run_id},x.run_id))return send(200,{current:null,history:[],examples:[],result_pending:true,result:null});return send(200,{current,history,examples,result_pending:!result,result:result&&{classifier:{validation_original:cleanAccuracy(result.classifier?.validation_original),test:cleanAccuracy(result.classifier?.test),test_generated:cleanAccuracy(result.classifier?.test_generated)},attack:cleanAttack(result.attack),feature_attacks:Object.fromEntries(['conv1','stem','layer1','layer2','layer3','layer4'].map(k=>[k,{precisions:Object.fromEntries(['f32','f16','i8'].map(d=>{const leaf=result.feature_attacks?.[k]?.precisions?.[d];return [d,leaf?{...cleanAttack(leaf),transmission:leaf.transmission&&Object.fromEntries(['dtype','packet_bytes','sidecar_bytes','total_bytes','count','mean_total_bytes','quantization_mse'].filter(key=>Object.hasOwn(leaf.transmission,key)).map(key=>[key,leaf.transmission[key]]))}:null]}))}])),linking:Object.fromEntries(['conv1','stem','layer1','layer2','layer3','layer4'].map(k=>{const cleanLink=x=>x&&Object.fromEntries(['topk_source','topk_patient','count','gallery_size','state','reason','assumption'].filter(key=>Object.hasOwn(x,key)).map(key=>[key,x[key]]));return [k,{test:cleanLink(result.linking?.[k]?.test),test_generated:cleanLink(result.linking?.[k]?.test_generated),external:Object.fromEntries(['CSTL','Histo'].map(c=>[c,cleanLink(result.linking?.[k]?.external?.[c])]))}]})),membership_generated:result.membership_generated&&Object.fromEntries(['selected_score','validation_auc','test_auc','member_count','nonmember_count'].filter(key=>Object.hasOwn(result.membership_generated,key)).map(key=>[key,result.membership_generated[key]])),membership:result.membership&&{...Object.fromEntries(['selected_score','validation_auc','test_auc','member_count','nonmember_count','reason'].filter(key=>Object.hasOwn(result.membership,key)).map(key=>[key,result.membership[key]])),external:Object.fromEntries(['CSTL','Histo'].map(c=>[c,result.membership.external?.[c]&&Object.fromEntries(['auc','reason','interpretation'].filter(key=>Object.hasOwn(result.membership.external[c],key)).map(key=>[key,result.membership.external[c][key]]))]))},external:Object.fromEntries(['CSTL','Histo'].map(k=>[k,result.external?.[k]?.state?{state:result.external[k].state,reason:typeof result.external[k].reason==='string'&&!/[\\/]/.test(result.external[k].reason)?result.external[k].reason:'자료 준비 미완료'}:{classifier:{test:cleanAccuracy(result.external?.[k]?.test||result.external?.[k]),test_generated:cleanAccuracy(result.external?.[k]?.test_generated)}}])),packet:{mean_bytes:result.packet?.mean_bytes,total_bytes:result.packet?.total_bytes,encode_seconds:result.packet?.encode_seconds}}});}
let file=asset.get(u.pathname);if(!file&&/^\/fonts\/[A-Za-z0-9_.-]+$/.test(u.pathname))file=u.pathname.slice(1);if(!file)return send(404,{error:'없는 주소'});const buf=await fs.readFile(path.join(here,file));const ext=path.extname(file);return send(200,buf,ext==='.html'?'text/html; charset=utf-8':ext==='.js'?'text/javascript; charset=utf-8':ext==='.css'?'text/css; charset=utf-8':'font/ttf');
}catch{return send(500,{error:'17차 자료를 읽지 못했습니다.'});}})}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){const server=createServer();server.on('error',e=>{console.error(e.message);process.exitCode=1});server.listen(8788,'127.0.0.1',()=>console.log('17차 조회 http://127.0.0.1:8788/'));}
