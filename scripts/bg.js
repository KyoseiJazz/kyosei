// Sets a per-page background image when the page <body> has a `data-bg` attribute.
(function(){
  const body = document.body;
  if (!body) return;
  const file = body.dataset && body.dataset.bg;
  if (!file) return;

  function applyBackground(filename) {
    const path = `../Images/textures/${filename}`;
    body.style.backgroundImage = `url("${path}")`;
    body.style.backgroundSize = 'cover';
    body.style.backgroundRepeat = 'no-repeat';
    body.style.backgroundPosition = 'center center';
    const page = document.getElementById('page');
    if (page) page.style.background = 'rgba(255,255,255,0.92)';
  }

  function chooseRandom(list) {
    return list[Math.floor(Math.random() * list.length)];
  }

  async function fetchDirectoryList(url) {
    try {
      const res = await fetch(url, {cache: 'no-store'});
      if (!res.ok) throw new Error('Fetch failed');
      const text = await res.text();
      // Parse anchor hrefs from directory listing HTML
      const parser = new DOMParser();
      const doc = parser.parseFromString(text, 'text/html');
      const anchors = Array.from(doc.querySelectorAll('a'));
      const imgs = anchors.map(a => a.getAttribute('href')).filter(h => !!h).filter(h => /\.(jpe?g|png|gif)$/i.test(h));
      return imgs.map(h => decodeURIComponent(h)).filter(Boolean);
    } catch (e) {
      return [];
    }
  }

  (async function(){
    if (file === 'random') {
      // Prefer an explicitly-provided list (bg-list.js) for file:// and other hosts
      let list = window.BG_TEXTURES && window.BG_TEXTURES.length ? window.BG_TEXTURES.slice() : [];

      // If no explicit list, try to discover textures dynamically from server directory listing
      if (!list.length) {
        const dir = await fetchDirectoryList('../Images/textures/');
        if (dir && dir.length) {
          list = dir.map(p => {
            const parts = p.split('/');
            return parts[parts.length-1];
          });
        }
      }

      if (!list || !list.length) return;
      const chosen = chooseRandom(list);
      applyBackground(chosen);
    } else {
      applyBackground(file);
    }
  })();

})();
