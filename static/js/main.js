document.addEventListener('DOMContentLoaded', () => {
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    const toastList = toastElList.map((toastEl) => new bootstrap.Toast(toastEl));
    toastList.forEach(toast => toast.show());
});
