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

  /* --- Subcategory Pill Filter --- */
  function initSubPills() {
    var pills = document.querySelectorAll('.sub-pill[data-filter]');
    var rows = document.querySelectorAll('.row[data-reveal]');
    if (!pills.length || !rows.length) return;

    pills.forEach(function(pill) {
      pill.addEventListener('click', function(e) {
        e.preventDefault();
        var filter = pill.getAttribute('data-filter');

        // Update active state
        pills.forEach(function(p) { p.classList.remove('sub-pill--active'); });
        pill.classList.add('sub-pill--active');

        // Filter rows
        rows.forEach(function(row) {
          var subTag = row.querySelector('.row-sub');
          var rowSub = subTag ? subTag.textContent.trim() : '';
          if (filter === 'all') {
            row.style.display = '';
          } else if (filter === '') {
            row.style.display = rowSub ? 'none' : '';
          } else {
            row.style.display = (rowSub === filter) ? '' : 'none';
          }
        });
      });
    });
  }

  /* --- Unified Header / Footer Injection --- */
  function initUnifiedChrome() {
    // Only apply to report pages (identified by .report-wrap)
    if (!document.querySelector('.report-wrap')) return;
    var HOME = 'https://www.rego.vip/claw/';
    var BRAND = '传琪';
    var HOME_SVG = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>';
    var CHEVRON_SVG = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>';
    var isInIframe = window.self !== window.top;

    // --- Detect if loaded inside iframe viewer ---
    function navigateHome(e) {
      if (isInIframe) {
        // Notify parent to close viewer instead of navigating inside iframe
        try { window.parent.postMessage({ type: 'claw-navigate-home' }, '*'); } catch(ex) {}
        e.preventDefault();
      }
      // If not in iframe, let the default link behavior work
    }

    // --- Fix breadcrumb: normalize all report-header breadcrumbs ---
    var bc = document.querySelector('.report-header__breadcrumb');
    if (bc) {
      var existingLink = bc.querySelector('a[href]');
      if (existingLink) {
        existingLink.href = HOME;
        existingLink.innerHTML = HOME_SVG;
        existingLink.setAttribute('aria-label', '返回首页');
        existingLink.addEventListener('click', navigateHome);
      }
      // Ensure chevron separator exists before the last child
      if (!bc.querySelector('svg[width="14"]')) {
        var sepSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        sepSvg.setAttribute('viewBox', '0 0 24 24');
        sepSvg.setAttribute('width', '14');
        sepSvg.setAttribute('height', '14');
        sepSvg.setAttribute('fill', 'none');
        sepSvg.setAttribute('stroke', 'currentColor');
        sepSvg.setAttribute('stroke-width', '2');
        sepSvg.setAttribute('stroke-linecap', 'round');
        sepSvg.setAttribute('stroke-linejoin', 'round');
        var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', 'm9 18 6-6-6-6');
        sepSvg.appendChild(path);
        bc.insertBefore(sepSvg, bc.lastElementChild);
      }
    }

    // --- Fix footer: remove all existing footers, inject unified one ---
    document.querySelectorAll('.page-footer').forEach(function(f) { f.remove(); });
    document.querySelectorAll('div[style*="text-align:center"][style*="padding:24px"]').forEach(function(f) { f.remove(); });

    var footer = document.createElement('footer');
    footer.className = 'page-footer';
    footer.innerHTML =
      '<div class="page-footer__logo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>' +
      '<span class="page-footer__sep"></span>' +
      '<a href="' + HOME + '" class="page-footer__link">' + BRAND + '</a>' +
      '<span class="page-footer__sep"></span>' +
      '<span>\u00A9 ' + new Date().getFullYear() + '</span>';
    footer.querySelector('.page-footer__link').addEventListener('click', navigateHome);
    document.body.appendChild(footer);

    // --- Fix: ensure content is visible immediately (no hidden state) ---
    document.querySelectorAll('[data-reveal]').forEach(function(el) {
      el.classList.add('revealed');
    });
  }

  /* --- Init --- */
  document.addEventListener('DOMContentLoaded', function() {
    initScrollReveal();
    initTOC();
    initScrollProgress();
    initSubPills();
    initUnifiedChrome();
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
