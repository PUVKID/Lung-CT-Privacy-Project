import * as THREE from './vendor/three.module.js';

export function createPipeline(canvas) {
  canvas.__pipelineDispose?.();
  const workspace=canvas.closest('.model-workspace')||canvas.parentElement;
  // 설명은 화면의 글자로 읽히게 두고 입체 모형은 처리 순서만 보조합니다.
  workspace.querySelector('.pipeline-guide')?.remove();
  workspace.querySelector('.pipeline-learning')?.remove();
  workspace.querySelector('.pipeline-technical')?.remove();
  workspace.querySelector('.pipeline-gallery')?.remove();
  let viewport=canvas.parentElement;
  if(!viewport.classList.contains('pipeline-viewport')){
    viewport=document.createElement('div');viewport.className='pipeline-viewport';canvas.before(viewport);viewport.append(canvas);
  }
  viewport.removeAttribute('tabindex');viewport.setAttribute('role','img');
  viewport.setAttribute('aria-label','실제 영상이 아닌 처리 순서 안내: CT 입력, 특징맵 64개 추출, 특징에만 블러, OK와 NG 분류');
  canvas.setAttribute('aria-label','CT 문서 아이콘, 무늬 없는 특징 시트, 경계가 부드러워지는 개념, 이진 분류의 보조 모형');
  const guide=document.createElement('section');guide.className='pipeline-guide';guide.setAttribute('aria-label','무엇을 학습하는 실험인가요');
  function easyText(node,text){const space=text.indexOf(' ');if(space>0&&/\p{Extended_Pictographic}/u.test(text.slice(0,space))){const icon=document.createElement('span');icon.className='pipeline-emoji';icon.setAttribute('aria-hidden','true');icon.textContent=text.slice(0,space);node.replaceChildren(icon,document.createTextNode(text.slice(space)));}else node.textContent=text;}
  const core=document.createElement('p');core.className='pipeline-core';easyText(core,'💡 원본 사진은 그대로 둡니다. 사진에서 찾은 선과 무늬만 부드럽게 바꿔 비교해요.');guide.append(core);
  const list=document.createElement('ol');list.className='pipeline-cards';guide.append(list);
  const definitions=[
    ['📷 ① 몸속 사진 넣기','CT는 몸속을 찍은 사진이에요. 원본 사진은 바꾸지 않아요.','원본은 그대로'],
    ['🔎 ② 선·무늬 찾기','서로 다른 돋보기 64개로 보는 것과 비슷해요. 사진 한 장에서 특징 그림 64개가 나와요.','돋보기는 이해를 돕는 비유'],
    ['🌫️ ③ 무늬 부드럽게','찾아낸 선과 무늬의 경계를 흐리게 해요. 원본 CT를 흐리는 것은 아니에요.','숫자가 클수록 더 부드럽게'],
    ['🗂️ ④ 두 묶음으로 나누기','자료의 이름에 따라 정상·양성은 OK, 악성은 NG로 나누도록 배워요.','OK·NG는 자료의 분류 이름']
  ];
  const cards=definitions.map(([title,description,note])=>{
    const card=document.createElement('li'),heading=document.createElement('h3'),p=document.createElement('p'),badge=document.createElement('span');
    easyText(heading,title);p.textContent=description;badge.textContent=note;badge.className='pipeline-card-note';card.append(heading,p,badge);list.append(card);return card;
  });
  viewport.before(guide);
  const learning=document.createElement('div');learning.className='pipeline-learning';
  const learningTitle=document.createElement('strong'),learningNote=document.createElement('span');
  easyText(learningTitle,'✏️ 배우는 곳: 모델 맨 뒤의 두 부분');
  learningNote.textContent='마지막 잔차 블록과 분류층만 배웁니다. 부드럽게 만드는 강도(σ)마다 모델을 따로 비교해요. 0은 흐리지 않은 기준이에요.';
  learning.append(learningTitle,learningNote);viewport.before(learning);
  const technical=document.createElement('details');technical.className='pipeline-technical';
  const summary=document.createElement('summary');easyText(summary,'🔧 정확한 모델 구조 보기');
  const fixed=document.createElement('p');fixed.textContent='돋보기는 비유입니다. 실제로는 첫 합성곱(conv1)의 서로 다른 필터 64개가 각각 반응한 특징맵입니다. 고정: conv1, DCT 가우시안 블러, bn1·relu·maxpool·layer1~3.';
  const train=document.createElement('p');train.textContent='학습: 마지막 잔차 블록(layer4)과 분류층(head). 배치정규화는 고정합니다.';
  const concept=document.createElement('p');concept.textContent='구조 개념 애니메이션이며 실제 영상·특징값·배치 이동·처리 속도를 나타내지 않습니다.';
  technical.append(summary,fixed,train,concept);viewport.after(technical);
  const oldSteps=workspace.querySelector('.steps');if(oldSteps)oldSteps.hidden=true;
  const oldNote=workspace.querySelector('.model-footnote');
  if(oldNote){oldNote.replaceChildren();const text=document.createElement('span');text.textContent='위 모형은 순서를 알려 주는 그림이에요. 실제 사진과 특징 그림은 아래에서 보세요.';oldNote.append(text);}
  const toolsText=workspace.querySelector('.model-tools>span');if(toolsText)toolsText.textContent='처리 순서 안내 · 실제 사진의 이동은 아닙니다';

  // 완료 강도 × 세 범주 × 여섯 단계를 파일 ID로 구분해 전체 구성을 보여줍니다.
  const gallery=document.createElement('section');gallery.className='pipeline-gallery';gallery.setAttribute('aria-label','블러 강도별 원본과 특징 맵 전체 구성');
  const galleryTitle=document.createElement('h2');easyText(galleryTitle,'🖼️ 사진과 특징 그림 살펴보기');
  const galleryDescription=document.createElement('p');galleryDescription.className='pipeline-gallery-description';
  galleryDescription.textContent='먼저 부드럽게 만드는 강도를 고르세요. 다음으로 양성·악성·정상 중 하나를 고르세요. 원본 1장과 특징 5단계를 볼 수 있어요. 모두 모이면 180장입니다.';
  const galleryNormalization=document.createElement('p');galleryNormalization.className='pipeline-gallery-normalization';
  galleryNormalization.textContent='특징 사진 한 장에는 작은 그림 10개가 있어요. 전체 평균 1개, 가장 큰 반응 1개, 골라낸 특징 8개입니다. 그림마다 색의 기준이 달라요. 밝은 곳이 암의 위치나 확률은 아닙니다.';
  const galleryStatus=document.createElement('p');galleryStatus.className='pipeline-gallery-status';galleryStatus.setAttribute('role','status');galleryStatus.setAttribute('aria-live','polite');galleryStatus.textContent='완료된 강도의 전체 사진을 기다리는 중입니다.';
  const galleryStatistics=document.createElement('p');galleryStatistics.className='pipeline-gallery-statistics';
  const sigmaFieldset=document.createElement('fieldset');sigmaFieldset.className='pipeline-gallery-controls';
  const sigmaLegend=document.createElement('legend');easyText(sigmaLegend,'🌫️ 1. 얼마나 부드럽게 만들까요? 숫자가 클수록 더 부드러워요');
  const sigmaControls=document.createElement('div');sigmaControls.className='pipeline-gallery-options';sigmaFieldset.append(sigmaLegend,sigmaControls);
  const classFieldset=document.createElement('fieldset');classFieldset.className='pipeline-gallery-controls';
  const classLegend=document.createElement('legend');easyText(classLegend,'🗂️ 2. 어떤 자료를 볼까요?');
  const classControls=document.createElement('div');classControls.className='pipeline-gallery-options pipeline-gallery-class-options';classFieldset.append(classLegend,classControls);
  const selectionStatistics=document.createElement('p');selectionStatistics.className='pipeline-gallery-selection';
  const galleryOverview=document.createElement('div');galleryOverview.className='pipeline-gallery-overview';galleryOverview.hidden=true;
  const overviewTitle=document.createElement('p');easyText(overviewTitle,'👆 사진 6장 한눈에 보기 · 사진을 누르면 쉬운 설명과 설정이 열려요');
  const galleryThumbnails=document.createElement('div');galleryThumbnails.className='pipeline-gallery-thumbnails';galleryThumbnails.setAttribute('role','group');galleryThumbnails.setAttribute('aria-label','선택한 여섯 그림의 설정과 설명');galleryOverview.append(overviewTitle,galleryThumbnails);
  const galleryGrid=document.createElement('div');galleryGrid.className='pipeline-gallery-grid';
  gallery.append(galleryTitle,galleryDescription,galleryNormalization,galleryStatus,galleryStatistics,sigmaFieldset,classFieldset,selectionStatistics,galleryOverview,galleryGrid);workspace.append(gallery);
  const sigmaOrder=[0,1,2,4,8,16,32,64,128,256],allowedSigmas=new Set(sigmaOrder);
  const classLabels={Bengin_cases:'양성',Malignant_cases:'악성',Normal_cases:'정상'};
  const previewIdPattern=/^(0|1|2|4|8|16|32|64|128|256)-(Bengin_cases|Malignant_cases|Normal_cases)-[0-5]$/;
  const previewRunPattern=/^[a-f0-9]{16}$/,galleryFigures=new Map(),sigmaButtons=new Map(),classButtons=new Map();
  let currentPreviewRun=null,externalSigma=null,externalRun=null;
  let previewItems=new Map(),completedSigmas=new Set(),reportedSigmas=new Set(),selectedSigma=null,selectedClass='Bengin_cases';
  let galleryController=null,galleryInterval=0,galleryTimeout=0,galleryBusy=false;
  function previewMessage(text){if(galleryStatus.textContent!==text)galleryStatus.textContent=text;}
  function choiceButton(parent){
    const button=document.createElement('button');button.type='button';button.className='pipeline-gallery-choice';button.disabled=true;button.setAttribute('aria-pressed','false');
    const name=document.createElement('span'),note=document.createElement('small');button.append(name,note);parent.append(button);return {button,name,note};
  }
  for(const sigma of sigmaOrder){
    const entry=choiceButton(sigmaControls);entry.name.textContent=`σ ${sigma}`;entry.note.textContent='대기';sigmaButtons.set(sigma,entry);
    entry.button.addEventListener('click',()=>{if(disposed||!completedSigmas.has(sigma))return;externalSigma=sigma;selectedSigma=sigma;renderGallery();canvas.dispatchEvent(new CustomEvent('ct-sigma-select',{detail:{sigma,run_id:currentPreviewRun}}));});
  }
  for(const [key,label] of Object.entries(classLabels)){
    const entry=choiceButton(classControls);entry.name.textContent=label;entry.note.textContent='대기';classButtons.set(key,entry);
    entry.button.addEventListener('click',()=>{if(disposed||selectedSigma===null)return;selectedClass=key;renderGallery();});
  }
  // 화면에는 허용된 생성 설정만 옮기며 경로·해시·원자료 목록은 열거하지 않습니다.
  function settingNumber(value){return typeof value==='number'&&Number.isFinite(value)?String(value):'미확인';}
  function settingText(value){return typeof value==='string'&&value.trim()?value:typeof value==='number'?settingNumber(value):'미확인';}
  function previewDescription(item){
    const settings=item.settings&&typeof item.settings==='object'&&!Array.isArray(item.settings)?item.settings:{};
    const shape=Array.isArray(settings.shape)&&settings.shape.length===3&&settings.shape.every(n=>Number.isInteger(n)&&n>0)?settings.shape:null;
    const indices=Array.isArray(settings.panel_indices)?settings.panel_indices.filter(n=>Number.isInteger(n)&&n>=0):null;
    const original=item.stage===0,label=classLabels[item.class_key];
    const places=['원본 CT','첫 합성곱과 특징 블러','첫 번째 잔차 블록','두 번째 잔차 블록','세 번째 잔차 블록','마지막 잔차 블록'];
    const summary=original?[
      `몸속을 찍은 CT 사진이에요. 이 자료의 분류 이름은 '${label}'입니다.`,
      '같은 사진이 모델을 지나는 모습을 원본 1장과 특징 5단계로 나눠 보여 줘요.',
      '원본 사진은 흐리지 않아요. 여기의 밝고 어두운 색은 사진의 픽셀 밝기예요.'
    ]:[
      `${label} 자료 한 장에서 모델이 찾은 선과 무늬예요. ${item.stage}단계에서 꺼내 본 특징 그림입니다.`,
      '작은 그림 10개를 모았어요. 전체 반응의 평균 1개, 각 위치의 가장 큰 반응 1개, 골라낸 특징 8개예요.',
      '그림마다 색의 기준이 달라요. 밝은 곳이 암의 위치나 확률을 뜻하지는 않아요.'
    ];
    const shapeExplanation=shape?`특징 그림이 ${shape[0]}개예요. 하나는 세로 ${shape[1]}칸, 가로 ${shape[2]}칸입니다.${item.stage>=2?' 작은 모눈종이처럼 칸이 커 보이는 것은 뒤 단계에서 그림의 칸 수가 줄었기 때문이에요.':''}`:'그림의 크기 정보는 아직 없어요.';
    const rows=[['현재 블러 강도',`σ = ${settingNumber(item.sigma)}`],['원본 범주',label],['처리 단계',original?'0단계 · 원본 CT':`${item.stage}단계 · ${places[item.stage]}`],['추출 지점',settingText(settings.layer)],
      [original?'입력 크기 (채널 × 높이 × 너비)':'특징 크기 (채널 × 높이 × 너비)',shape?shape.map(settingNumber).join(' × '):'미확인'],['실제 채널 수',shape?settingNumber(shape[0]):'미확인'],
      ['선택한 채널',original?'해당 없음 · 원본 한 장':indices?indices.map(settingNumber).join(' · ')||'없음':'미확인'],['그림 구성',original?'원본 CT 1패널':`평균 · 최댓값 · 개별 ${indices?indices.length:'미확인'}채널 (총 ${settingNumber(settings.panel_count)}패널)`],
      ['색 정규화',settingText(settings.normalization)],['사진 생성 정밀도',settingText(settings.precision)],['입력 전처리',settingText(settings.preprocessing)],['완료 모델의 최적 학습 회차',typeof settings.checkpoint_epoch==='number'?`${settingNumber(settings.checkpoint_epoch)}회`:'미확인']];
    const policy=settings.training_policy&&typeof settings.training_policy==='object'?settings.training_policy:{};
    const trainingRows=[['최적화 방법',settingText(policy.optimizer)],['학습 배치 크기',settingNumber(policy.batch_size)],['초기 학습률',settingNumber(policy.initial_learning_rate)],['가중치 감쇠',settingNumber(policy.weight_decay)],['최대 학습 회차',settingNumber(policy.max_epochs)],['조기 종료 대기 회차',settingNumber(policy.patience)],['의미 있는 손실 개선 기준',settingNumber(policy.min_delta)]];
    const limits=Array.isArray(settings.panel_minmax)?settings.panel_minmax.slice(0,original?1:10):[];
    const minmaxRows=limits.map((entry,index)=>[original?'원본 CT':index===0?'전체 채널 평균':index===1?'채널 최댓값':`채널 ${indices&&indices[index-2]!==undefined?indices[index-2]:'미확인'}`,settingNumber(entry?.min),settingNumber(entry?.max)]);
    return {title:original?'📷 원본 사진 이야기':`🔎 ${item.stage}단계 특징 그림 이야기`,summary,shapeExplanation,rows,trainingRows,minmaxRows,indices,original};
  }
  const settingsDialog=document.createElement('dialog');settingsDialog.className='pipeline-settings-dialog';settingsDialog.setAttribute('role','dialog');settingsDialog.setAttribute('aria-modal','true');
  const dialogTitleId=`${canvas.id||'pipeline'}-feature-settings-title`,dialogSummaryId=`${canvas.id||'pipeline'}-feature-settings-summary`;
  settingsDialog.setAttribute('aria-labelledby',dialogTitleId);settingsDialog.setAttribute('aria-describedby',dialogSummaryId);
  const dialogHeader=document.createElement('div');dialogHeader.className='pipeline-settings-header';
  const dialogHeading=document.createElement('h2');dialogHeading.id=dialogTitleId;dialogHeading.tabIndex=-1;
  const dialogClose=document.createElement('button');dialogClose.type='button';dialogClose.className='pipeline-settings-close';dialogClose.textContent='닫기';dialogClose.setAttribute('aria-label','사진 설정과 설명 닫기');
  const dialogBody=document.createElement('div');dialogBody.className='pipeline-settings-body';dialogHeader.append(dialogHeading,dialogClose);settingsDialog.append(dialogHeader,dialogBody);gallery.append(settingsDialog);
  let dialogOpener=null,dialogReturnId=null,dialogReturnKind='thumbnail',previousBodyOverflow=null,galleryRenderPending=false;
  function settingList(rows){const dl=document.createElement('dl');dl.className='pipeline-settings-list';for(const [name,value] of rows){const row=document.createElement('div'),dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=name;dd.textContent=value;row.append(dt,dd);dl.append(row);}return dl;}
  function restoreDialogState(restoreFocus=true){
    if(previousBodyOverflow===null)return;
    document.body.style.overflow=previousBodyOverflow;previousBodyOverflow=null;
    const oldOpener=dialogOpener,returnId=dialogReturnId,returnKind=dialogReturnKind;dialogOpener=null;dialogReturnId=null;
    if(galleryRenderPending&&!disposed){galleryRenderPending=false;renderGallery();}
    const entry=galleryFigures.get(returnId),fallback=entry?.[returnKind]||[...sigmaButtons.values()].find(x=>!x.button.disabled)?.button;
    if(restoreFocus)(oldOpener?.isConnected?oldOpener:fallback)?.focus({preventScroll:true});
  }
  function closePreviewSettings(restoreFocus=true){if(settingsDialog.open)settingsDialog.close();restoreDialogState(restoreFocus);}
  function onDialogKey(event){
    if(!settingsDialog.open)return;
    if(event.key==='Escape'){event.preventDefault();event.stopPropagation();closePreviewSettings();return;}
    if(event.key!=='Tab')return;
    const focusable=[...settingsDialog.querySelectorAll('button:not([disabled]),a[href],summary,[tabindex]:not([tabindex="-1"])')].filter(node=>node.getClientRects().length>0);
    const first=focusable[0],last=focusable.at(-1);if(!first){event.preventDefault();dialogHeading.focus();return;}
    if(event.shiftKey&&(document.activeElement===first||!focusable.includes(document.activeElement))){event.preventDefault();last.focus();}
    else if(!event.shiftKey&&(document.activeElement===last||!focusable.includes(document.activeElement))){event.preventDefault();first.focus();}
  }
  settingsDialog.addEventListener('cancel',event=>{event.preventDefault();closePreviewSettings();});
  settingsDialog.addEventListener('close',()=>restoreDialogState());
  settingsDialog.addEventListener('click',event=>{if(event.target===settingsDialog){const r=settingsDialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)closePreviewSettings();}});
  dialogClose.addEventListener('click',()=>closePreviewSettings());
  function openPreviewSettings(id,trigger){
    if(disposed)return;const item=previewItems.get(id);if(!validPreview(item))return;
    const description=previewDescription(item);easyText(dialogHeading,description.title);dialogBody.replaceChildren();
    const identity=document.createElement('p');identity.className='pipeline-settings-identity';identity.textContent=`σ = ${item.sigma} · ${classLabels[item.class_key]} · ${item.stage}단계`;
    const easy=document.createElement('div');easy.className='pipeline-settings-summary';easy.id=dialogSummaryId;
    for(const [index,sentence] of description.summary.entries()){const section=document.createElement('section'),h=document.createElement('h3'),p=document.createElement('p');easyText(h,['📷 이 사진은 무엇인가요?','🧩 그림이 왜 여러 개인가요?','💡 어떻게 보면 되나요?'][index]);p.textContent=sentence;section.append(h,p);easy.append(section);}
    const image=document.createElement('img');image.className='pipeline-settings-image';image.src=item.image_url;image.alt=item.stage===0?'선택한 대표 원본 CT':`${item.stage}단계 실제 특징 맵 10패널`;image.decoding='async';image.referrerPolicy='same-origin';
    const openLink=document.createElement('a');openLink.className='pipeline-preview-open';openLink.href=item.image_url;openLink.target='_blank';openLink.rel='noopener noreferrer';openLink.textContent='사진을 원본 크기로 새 탭에서 보기';
    const caption=document.createElement('p');caption.className='pipeline-settings-caption';caption.textContent=typeof item.caption==='string'?item.caption:'사진의 생성 설명은 아직 없습니다.';
    const shapeMeaning=document.createElement('p');shapeMeaning.className='pipeline-settings-help';shapeMeaning.textContent=description.original?'입력의 3채널은 같은 회색조를 복제한 것입니다. 서로 다른 특징 그림 3개가 아닙니다.':description.shapeExplanation+(description.indices?` 채널 ${description.indices.join('·')}은 전체 채널 중 균등 간격으로 고른 ${description.indices.length}개입니다.`:'');
    const numbers=document.createElement('details');numbers.className='pipeline-settings-advanced';const numbersTitle=document.createElement('summary');easyText(numbersTitle,'🔧 자세한 숫자와 설정 보기');numbers.append(numbersTitle,shapeMeaning,settingList(description.rows),caption);
    const panels=document.createElement('p');panels.className='pipeline-panel-guide';if(description.original)panels.textContent='원본 한 장이에요. 같은 회색조를 3채널에 복제해 입력하며 서로 다른 특징 3개라는 뜻은 아닙니다.';else for(const text of ['🧩 전체 반응 모아 보기(평균)','🔥 가장 큰 반응 고르기(최댓값)','🔍 특징 8개 골라 보기']){const part=document.createElement('span');easyText(part,text);panels.append(part);}
    dialogBody.append(identity,easy,image,openLink,panels,numbers);
    const training=document.createElement('details');training.className='pipeline-settings-advanced';const trainingTitle=document.createElement('summary');easyText(trainingTitle,'✏️ 모델이 배울 때 쓴 설정');
    const precisionNote=document.createElement('p');precisionNote.textContent='사진 생성 정밀도는 이 그림을 추출한 평가 추론의 정밀도입니다. 훈련 중 사용한 정밀도와는 별도 항목입니다.';training.append(trainingTitle,precisionNote,settingList(description.trainingRows));dialogBody.append(training);
    const advanced=document.createElement('details');advanced.className='pipeline-settings-advanced';const advancedTitle=document.createElement('summary');easyText(advancedTitle,'📊 작은 그림마다 색의 숫자 보기');advanced.append(advancedTitle);
    if(description.minmaxRows.length){const table=document.createElement('table'),thead=document.createElement('thead'),head=document.createElement('tr'),tbody=document.createElement('tbody');for(const title of ['패널','최솟값','최댓값']){const cell=document.createElement('th');cell.textContent=title;head.append(cell);}thead.append(head);for(const values of description.minmaxRows){const row=document.createElement('tr');for(const value of values){const cell=document.createElement('td');cell.textContent=value;row.append(cell);}tbody.append(row);}table.append(thead,tbody);const scroll=document.createElement('div');scroll.className='pipeline-settings-table';scroll.append(table);advanced.append(scroll);}
    else {const note=document.createElement('p');note.textContent='패널 범위 정보가 아직 없습니다.';advanced.append(note);}
    const normalizationNote=document.createElement('p');normalizationNote.textContent=description.original?'원본 CT의 회색조 표시 조건입니다.':'각 패널은 자체 범위로 정규화됩니다. 같은 색이 같은 절대 반응값을 뜻하지 않습니다. 숫자는 반올림하지 않은 원값입니다.';advanced.append(normalizationNote);dialogBody.append(advanced);
    if(typeof settingsDialog.showModal!=='function'){previewMessage('이 브라우저에서는 설정 창을 열 수 없습니다. 사진 아래 설명과 원본 크기 링크를 확인해 주세요.');return;}
    dialogOpener=trigger;dialogReturnId=id;dialogReturnKind=trigger.classList.contains('pipeline-preview-image-button')?'imageButton':'thumbnail';previousBodyOverflow=document.body.style.overflow;
    try{settingsDialog.showModal();document.body.style.overflow='hidden';dialogBody.scrollTop=0;dialogHeading.focus({preventScroll:true});}
    catch(error){restoreDialogState(false);previewMessage('설정 창을 열지 못했습니다. 사진 아래 설명은 계속 확인할 수 있습니다.');}
  }
  function validPreview(item){
    if(!item||typeof item.id!=='string'||!previewIdPattern.test(item.id)||!Number.isInteger(item.sigma)||!allowedSigmas.has(item.sigma)||!Number.isInteger(item.stage)||item.stage<0||item.stage>5)return false;
    if(!Object.hasOwn(classLabels,item.class_key)||item.class_label!==classLabels[item.class_key])return false;
    return item.id===`${item.sigma}-${item.class_key}-${item.stage}`&&item.image_url===`/api/feature-previews/image/${item.id}`;
  }
  function readySigma(sigma){
    if(!reportedSigmas.has(sigma))return false;
    for(const key of Object.keys(classLabels))for(let stage=0;stage<=5;stage++)if(!previewItems.has(`${sigma}-${key}-${stage}`))return false;
    return true;
  }
  function renderGallery(){
    if(disposed)return;
    if(settingsDialog.open){galleryRenderPending=true;return;}
    for(const [sigma,entry] of sigmaButtons){
      const ready=completedSigmas.has(sigma),count=[...previewItems.values()].filter(item=>item.sigma===sigma).length;
      entry.button.disabled=!ready;entry.button.setAttribute('aria-pressed',String(ready&&selectedSigma===sigma));
      entry.note.textContent=ready?'완료 · 18장':reportedSigmas.has(sigma)?`생성 중 · ${count}/18`:'대기';
      entry.button.setAttribute('aria-label',`블러 강도 ${sigma}, ${entry.note.textContent}`);
    }
    const chosen=selectedSigma===null?[]:[...previewItems.values()].filter(item=>item.sigma===selectedSigma);
    for(const [key,entry] of classButtons){
      const count=chosen.filter(item=>item.class_key===key).length;entry.button.disabled=selectedSigma===null;
      entry.button.setAttribute('aria-pressed',String(selectedSigma!==null&&selectedClass===key));entry.note.textContent=selectedSigma===null?'대기':`${count}장`;
    }
    galleryStatistics.textContent=`완료 ${completedSigmas.size} / 10강도 · ${previewItems.size} / 180장`;
    const visible=chosen.filter(item=>item.class_key===selectedClass).sort((a,b)=>a.stage-b.stage);
    selectionStatistics.textContent=selectedSigma!==null&&!completedSigmas.has(selectedSigma)?`σ ${selectedSigma}의 사진은 아직 준비되지 않았어요.`:selectedSigma===null?'강도별 18장이 준비되면 선택할 수 있습니다.':`선택 강도 σ = ${selectedSigma}: ${chosen.length}장 · 현재 ${classLabels[selectedClass]}: ${visible.length}장 (원본 + 1~5단계)`;
    const ids=new Set(),figures=[],thumbnails=[];galleryOverview.hidden=selectedSigma===null;
    for(const item of visible){
      ids.add(item.id);let entry=galleryFigures.get(item.id);
      if(!entry){
        const figure=document.createElement('figure'),heading=document.createElement('div'),title=document.createElement('h3'),link=document.createElement('a'),image=document.createElement('img'),caption=document.createElement('figcaption'),imageError=document.createElement('p');
        figure.className=item.stage===0?'pipeline-preview-original':'pipeline-preview-montage';figure.dataset.previewId=item.id;figure.id=`feature-stage-${item.id}`;heading.className='pipeline-preview-heading';
        title.textContent=item.stage===0?`0단계 · ${classLabels[item.class_key]} 원본 CT`:`${item.stage}단계 · ${classLabels[item.class_key]} 특징 맵 · 10패널`;
        link.className='pipeline-preview-open';link.textContent='원본 크기로 보기';link.href=item.image_url;link.target='_blank';link.rel='noopener noreferrer';
        link.setAttribute('aria-label',`${classLabels[item.class_key]} σ ${item.sigma} ${item.stage}단계 그림 원본 크기로 새 탭에서 보기`);heading.append(title,link);
        image.alt=item.stage===0?`블러 강도 ${item.sigma} 비교에 사용하는 ${classLabels[item.class_key]} 대표 원본 CT`:`블러 강도 ${item.sigma}, ${classLabels[item.class_key]}, ${item.stage}단계의 채널 평균·최대·8개 채널 10패널`;
        image.loading='lazy';image.decoding='async';image.referrerPolicy='same-origin';imageError.className='pipeline-preview-error';imageError.hidden=true;imageError.textContent='이 그림을 불러오지 못했습니다. 다음 갱신 때 다시 확인합니다.';
        image.onerror=()=>{if(disposed)return;image.dataset.failed='true';image.hidden=true;imageError.hidden=false;};
        image.onload=()=>{if(disposed)return;image.dataset.failed='false';image.hidden=false;imageError.hidden=true;};
        const thumbnail=document.createElement('button'),thumbImage=document.createElement('img'),thumbLabel=document.createElement('span');
        thumbnail.type='button';thumbnail.className='pipeline-preview-thumbnail';thumbnail.dataset.previewId=item.id;thumbnail.setAttribute('aria-haspopup','dialog');thumbnail.setAttribute('aria-label',`${classLabels[item.class_key]} ${item.stage}단계 사진 설정과 설명 열기`);thumbnail.addEventListener('click',()=>openPreviewSettings(item.id,thumbnail));
        thumbImage.alt=item.stage===0?'원본 CT 미리보기':`${item.stage}단계 10패널 특징 맵 미리보기`;thumbImage.loading='eager';thumbImage.decoding='async';thumbImage.referrerPolicy='same-origin';
        thumbLabel.textContent=item.stage===0?'0 · 원본 CT':`${item.stage} · 특징 맵`;thumbnail.append(thumbImage,thumbLabel);
        const imageButton=document.createElement('button');imageButton.type='button';imageButton.className='pipeline-preview-image-button';imageButton.dataset.previewId=item.id;imageButton.setAttribute('aria-haspopup','dialog');imageButton.setAttribute('aria-label',`${classLabels[item.class_key]} ${item.stage}단계 사진 설정과 설명 열기`);imageButton.append(image);imageButton.addEventListener('click',()=>openPreviewSettings(item.id,imageButton));
        const short=document.createElement('p');short.className='pipeline-preview-easy';const exact=document.createElement('details'),exactTitle=document.createElement('summary');exact.className='pipeline-preview-exact';exactTitle.textContent='정확한 생성 설명 보기';exact.append(exactTitle,caption);figure.append(heading,imageButton,imageError,short,exact);entry={figure,image,caption,short,link,thumbnail,thumbImage,imageButton};galleryFigures.set(item.id,entry);
      }
      entry.short.textContent=previewDescription(item).summary[0]+(item.stage===0?' 원본은 그대로예요.':' 작은 그림 10개를 모아 놓았어요. 사진을 누르면 설명이 열려요.');
      entry.caption.textContent=typeof item.caption==='string'?item.caption:'이 단계의 생성 조건과 설명을 기다리는 중입니다.';
      entry.image.width=Number.isInteger(item.width)&&item.width>0&&item.width<=16384?item.width:item.stage===0?512:2288;
      entry.image.height=Number.isInteger(item.height)&&item.height>0&&item.height<=16384?item.height:512;
      if(entry.image.getAttribute('src')!==item.image_url||entry.image.dataset.failed==='true')entry.image.src=item.image_url;
      if(entry.thumbImage.getAttribute('src')!==item.image_url)entry.thumbImage.src=item.image_url;
      figures.push(entry.figure);thumbnails.push(entry.thumbnail);
    }
    for(const [id,entry] of galleryFigures)if(!ids.has(id)){entry.image.onload=null;entry.image.onerror=null;entry.figure.remove();galleryFigures.delete(id);}
    if(galleryGrid.children.length!==figures.length||figures.some((figure,index)=>galleryGrid.children[index]!==figure))galleryGrid.replaceChildren(...figures);
    if(galleryThumbnails.children.length!==thumbnails.length||thumbnails.some((thumbnail,index)=>galleryThumbnails.children[index]!==thumbnail))galleryThumbnails.replaceChildren(...thumbnails);
  }
  async function refreshPreviews(){
    if(disposed||galleryBusy||document.hidden)return;galleryBusy=true;const controller=new AbortController();galleryController=controller;
    galleryTimeout=window.setTimeout(()=>controller.abort(),8000);
    try{
      const response=await fetch('/api/feature-previews',{credentials:'same-origin',cache:'no-store',signal:controller.signal});if(disposed)return;
      if(response.status===404){previewMessage('완료된 강도의 전체 사진을 기다리는 중입니다.');return;}
      if(!response.ok)throw new Error('preview unavailable');
      const payload=await response.json();if(disposed)return;
      if(typeof payload.run_id!=='string'||!previewRunPattern.test(payload.run_id)||!Array.isArray(payload.items)){previewMessage('현재 실행에 맞는 전체 특징 맵을 기다리는 중입니다.');return;}
      if(externalRun!==null&&payload.run_id!==externalRun){previewMessage('새 실험의 사진을 기다리고 있어요.');return;}
      if(currentPreviewRun!==payload.run_id){closePreviewSettings(false);for(const entry of galleryFigures.values()){entry.image.onload=null;entry.image.onerror=null;}galleryFigures.clear();galleryGrid.replaceChildren();galleryThumbnails.replaceChildren();selectedSigma=null;if(currentPreviewRun!==null)externalSigma=null;currentPreviewRun=payload.run_id;}
      const valid=new Map();for(const item of payload.items)if(validPreview(item))valid.set(item.id,item);previewItems=valid;
      reportedSigmas=new Set(Array.isArray(payload.completed_sigmas)?payload.completed_sigmas.filter(sigma=>Number.isInteger(sigma)&&allowedSigmas.has(sigma)):[]);
      completedSigmas=new Set(sigmaOrder.filter(readySigma));
      if(externalSigma!==null)selectedSigma=externalSigma;else if(selectedSigma===null||!completedSigmas.has(selectedSigma))selectedSigma=sigmaOrder.find(sigma=>completedSigmas.has(sigma))??null;
      renderGallery();
      previewMessage(completedSigmas.size?'완료된 강도와 범주를 선택하면 원본부터 5단계까지 6개 그림이 아래에 모두 표시됩니다.':'완료된 강도당 18장의 사진이 준비되기를 기다리는 중입니다.');
    }catch(error){
      if(!disposed)previewMessage(galleryFigures.size?'선택한 그림을 표시하고 있습니다. 목록을 잠시 갱신하지 못했습니다.':'전체 특징 맵을 기다리는 중입니다. 현재 미리보기를 불러올 수 없습니다.');
    }finally{window.clearTimeout(galleryTimeout);galleryTimeout=0;galleryBusy=false;if(galleryController===controller)galleryController=null;}
  }
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,powerPreference:'low-power'});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  const scene=new THREE.Scene(),root=new THREE.Group();scene.add(root);
  const camera=new THREE.OrthographicCamera(-10,10,3,-3,.1,60);camera.position.set(.7,5.5,19);camera.lookAt(0,.5,0);camera.updateMatrixWorld();
  const ambient=new THREE.HemisphereLight(0xf2f6ff,0x8b98ad,1.3);scene.add(ambient);
  const key=new THREE.DirectionalLight(0xfffcf8,2.6);key.position.set(-5,10,8);key.castShadow=true;
  Object.assign(key.shadow.camera,{left:-11,right:11,top:4,bottom:-4,near:.5,far:30});key.shadow.mapSize.set(1024,512);key.shadow.normalBias=.025;scene.add(key);
  const fill=new THREE.DirectionalLight(0xd5e4ff,1.2);fill.position.set(7,5,-4);scene.add(fill);
  const geometries=new Set(),materials=new Set(),textures=new Set(),themed=[],labels=[],modules=[];
  const colors={paper:[0xf0f3f8,0x7d8ca4],frame:[0x637790,0x394b66],blue:[0x7895bd,0x97b5df],line:[0x506b91,0xb8ccea],soft:[0xc1cfe2,0x7188aa]};
  function material(type,options={}){const m=new THREE.MeshStandardMaterial({color:colors[type][0],roughness:.55,metalness:.1,...options});materials.add(m);themed.push({m,type});return m;}
  const shell=material('paper'),frameMat=material('frame'),blue=material('blue'),lineMat=material('line'),soft=material('soft');
  const geometryCache=new Map();
  function box(w,h,d,m,x,y,z,parent=root){
    const cacheKey=[w,h,d].join(':');let geometry=geometryCache.get(cacheKey);
    if(!geometry){geometry=new THREE.BoxGeometry(w,h,d);geometries.add(geometry);geometryCache.set(cacheKey,geometry);}
    const mesh=new THREE.Mesh(geometry,m);mesh.position.set(x,y,z);mesh.castShadow=true;mesh.receiveShadow=true;parent.add(mesh);return mesh;
  }
  function tube(points,r=.025,m=lineMat,parent=root){const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)),false,'centripetal');const g=new THREE.TubeGeometry(curve,20,r,8,false);geometries.add(g);const mesh=new THREE.Mesh(g,m);parent.add(mesh);return mesh;}
  function label(text,x,y,width=1.4,parent=root){
    const c=document.createElement('canvas');c.height=112;let ctx=c.getContext('2d');ctx.font='700 64px Nanum, sans-serif';c.width=Math.ceil(ctx.measureText(text).width+32);ctx=c.getContext('2d');
    const texture=new THREE.CanvasTexture(c);texture.colorSpace=THREE.SRGBColorSpace;textures.add(texture);
    const m=new THREE.SpriteMaterial({map:texture,transparent:true,depthTest:false,depthWrite:false,toneMapped:false});materials.add(m);
    const sprite=new THREE.Sprite(m);sprite.position.set(x,y,.8);sprite.scale.set(width,width*c.height/c.width,1);parent.add(sprite);labels.push({ctx,texture,text});return sprite;
  }
  const centers=[-6.6,-2.2,2.2,6.6];
  for(let i=0;i<4;i++){
    const group=new THREE.Group();group.position.x=centers[i];root.add(group);
    const rail=material('soft');box(3.1,.045,.12,rail,0,-.43,.9,group);modules.push({group,rail});
  }
  // CT 표시는 문서 아이콘일 뿐 영상이나 영상의 대체 무늬가 아닙니다.
  const input=modules[0].group;
  box(1.55,1.8,.1,frameMat,0,.54,0,input);box(1.37,1.62,.03,shell,0,.54,.075,input);
  label('CT',0,.76,1.02,input);box(.82,.035,.025,soft,0,.18,.11,input);box(.6,.035,.025,soft,-.11,-.02,.11,input);
  // 64개 모두를 모사하지 않고 무늬 없는 시트 묶음과 숫자로 개념을 표시합니다.
  const sheets=modules[1].group;
  for(let i=0;i<5;i++)box(1.5,1.5,.055,i===4?shell:soft,-.32+i*.16,.52,-.4+i*.18,sheets);
  label('64',.18,.67,1.12,sheets);
  // 단순한 선 하나의 경계가 넓고 부드러워지는 개념입니다. 실제 특징 영상은 아닙니다.
  const blur=modules[2].group;
  box(1.12,1.5,.06,shell,-.78,.52,0,blur);box(1.12,1.5,.06,shell,.78,.52,0,blur);
  box(.045,.96,.025,lineMat,-.78,.52,.06,blur);
  const blurred=[];
  for(let i=-5;i<=5;i++){
    const m=material('line',{transparent:true,opacity:.68*Math.exp(-i*i/8),depthWrite:false});
    blurred.push(box(.026,.96,.025,m,.78+i*.026,.52,.06,blur));
  }
  tube([[-.15,.52,.1],[.15,.52,.1]],.018,lineMat,blur);
  const arrowGeometry=new THREE.ConeGeometry(.065,.14,4);geometries.add(arrowGeometry);
  const blurArrow=new THREE.Mesh(arrowGeometry,lineMat);blurArrow.rotation.z=-Math.PI/2;blurArrow.position.set(.16,.52,.1);blur.add(blurArrow);
  label('적용 전',-.78,1.61,1.05,blur);label('적용 후',.78,1.61,1.05,blur);
  // 정상·양성과 악성의 분류 이름만 표시하며 확률이나 성능을 만들지 않습니다.
  const output=modules[3].group;
  box(2.25,1.65,.28,frameMat,0,.54,0,output);
  box(.91,1.22,.06,shell,-.54,.54,.18,output);box(.91,1.22,.06,soft,.54,.54,.18,output);
  label('OK',-.54,.62,.74,output);label('NG',.54,.62,.74,output);
  for(let i=0;i<3;i++){
    tube([[centers[i]+1.65,.5,0],[centers[i+1]-1.65,.5,0]],.022,lineMat);
    const arrow=new THREE.Mesh(arrowGeometry,lineMat);arrow.rotation.z=-Math.PI/2;arrow.position.set(centers[i+1]-1.65,.5,0);root.add(arrow);
  }
  const floorGeometry=new THREE.PlaneGeometry(22,8);geometries.add(floorGeometry);
  const floorMaterial=new THREE.ShadowMaterial({color:0x4f617b,opacity:.14});materials.add(floorMaterial);
  const floor=new THREE.Mesh(floorGeometry,floorMaterial);floor.rotation.x=-Math.PI/2;floor.position.y=-.49;floor.receiveShadow=true;scene.add(floor);
  let dark=false,paused=false,running=false,active=-1,status='waiting',phase=0,last=0,dirty=true,disposed=false,raf=0,lastWidth=0,lastHeight=0;
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  const bounds=new THREE.Box3().setFromObject(root),corners=[];
  for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z])corners.push(new THREE.Vector3(x,y,z).applyMatrix4(camera.matrixWorldInverse));
  const edges={left:Math.min(...corners.map(p=>p.x)),right:Math.max(...corners.map(p=>p.x)),bottom:Math.min(...corners.map(p=>p.y)),top:Math.max(...corners.map(p=>p.y))};
  function resize(){
    const rect=canvas.getBoundingClientRect(),w=Math.round(rect.width),h=Math.round(rect.height);if(!w||!h||w===lastWidth&&h===lastHeight||disposed)return;
    lastWidth=w;lastHeight=h;renderer.setSize(w,h,false);const aspect=w/h,height=Math.max((edges.top-edges.bottom)/.8,(edges.right-edges.left)/(aspect*.94)),x=(edges.left+edges.right)/2,y=(edges.top+edges.bottom)/2;
    camera.left=x-height*aspect/2;camera.right=x+height*aspect/2;camera.top=y+height/2;camera.bottom=y-height/2;camera.updateProjectionMatrix();dirty=true;
  }
  function repaintLabels(){for(const item of labels){const ctx=item.ctx;ctx.clearRect(0,0,ctx.canvas.width,112);ctx.font='700 64px Nanum, sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=dark?'#e1eaf7':'#304967';ctx.fillText(item.text,ctx.canvas.width/2,58);item.texture.needsUpdate=true;}}
  function updateState(){
    for(let i=0;i<4;i++){
      const selected=i===active;modules[i].rail.color.setHex(selected?(dark?0xbed3ef:0x5d80b1):(dark?0x5e7392:0xb7c8de));
      cards[i].classList.toggle('is-active',selected&&running);
    }
    easyText(learningTitle,running?'✏️ 지금 배우는 곳: 모델 맨 뒤의 두 부분':'✏️ 배우는 곳: 모델 맨 뒤의 두 부분');
    viewport.dataset.pipelineState=running?'running':status;dirty=true;
  }
  function setTheme(theme){dark=theme==='dark';for(const {m,type} of themed)m.color.setHex(colors[type][dark?1:0]);ambient.intensity=dark?1.1:1.3;key.intensity=dark?2.1:2.6;fill.intensity=dark?1.5:1.2;floorMaterial.opacity=dark?.25:.14;repaintLabels();updateState();}
  const observer=new ResizeObserver(resize);observer.observe(viewport);observer.observe(canvas);
  function resetClock(){last=0;dirty=true;}reduced.addEventListener('change',resetClock);document.addEventListener('visibilitychange',resetClock);document.addEventListener('keydown',onDialogKey,true);
  function dispose(){if(disposed)return;disposed=true;closePreviewSettings(false);document.removeEventListener('keydown',onDialogKey,true);settingsDialog.remove();window.clearInterval(galleryInterval);window.clearTimeout(galleryTimeout);galleryController?.abort();for(const entry of galleryFigures.values()){entry.image.onload=null;entry.image.onerror=null;}galleryFigures.clear();cancelAnimationFrame(raf);observer.disconnect();reduced.removeEventListener('change',resetClock);document.removeEventListener('visibilitychange',resetClock);for(const g of geometries)g.dispose();for(const m of materials)m.dispose();for(const t of textures)t.dispose();key.shadow.dispose();renderer.dispose();if(canvas.__pipelineDispose===dispose)delete canvas.__pipelineDispose;}
  canvas.__pipelineDispose=dispose;
  function frame(time){
    if(disposed)return;if(!canvas.isConnected){dispose();return;}raf=requestAnimationFrame(frame);
    const elapsed=last?Math.min((time-last)/1000,.05):0;last=time;
    if(running&&!paused&&!reduced.matches&&!document.hidden){phase+=elapsed;dirty=true;}
    if(!dirty||document.hidden)return;
    // 선의 느린 변화는 구조 설명이며 실제 처리량이나 현재 블러 수치와 연결하지 않습니다.
    const width=1+Math.sin(phase*.8)*.12;for(const line of blurred)line.scale.x=width;
    renderer.render(scene,camera);dirty=false;
  }
  setTheme(document.documentElement.dataset.theme||'light');resize();raf=requestAnimationFrame(frame);renderGallery();refreshPreviews();galleryInterval=window.setInterval(refreshPreviews,15000);
  return {setSelectedSigma(value,runId){if(!allowedSigmas.has(value))return;externalRun=runId;if(currentPreviewRun&&runId!==currentPreviewRun){closePreviewSettings(false);for(const entry of galleryFigures.values()){entry.image.onload=null;entry.image.onerror=null;}galleryFigures.clear();galleryGrid.replaceChildren();galleryThumbnails.replaceChildren();previewItems=new Map();completedSigmas=new Set();reportedSigmas=new Set();currentPreviewRun=runId;previewMessage('새 실험의 사진을 기다리고 있어요.');}externalSigma=value;selectedSigma=value;renderGallery();},setPaused(value){paused=Boolean(value);last=0;dirty=true;},setStatus(index,nextStatus,isRunning){const changed=active!==index||status!==nextStatus||running!==Boolean(isRunning);active=index;status=nextStatus;running=Boolean(isRunning);if(changed)updateState();},setTheme};
}
