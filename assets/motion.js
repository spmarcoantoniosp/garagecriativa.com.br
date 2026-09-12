/* =========================================================================
   GARAGE · motion.js
   O movimento revela estrutura. Uma direção, uma curva, uma vez só.
   Sem dependência externa. Degrada para site estático se o JS falhar.
   ========================================================================= */
(function () {
  'use strict';

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var supports = 'IntersectionObserver' in window;
  var root = document.documentElement;

  /* ---------------------------------------------------------------------
     1. MENU EM CELULAR — funciona mesmo com movimento reduzido
     --------------------------------------------------------------------- */
  var burger = document.querySelector('.nav__burger');
  var panel = document.getElementById('nav-panel');
  if (burger && panel) {
    var close = function () {
      burger.setAttribute('aria-expanded', 'false');
      panel.classList.remove('is-open');
      document.body.classList.remove('is-locked');
    };
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      if (open) { close(); return; }
      burger.setAttribute('aria-expanded', 'true');
      panel.classList.add('is-open');
      document.body.classList.add('is-locked');
    });
    panel.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) close();
    });
  }

  /* ---------------------------------------------------------------------
     2. CABEÇALHO QUE RESPONDE À ROLAGEM
     --------------------------------------------------------------------- */
  var nav = document.querySelector('.nav');
  if (nav) {
    var onScroll = function () {
      if (window.scrollY > 24) nav.classList.add('is-stuck');
      else nav.classList.remove('is-stuck');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------------------------------------------------------------------
     3. FORMULÁRIO — validação e envio provisório por e-mail
        Substituir o handler por um endpoint real quando existir.
     --------------------------------------------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll('form[data-mailto]'), function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var to = form.getAttribute('data-mailto');
      var subject = form.getAttribute('data-subject') || 'Contato pelo site';
      var lines = [];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || el.type === 'submit') return;
        var label = form.querySelector('label[for="' + el.id + '"]');
        lines.push((label ? label.textContent.trim() : el.name) + ': ' + el.value);
      });
      var note = form.querySelector('[data-form-note]');
      if (note) note.hidden = false;
      window.location.href = 'mailto:' + to
        + '?subject=' + encodeURIComponent(subject)
        + '&body=' + encodeURIComponent(lines.join('\n'));
    });
  });

  /* ---------------------------------------------------------------------
     4. SISTEMA DE ENTRADA — daqui para baixo, só se houver movimento
     --------------------------------------------------------------------- */
  if (reduce || !supports) return;
  root.classList.add('mo');

  /* Quem entra, em que ordem. Nenhuma marcação no HTML: tudo por seletor. */
  var groups = [
    ['.hero .lbl', '.hero h1', '.hero .lede', '.hero .btnrow', '.hero .proof'],
    ['.head > div', '.head > .lede'],
    ['.tempo'],
    ['.step'],
    ['.case'],
    ['.door'],
    ['.wcard'],
    ['.trilha'],
    ['.premium > div'],
    ['.contato > div'],
    ['.slab__l', '.slab__r'],
    ['.tblock__id', '.tblock h2', '.tblock__q'],
    ['.tok'],
    ['.spec']
  ];

  /* marca os elementos e guarda o atraso de escalonamento */
  groups.forEach(function (sel) {
    var list = document.querySelectorAll(sel.join(','));
    /* agrupa por container próximo para escalonar irmãos, não a página toda */
    var byParent = new Map();
    Array.prototype.forEach.call(list, function (el) {
      var p = el.parentElement;
      if (!byParent.has(p)) byParent.set(p, []);
      byParent.get(p).push(el);
    });
    byParent.forEach(function (items) {
      items.forEach(function (el, i) {
        el.setAttribute('data-mo', '');
        el.style.setProperty('--mo-d', Math.min(i, 8) * 65 + 'ms');
      });
    });
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-in');
      io.unobserve(entry.target);
      if (entry.target.hasAttribute('data-count')) count(entry.target);
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });

  Array.prototype.forEach.call(
    document.querySelectorAll('[data-mo], .visline, .slab, .steps, .tblock__h'),
    function (el) { io.observe(el); }
  );

  /* ---------------------------------------------------------------------
     5. CONTAGEM DOS NÚMEROS DE PROVA
     --------------------------------------------------------------------- */
  function count(el) {
    var raw = el.getAttribute('data-count');
    var target = parseFloat(raw.replace(/\./g, '').replace(',', '.'));
    if (isNaN(target)) return;
    var suffix = el.getAttribute('data-suffix') || '';
    var dur = 1100, t0 = null;
    function frame(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      var v = Math.round(target * eased);
      el.textContent = v.toLocaleString('pt-BR') + (p === 1 ? suffix : '');
      if (p < 1) requestAnimationFrame(frame);
    }
    el.textContent = '0';
    requestAnimationFrame(frame);
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-count]'), function (el) {
    io.observe(el);
  });
})();
