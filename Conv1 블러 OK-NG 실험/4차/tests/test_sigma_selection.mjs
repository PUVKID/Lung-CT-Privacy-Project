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
 [.9878048780487805,'98.78%'],[.5365853658536586,'53.65%'],[1,'100.00%'],[0,'0.00%'],[.99999,'99.99%'],[.25,'25.00%'],[1e-7,'0.00%'],
 [.9878,'98.78%'],[.29,'29.00%'],[131/164,'79.87%'],[102/164,'62.19%'],[163/164,'99.39%'],[159/164,'96.95%'],[.0001,'0.01%']
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
for(const sigma of sigmas){api.selectSigma(sigma);const req=requests.at(-1);assert.equal(req.url,`/api/sigma-results/${sigma}`);await settle(req,payload(sigma));assert.equal(api.getResult().sigma,sigma);assert.equal(charts.at(-1).sigma,sigma);}
api.selectSigma(0);const old=requests.at(-1);api.selectSigma(256);const middle=requests.at(-1);api.selectSigma(0);const newest=requests.at(-1);
await settle(newest,payload(0));await settle(middle,payload(256));await settle(old,payload(0));assert.equal(api.getResult().sigma,0);assert.equal(nodes.get('testAccuracy').textContent,'100.00%');
const queueNodes=[...nodes.get('queue').children];api.renderQueue(state);assert.deepEqual(nodes.get('queue').children,queueNodes);assert.equal(api.getSigma(),0);
const count=requests.length;api.loadSelectedResult();api.loadSelectedResult();assert.equal(requests.length,count+1);await settle(requests.at(-1),payload(0,'fedcba9876543210'));assert.equal(api.getResult(),null);assert.equal(nodes.get('testAccuracy').textContent,'미측정');
api.selectSigma(3);assert.equal(api.getSigma(),0);
api.selectSigma(8);const precise=payload(8);precise.metrics.test={accuracy:.9878048780487805,auc:.9999999999999999,loss:1e-16};await settle(requests.at(-1),precise);
assert.equal(nodes.get('testAccuracy').textContent,'98.78%');
assert.equal(nodes.get('testAccuracyRaw').textContent,'0.9878048780487805');
assert.equal(nodes.get('testAccuracyFull').textContent,'98.78048780487805%');
assert.equal(nodes.get('testAuc').textContent,'0.9999999999999999');
assert.equal(nodes.get('testLossRaw').textContent,'1e-16');
api.selectSigma(16);const undefinedAuc=payload(16);undefinedAuc.metrics.test.auc=null;await settle(requests.at(-1),undefinedAuc);assert.equal(nodes.get('testAuc').textContent,'정의 불가');

// 새 실행의 응답 전 비우기와 이전 실행 응답 거부는 Python의 실제 render 실행 회귀에 결합합니다.
console.log(`수치 표시 PASS: 백분율 ${percentCases.length}개·미측정/범위 6개·원값 7개·실제결과표시 6개`);
console.log('선택 회귀 PASS: 강도10개, 0→256→0 역순응답, 중복요청, 다른실행, 잘못된강도, 버튼재사용');
