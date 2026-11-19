/* Silva HAMA | Portfolio — main.js (no dependencies)
   1. Intro (loader / wipe)  2. Scroll reveal  3. Scroll-linked motion  4. Page transition
   5. Profile photo toggle   6. Lightbox */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement, win = window;
  var reduce = win.matchMedia && win.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var motion = !reduce && typeof requestAnimationFrame === 'function';
  var first = root.classList.contains('is-first');

  /* 1. Intro ------------------------------------------------------------------- */
  var readyQueue = [], isReady = false;
  function onReady(fn) { if (isReady) fn(); else readyQueue.push(fn); }
  function ready() {
    if (isReady) return;
    isReady = true;
    root.classList.add('is-ready');
    readyQueue.forEach(function (fn) { fn(); });
    setTimeout(function () { root.classList.add('is-settled'); }, 2800);
  }
  if (motion) root.classList.add('anim');
  if (first && motion) {
    var loader = doc.querySelector('.loader'), num = doc.querySelector('.loader__num');
    var t0 = performance.now(), MIN = 1500, MAX = 4200, loaded = doc.readyState === 'complete', done = false;
    win.addEventListener('load', function () { loaded = true; });
    var finish = function () {
      if (done) return;
      done = true;
      if (num) num.textContent = '100';
      if (loader) loader.style.setProperty('--load', 1);
      setTimeout(function () {
        root.classList.add('is-loaded');
        setTimeout(ready, 380);
        setTimeout(function () { if (loader && loader.parentNode) loader.parentNode.removeChild(loader); }, 1300);
      }, 180);
    };
    var tick = function (now) {
      var t = now - t0, p = Math.min(t / MIN, 1);
      p = 1 - Math.pow(1 - p, 3);
      if (!loaded) p = Math.min(p, 0.92);
      if (num) num.textContent = String(Math.round(p * 100));
      if (loader) loader.style.setProperty('--load', p.toFixed(3));
      if ((loaded && t >= MIN) || t >= MAX) finish(); else requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    setTimeout(finish, MAX + 300);            // also covers background tabs where rAF is paused
  } else {
    root.classList.add('is-loaded');
    setTimeout(ready, root.classList.contains('is-return') ? 420 : 0);
  }

  /* 2. Scroll reveal --------------------------------------------------------- */
  // Checked from the scroll frame (not IntersectionObserver) so that blocks which are jumped
  // over by an anchor link / fast fling are revealed too and can never stay hidden.
  var pending = motion ? [].slice.call(doc.querySelectorAll('.reveal')) : [];
  var revealOn = false;
  function reveal(vh) {
    if (!revealOn || !pending.length) return;
    pending = pending.filter(function (el) {
      if (el.getBoundingClientRect().top > vh * 0.92) return true;
      el.classList.add('is-in');
      return false;
    });
  }
  onReady(function () { revealOn = true; requestFrame(); });

  /* 3. Scroll-linked motion: header state, neon curve, parallax, drifting words --- */
  var header = doc.querySelector('.site-header');
  var overHero = !!doc.querySelector('.hero, .works-hero');
  var drift = [].slice.call(doc.querySelectorAll('[data-drift]'));
  var para = [].slice.call(doc.querySelectorAll('[data-parallax]'));
  var ticking = false;
  function frame() {
    ticking = false;
    var y = win.pageYOffset || 0, vh = win.innerHeight || 1;
    if (header) header.classList.toggle('is-top', overHero && y < 24);
    if (!motion) return;
    reveal(vh);
    var max = Math.max(1, doc.documentElement.scrollHeight - vh);
    root.style.setProperty('--scroll', (0.16 + 0.84 * Math.min(1, y / max)).toFixed(4));
    drift.forEach(function (el) {
      var r = el.parentNode.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      var k = parseFloat(el.getAttribute('data-drift')) || 0;
      var off = (r.top - vh) * k;
      // k < 0: the word slides to the right from its resting place / k > 0: it arrives from the right
      el.style.transform = 'translate3d(' + (k > 0 ? off + k * (vh + r.height) : off).toFixed(1) + 'px,0,0)';
    });
    para.forEach(function (el) {
      if (y > vh * 1.2) return;
      el.style.setProperty('--py', (y * (parseFloat(el.getAttribute('data-parallax')) || 0)).toFixed(1) + 'px');
    });
  }
  function requestFrame() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  win.addEventListener('scroll', requestFrame, { passive: true });
  win.addEventListener('resize', requestFrame);
  frame();

  /* 4. Page transition (internal links slide a black panel in before navigating) --- */
  if (motion) {
    doc.addEventListener('click', function (ev) {
      if (ev.defaultPrevented || ev.button || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
      var a = ev.target.closest ? ev.target.closest('a[href]') : null;
      if (!a || a.target || a.hasAttribute('download') || a.hasAttribute('data-zoom')) return;
      if (a.protocol !== location.protocol || a.host !== location.host) return;
      if (a.pathname === location.pathname && a.search === location.search) return;   // in-page anchor
      ev.preventDefault();
      root.classList.add('is-leaving');
      setTimeout(function () { location.href = a.href; }, 400);
    });
    win.addEventListener('pageshow', function (ev) { if (ev.persisted) root.classList.remove('is-leaving'); });
  }

  /* 5. Profile photo toggle (hover on desktop / tap on touch) ------------------- */
  [].forEach.call(doc.querySelectorAll('.flip'), function (btn) {
    btn.addEventListener('click', function () {
      btn.setAttribute('aria-pressed', btn.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
    });
  });

  /* 6. Lightbox for work images ------------------------------------------------ */
  var links = [].slice.call(doc.querySelectorAll('a[data-zoom]'));
  if (!links.length || typeof HTMLDialogElement !== 'function') return;
  var dlg = doc.createElement('dialog');
  dlg.className = 'lightbox';
  dlg.setAttribute('aria-label', '画像ビューア');
  dlg.innerHTML =
    '<button type="button" class="lightbox__btn lightbox__close" aria-label="閉じる">&times;</button>' +
    '<button type="button" class="lightbox__btn lightbox__prev" aria-label="前の画像">&#8249;</button>' +
    '<div class="lightbox__stage"><img class="lightbox__img" alt=""></div>' +
    '<button type="button" class="lightbox__btn lightbox__next" aria-label="次の画像">&#8250;</button>' +
    '<p class="lightbox__count" aria-live="polite"></p>';
  doc.body.appendChild(dlg);
  var img = dlg.querySelector('.lightbox__img'), count = dlg.querySelector('.lightbox__count');
  var prev = dlg.querySelector('.lightbox__prev'), next = dlg.querySelector('.lightbox__next');
  var index = 0, opener = null;
  function show(i) {
    index = (i + links.length) % links.length;
    var a = links[index], thumb = a.querySelector('img');
    img.src = a.getAttribute('href');
    img.alt = thumb ? thumb.alt : '';
    count.textContent = (index + 1) + ' / ' + links.length;
    prev.hidden = next.hidden = links.length < 2;
  }
  links.forEach(function (a, i) {
    a.addEventListener('click', function (ev) {
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button) return;
      ev.preventDefault(); opener = a; show(i); dlg.showModal();
    });
  });
  dlg.querySelector('.lightbox__close').addEventListener('click', function () { dlg.close(); });
  prev.addEventListener('click', function () { show(index - 1); });
  next.addEventListener('click', function () { show(index + 1); });
  dlg.addEventListener('click', function (ev) {
    if (ev.target === dlg || ev.target.classList.contains('lightbox__stage')) dlg.close();
  });
  dlg.addEventListener('keydown', function (ev) {
    if (ev.key === 'ArrowLeft') show(index - 1);
    else if (ev.key === 'ArrowRight') show(index + 1);
  });
  dlg.addEventListener('close', function () { img.removeAttribute('src'); if (opener) opener.focus(); });
})();
