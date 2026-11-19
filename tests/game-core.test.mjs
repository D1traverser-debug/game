import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';

const html = await readFile(new URL('../index.html', import.meta.url), 'utf8');
const match = html.match(/<script>([\s\S]*?)<\/script>/);
assert.ok(match, 'single inline game script must exist');

const productionScript = match[1];

const testApi = [
  'window.__TEST_API = {',
  '  saveJson: () => JSON.stringify(save),',
  '  spellPool: () => spells.filter(s => save.unlocks.includes(s.id)).map(s => s.id),',
  '  playerJson: () => {',
  '    const p = makePlayer();',
  '    return JSON.stringify({',
  '      luck: p.luck,',
  '      findBonus: p.findBonus,',
  '      spellSize: p.spellSize,',
  '      spells: p.spells.map(s => ({id:s.id, cd:s.cd, sizeMultiplier:s.sizeMultiplier || 1}))',
  '    });',
  '  },',
  '  start: () => { startRun(); },',
  '  fireJson: (id) => {',
  '    const def = spells.find(s => s.id === id);',
  '    if (!def) throw new Error("unknown spell " + id);',
  '    const sp = {...def, level:1, cdNow:0, infusions:[], augments:[]};',
  '    game.player.spells = [sp];',
  '    fireSpell(sp);',
  '    return JSON.stringify({',
  '      shots: game.shots.map(s => ({kind:s.kind, face:s.face, remainingHits:s.remainingHits})),',
  '      hazards: game.hazards.map(h => ({kind:h.kind, radius:h.r, damage:h.dmg}))',
  '    });',
  '  }',
  '};'
].join('\n');
const marker = "\npersist();$('goldTop').textContent=save.gold;\n})();";
assert.ok(productionScript.includes(marker), 'test injection anchor must exist');
const instrumentedScript = productionScript.replace(marker, "\npersist();$('goldTop').textContent=save.gold;\n" + testApi + "\n})();");

function makeElement() {
  return {
    style: {},
    dataset: {},
    textContent: '',
    innerHTML: '',
    className: '',
    classList: {
      add() {},
      remove() {},
      toggle() {},
      contains() { return false; }
    },
    addEventListener() {},
    setPointerCapture() {},
    appendChild() {},
    querySelector() { return makeElement(); },
    getBoundingClientRect() { return {left:0, top:0, width:100, height:100}; }
  };
}

function boot(seed) {
  const elements = new Map();
  const ctx2d = new Proxy({
    setTransform() {},
    clearRect() {},
    save() {},
    restore() {},
    translate() {},
    scale() {},
    rotate() {},
    beginPath() {},
    closePath() {},
    moveTo() {},
    lineTo() {},
    stroke() {},
    fill() {},
    arc() {},
    ellipse() {},
    fillRect() {},
    strokeRect() {},
    roundRect() {},
    quadraticCurveTo() {},
    bezierCurveTo() {},
    createRadialGradient() { return {addColorStop(){}}; },
    createLinearGradient() { return {addColorStop(){}}; },
    createPattern() { return {}; },
    fillText() {},
    strokeText() {},
    drawImage() {},
    setLineDash() {}
  }, {
    get(target, key) {
      if (key in target) return target[key];
      return () => {};
    },
    set(target, key, value) { target[key] = value; return true; }
  });

  const document = {
    getElementById(id) {
      if (!elements.has(id)) elements.set(id, makeElement());
      const el = elements.get(id);
      if (id === 'world') el.getContext = () => ctx2d;
      return el;
    },
    querySelectorAll() { return []; },
    createElement() {
      const el = makeElement();
      el.getContext = () => ctx2d;
      return el;
    },
    documentElement: makeElement(),
    fullscreenElement: null
  };

  const store = new Map();
  if (seed !== undefined) store.set('spellbrigade_solo_v1', JSON.stringify(seed));
  const localStorage = {
    getItem(key) { return store.has(key) ? store.get(key) : null; },
    setItem(key, value) { store.set(key, String(value)); },
    removeItem(key) { store.delete(key); }
  };

  const window = {AudioContext: undefined, webkitAudioContext: undefined};
  const sandbox = {
    document,
    window,
    localStorage,
    location: {search:''},
    URLSearchParams,
    Math,
    performance: {now: () => 1000},
    navigator: {getGamepads: () => []},
    innerWidth: 1280,
    innerHeight: 720,
    devicePixelRatio: 1,
    requestAnimationFrame() {},
    addEventListener() {},
    setTimeout() { return 1; },
    clearTimeout() {},
    console
  };
  vm.runInContext(instrumentedScript, vm.createContext(sandbox), {timeout:2000});
  return {api: window.__TEST_API, store};
}

