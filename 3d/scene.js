/* =========================================================================
   Árbol — versión 3D
   A procedural tree built entirely from tangled tubes, so it reads as the
   agency's scribble logo extruded into three dimensions rather than as a
   generic 3D plant. The camera climbs it as the visitor scrolls up.

   Everything is deterministic (seeded PRNG) so the tree is identical on
   every load and on every device.
   ========================================================================= */
import * as THREE from './vendor/three.module.min.js';

const root = document.documentElement;
const canvas = document.getElementById('scene');
const scroller = document.getElementById('scroller');

/* ------------------------------------------------------------ capability */
function webglOK() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext &&
      (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (e) { return false; }
}
if (!webglOK()) {
  root.classList.add('no-webgl');   // CSS falls back to the flat SVG tree
  throw new Error('WebGL unavailable — using 2D fallback');
}

const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ------------------------------------------------------------------ rng */
let _s = 20260721;
const rnd = () => ((_s = (_s * 1664525 + 1013904223) >>> 0) / 4294967296);
const rr = (a, b) => a + (b - a) * rnd();

/* --------------------------------------------------------------- palette */
const LEAF = 0x7cc01f, MID = 0x689f1e, CANOPY = 0x375b29, BRAND = 0x00690c;
const mat = (hex, rough = 0.55) => new THREE.MeshStandardMaterial({
  color: hex, roughness: rough, metalness: 0.0,
});
const M = { leaf: mat(LEAF), mid: mat(MID), canopy: mat(CANOPY, 0.65), brand: mat(BRAND, 0.6) };
const TONES = [M.leaf, M.mid, M.canopy];

/* ----------------------------------------------------------------- scene */
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);
scene.fog = new THREE.Fog(0xffffff, 26, 62);

const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 200);

const renderer = new THREE.WebGLRenderer({
  canvas, antialias: true, alpha: false, powerPreference: 'high-performance',
});
renderer.setClearColor(0xffffff, 1);

scene.add(new THREE.HemisphereLight(0xffffff, 0xd8e6d0, 1.15));
const key = new THREE.DirectionalLight(0xffffff, 1.5);
key.position.set(6, 14, 8);
scene.add(key);
const rim = new THREE.DirectionalLight(0xbfe08a, 0.5);
rim.position.set(-8, 4, -6);
scene.add(rim);

const tree = new THREE.Group();
scene.add(tree);

/* ------------------------------------------------------------- geometry */
function tube(points, radius, material, closed = false, tubular = null, radial = 6) {
  const curve = new THREE.CatmullRomCurve3(points, closed, 'catmullrom', 0.5);
  const seg = tubular || Math.max(24, Math.round(points.length * 7));
  const g = new THREE.TubeGeometry(curve, seg, radius, radial, closed);
  return new THREE.Mesh(g, material);
}

/* A wobbly closed loop on a sphere — the 3D echo of the logo's scribble. */
function scribbleLoop(cx, cy, cz, radius, material, thickness) {
  const pts = [];
  const n = 26;
  const tilt = rr(0, Math.PI), yaw = rr(0, Math.PI * 2);
  const k1 = 2 + Math.floor(rnd() * 3), k2 = 3 + Math.floor(rnd() * 4);
  const w1 = rr(0.14, 0.3), w2 = rr(0.06, 0.18);
  const squash = rr(0.55, 0.95);
  for (let i = 0; i < n; i++) {
    const t = (i / n) * Math.PI * 2;
    const m = 1 + w1 * Math.sin(k1 * t + yaw) + w2 * Math.sin(k2 * t + tilt);
    let x = Math.cos(t) * radius * m;
    let y = Math.sin(t) * radius * m * squash;
    let z = Math.sin(t * 2 + yaw) * radius * 0.42 * m;
    // rotate the loop into a random plane so the crown tangles in 3D
    const cy1 = Math.cos(tilt), sy1 = Math.sin(tilt);
    let y2 = y * cy1 - z * sy1, z2 = y * sy1 + z * cy1;
    const cy2 = Math.cos(yaw), sy2 = Math.sin(yaw);
    let x2 = x * cy2 - z2 * sy2, z3 = x * sy2 + z2 * cy2;
    pts.push(new THREE.Vector3(cx + x2, cy + y2, cz + z3));
  }
  return tube(pts, thickness, material, true, 150, 5);
}

