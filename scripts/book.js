
(() => {
  // Book page flip logic for new diary layout
  const pages = Array.from(document.querySelectorAll('.book-page'));
  let current = 0;

  function showPair(index) {
    // Clamp to valid range (always even index for left page)
    if (index < 0) index = 0;
    if (index > pages.length - 2) index = pages.length - 2;
    pages.forEach((p, i) => {
      p.classList.remove('current');
      if (i === index || i === index + 1) p.classList.add('current');
    });
    current = index;
    // Update hash for deep-linking
    const id = pages[current].id;
    if (id) history.replaceState(null, '', `#${id}`);
  }

  function nextPage() {
    if (current < pages.length - 2) showPair(current + 2);
  }
  function prevPage() {
    if (current > 0) showPair(current - 2);
  }

  document.getElementById('next').addEventListener('click', nextPage);
  document.getElementById('prev').addEventListener('click', prevPage);

  // TOC links (if present)
  document.querySelectorAll('.book-page a[href^="#page-"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const id = a.getAttribute('href').replace('#', '');
      const idx = pages.findIndex(p => p.id === id);
      if (idx >= 0) showPair(idx % 2 === 0 ? idx : idx - 1);
    });
  });

  // On load, respect hash to open specific page
  function openFromHash() {
    const raw = location.hash.replace('#', '');
    if (!raw) return showPair(0);
    const idx = pages.findIndex(p => p.id === raw);
    if (idx >= 0) showPair(idx % 2 === 0 ? idx : idx - 1);
    else showPair(0);
  }

  window.addEventListener('hashchange', openFromHash);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', openFromHash);
  else openFromHash();
})();
