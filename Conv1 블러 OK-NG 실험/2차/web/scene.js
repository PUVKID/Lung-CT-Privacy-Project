import * as THREE from './vendor/three.module.js';
export function createPipeline(canvas) {
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  const scene=new THREE.Scene(),root=new THREE.Group();scene.add(root);
  const camera=new THREE.OrthographicCamera(-9,9,4,-4,.1,100);
  camera.position.set(1.1,5.2,19);camera.lookAt(0,.8,0);
  const ambient=new THREE.HemisphereLight(0xffffff,0x9da9bb,2.6);scene.add(ambient);
  const light=new THREE.DirectionalLight(0xffffff,3.8);light.position.set(-5,9,9);light.castShadow=true;light.shadow.mapSize.set(2048,1024);scene.add(light);
  const surfaces=[],accents=[],outlines=[],labels=[];
  const surface=()=>{const m=new THREE.MeshStandardMaterial({color:0xe4e9f1,metalness:.3,roughness:.3});surfaces.push(m);return m;};
  const accent=()=>{const m=new THREE.MeshStandardMaterial({color:0x8aa7d5,metalness:.22,roughness:.34});accents.push(m);return m;};
  function box(w,h,d,mat,x,y,z,parent=root,edge=true){
    const geometry=new THREE.BoxGeometry(w,h,d),mesh=new THREE.Mesh(geometry,mat);mesh.position.set(x,y,z);mesh.castShadow=true;mesh.receiveShadow=true;parent.add(mesh);
    if(edge){const m=new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:.24});const border=new THREE.LineSegments(new THREE.EdgesGeometry(geometry),m);mesh.add(border);outlines.push(m);}
    return mesh;
  }
  function path(points,color=0x8a9bb4,width=1){const material=new THREE.LineBasicMaterial({color,linewidth:width});outlines.push(material);const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints(points.map(p=>new THREE.Vector3(...p))),material);root.add(line);return line;}
  // 의료 원본 없이 수식으로 만든 추상 면을 입력 영상의 구조 모형으로 사용합니다.
  const abstract=document.createElement('canvas');abstract.width=128;abstract.height=160;
  const ctx=abstract.getContext('2d'),pixels=ctx.createImageData(128,160);
  for(let y=0;y<160;y++)for(let x=0;x<128;x++){const v=Math.round(90+26*Math.sin(x*.23+y*.09)+24*Math.cos(x*.11-y*.16)+18*Math.sin(x*.36)*Math.cos(y*.29));const k=(y*128+x)*4;pixels.data[k]=v;pixels.data[k+1]=v+3;pixels.data[k+2]=v+8;pixels.data[k+3]=255;}
  ctx.putImageData(pixels,0,0);const texture=new THREE.CanvasTexture(abstract);texture.colorSpace=THREE.SRGBColorSpace;
  const inputMaterial=new THREE.MeshStandardMaterial({map:texture,roughness:.55,metalness:.08});
  for(let i=0;i<4;i++)box(1.65,2.55,.035,inputMaterial,-7.7+i*.16,1.05,-.48+i*.32);
  // 고정된 첫 합성곱의 7×7 커널을 독립 모듈로 보여줍니다.
  box(1.12,1.34,.75,surface(),-5.1,.55,0);
  for(let x=0;x<7;x++)for(let y=0;y<7;y++){
    const m=new THREE.MeshStandardMaterial({color:(x+y)%3===0?0x75849d:(x+y)%3===1?0xc0c9d6:0x99a7bc,roughness:.6});
    box(.115,.115,.025,m,-5.53+x*.143,.12+y*.143,.39,root,false);
  }
  // 64개 채널의 특징 맵을 대표 적층 면으로 요약합니다.
  const featurePanels=[];
  for(let i=0;i<12;i++)featurePanels.push(box(1.35,2.35,.027,accent(),-3.77+i*.085,.98,-.75+i*.14));
  // sigma에 따라 달라지는 블러 연산을 가우시안 곡면으로 표현합니다.

  const gaussGeometry=new THREE.PlaneGeometry(1.12,1.24,28,28),vertices=gaussGeometry.attributes.position;
  for(let i=0;i<vertices.count;i++){const x=vertices.getX(i),y=vertices.getY(i);vertices.setZ(i,.72*Math.exp(-(x*x+y*y)/.09));}
  gaussGeometry.computeVertexNormals();
  const gaussian=new THREE.Mesh(gaussGeometry,new THREE.MeshStandardMaterial({color:0x7f9bc5,roughness:.35,metalness:.2,side:THREE.DoubleSide}));gaussian.rotation.x=-Math.PI/2;gaussian.position.set(-1.7,.1,.08);gaussian.castShadow=true;root.add(gaussian);
  const gaussianWire=new THREE.Mesh(gaussGeometry,new THREE.MeshBasicMaterial({color:0xc1d2eb,wireframe:true,transparent:true,opacity:.4}));gaussian.add(gaussianWire);
  // 네 잔차 계층과 건너뛰기 연결은 구조 모형이며 실제 텐서 값이 아닙니다.
  const deep=[];
  for(let i=0;i<4;i++){
    const center=.08+i*1.52,group=new THREE.Group();group.position.x=center;root.add(group);deep.push(group);
    for(let j=0;j<4;j++)box(.2,2.16,1.08,j===3?accent():surface(),-.35+j*.23,.94,0,group);
    const points=[[center-.4,-.18,.7],[center-.4,-.37,.7],[center+.58,-.37,.7],[center+.58,.85,.7],[center+.78,.85,.7]];
    path(points,0x95aac9);
    const plusMat=surface();const disk=new THREE.Mesh(new THREE.CylinderGeometry(.14,.14,.04,24),plusMat);disk.rotation.x=Math.PI/2;disk.position.set(center-.37,-.18,.75);root.add(disk);
    path([[center-.43,-.18,.79],[center-.31,-.18,.79]],0x657a9c);path([[center-.37,-.24,.79],[center-.37,-.12,.79]],0x657a9c);
  }
  box(.25,1.24,.73,surface(),6.4,.48,0);box(.25,1.1,.6,surface(),6.9,.48,.12);
  for(let i=0;i<2;i++){const sphere=new THREE.Mesh(new THREE.SphereGeometry(.11,20,16),accent());sphere.position.set(6.91,.25+i*.43,.45);root.add(sphere);}
  function label(text,x,y,size=100){const c=document.createElement('canvas');c.width=384;c.height=80;const context=c.getContext('2d');context.clearRect(0,0,384,80);context.font='700 34px Nanum, sans-serif';context.textAlign='center';context.fillStyle='#73849f';context.fillText(text,192,52);const map=new THREE.CanvasTexture(c);const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map,transparent:true,depthTest:false}));sprite.position.set(x,y,0);sprite.scale.set(size/100*1.72,size/100*.36,1);root.add(sprite);labels.push(sprite);}
  label('7 × 7',-5.1,1.72,85);label('64',-3.28,2.54,90);label('Gaussian σ',-1.7,1.7,75);
  for(let i=0;i<4;i++)label(`Res Block ${i+1}`,.08+i*1.52,2.27,80);
  const links=[[-6.8,-5.75],[-4.48,-4.02],[-2.7,-2.24],[-1.18,-.62],[5.55,6.18]],particles=[];
  for(const [from,to] of links){path([[from,.55,0],[to,.55,0]],0x8497b5);const cone=new THREE.Mesh(new THREE.ConeGeometry(.075,.19,4),accent());cone.rotation.z=-Math.PI/2;cone.position.set(to,.55,0);root.add(cone);for(let j=0;j<2;j++)particles.push({mesh:box(.055,.055,.055,accent(),from,.55,0,root,false),from,to,offset:j/2});}
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(80,80),new THREE.ShadowMaterial({opacity:.13}));floor.rotation.x=-Math.PI/2;floor.position.y=-.52;floor.receiveShadow=true;scene.add(floor);
  let paused=false,running=false,phase=0,last=0,dark=false;
  function resize(){
    const r=canvas.getBoundingClientRect();renderer.setSize(r.width,r.height,false);camera.updateMatrixWorld();const bounds=new THREE.Box3().setFromObject(root),corners=[];
    for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z])corners.push(new THREE.Vector3(x,y,z).applyMatrix4(camera.matrixWorldInverse));
    const minX=Math.min(...corners.map(p=>p.x)),maxX=Math.max(...corners.map(p=>p.x)),minY=Math.min(...corners.map(p=>p.y)),maxY=Math.max(...corners.map(p=>p.y));
    const aspect=r.width/Math.max(1,r.height),height=Math.max((maxY-minY)/.86,(maxX-minX)/(aspect*.94));const x=(minX+maxX)/2,y=(minY+maxY)/2;
    camera.left=x-height*aspect/2;camera.right=x+height*aspect/2;camera.top=y+height/2;camera.bottom=y-height/2;camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(canvas);resize();
  function animate(time){requestAnimationFrame(animate);const delta=Math.min(.05,(time-last)/1000||0);last=time;if(!paused&&running&&!document.hidden)phase+=delta;
    particles.forEach(({mesh,from,to,offset})=>{mesh.visible=running;mesh.position.x=from+((phase*.5+offset)%1)*(to-from);});
    featurePanels.forEach((panel,i)=>panel.material.emissive.setRGB(0,0,(!paused&&running?Math.sin(phase*1.7+i*.23)*.025+.025:0)));
    gaussian.rotation.y=!paused&&running?Math.sin(phase)*.06:0;renderer.render(scene,camera);
  }
  requestAnimationFrame(animate);
  return {setPaused(value){paused=value;},setStatus(_index,_status,isRunning){running=isRunning;},setTheme(theme){dark=theme==='dark';surfaces.forEach(m=>m.color.setHex(dark?0x546176:0xe4e9f1));accents.forEach(m=>m.color.setHex(dark?0x91afd9:0x8aa7d5));inputMaterial.color.setHex(dark?0xc2cee0:0xffffff);ambient.intensity=dark?2:2.6;light.intensity=dark?2.8:3.8;floor.material.opacity=dark?.2:.13;labels.forEach(s=>s.material.color.setHex(dark?0xc2d2ee:0xffffff));}};
}
