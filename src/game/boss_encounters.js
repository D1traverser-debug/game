/* Boss pool and combat patterns. Krog'wa/Mul'gath mechanics are an independently
   authored approximation pending source-version frame-by-frame comparison. */
const BOSS_ARCHETYPES=[
 {id:'sol',name:"Sol'phish",label:"SOL'PHISH · 深渊之长",hp:22000,r:52,speed:70},
 {id:'krog',name:"Krog'wa",label:"KROG'WA · 膨胀之王",hp:23500,r:60,speed:77},
 {id:'mul',name:"Mul'gath",label:"MUL'GATH · 扭曲之主",hp:24000,r:56,speed:73}
];
function spawnBoss(){
 let p=game.player,loc=game.bossPending||{x:p.x+rand(-400,400),y:p.y-520};
 let archetype=pick(BOSS_ARCHETYPES),mult=selectedThreat==='hardcore'?2.1:selectedThreat==='severe'?1.45:1;
 let b={id:'boss',type:'boss',bossId:archetype.id,name:archetype.name,x:loc.x,y:loc.y,r:archetype.r,hp:archetype.hp*mult,max:archetype.hp*mult,speed:archetype.speed,attack:2.5,rune:4,stagger:0,vulnerable:0,dead:false,hitFlash:0,elite:true,burn:0,burnDmg:0,acid:0,slow:0,freeze:0,weakness:0,corrupt:0,corruptT:0,age:0,phase:'hunt',phaseT:0,healTimer:8,leapTimer:7};
 save.stats.bossesEncountered=(save.stats.bossesEncountered||0)+1;persist();game.boss=b;game.bossPending=null;game.enemies.push(b);
 toast(archetype.name+' 正在穿越裂隙！');sound(75,.7,'sawtooth',.04);
}
function spawnBossHealer(b){
 if(game.enemies.filter(e=>!e.dead&&e.bossHealer).length>=5)return;
 spawnEnemy(false,'buffer');let e=game.enemies[game.enemies.length-1];
 e.x=b.x+rand(-150,150);e.y=b.y+rand(-145,145);e.hp=e.max=400;e.speed=45;e.dmg=22;e.bossHealer=true;e.elite=false;e.type='buffer';e.state='chase';
 game.fx.push({x:e.x,y:e.y,r:55,life:.4,max:.4,color:'#c0e6a0',type:'ring'});
}
function updateBossEncounter(dt){
 const g=game,b=g?.boss,p=g?.player;if(!b||b.dead)return;
 const spec=BOSS_ARCHETYPES.find(x=>x.id===b.bossId)||BOSS_ARCHETYPES[0];
 b.age=(b.age||0)+dt;b.hitFlash=Math.max(0,(b.hitFlash||0)-dt);b.burn=Math.max(0,(b.burn||0)-dt);b.acid=Math.max(0,(b.acid||0)-dt);
 b.slow=Math.max(0,(b.slow||0)-dt*.025);b.freeze=Math.max(0,(b.freeze||0)-dt);b.vulnerable=Math.max(0,(b.vulnerable||0)-dt);
 if(b.burn>0){b.burnTick=(b.burnTick||0)-dt;if(b.burnTick<=0){b.burnTick=.5;damageEnemy(b,b.burnDmg||4,'burn',null,false)}}
 if(b.stagger>=100){b.stagger=0;b.vulnerable=2.6;b.phase='stagger';b.phaseT=2.6;toast(spec.name+' 失衡！伤害提高 200%');sound(460,.34,'square',.035)}
 let dx=p.x-b.x,dy=p.y-b.y,d=Math.hypot(dx,dy)||1,a=Math.atan2(dy,dx);
 const status=$('bossname');status.textContent=spec.label+(b.vulnerable>0?' · 失衡 +200%':'');status.style.textShadow=b.vulnerable>0?'0 0 14px #ffd887':'0 2px 9px #060e0d';
 if(b.vulnerable<=0){
  if(b.bossId==='sol'){
   b.speed=spec.speed+Math.min(150,b.age*1.7);
   b.x+=Math.cos(a)*b.speed*(1-b.slow)*dt;b.y+=Math.sin(a)*b.speed*(1-b.slow)*dt;
   b.attack-=dt;if(b.attack<=0){b.attack=Math.max(1.5,3.7-b.age*.01);
    // Rune stones are telegraphed and can hurt enemies and the boss.
    let x=p.x+rand(-48,48),y=p.y+rand(-48,48);
    g.hazards.push({x,y,r:85,timer:1.20,dmg:65,el:'dark',color:'#d08cae',kind:'runestone',life:1.85,boss:true});
   }
  }else if(b.bossId==='krog'){
   b.leapTimer-=dt;
   if(b.phase==='charge'){b.phaseT-=dt;if(b.phaseT<=0){b.x=b.leapX;b.y=b.leapY;b.phase='hunt';
    g.hazards.push({x:b.x,y:b.y,r:144,timer:.02,dmg:85,el:'acid',kind:'krogLeap',color:'#c9df77',life:.70,boss:true});
    for(let i=0;i<5;i++){let angle=i*TAU/5;g.hazards.push({x:b.x+Math.cos(angle)*180,y:b.y+Math.sin(angle)*180,r:48,timer:.6,dmg:40,kind:'krogAcid',color:'#9cdb77',life:2.3,boss:true})}
    toast('Krog’wa 落地：注意环形冲击！');
   }}else{
    b.x+=Math.cos(a)*spec.speed*(1-b.slow)*dt;b.y+=Math.sin(a)*spec.speed*(1-b.slow)*dt;
    if(b.leapTimer<=0){b.leapTimer=7;b.phase='charge';b.phaseT=1.25;b.leapX=p.x;b.leapY=p.y;
     g.hazards.push({x:p.x,y:p.y,r:132,timer:1.23,dmg:0,kind:'warning',color:'#d7eb8e',life:1.25,boss:true});toast('Krog’wa 准备跳跃！')}
   }
  }else if(b.bossId==='mul'){
   if(b.corruptT>0)b.corruptT-=dt;
   b.speed=spec.speed+Math.min(60,b.age*.45);
   b.x+=Math.cos(a)*b.speed*(1-b.slow)*dt;b.y+=Math.sin(a)*b.speed*(1-b.slow)*dt;
   b.healTimer-=dt;if(b.healTimer<=0){b.healTimer=9;for(let i=0;i<2;i++)spawnBossHealer(b);toast('Mul’gath 召唤了治疗眷属！')}
   b.attack-=dt;if(b.attack<=0){b.attack=3.7;for(let i=0;i<3;i++){let ang=a+(i-1)*.45;
    g.shots.push({x:b.x+Math.cos(ang)*b.r,y:b.y+Math.sin(ang)*b.r,vx:Math.cos(ang)*230,vy:Math.sin(ang)*230,life:3,dmg:36,r:11,kind:'enemy',color:'#d6a2f9'})}}
  }
 }
 if(b.bossId==='mul'){
  // Healing servants can be corrupted: official 1.1 confirms they instead damage Mul'gath.
  for(const e of g.enemies)if(!e.dead&&e.bossHealer){
   let dd=Math.hypot(e.x-b.x,e.y-b.y);
   if(e.corruptT>0&&dd<b.r+e.r+16){damageEnemy(b,b.max*.035,'corruptedHealer',null,false);e.dead=true;continue}
   if(e.corruptT<=0&&dd<250)b.hp=Math.min(b.max,b.hp+dt*b.max*.0007);
  }
 }
 if(d<b.r+p.r+8&&b.phase!=='charge'){
  b.touch=(b.touch||0)-dt;if(b.touch<=0){damagePlayer(b.bossId==='krog'?41:32,'boss');b.touch=.9}
 }
 if(b.hp<=0&&!b.dead)killEnemy(b);
}

