// Fade sections in as they scroll into view
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  },
  { threshold: 0.08 }
);

document.querySelectorAll('section').forEach((el) => observer.observe(el));

// ── Generic modal wiring ──
function wireModal(triggerSelector, modalId, closeSelector) {
  const modal = document.getElementById(modalId);
  if (!modal) return;
  const triggers = document.querySelectorAll(triggerSelector);
  const closeBtn = modal.querySelector(closeSelector);

  const open = (e) => {
    if (e) e.preventDefault();
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
  };
  const close = () => {
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
  };

  triggers.forEach((t) => t.addEventListener('click', open));
  if (closeBtn) closeBtn.addEventListener('click', close);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) close();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.style.display === 'flex') close();
  });
}

wireModal('.open-demo',            'demo-modal',       '.modal-close');
wireModal('.open-demo-diffusion',  'diffusion-modal',  '.modal-close');
wireModal('.open-demo-raytracing', 'raytracing-modal', '.modal-close');
wireModal('#open-dex',             'dex-modal',        '.pokedex-close');

// ── Hero Pokedex: flip lid open, then launch the BIO modal ──
const heroDex = document.getElementById('hero-dex');
const dexModal = document.getElementById('dex-modal');
if (heroDex && dexModal) {
  heroDex.addEventListener('click', () => {
    if (heroDex.classList.contains('open')) return;
    heroDex.classList.add('open');
    setTimeout(() => {
      dexModal.style.display = 'flex';
      dexModal.setAttribute('aria-hidden', 'false');
    }, 450);
  });
  // Reset the lid to closed whenever the BIO modal is dismissed.
  const resetLid = () => {
    if (dexModal.style.display !== 'flex') heroDex.classList.remove('open');
  };
  dexModal.addEventListener('click', resetLid);
  const dexClose = dexModal.querySelector('.pokedex-close');
  if (dexClose) dexClose.addEventListener('click', resetLid);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setTimeout(resetLid, 0);
  });
}

// ── Touch devices (iPhone/iPad): no hover, so make Lucario tappable ──
const isTouch = window.matchMedia('(hover: none)').matches;
const lucarioWrap = document.querySelector('.lucario-wrap');

if (isTouch && lucarioWrap) {
  const lucarioLabel = lucarioWrap.querySelector('.lucario-label');
  if (lucarioLabel) lucarioLabel.textContent = 'TAP ME!';
  const skillsHint = document.querySelector('.skills-hint');
  if (skillsHint) skillsHint.textContent = 'TAP ME!';

  lucarioWrap.addEventListener('click', (e) => {
    e.stopPropagation();
    lucarioWrap.classList.toggle('show-bubble');
  });
  // Tap anywhere else closes the bubble
  document.addEventListener('click', () => {
    lucarioWrap.classList.remove('show-bubble');
  });
}

// ── Click-to-open pokeballs (single-open) ──
const pokeballBtns = document.querySelectorAll('.pokeball-btn');

pokeballBtns.forEach((btn) => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.pokeball-item');
    const wasOpen = item.classList.contains('open');

    document.querySelectorAll('.pokeball-item.open').forEach((el) => {
      el.classList.remove('open');
      const b = el.querySelector('.pokeball-btn');
      if (b) b.setAttribute('aria-expanded', 'false');
      const d = el.querySelector('.skill-detail');
      if (d) d.setAttribute('hidden', '');
    });

    if (!wasOpen) {
      item.classList.add('open');
      btn.setAttribute('aria-expanded', 'true');
      const detail = item.querySelector('.skill-detail');
      if (detail) detail.removeAttribute('hidden');
    }
  });
});
