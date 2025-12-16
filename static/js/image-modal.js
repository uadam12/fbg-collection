document.addEventListener('click', function (e) {
    const img = e.target.closest('.cap-image');
    if (!img) return;

    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');

    modalImage.src = img.dataset.src;
    modalTitle.textContent = img.dataset.name;
});