/* ---------------------------------------------------------------- branches */
function buildBranch(origin, dir, len, thick, depth) {
  const pts = [origin.clone()];
  let p = origin.clone(), d = dir.clone().normalize();
  const steps = 5;
  for (let i = 1; i <= steps; i++) {
    d.x += rr(-0.22, 0.22); d.y += rr(-0.1, 0.06); d.z += rr(-0.22, 0.22);
    d.normalize();
    p = p.clone().addScaledVector(d, len / steps);
    pts.push(p.clone());
  }
  tree.add(tube(pts, thick, TONES[depth % 3], false, 40, 5));
  if (depth < 2) {
    const kids = depth === 0 ? 2 : 1;
    for (let k = 0; k < kids; k++) {
      buildBranch(p, new THREE.Vector3(d.x + rr(-0.6, 0.6), d.y + rr(0.1, 0.5), d.z + rr(-0.6, 0.6)),
        len * 0.62, thick * 0.62, depth + 1);
    }
  }
}

/* ------------------------------------------------------------------ trunk */
const TRUNK_TOP = 8.4;
function buildTrunk() {
  // Four strands twisting around each other. Two read as a stick from a
  // distance; four give the trunk real body while staying line-drawn.
  const STRANDS = 4;
  for (let s = 0; s < STRANDS; s++) {
    const pts = [];
    const phase = (s / STRANDS) * Math.PI * 2;
    for (let i = 0; i <= 14; i++) {
      const t = i / 14;
      const y = -0.35 + t * TRUNK_TOP;
      const flare = Math.pow(1 - t, 2.4) * 0.7;
      const twist = t * 2.2 + phase;
      const r = 0.2 + flare;
      pts.push(new THREE.Vector3(
        Math.cos(twist) * r + Math.sin(t * 2.2) * 0.24,
        y,
        Math.sin(twist) * r + Math.cos(t * 1.7) * 0.2
      ));
    }
    tree.add(tube(pts, 0.075, [M.canopy, M.brand, M.mid, M.canopy][s], false, 130, 7));
  }

  // Branches all the way up the trunk, not just at the top — this is what
  // stops the middle of the climb from feeling empty.
  for (let i = 0; i < 9; i++) {
    const t = 0.3 + (i / 9) * 0.62;
    const a = i * 2.4;
    const y = -0.35 + t * TRUNK_TOP;
    buildBranch(
      new THREE.Vector3(Math.cos(a) * 0.3, y, Math.sin(a) * 0.3),
      new THREE.Vector3(Math.cos(a), rr(0.35, 0.8), Math.sin(a)),
      rr(1.3, 2.4), rr(0.04, 0.06), 1
    );
  }
}

/* ------------------------------------------------------------------ roots */
function buildRoots() {
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * Math.PI * 2 + rr(-0.3, 0.3);
    const reach = rr(1.6, 4.2), drop = rr(1.4, 3.8);
    const pts = [new THREE.Vector3(0, -0.1, 0)];
    const steps = 5;
    for (let s = 1; s <= steps; s++) {
      const t = s / steps;
      pts.push(new THREE.Vector3(
        Math.cos(a) * Math.pow(t, 1.3) * reach + Math.sin(t * 4 + i) * 0.22,
        -Math.pow(t, 0.8) * drop,
        Math.sin(a) * Math.pow(t, 1.3) * reach + Math.cos(t * 3 + i) * 0.22
      ));
    }
    tree.add(tube(pts, 0.075 * (1 - i / 16), TONES[i % 3], false, 50, 5));
  }
}

/* ------------------------------------------------------------------ crown */
const CROWN_Y = 11.2;
function buildCrown() {
  for (let i = 0; i < 34; i++) {
    const a = rnd() * Math.PI * 2, b = Math.acos(rr(-1, 1));
    const spread = Math.pow(rnd(), 0.45);
    const cx = Math.sin(b) * Math.cos(a) * 1.5 * spread;
    const cz = Math.sin(b) * Math.sin(a) * 1.5 * spread;
    const cy = CROWN_Y + Math.cos(b) * 1.1 * spread;
    tree.add(scribbleLoop(cx, cy, cz, rr(1.1, 2.6), TONES[i % 3], rr(0.032, 0.062)));
  }
  // a few branches reaching from the trunk into the crown
  for (let i = 0; i < 5; i++) {
    const a = (i / 5) * Math.PI * 2;
    buildBranch(
      new THREE.Vector3(0, TRUNK_TOP - rr(0, 1.2), 0),
      new THREE.Vector3(Math.cos(a) * 0.8, 1, Math.sin(a) * 0.8),
      2.0, 0.055, 0
    );
  }
}

