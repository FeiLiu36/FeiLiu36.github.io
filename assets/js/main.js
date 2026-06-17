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
