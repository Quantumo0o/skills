/* ============================================
   传霜 · 交互系统 v6
   ============================================ */

(function() {
  'use strict';

  /* --- Scroll Reveal --- */
  function initScrollReveal() {
    var els = document.querySelectorAll('[data-reveal]');
    if (!els.length) return;
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var delay = entry.target.getAttribute('data-reveal-delay') || 0;
          setTimeout(function() { entry.target.classList.add('revealed'); }, parseInt(delay));
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -20px 0px' });
    els.forEach(function(el) { observer.observe(el); });
  }

  /* --- Fixed Left TOC --- */
  function initTOC() {
    var sidebar = document.querySelector('.toc-sidebar');
    var toggle = document.querySelector('.toc-toggle');
    var closeBtn = document.querySelector('.toc-sidebar__close');
    if (!sidebar || !toggle) return;

    var isOpen = window.innerWidth >= 1024;

    function applyState() {
      if (isOpen) {
        sidebar.classList.add('toc-sidebar--open');
        toggle.classList.add('toc-toggle--hidden');
        document.body.classList.add('toc-open');
      } else {
        sidebar.classList.remove('toc-sidebar--open');
        toggle.classList.remove('toc-toggle--hidden');
        document.body.classList.remove('toc-open');
      }
    }

    toggle.addEventListener('click', function() {
      isOpen = true;
      applyState();
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', function() {
        isOpen = false;
        applyState();
      });
    }

    // Generate TOC from headings
    var content = document.querySelector('.page-body');
    if (!content) return;
    var headings = content.querySelectorAll('h2[id], h3[id]');
    if (!headings.length) { sidebar.style.display = 'none'; toggle.style.display = 'none'; return; }

    var list = sidebar.querySelector('.toc-list');
    if (!list) return;
    list.innerHTML = '';

    headings.forEach(function(h) {
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      a.className = 'toc-list__item toc-list__item--' + h.tagName.toLowerCase();
      a.addEventListener('click', function(e) {
        e.preventDefault();
        var target = document.getElementById(h.id);
        if (target) {
          var offset = 90;
          var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
          window.scrollTo({ top: top, behavior: 'smooth' });
        }
      });
      list.appendChild(a);
    });

    // Active tracking
    var sections = [];
    headings.forEach(function(h) { sections.push({ id: h.id, el: h, top: 0 }); });

    function updateActive() {
      var scrollY = window.pageYOffset;
      var current = '';
      sections.forEach(function(s) {
        s.top = s.el.getBoundingClientRect().top + window.pageYOffset - 120;
        if (scrollY >= s.top) current = s.id;
      });
      var items = list.querySelectorAll('.toc-list__item');
      items.forEach(function(item) {
        item.classList.toggle('toc-list__item--active', item.getAttribute('href') === '#' + current);
      });
    }

    var ticking = false;
    window.addEventListener('scroll', function() {
      if (!ticking) { requestAnimationFrame(function() { updateActive(); ticking = false; }); ticking = true; }
    });
    updateActive();
    applyState();
  }

  /* --- Scroll Progress --- */
  function initScrollProgress() {
    var bar = document.querySelector('.scroll-progress');
    if (!bar) return;
    window.addEventListener('scroll', function() {
      var scrollTop = window.pageYOffset;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (docHeight > 0 ? (scrollTop / docHeight) * 100 : 0) + '%';
    });
  }

  /* --- Back to Top --- */
  function initBackToTop() {
    var btn = document.querySelector('.back-to-top');
    if (!btn) return;
    window.addEventListener('scroll', function() {
      btn.classList.toggle('back-to-top--visible', window.pageYOffset > 400);
    });
    btn.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* --- Init --- */
  document.addEventListener('DOMContentLoaded', function() {
    initScrollReveal();
    initTOC();
    initScrollProgress();
    initBackToTop();
  });
})();

// ── Chart.js 自动初始化 ──
document.addEventListener('DOMContentLoaded', function() {
  if (typeof Chart === 'undefined') return;
  document.querySelectorAll('.chart-container[data-chart]').forEach(function(el) {
    var canvas = el.querySelector('canvas');
    if (!canvas) return;
    try {
      var config = {
        type: el.dataset.chart,
        data: {
          labels: JSON.parse(el.dataset.labels || '[]'),
          datasets: JSON.parse(el.dataset.datasets || '[]')
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } }
      };
      var h = el.dataset.height || '300px';
      canvas.style.height = h;
      canvas.parentElement.style.height = h;
      new Chart(canvas, config);
    } catch(e) { console.warn('Chart.js init error:', e); }
  });
});