const START = ['astral', 'loadedDice', 'tinyTremors', 'wickedBuzzsaw'];

test('release HTML contains no callable QA/debug API', () => {
  assert.doesNotMatch(match[1], /window\.__QA|runSteps|damageBoss|immortal=false/);
  assert.doesNotMatch(match[1], /new URLSearchParams\(location\.search\)\.has\('qa'\)/);
});

test('fresh profile exposes only the source-confirmed start spell pool', () => {
  const {api} = boot();
  const unlocked = JSON.parse(api.saveJson()).unlocks;
  assert.deepEqual(unlocked, START);
  assert.deepEqual(JSON.parse(JSON.stringify(api.spellPool())).sort(), [...START].sort());
});

test('v1 migration preserves meta progress but discards unreliable all-unlocked spell state', () => {
  const oldIds = ['astral','missile','solar','moon','sword','beam','stars','blades','runes','rocky','wings','bell','hex','necro','spear','sprout','talon','imp','sickle','orbital','seismic','mesh'];
  const {api, store} = boot({
    gold: 321,
    runs: 7,
    wins: 2,
    best: 900,
    enchant: {damage: 2},
    unlocks: oldIds,
    stats: {kills: 40},
  });
  const save = JSON.parse(api.saveJson());
  assert.equal(save.gold, 321);
  assert.equal(save.runs, 7);
  assert.equal(save.wins, 2);
  assert.equal(save.stats.kills, 40);
  assert.deepEqual(save.unlocks, START);
  assert.equal(save.schemaVersion, 2);
  const persisted = JSON.parse(store.get('spellbrigade_solo_v1'));
  assert.equal(persisted.schemaVersion, 2);
});

test('v2 save preserves known unlocks and rejects unknown spell identifiers', () => {
  const {api} = boot({
    schemaVersion: 2,
    gold: 9,
    enchant: {},
    unlocks: ['astral','missile','not-a-spell','missile'],
    stats: {}
  });
  const unlocked = JSON.parse(api.saveJson()).unlocks;
  assert.deepEqual(unlocked, ['astral','loadedDice','tinyTremors','wickedBuzzsaw','missile']);
});

test('Reginald bonuses are scoped to his signature spell and drop discovery', () => {
  const {api} = boot();
  const player = JSON.parse(api.playerJson());
  assert.equal(player.luck, 2);
  assert.equal(player.findBonus, 0.1);
  assert.equal(player.spellSize, 1);
  const astral = player.spells.find(s => s.id === 'astral');
  assert.equal(astral.sizeMultiplier, 1.25);
  assert.ok(Math.abs(astral.cd - 0.99 * 0.88) < 1e-9);
  assert.ok(player.spells.every(s => s.id === 'astral' || s.sizeMultiplier === 1));
});

test('Loaded Dice has its own rolling projectile and face-dependent explosion data', () => {
  const {api} = boot();
  api.start();
  const out = JSON.parse(api.fireJson('loadedDice'));
  assert.equal(out.shots.length, 1);
  assert.equal(out.shots[0].kind, 'dice');
  assert.ok(out.shots[0].face >= 1 && out.shots[0].face <= 6);
});

test('Tiny Tremors creates multiple independent quake impacts', () => {
  const {api} = boot();
  api.start();
  const out = JSON.parse(api.fireJson('tinyTremors'));
  assert.ok(out.hazards.length >= 3);
  assert.ok(out.hazards.every(h => h.kind === 'quake'));
});

test('Wicked Buzzsaw creates a distinct homing spinning blade', () => {
  const {api} = boot();
  api.start();
  const out = JSON.parse(api.fireJson('wickedBuzzsaw'));
  assert.equal(out.shots.length, 1);
  assert.equal(out.shots[0].kind, 'buzzsaw');
  assert.ok(out.shots[0].remainingHits >= 1);
});
