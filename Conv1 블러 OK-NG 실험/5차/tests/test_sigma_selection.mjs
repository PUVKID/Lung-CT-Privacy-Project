import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
// 실제 선택 함수와 응답 처리를 읽어 지연 응답의 순서만 제어합니다.
const source=fs.readFileSync('web/app.js','utf8');
class Element {
  constructor(){this.children=[];this.dataset={};this.attrs={};this.textContent='';}
  append(...nodes){this.children.push(...nodes);}
  querySelector(selector){return selector==='small'?this.children[1]:this.children.find(x=>String(x.dataset.sigma)===selector.match(/"(\d+)"/)?.[1]);}
  replaceChildren(...nodes){this.children=nodes;}
  addEventListener(){}
  setAttribute(key,value){this.attrs[key]=value;}
}
const nodes=new Map(),requests=[],charts=[];
const context={console,AbortController,setTimeout,clearTimeout,
  $:id=>{if(!nodes.has(id))nodes.set(id,new Element());return nodes.get(id);},
  states:{completed:'완료'},document:{createElement:()=>new Element()},
  pipeline:{setSelectedSigma(){}},drawChart:s=>charts.push(s),
  fetch:(url)=>new Promise(resolve=>requests.push({url,resolve}))};
vm.createContext(context);
const start=source.indexOf('const number ='),end=source.indexOf('let pipeline =');
vm.runInContext(source.slice(start,end)+`;globalThis.api={selectSigma,loadSelectedResult,renderQueue,percent,fullPercent,rawNumber,decimalShift,getSigma:()=>selectedSigma,getResult:()=>selectedResult,setState:s=>{latest=s;selectionRun=s.run_id;}};`,context);
const display=context.api;
const percentCases=[
 [.9878048780487805,'98.8%'],[.5365853658536586,'53.7%'],[1,'100.0%'],[0,'0.0%'],[.99999,'100.0%'],[.25,'25.0%'],[1e-7,'0.0%'],
 [.9878,'98.8%'],[.29,'29.0%'],[131/164,'79.9%'],[102/164,'62.2%'],[163/164,'99.4%'],[159/164,'97.0%'],[.0001,'0.0%'],
 [.9995,'100.0%'],[.9994999999999999,'99.9%'],[.0055,'0.6%'],[.0005,'0.1%'],[.0015,'0.2%'],[.2995,'30.0%']
];
for(const [value,expected] of percentCases)assert.equal(display.percent(value),expected);
for(const value of [null,undefined,NaN,Infinity,-.01,1.01])assert.equal(display.percent(value),'미측정');
assert.equal(display.fullPercent(.9878048780487805),'98.78048780487805%');
assert.equal(display.fullPercent(1e-7),'0.00001%');
assert.equal(display.rawNumber(.9999999999999999),'0.9999999999999999');
assert.equal(display.rawNumber(3e-5),'0.00003');
assert.equal(display.rawNumber(1e-16),'1e-16');
assert.equal(display.rawNumber(0),'0');
assert.equal(display.rawNumber(null),'미측정');
const api=context.api,run='0123456789abcdef',sigmas=[0,1,2,4,8,16,32,64,128,256];
const state={run_id:run,sigma:256,sigma_queue:sigmas.map(sigma=>({sigma,status:'completed'}))};api.setState(state);
const payload=(sigma,run_id=run)=>({run_id,sigma,status:'completed',message:'완료',history:[{sigma,epoch:sigma===256?16:17}],metrics:{best_epoch:15,epochs_ran:sigma===256?16:17,optimizer_steps:10,test:{accuracy:sigma===256?.537:1,auc:sigma===256?.573:1}}});
const settle=async(req,data)=>{req.resolve({ok:true,json:async()=>data});await new Promise(resolve=>setImmediate(resolve));};
// 실제 조회 함수에 준비 상태를 전달해 요청 수와 표시 결과를 검사합니다.
for(const run_id of [undefined,null,'','not-a-run',123]){
  api.setState({status:'ready',run_id,history:[]});
  api.selectSigma(0);
  assert.equal(requests.length,0,'유효한 실행 ID가 없으면 결과를 조회하지 않아야 합니다');
  assert.match(nodes.get('selectionNote').textContent,/학습 결과.*기다/);
  assert.equal(nodes.get('testAccuracy').textContent,'미측정');
  assert.equal(api.getResult(),null);
}
api.setState(state);
for(const sigma of sigmas){api.selectSigma(sigma);const req=requests.at(-1);assert.equal(req.url,`/api/sigma-results/${sigma}`);await settle(req,payload(sigma));assert.equal(api.getResult().sigma,sigma);assert.equal(charts.at(-1).sigma,sigma);}
api.selectSigma(0);const old=requests.at(-1);api.selectSigma(256);const middle=requests.at(-1);api.selectSigma(0);const newest=requests.at(-1);
await settle(newest,payload(0));await settle(middle,payload(256));await settle(old,payload(0));assert.equal(api.getResult().sigma,0);assert.equal(nodes.get('testAccuracy').textContent,'100.0%');
const queueNodes=[...nodes.get('queue').children];api.renderQueue(state);assert.deepEqual(nodes.get('queue').children,queueNodes);assert.equal(api.getSigma(),0);
const count=requests.length;api.loadSelectedResult();api.loadSelectedResult();assert.equal(requests.length,count+1);await settle(requests.at(-1),payload(0,'fedcba9876543210'));assert.equal(api.getResult(),null);assert.equal(nodes.get('testAccuracy').textContent,'미측정');
api.selectSigma(3);assert.equal(api.getSigma(),0);
api.selectSigma(8);const precise=payload(8);precise.metrics.test={accuracy:.9878048780487805,auc:.9999999999999999,loss:1e-16};await settle(requests.at(-1),precise);
assert.equal(nodes.get('testAccuracy').textContent,'98.8%');
assert.equal(nodes.get('testAccuracyRaw').textContent,'0.9878048780487805');
assert.equal(nodes.get('testAccuracyFull').textContent,'98.78048780487805%');
assert.equal(nodes.get('testAuc').textContent,'0.9999999999999999');
assert.equal(nodes.get('testLossRaw').textContent,'1e-16');
precise.metrics.test.correct_count=162;precise.metrics.test.n_images=164;api.selectSigma(4);const countResult=payload(4);countResult.metrics.test=precise.metrics.test;await settle(requests.at(-1),countResult);assert.equal(nodes.get('testCorrectCount').textContent,'정답 162 / 164장');
api.selectSigma(16);const undefinedAuc=payload(16);undefinedAuc.metrics.test.auc=null;await settle(requests.at(-1),undefinedAuc);assert.equal(nodes.get('testAuc').textContent,'정의 불가');

