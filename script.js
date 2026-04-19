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

wireModal('.open-demo',  'demo-modal', '.modal-close');
wireModal('#open-dex',   'dex-modal',  '.pokedex-close');

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
