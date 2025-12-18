const closeFilterMenuBtn = document.getElementById('close-filter-menu-btn');
const filterMenu = document.getElementById('filterSidebar');

const offcanvasInstance =
  bootstrap.Offcanvas.getOrCreateInstance(filterMenu);

closeFilterMenuBtn.addEventListener('click', () => {
  offcanvasInstance.hide();
});