/* ------------------------------------------------------------------ ground */
function buildGround() {
  for (let i = 0; i < 4; i++) {
    const pts = [];
    const z = -3 + i * 2.1 + rr(-0.4, 0.4);
    for (let x = -22; x <= 22; x += 2) {
      pts.push(new THREE.Vector3(x, Math.sin(x * 0.32 + i) * 0.14 + rr(-0.05, 0.05), z));
    }
    tree.add(tube(pts, 0.035, TONES[i % 3], false, 90, 5));
  }
}

buildRoots();
buildTrunk();
buildCrown();
buildGround();

/* ------------------------------------------------------------------ camera
   Drives off the same reversed scroller as the flat version: progress 0 is
   the seed (underground), 1 is above the crown. */
let topIsZero = true;
function maxScroll() { return scroller.scrollHeight - scroller.clientHeight; }
function measureConvention() {
  const before = scroller.scrollTop;
  scroller.scrollTop = maxScroll();
  if (scroller.scrollTop < maxScroll() / 2) topIsZero = false;
  scroller.scrollTop = before;
}
function progress() {
  const m = maxScroll();
  if (m <= 0) return 0;
  const st = scroller.scrollTop;
  return Math.max(0, Math.min(1, topIsZero ? 1 - st / m : Math.abs(st) / m));
}

const lerp = (a, b, t) => a + (b - a) * t;
const easeIO = (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;

/* The tree is ~15 units tall, so the camera has to stand well back or the
   tubes fill the frame and read as pipes instead of a tree. These distances
   were set by rendering at p = 0, .25, .5, .75, 1 and looking at each. */
const SHOT = [
  //  p     camY    dist   lookY
  [0.00, -2.20, 15.5, 1.60],   // among the roots, trunk already rising
  [0.28, 1.40, 16.5, 4.60],   // ground level, full tree in frame
  [0.55, 5.20, 15.0, 7.60],   // climbing the trunk
  [0.80, 9.60, 12.5, 10.60],  // entering the crown
  [1.00, 14.20, 10.5, 11.60],  // above the canopy
];
function sample(p) {
  for (let i = 0; i < SHOT.length - 1; i++) {
    const a = SHOT[i], b = SHOT[i + 1];
    if (p <= b[0]) {
      const t = (p - a[0]) / (b[0] - a[0]);
      const e = easeIO(Math.max(0, Math.min(1, t)));
      return [lerp(a[1], b[1], e), lerp(a[2], b[2], e), lerp(a[3], b[3], e)];
    }
  }
  const l = SHOT[SHOT.length - 1];
  return [l[1], l[2], l[3]];
}

let shown = 0;                 // smoothed progress
/* On desktop the copy sits in a column on the left, so the camera aims to the
   left of the trunk and pushes the tree into the free right-hand space.
   On narrow screens the copy spans the width, so the tree stays centred. */
function aimOffset() { return window.innerWidth >= 900 ? -2.6 : 0; }

function placeCamera(p) {
  const [camY, dist, lookY] = sample(p);
  const ang = lerp(-0.5, 0.85, easeIO(p)) + (reduced ? 0 : Math.sin(p * 2.4) * 0.1);
  const ox = aimOffset();
  camera.position.set(Math.sin(ang) * dist + ox, camY, Math.cos(ang) * dist);
  camera.lookAt(ox, lookY, 0);
}

/* ------------------------------------------------------------------- loop */
function resize() {
  const w = window.innerWidth, h = window.innerHeight;
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', resize);
resize();
measureConvention();

let raf = null;
function frame() {
  const target = progress();
  shown += (target - shown) * (reduced ? 1 : 0.09);   // smooth the climb
  placeCamera(shown);
  if (!reduced) tree.rotation.y += 0.00035;            // slow ambient turn
  renderer.render(scene, camera);
  raf = requestAnimationFrame(frame);
}
frame();

// Stop drawing when the tab is hidden — no point burning a phone battery
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { cancelAnimationFrame(raf); raf = null; }
  else if (!raf) frame();
});

root.classList.add('scene-ready');