// 시작 전 상태로 돌아오면 이전 응답도 결과를 다시 채우지 않습니다.
api.selectSigma(0);const beforeReady=requests.at(-1),readyRequestCount=requests.length;
api.setState({status:'ready',history:[]});api.selectSigma(0);
assert.equal(requests.length,readyRequestCount);assert.equal(api.getResult(),null);assert.equal(nodes.get('testAccuracy').textContent,'미측정');
await settle(beforeReady,payload(0));assert.equal(api.getResult(),null);assert.equal(nodes.get('testAccuracy').textContent,'미측정');
api.setState(state);api.selectSigma(0);await settle(requests.at(-1),payload(0));assert.equal(api.getResult().run_id,run);assert.equal(nodes.get('testAccuracy').textContent,'100.0%');
console.log('실행 준비 회귀 PASS: 실행 ID 없는 5상태 조회0회·대기·미측정, 이전 응답 거부, 유효 ID 생성 뒤 조회');
// 새 실행의 응답 전 비우기와 이전 실행 응답 거부는 Python의 실제 render 실행 회귀에 결합합니다.
console.log(`수치 표시 PASS: 백분율 ${percentCases.length}개·미측정/범위 6개·원값 7개·실제결과표시 7개`);
console.log('선택 회귀 PASS: 강도10개, 0→256→0 역순응답, 중복요청, 다른실행, 잘못된강도, 버튼재사용');
