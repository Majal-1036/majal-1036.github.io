const page = document.body.dataset.page;
document.querySelectorAll("[data-page-link]").forEach((link) => {
  if (link.dataset.pageLink === page) {
    link.classList.add("active");
    link.setAttribute("aria-current", "page");
  }
});

const menuButton = document.querySelector(".menu-toggle");
const navPanel = document.querySelector(".nav-panel");

if (menuButton && navPanel) {
  menuButton.addEventListener("click", () => {
    const isOpen = navPanel.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", String(isOpen));
  });

  navPanel.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navPanel.classList.remove("open");
      menuButton.setAttribute("aria-expanded", "false");
    });
  });
}

document.querySelectorAll("[data-current-year]").forEach((element) => {
  element.textContent = new Date().getFullYear();
});
