(function () {
  'use strict';

  // ── Active-section nav highlight ──────────────────────────────────────────
  const sections  = Array.from(document.querySelectorAll('section[id]'));
  const navLinks  = Array.from(document.querySelectorAll('#nav-links a[data-section]'));
  const OFFSET    = 80; // px below viewport top to count a section as active

  function updateActive() {
    let current = sections[0]?.id ?? '';
    for (const sec of sections) {
      if (sec.getBoundingClientRect().top <= OFFSET) current = sec.id;
    }
    for (const link of navLinks) {
      link.classList.toggle('active', link.dataset.section === current);
    }
  }

  window.addEventListener('scroll', updateActive, { passive: true });
  updateActive();

  // ── Light / dark theme ────────────────────────────────────────────────────
  // The initial theme is set by an inline script in <head> to avoid a flash.
  const root        = document.documentElement;
  const themeBtn    = document.getElementById('theme-toggle');
  const darkQuery   = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function syncGiscus(theme) {
    const frame = document.querySelector('iframe.giscus-frame');
    if (frame) {
      frame.contentWindow.postMessage(
        { giscus: { setConfig: { theme: theme === 'dark' ? 'dark' : 'light' } } },
        'https://giscus.app'
      );
    }
  }

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    if (themeBtn) {
      const label = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
      themeBtn.setAttribute('aria-label', label);
      themeBtn.title = label;
    }
    syncGiscus(theme);
  }

  applyTheme(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');

  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('theme', next); } catch (e) {}
      applyTheme(next);
    });
  }

  // Follow OS changes until the visitor makes an explicit choice.
  if (darkQuery && darkQuery.addEventListener) {
    darkQuery.addEventListener('change', function (e) {
      let stored = null;
      try { stored = localStorage.getItem('theme'); } catch (err) {}
      if (stored !== 'light' && stored !== 'dark') applyTheme(e.matches ? 'dark' : 'light');
    });
  }

  // ── Mobile menu toggle ────────────────────────────────────────────────────
  const toggle  = document.getElementById('menu-toggle');
  const navList = document.getElementById('nav-links');

  toggle.addEventListener('click', function () {
    const open = navList.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  // Close on nav-link click
  for (const link of navList.querySelectorAll('a')) {
    link.addEventListener('click', function () {
      navList.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  }

  // Close when clicking outside the nav
  document.addEventListener('click', function (e) {
    if (!e.target.closest('#navbar')) {
      navList.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}());
