/* =========================================================================
   Árbol Trade & Marketing — behaviour
   No dependencies. Everything here is progressive enhancement: with this file
   removed the site is a complete, readable, conventional page.
   ========================================================================= */
(function () {
  'use strict';

  var scroller = document.getElementById('scroller');
  var railFill = document.getElementById('railFill');
  var header = document.querySelector('.hdr');
  var hint = document.getElementById('hint');
  var toggle = document.getElementById('motionToggle');
  var seed = document.getElementById('s1');
  if (!scroller) return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------- user motion preference */
  var OFF_KEY = 'arbol:motion-off';
  function applyMotionPref(off) {
    document.documentElement.classList.toggle('no-motion', off);
    if (toggle) {
      toggle.setAttribute('aria-pressed', off ? 'true' : 'false');
      toggle.textContent = off ? 'Activar animación' : 'Reducir animación';
    }
  }
  var motionOff = false;
  try { motionOff = localStorage.getItem(OFF_KEY) === '1'; } catch (e) {}
  applyMotionPref(motionOff);

  if (toggle) {
    toggle.addEventListener('click', function () {
      motionOff = !motionOff;
      try { motionOff ? localStorage.setItem(OFF_KEY, '1') : localStorage.removeItem(OFF_KEY); } catch (e) {}
      applyMotionPref(motionOff);
      if (motionOff) revealEverything();
    });
  }

  /* ------------------------------------------------------- scroll geometry
     The scroller is flex column-reverse, so the visitor starts at the visual
     BOTTOM (the seed) and travels up. Browsers have not always agreed on how
     scrollTop is reported in a reversed container, so rather than assume, we
     measure the convention once at startup and normalise everything through
     progress(), where 0 = at the seed and 1 = at the canopy. */
  var topIsZero = true;

  function maxScroll() { return scroller.scrollHeight - scroller.clientHeight; }

  function goToSeed() {
    // Ask for the flow-start edge; the browser clamps to whichever end that is.
    scroller.scrollTop = maxScroll();
    if (scroller.scrollTop < maxScroll() / 2) {
      // Reversed convention: the start edge reports as 0.
      topIsZero = false;
      scroller.scrollTop = 0;
    }
  }

  function progress() {
    var m = maxScroll();
    if (m <= 0) return 0;
    var st = scroller.scrollTop;
    return topIsZero ? 1 - st / m : Math.abs(st) / m;
  }

  // Don't let the browser restore a stale position into a reversed container.
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

  /* Images and fonts change the scroll height, so the position is re-asserted
     after load — but never against the visitor. If they have already started
     climbing, yanking them back to the seed would be worse than a few pixels
     of drift. */
  var userScrolled = false;
  scroller.addEventListener('scroll', function () { userScrolled = true; }, { passive: true, once: true });

  function anchor(force) {
    if (!force && userScrolled) return;
    if (location.hash && document.querySelector(location.hash)) return;
    goToSeed();
    userScrolled = false;
  }
  anchor();
  window.addEventListener('load', function () { anchor(); });
  // bfcache restores put the reversed container back at a stale offset
  window.addEventListener('pageshow', function (e) { if (e.persisted) anchor(true); });

  /* --------------------------------------------------------------- reveals
     IntersectionObserver rather than scroll math: it does not care which
     direction the container runs, so the reversed layout cannot break it. */
  var revealables = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
  var artBlocks = Array.prototype.slice.call(document.querySelectorAll('.art'));
  var watched = revealables.concat(artBlocks);

  function revealEverything() {
    watched.forEach(function (el) { el.classList.add('in'); });
  }

  if (reduced || motionOff || !('IntersectionObserver' in window)) {
    revealEverything();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { root: scroller, rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    watched.forEach(function (el) { io.observe(el); });
  }

  /* Keyboard-focus guard: an element mid-reveal is still focusable. If focus
     lands anywhere not yet revealed, reveal it immediately so a keyboard user
     is never sitting on something they cannot see. */
  document.addEventListener('focusin', function (e) {
    var el = e.target;
    while (el && el !== document.body) {
      if (el.hasAttribute && el.hasAttribute('data-reveal')) el.classList.add('in');
      el = el.parentElement;
    }
  });

  /* ------------------------------------------------- rail + header state */
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var p = Math.max(0, Math.min(1, progress()));
      if (railFill) railFill.style.height = (p * 100).toFixed(1) + '%';
      if (header) header.classList.toggle('stuck', p > 0.02);
      if (hint) hint.style.opacity = p > 0.04 ? '0' : '1';
      ticking = false;
    });
  }
  scroller.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ------------------------------------------------------------ the hint
     Landing at the bottom and being asked to scroll UP is unfamiliar, so the
     cue is explicit and also clickable. */
  if (hint) {
    hint.style.transition = 'opacity .3s';
    hint.addEventListener('click', function () {
      var step = scroller.clientHeight * 0.85;
      scroller.scrollBy({ top: topIsZero ? -step : step, behavior: reduced || motionOff ? 'auto' : 'smooth' });
    });
  }

  /* --------------------------------------------------------------- misc */
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // Header logo returns to the seed rather than jumping via the hash.
  var logoLink = document.querySelector('.hdr__logo');
  if (logoLink && seed) {
    logoLink.addEventListener('click', function (e) {
      e.preventDefault();
      if (reduced || motionOff) { goToSeed(); return; }
      scroller.scrollTo({ top: topIsZero ? maxScroll() : 0, behavior: 'smooth' });
    });
  }
})();
