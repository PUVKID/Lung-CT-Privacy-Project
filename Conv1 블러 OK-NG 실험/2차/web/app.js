import { createPipeline } from './scene.js';
const $ = id => document.getElementById(id);
const stages = {preparing:'학습 데이터를 준비하고 있습니다',ready:'학습 준비를 마쳤습니다',loading_model:'모델을 불러오고 있습니다',training:'분류기를 학습하고 있습니다',validation:'검증 결과를 확인하고 있습니다',testing:'시험 영상을 평가하고 있습니다',completed:'실험을 마쳤습니다',interrupted:'학습을 중단했습니다',error:'학습을 멈췄습니다'};
const states = {running:'진행 중',ready:'준비 완료',completed:'완료',failed:'오류',pending:'대기',waiting:'기록 대기',interrupted:'중단'};
const number = v => typeof v === 'number' && Number.isFinite(v);
const shown = v => number(v) ? v.toLocaleString('ko-KR') : '—';
const measured = v => number(v) ? v.toLocaleString('ko-KR') : '미측정';
const lossText = v => !number(v) ? '미측정' : v===0 ? '0' : Math.abs(v)<0.001 || Math.abs(v)>=10000 ? v.toExponential(3) : v.toPrecision(4);
const percent = v => number(v) ? `${(v * 100).toFixed(1)}%` : '미측정';
let latest = null;
let pipeline = null;
let refreshing = false;
let manualPaused = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function setMotion() {
  $('motion').textContent = manualPaused ? '움직임 재생' : '움직임 정지';
  $('motion').setAttribute('aria-pressed', String(manualPaused));
  pipeline?.setPaused(manualPaused);
}
$('motion').addEventListener('click', () => { manualPaused = !manualPaused; setMotion(); });
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
reduced.addEventListener('change', e => { manualPaused = e.matches; setMotion(); });
await document.fonts.ready;
try { pipeline = createPipeline($('scene')); setMotion(); pipeline.setTheme(window.ctTheme?.current() || 'light'); }
catch { $('sceneError').textContent = '이 브라우저에서 3D 모형을 표시할 수 없습니다. 아래 단계와 실제 상태는 계속 확인할 수 있습니다.'; }
function updateTheme() {
  const dark=window.ctTheme?.current()==='dark';
  $('theme')?.setAttribute('aria-pressed',String(dark));
  $('theme')?.setAttribute('aria-label',dark?'밝은 화면으로 전환':'어두운 화면으로 전환');
  if($('themeText'))$('themeText').textContent=dark?'라이트':'다크';
  pipeline?.setTheme(dark?'dark':'light');
  if(latest)drawChart(latest);
}
$('theme')?.addEventListener('click',()=>window.ctTheme?.toggle());
window.addEventListener('ct-theme-change',updateTheme);updateTheme();
function stageVisual(s, blocked) {
  const active = s.status==='waiting'?-1:({preparing:0,ready:0,loading_model:1,training:3,validation:3,testing:3,completed:4,error:3}[s.stage] ?? -1);
  const interrupted=s.status==='interrupted' || s.stage==='interrupted';
  for (let i=0;i<4;i++) {
    const node = $('step'+i).parentElement;
    node.className = interrupted ? 'interrupted' : i<active ? 'complete' : i===active ? (blocked?'failed':'active') : '';
    $('step'+i).textContent = interrupted ? '중단' : i<active ? '완료' : i===active ? (blocked?'확인 필요':'진행 중') : '대기';
  }
  // 모형의 순서는 연산 구조이며, 학습 중 앞 단계도 실제 배치마다 함께 실행됩니다.
  pipeline?.setStatus(active, interrupted ? 'interrupted' : blocked ? 'failed' : s.status, !blocked && !interrupted && s.status==='running');
  $('motion').disabled=interrupted;
  if(interrupted){$('motion').textContent='모형 정지 · 학습 중단';$('motion').setAttribute('aria-pressed','true');}
  else setMotion();
}
function drawChart(s) {
  const rows = (Array.isArray(s.history) ? s.history : []).filter(row => row.sigma === s.sigma);
  const canvas = $('chart');
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.max(1, Math.floor(rect.width*dpr)); canvas.height = Math.floor(210*dpr);
  const ctx = canvas.getContext('2d'); ctx.scale(dpr,dpr);
  const width=rect.width, height=210, left=38, right=40, top=16, bottom=30;
  const metrics=[['train_loss','#647fba'],['val_loss','#4c83cf'],['val_accuracy','#c49b48']];
  const measured = rows.some(r=>metrics.some(([key])=>number(r[key])));
  $('emptyChart').hidden = measured;
  $('curveSigma').textContent = number(s.sigma) ? `σ = ${s.sigma}` : '현재 σ 미측정';
  if (!measured) {$('latestLoss').textContent='최근 손실 미측정';return;}
  const recent=rows.at(-1);
  $('latestLoss').textContent=recent ? `최근 학습 손실 ${lossText(recent.train_loss)} · 검증 손실 ${lossText(recent.val_loss)}` : '최근 손실 미측정';
  const lossValues=rows.flatMap(r=>[r.train_loss,r.val_loss]).filter(number);
  const maxLoss=Math.max(1,...lossValues)*1.1;
  const maxEpoch=Math.max(1,...rows.map(r=>number(r.epoch)?r.epoch:0));
  const chartWidth=width-left-right, chartHeight=height-top-bottom;
  ctx.font='700 9px Nanum'; ctx.lineWidth=1;
  for(let i=0;i<5;i++) {
    const y=top+chartHeight*i/4;
    ctx.strokeStyle=window.ctTheme?.current()==='dark'?'#293346':'#e5e9f0';ctx.beginPath();ctx.moveTo(left,y);ctx.lineTo(width-right,y);ctx.stroke();
    ctx.fillStyle=window.ctTheme?.current()==='dark'?'#8391a8':'#8793a7';ctx.textAlign='right';ctx.fillText((maxLoss*(1-i/4)).toFixed(2),left-7,y+3);
    ctx.textAlign='left';ctx.fillText(`${100-i*25}%`,width-right+6,y+3);
  }
  for (const [key,color] of metrics) {
    ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=2;ctx.beginPath();let started=false;
    for(const row of rows) {
      if(!number(row[key]) || !number(row.epoch)) {started=false;continue;}
      const x=left+(row.epoch-1)/Math.max(1,maxEpoch-1)*chartWidth;
      const y=top+chartHeight*(1-row[key]/(key==='val_accuracy'?1:maxLoss));
      if(started)ctx.lineTo(x,y);else ctx.moveTo(x,y);started=true;
    }
    ctx.stroke();
    for(const row of rows){if(!number(row[key])||!number(row.epoch))continue;ctx.beginPath();ctx.arc(left+(row.epoch-1)/Math.max(1,maxEpoch-1)*chartWidth,top+chartHeight*(1-row[key]/(key==='val_accuracy'?1:maxLoss)),3,0,Math.PI*2);ctx.fill();}
  }
  ctx.fillStyle=window.ctTheme?.current()==='dark'?'#8391a8':'#8793a7';ctx.textAlign='left';ctx.fillText('1회',left,height-7);ctx.textAlign='right';ctx.fillText(`${maxEpoch}회`,width-right,height-7);
}
function render(s) {
  latest=s;
  const meta=s._dashboard || {};
  const dead=meta.process_alive===false && s.status==='running';
  const interrupted=s.status==='interrupted' || s.stage==='interrupted';
  const failed=!interrupted && (s.status==='failed' || Boolean(s.error));
  const blocked=failed || dead || meta.stale || interrupted;
  $('currentTitle').textContent=interrupted ? '학습을 중단했습니다' : s.stage==='ready' && s.status==='waiting' ? '학습 상태를 기다리고 있습니다' : stages[s.stage] || '학습 상태를 확인하고 있습니다';
  $('message').textContent=interrupted?'학습과 모형의 움직임을 멈추고 마지막 기록을 표시합니다.':s.status==='failed'?'오류를 확인한 뒤 다시 시작합니다. 실행 기록은 보존되어 있습니다.':s.stage==='training'?`현재 블러 강도에서 학습과 검증을 반복합니다.`:'첫 합성곱 특징에 블러를 적용해 분류 성능을 비교합니다.';
  $('badge').textContent=interrupted?'중단':states[s.status] || '상태 확인 중';
  let warning=interrupted ? '학습이 중단되었습니다. 마지막 기록을 표시하며 모형의 움직임도 멈췄습니다.' : failed ? '실험이 오류로 중단되었습니다. 작업 기록을 확인해 주세요.' : dead ? '학습 프로세스가 종료되었습니다. 마지막 기록을 표시합니다.' : meta.read_error ? meta.read_error : meta.stale ? '60초 이상 새 기록이 없습니다. 실행 상태를 확인해 주세요.' : '';
  $('alert').textContent=warning;$('alert').className=warning?`alert visible${failed||dead?' failed':''}`:'alert';
  $('sigmaLabel').textContent=number(s.sigma)?`σ ${s.sigma} · ${shown(s.sigma_index)} / ${Array.isArray(s.sigmas)?s.sigmas.length:'—'}번째 실험`:'블러 강도 기록 대기';
  const policy=s.training_policy || {};
  const maximum=number(policy.max_epochs)?policy.max_epochs:s.epochs;
  $('epoch').textContent=`${measured(s.epoch)}회 / 최대 ${measured(maximum)}회`;
  $('learningRate').textContent=number(s.learning_rate)?(s.learning_rate===0?'0':s.learning_rate.toExponential(3)):'미측정';
  $('earlyStopping').textContent=!number(s.early_stopping_wait) && !number(policy.patience) ? '미측정' : `${measured(s.early_stopping_wait)} / ${measured(policy.patience)}회`;
  $('bestEpoch').textContent=number(s.best_epoch)?`${s.best_epoch}회`:'미측정';
  $('optimizerSteps').textContent=measured(s.optimizer_steps);
  $('batch').textContent=`배치 ${shown(s.batch)} / ${shown(s.batches)}`;
  $('progress').value=number(s.batch)&&number(s.batches)&&s.batches>0?Math.min(100,s.batch/s.batches*100):0;
  const device=s.device || {};
  $('device').textContent=typeof device==='string'?device:device.name || device.type || '미확인';
  $('process').textContent=interrupted?'학습 중단':meta.process_alive===true?'학습 프로세스 실행 중':meta.process_alive===false?'학습 프로세스 종료':'학습 프로세스 확인 대기';
  $('seen').textContent=`이번 회차 OK ${shown(s.seen_per_class?.OK)} / NG ${shown(s.seen_per_class?.NG)}`;
  const stamp=new Date(s.updated_at);
  const stampText=Number.isNaN(stamp.getTime())?'갱신 시각 미확인':stamp.toLocaleString('ko-KR',{timeZone:'Asia/Seoul',hour12:false});
  $('updated').textContent=`최근 갱신 ${stampText}`;
  $('freshness').textContent=`한국 시각 ${stampText} · ${number(meta.age_seconds)?Math.floor(meta.age_seconds)+'초 전 관측':'관측 대기'}`;
  stageVisual(s,blocked);
  const queue=Array.isArray(s.sigma_queue)?s.sigma_queue:[];
  $('queue').replaceChildren();
  if(!queue.length){const el=document.createElement('p');el.className='muted';el.textContent='실제 블러 강도 순서 기록 대기';$('queue').append(el);}
  for(const item of queue){const div=document.createElement('div');div.className=['running','completed','failed'].includes(item.status)?item.status:'';const strong=document.createElement('strong');strong.textContent=`σ ${item.sigma}`;const small=document.createElement('small');small.textContent=states[item.status] || '대기';div.append(strong,small);$('queue').append(div);}
  $('queueCount').textContent=queue.length?`${queue.filter(x=>x.status==='completed').length} / ${queue.length} 완료`:'10단계 · 기록 대기';
  drawChart(s);
  const test=s.evaluation?.test;
  $('testAccuracy').textContent=percent(test?.accuracy);
  $('testAuc').textContent=number(test?.auc)?test.auc.toFixed(3):'미측정';
  $('evaluationNote').textContent=test?`σ ${s.evaluation.sigma} · 학습에 사용하지 않은 영상`:'시험 평가가 끝나면 표시됩니다.';
  const splits=s.dataset?.splits;
  $('splits').replaceChildren();
  if(splits){for(const [key,label] of [['train','학습'],['validation','검증'],['test','시험']]){const row=document.createElement('tr');for(const value of [label,shown(splits[key]?.OK),shown(splits[key]?.NG),shown(splits[key]?.total)]){const cell=document.createElement('td');cell.textContent=value;row.append(cell);}$('splits').append(row);}}
  else {const row=document.createElement('tr');const cell=document.createElement('td');cell.colSpan=4;cell.textContent='분할 결과 대기 · 미측정';row.append(cell);$('splits').append(row);}
  $('record').textContent=`${stampText} · ${states[s.status] || '기록 대기'} · ${stages[s.stage] || '상태 확인 중'}`;
  $('error').textContent=s.error ? `오류 유형: ${typeof s.error==='object' ? s.error.error_type || '실행 오류' : '실행 오류'} · 상세 원문은 이 PC의 실행 기록에 보관됩니다.` : '';
  if($('quickSigma'))$('quickSigma').textContent=number(s.sigma)?`σ ${s.sigma}`:'—';
  if($('quickEpoch'))$('quickEpoch').textContent=number(s.epoch)?`${s.epoch} / ${shown(s.epochs)}`:'—';
  if($('originalCount'))$('originalCount').textContent=number(s.dataset?.original_total)?s.dataset.original_total.toLocaleString('ko-KR'):'1,097';
}
async function refresh() {
  if(refreshing)return;refreshing=true;
  try {const response=await fetch('/api/status',{cache:'no-store'});if(!response.ok)throw new Error(String(response.status));render(await response.json());}
  catch { $('alert').className='alert visible failed';$('alert').textContent='상태 서버에 연결할 수 없습니다. 마지막 관측값을 표시합니다. 세션 URL과 서버 실행 상태를 확인해 주세요.';pipeline?.setStatus(0,'failed',false); }
  finally {refreshing=false;}
}
$('refresh').addEventListener('click',refresh);
window.addEventListener('resize',()=>{if(latest)drawChart(latest);});
for(const link of document.querySelectorAll('nav a'))link.addEventListener('click',()=>{document.querySelector('nav .active')?.classList.remove('active');link.classList.add('active');});
refresh();setInterval(refresh,3000);
