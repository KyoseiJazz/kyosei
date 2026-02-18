// Random gallery viewer: opens a lightbox and navigates through a shuffled list
(function () {
    function shuffle(arr) {
        const a = arr.slice();
        for (let i = a.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [a[i], a[j]] = [a[j], a[i]];
        }
        return a;
    }

    let order = [];
    let idx = 0;

    function showAt(i, lbImage, lb) {
        if (!order.length) order = shuffle(window.ALL_GALLERY_IMAGES || []);
        if (!order.length) return;
        idx = ((i % order.length) + order.length) % order.length;
        lbImage.src = order[idx];
        lb.classList.remove('hidden');
    }

    function openRandom(lbImage, lb) {
        order = shuffle(window.ALL_GALLERY_IMAGES || []);
        idx = 0;
        showAt(0, lbImage, lb);
    }

    document.addEventListener('DOMContentLoaded', () => {
        const list = window.ALL_GALLERY_IMAGES || [];
        const btn = document.getElementById('rand-btn');
        const lb = document.getElementById('rand-lightbox');
        const lbImage = document.getElementById('rand-lb-image');
        const lbClose = document.getElementById('rand-lb-close');
        const lbPrev = document.getElementById('rand-lb-prev');
        const lbNext = document.getElementById('rand-lb-next');

        if (!btn || !lb || !lbImage || !lbPrev || !lbNext || !lbClose) return;
        if (!list.length) {
            console.warn('Random viewer: no images found (window.ALL_GALLERY_IMAGES is empty)');
        }

        btn.addEventListener('click', (e) => { e.preventDefault(); openRandom(lbImage, lb); });

        lbClose.addEventListener('click', () => lb.classList.add('hidden'));
        lbPrev.addEventListener('click', () => { showAt(idx - 1, lbImage, lb); });
        lbNext.addEventListener('click', () => { showAt(idx + 1, lbImage, lb); });

        lb.addEventListener('click', (e) => { if (e.target === lb) lb.classList.add('hidden'); });
        document.addEventListener('keydown', (e) => {
            if (lb.classList.contains('hidden')) return;
            if (e.key === 'ArrowLeft') lbPrev.click();
            else if (e.key === 'ArrowRight') lbNext.click();
            else if (e.key === 'Escape') lbClose.click();
        });
    });
})();
