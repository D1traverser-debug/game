/* Shared, data-driven boss attack lifecycle. Numerical values are adaptation tuning. */
const BOSS_ARCHETYPES=[
 {id:'sol',name:"Sol'phish",label:"SOL'PHISH · 深渊之长",hp:22000,r:52,speed:70,phaseCount:1},
 {id:'krog',name:"Krog'wa",label:"KROG'WA · 膨胀之王",hp:23500,r:60,speed:77,phaseCount:3},
 {id:'mul',name:"Mul'gath",label:"MUL'GATH · 扭曲之主",hp:24000,r:56,speed:73,phaseCount:3}
];
const BOSS_ATTACK_DEFS={
 sol:[
  {id:'obelisk',label:'符文石落击',shape:'circle',effect:'impact',telegraph:1.05,active:.12,recovery:.62,cooldown:3.6,radius:88,damage:64,color:'#d08cae'},
  {id:'radialBurst',label:'环形弹幕',shape:'radial',effect:'radial',telegraph:.82,active:.12,recovery:.78,cooldown:4.8,radius:168,count:8,phaseCount:2,speed:220,damage:29,color:'#d99ad4'},
  {id:'homingVolley',label:'追踪法球',shape:'target',effect:'homing',telegraph:.92,active:.12,recovery:.68,cooldown:5.2,radius:58,count:2,phaseCount:1,speed:165,turnRate:2.2,damage:34,color:'#ff83b2'}
 ],
 krog:[
  {id:'inhale',label:'深渊吸气',shape:'pull',effect:'pull',telegraph:1.02,active:1.15,recovery:.82,cooldown:5.4,radius:350,pullSpeed:158,damage:48,color:'#a7d875'},
  {id:'tongueSmash',label:'舌击冲锋',shape:'line',effect:'impact',telegraph:1.08,active:.14,recovery:.78,cooldown:4.8,length:465,width:92,damage:68,color:'#d3e58a'},
  {id:'trackingSpit',label:'追踪酸液',shape:'target',effect:'homing',telegraph:.86,active:.12,recovery:.68,cooldown:4.3,radius:55,count:1,phaseCount:1,speed:178,turnRate:1.65,damage:39,color:'#b6e67a'}
 ],
 mul:[
  {id:'headWhip',label:'多首横扫',shape:'line',effect:'impact',telegraph:.96,active:.14,recovery:.72,cooldown:4.3,length:355,width:96,damage:58,color:'#d7a1ef'},
  {id:'spikeGrid',label:'地脉尖刺',shape:'grid',effect:'impact',telegraph:1.22,active:.12,recovery:.86,cooldown:5.7,count:4,radius:52,damage:54,color:'#d6a0ee'},
  {id:'headVolley',label:'多首齐射',shape:'radial',effect:'radial',telegraph:.82,active:.12,recovery:.7,cooldown:4.6,radius:160,count:3,phaseCount:2,speed:195,damage:31,color:'#e1b2f6'}
 ]
};
function bossPhaseForHealth(b){
 if(b.bossId==='sol'||b.phaseCount===1)return 0;
 const ratio=clamp(b.hp/Math.max(1,b.max),0,1);
 return ratio>2/3?0:ratio>1/3?1:2;
}
function bossSyncPhase(b){
 const next=bossPhaseForHealth(b),old=b.phaseIndex||0;b.phaseCount=b.bossId==='sol'?1:3;
 if(next<=old)return false;
 b.phaseIndex=next;b.phaseTransitionTimer=1.15;bossCancelAttack(b);b.attackCooldown=1.25;
 if(b.bossId==='krog'&&next>=1&&!b.fieldActive){
  b.fieldActive=true;b.fieldCenter={x:game.player.x,y:game.player.y};b.fieldRadius=600;
  b.fieldHazard={x:b.fieldCenter.x,y:b.fieldCenter.y,r:b.fieldRadius,timer:99999,life:99999,dmg:0,kind:'warning',color:'#80e2e6',boss:true};
  game.hazards.push(b.fieldHazard);toast("Krog'wa 磁场展开：不要越过边界！");
 }
 if(b.bossId==='mul'){b.headCount=next+1;toast("Mul'gath 的头颅增殖："+b.headCount+" 首！")}
 game.fx.push({x:b.x,y:b.y,r:Math.max(90,b.r*2.8),life:.8,max:.8,color:'#e8d18b',type:'burst'});
 return true;
}
function bossPointSegmentDistance(px,py,x1,y1,x2,y2){
 const dx=x2-x1,dy=y2-y1,len=dx*dx+dy*dy,t=len?clamp(((px-x1)*dx+(py-y1)*dy)/len,0,1):0;
 return Math.hypot(px-(x1+t*dx),py-(y1+t*dy));
}
function bossAttackContainsPlayer(geometry,p){
 if(!geometry||!p)return false;
 if(geometry.kind==='circle')return Math.hypot(p.x-geometry.x,p.y-geometry.y)<=geometry.r+p.r;
 if(geometry.kind==='line')return bossPointSegmentDistance(p.x,p.y,geometry.x,geometry.y,geometry.tx,geometry.ty)<=geometry.width*.5+p.r;
 if(geometry.kind==='grid')return geometry.points.some(q=>Math.hypot(p.x-q.x,p.y-q.y)<=q.r+p.r);
 return false;
}
function bossAttackGeometry(b,def,p){
 const dx=p.x-b.x,dy=p.y-b.y,dist=Math.hypot(dx,dy)||1,angle=Math.atan2(dy,dx),phase=b.phaseIndex||0;
 if(def.shape==='circle')return{kind:'circle',x:p.x,y:p.y,r:def.radius+phase*8};
 if(def.shape==='pull')return{kind:'pull',x:b.x,y:b.y,r:def.radius+phase*18};
 if(def.shape==='line'){
  const length=Math.min(def.length+phase*28,Math.max(140,dist+70));
  return{kind:'line',x:b.x,y:b.y,tx:b.x+Math.cos(angle)*length,ty:b.y+Math.sin(angle)*length,width:def.width+phase*10};
 }
 if(def.shape==='grid'){
  const offsets=[[0,0],[-112,0],[112,0],[0,-112],[0,112],[-112,-112],[112,-112],[-112,112],[112,112]],count=Math.min(offsets.length,def.count+phase*2);
  return{kind:'grid',points:offsets.slice(0,count).map(([x,y])=>({x:p.x+x,y:p.y+y,r:def.radius+phase*5}))};
 }
 if(def.shape==='radial')return{kind:'radial',x:b.x,y:b.y,r:def.radius+phase*14};
 return{kind:'target',x:p.x,y:p.y,r:def.radius||58,originX:b.x,originY:b.y};
}
function bossEmitTelegraph(instance){
 const geo=instance.geometry,def=instance.def,first=geo.points?.[0]||{};
 game.hazards.push({x:geo.x??first.x??0,y:geo.y??first.y??0,r:geo.r??first.r??(geo.width||116)*.5,
  timer:def.telegraph,life:def.telegraph+.08,dmg:0,kind:'warning',color:def.color,boss:true,
  bossAttackToken:instance.token,bossAttackId:instance.id,bossShape:geo.kind,bossGeometry:geo,
  bossAttackCount:def.count+(def.phaseCount||0)*instance.phaseIndex});
}
function bossBeginAttack(b,def){
 const token=(b.attackToken||0)+1;b.attackToken=token;
 const a={id:def.id,token,def,geometry:bossAttackGeometry(b,def,game.player),stage:'telegraph',timer:def.telegraph,phaseIndex:b.phaseIndex||0,resolved:false,hitOnce:false};
 b.attackInstance=a;bossEmitTelegraph(a);return a;
}
function bossCancelAttack(b,cooldown=0){
 const a=b?.attackInstance;if(!a)return false;
 game.hazards=game.hazards.filter(h=>h.bossAttackToken!==a.token);
 b.attackInstance=null;
 if(cooldown>0)b.attackCooldown=Math.max(b.attackCooldown||0,cooldown);
 return true;
}
function bossFireProjectiles(b,a){
 const def=a.def,geo=a.geometry,phase=a.phaseIndex??b.phaseIndex??0,count=def.count+(def.phaseCount||0)*phase;
 const originX=geo.kind==='radial'?geo.x:(geo.originX??b.x),originY=geo.kind==='radial'?geo.y:(geo.originY??b.y);
 const targetX=geo.x??game.player.x,targetY=geo.y??game.player.y,base=Math.atan2(targetY-originY,targetX-originX);
 for(let i=0;i<count;i++){
  const angle=geo.kind==='radial'?i*TAU/count:base+(i-(count-1)/2)*.17,speed=def.speed||190;
  game.shots.push({x:originX+Math.cos(angle)*(b.r+8),y:originY+Math.sin(angle)*(b.r+8),vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,life:4.8,dmg:def.damage,r:9,kind:def.effect==='homing'?'enemyHoming':'enemy',speed,turnRate:def.turnRate||1.6,color:def.color,owner:'boss'});
 }
}
function bossApplyPull(b,a,dt){
 const geo=a.geometry,p=game.player,dx=geo.x-p.x,dy=geo.y-p.y,dist=Math.hypot(dx,dy)||1,def=a.def;
 if(dist<geo.r){const strength=.35+.65*(1-dist/geo.r),step=def.pullSpeed*strength*dt;worldMoveEntity(p,dx/dist*step,dy/dist*step,p.r);if(dist<118&&!a.hitOnce){a.hitOnce=true;damagePlayer(def.damage,'bossInhale')}}
}
function bossResolveAttack(b,a,dt){
 const def=a.def,p=game.player;
 if(def.effect==='pull'){bossApplyPull(b,a,dt);return}
 if(a.resolved)return;
 if(def.effect==='radial'||def.effect==='homing'){bossFireProjectiles(b,a);a.resolved=true;return}
 if(bossAttackContainsPlayer(a.geometry,p))damagePlayer(def.damage,'bossAttack');
 a.resolved=true;
}
function bossUpdateAttack(b,dt){
 if(b.phaseTransitionTimer>0||b.vulnerable>0||b.freeze>0){if(b.attackInstance?.stage==='telegraph')bossCancelAttack(b,.65);return}
 if(!b.attackInstance){
  b.attackCooldown=Math.max(0,(b.attackCooldown||0)-dt);
  if(b.attackCooldown<=0){const defs=BOSS_ATTACK_DEFS[b.bossId]||BOSS_ATTACK_DEFS.sol,def=defs[(b.attackSequence||0)%defs.length];b.attackSequence=(b.attackSequence||0)+1;bossBeginAttack(b,def)}
  return
 }
 const a=b.attackInstance;
 if(a.stage==='telegraph'){a.timer-=dt;if(a.timer<=0){a.stage='active';a.timer=a.def.active;bossResolveAttack(b,a,dt)}}
 else if(a.stage==='active'){if(a.def.effect==='pull')bossResolveAttack(b,a,dt);a.timer-=dt;if(a.timer<=0){a.stage='recovery';a.timer=a.def.recovery;game.fx.push({x:b.x,y:b.y,r:b.r*2.1,life:.3,max:.3,color:a.def.color,type:'burst'})}}
 else if(a.stage==='recovery'){a.timer-=dt;if(a.timer<=0){b.attackCooldown=a.def.cooldown;b.attackInstance=null}}
}
function bossUpdateHomingProjectile(s,dt,p){
 const dx=p.x-s.x,dy=p.y-s.y,dist=Math.hypot(dx,dy)||1,speed=s.speed||180,blend=Math.min(1,dt*(s.turnRate||1.6));
 s.vx+=(dx/dist*speed-s.vx)*blend;s.vy+=(dy/dist*speed-s.vy)*blend;s.x+=s.vx*dt;s.y+=s.vy*dt;
 if(Math.hypot(p.x-s.x,p.y-s.y)<p.r+s.r){damagePlayer(s.dmg,'bossProjectile');s.life=0}
}
function bossApplyMagneticField(b,dt){
 if(!b.fieldActive||!b.fieldCenter)return;
 const p=game.player,dx=p.x-b.fieldCenter.x,dy=p.y-b.fieldCenter.y,dist=Math.hypot(dx,dy)||1,limit=b.fieldRadius-24;
 if(dist>limit){const pull=Math.min(dist-limit,235*dt);worldMoveEntity(p,-dx/dist*pull,-dy/dist*pull,p.r)}
}
function spawnBoss(){
 const p=game.player,archetype=pick(BOSS_ARCHETYPES),rawLoc=game.bossPending||{x:p.x+rand(-400,400),y:p.y-520},loc=worldFindOpenPoint(rawLoc.x,rawLoc.y,Math.min(38,archetype.r*.45),360),mult=selectedThreat==='hardcore'?2.1:selectedThreat==='severe'?1.45:1;
 const b={id:'boss',type:'boss',bossId:archetype.id,name:archetype.name,x:loc.x,y:loc.y,r:archetype.r,hp:archetype.hp*mult,max:archetype.hp*mult,speed:archetype.speed,attack:2.5,rune:4,stagger:0,vulnerable:0,dead:false,hitFlash:0,elite:true,burn:0,burnDmg:0,acid:0,slow:0,freeze:0,weakness:0,corrupt:0,corruptT:0,age:0,phase:'hunt',phaseT:0,healTimer:8,phaseIndex:0,phaseCount:archetype.phaseCount,headCount:1,phaseTransitionTimer:0,attackCooldown:1.65,attackSequence:0,attackInstance:null,fieldActive:false,fieldCenter:null,fieldRadius:0,fieldHazard:null};
 save.stats.bossesEncountered=(save.stats.bossesEncountered||0)+1;persist();game.boss=b;game.bossPending=null;game.enemies.push(b);toast(archetype.name+' 正在穿越裂隙！');sound(75,.7,'sawtooth',.04);
}
function spawnBossHealer(b){
 if(game.enemies.filter(e=>!e.dead&&e.bossHealer).length>=5)return;
 spawnEnemy(false,'buffer');const e=game.enemies[game.enemies.length-1];
 const open=worldFindOpenPoint(b.x+rand(-210,210),b.y+rand(-190,190),e.r,260);e.x=open.x;e.y=open.y;e.hp=e.max=400;e.speed=52;e.dmg=22;e.bossHealer=true;e.bossOwnerId=b.id;e.heal=999999;e.elite=false;e.type='buffer';e.state='chase';
 game.fx.push({x:e.x,y:e.y,r:55,life:.4,max:.4,color:'#c0e6a0',type:'ring'});
 return e;
}
function bossUpdateMulMinions(b,dt){
 if(b.bossId!=='mul')return;
 b.healTimer-=dt;
 if(b.healTimer<=0){b.healTimer=Math.max(7.2,10.5-(b.phaseIndex||0)*.7);for(let i=0;i<1+(b.phaseIndex||0);i++)spawnBossHealer(b);toast("Mul'gath 召唤了治疗眷属！")}
 for(const e of game.enemies){
  if(e.dead||!e.bossHealer||e.bossOwnerId!==b.id)continue;
  const dx=b.x-e.x,dy=b.y-e.y,dist=Math.hypot(dx,dy)||1;
  if(e.corruptT>0||e.state==='corrupt'){
   if(dist>b.r+e.r+16){worldMoveEntity(e,dx/dist*e.speed*1.35*dt,dy/dist*e.speed*1.35*dt,e.r)}
   else{damageEnemy(b,b.max*(.035+(b.phaseIndex||0)*.008),'corruptedHealer',null,false);e.dead=true;game.fx.push({x:e.x,y:e.y,r:65,life:.45,max:.45,color:'#c98cf0',type:'burst'})}
  }else{if(dist>82){worldMoveEntity(e,dx/dist*e.speed*dt,dy/dist*e.speed*dt,e.r)}if(dist<250)b.hp=Math.min(b.max,b.hp+dt*b.max*.00072)}
 }
}
function updateBossEncounter(dt){
 const g=game,b=g?.boss,p=g?.player;if(!b)return;if(b.dead){if(b.fieldHazard)b.fieldHazard.life=0;return}
 const spec=BOSS_ARCHETYPES.find(x=>x.id===b.bossId)||BOSS_ARCHETYPES[0];
 b.age=(b.age||0)+dt;b.hitFlash=Math.max(0,(b.hitFlash||0)-dt);b.burn=Math.max(0,(b.burn||0)-dt);b.acid=Math.max(0,(b.acid||0)-dt);
 b.slow=Math.max(0,(b.slow||0)-dt*.025);b.freeze=Math.max(0,(b.freeze||0)-dt);b.vulnerable=Math.max(0,(b.vulnerable||0)-dt);
 if(b.burn>0){b.burnTick=(b.burnTick||0)-dt;if(b.burnTick<=0){b.burnTick=.5;damageEnemy(b,b.burnDmg||4,'burn',null,false)}}
 if(b.dead)return;
 bossSyncPhase(b);
 if(b.stagger>=100&&b.vulnerable<=0){b.stagger=0;b.vulnerable=2.6;bossCancelAttack(b);b.attackCooldown=1.2;toast(spec.name+' 失衡！伤害提高 200%');sound(460,.34,'square',.035)}
 b.phaseTransitionTimer=Math.max(0,(b.phaseTransitionTimer||0)-dt);
 const dx=p.x-b.x,dy=p.y-b.y,d=Math.hypot(dx,dy)||1,a=Math.atan2(dy,dx);
 const committedAttack=!!b.attackInstance&&(b.attackInstance.stage==='telegraph'||b.attackInstance.stage==='active');if(b.vulnerable<=0&&b.freeze<=0&&!committedAttack&&b.phaseTransitionTimer<=0){const speed=(spec.speed+Math.min(b.bossId==='sol'?150:60,b.age*(b.bossId==='sol'?1.7:.45)))*(1+(b.phaseIndex||0)*.12);worldMoveEntity(b,Math.cos(a)*speed*(1-b.slow)*dt,Math.sin(a)*speed*(1-b.slow)*dt,Math.min(38,b.r*.45))}
 bossApplyMagneticField(b,dt);bossUpdateMulMinions(b,dt);if(b.dead)return;bossUpdateAttack(b,dt);
 const phaseText=b.phaseCount>1?' · 阶段 '+((b.phaseIndex||0)+1)+'/'+b.phaseCount:'';
 const headText=b.bossId==='mul'?' · '+(b.headCount||1)+'首':'';
 const attackText=b.attackInstance?.stage==='telegraph'?' · 蓄势：'+b.attackInstance.def.label:'';
 const status=$('bossname');status.textContent=spec.label+phaseText+headText+(b.vulnerable>0?' · 失衡 +200%':'')+attackText;
 status.style.textShadow=b.vulnerable>0?'0 0 14px #ffd887':'0 2px 9px #060e0d';
 if(d<b.r+p.r+8&&b.vulnerable<=0){b.touch=(b.touch||0)-dt;if(b.touch<=0){damagePlayer(b.bossId==='krog'?41:32,'boss');b.touch=.9}}
 if(b.hp<=0&&!b.dead)killEnemy(b);
}
