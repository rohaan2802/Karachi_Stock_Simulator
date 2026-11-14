const root = document.documentElement;
const theme = document.querySelector("#theme");
function updateTheme(value) {
  root.dataset.theme = value;
  const label = value === "dark" ? "Switch to light theme" : "Switch to dark theme";
  theme.setAttribute("aria-label", label);
  theme.title = label;
}
updateTheme(root.dataset.theme === "dark" ? "dark" : "light");
theme.addEventListener("click", () => {
  const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
  updateTheme(nextTheme);
  try { localStorage.setItem("karachi-theme", nextTheme); } catch {}
});

const backTop = document.querySelector("#back-top");
function syncScroll() {
  backTop.hidden = window.scrollY < 450;
}
window.addEventListener("scroll", syncScroll, {passive: true});
syncScroll();
backTop.addEventListener("click", () => {
  window.scrollTo({top: 0, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth"});
  document.querySelector(".brand").focus({preventScroll: true});
});

const cards = Array.from(document.querySelectorAll(".capture"));
const search = document.querySelector("#search");
const status = document.querySelector("#gallery-status");
const filters = Array.from(document.querySelectorAll("[data-filter]"));
let category = "All";
let visible = cards;
function filter() {
  const term = search.value.trim().toLowerCase();
  visible = cards.filter(card => {
    const match = (category === "All" || card.dataset.category === category)
      && card.textContent.toLowerCase().includes(term);
    card.hidden = !match;
    return match;
  });
  status.textContent = visible.length ? visible.length + (visible.length === 1 ? " figure" : " figures") : "No figures match your search.";
}
search.addEventListener("input", filter);
filters.forEach(button => button.addEventListener("click", () => {
  category = button.dataset.filter;
  filters.forEach(option => option.setAttribute("aria-pressed", String(option === button)));
  filter();
}));

const viewer = document.querySelector("#viewer");
const title = document.querySelector("#figure-title");
const image = document.querySelector("#figure-image");
const caption = document.querySelector("#figure-caption");
const stage = document.querySelector("#image-stage");
const zoom = document.querySelector("#zoom");
let index = 0;
let opener;
function setZoom(zoomed) {
  stage.classList.toggle("zoomed", zoomed);
  stage.scrollTo(0, 0);
  zoom.setAttribute("aria-pressed", String(zoomed));
  zoom.textContent = zoomed ? "Zoom out" : "Zoom in";
}
function show(next) {
  index = (next + visible.length) % visible.length;
  const card = visible[index];
  title.textContent = card.querySelector("h3").textContent;
  image.src = card.querySelector("a").href;
  image.alt = title.textContent;
  caption.textContent = (index + 1) + " / " + visible.length + " · " + card.querySelector("p").textContent;
  setZoom(false);
}
cards.forEach(card => card.querySelector("a").addEventListener("click", event => {
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  event.preventDefault();
  opener = event.currentTarget;
  show(visible.indexOf(card));
  viewer.showModal();
  document.querySelector("#close").focus();
}));
document.querySelector("#close").addEventListener("click", () => viewer.close());
viewer.addEventListener("close", () => opener?.focus());
document.querySelector("#previous").addEventListener("click", () => show(index - 1));
document.querySelector("#next").addEventListener("click", () => show(index + 1));
zoom.addEventListener("click", () => setZoom(!stage.classList.contains("zoomed")));
stage.tabIndex = 0;
stage.setAttribute("aria-label", "Figure image area");
viewer.addEventListener("keydown", event => {
  if (stage.classList.contains("zoomed") && event.target === stage) return;
  if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
    event.preventDefault();
    show(index + (event.key === "ArrowRight" ? 1 : -1));
  }
});
let touchStart;
stage.addEventListener("touchstart", event => {
  touchStart = event.touches.length === 1 ? event.touches[0] : null;
}, {passive: true});
stage.addEventListener("touchend", event => {
  if (!touchStart || stage.classList.contains("zoomed")) return;
  const end = event.changedTouches[0];
  const dx = end.clientX - touchStart.clientX;
  const dy = end.clientY - touchStart.clientY;
  touchStart = null;
  if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.3) show(index + (dx < 0 ? 1 : -1));
}, {passive: true});


// The full navigation stays available when JavaScript is disabled.
const navToggle = document.querySelector("#nav-toggle");
const navLinks = document.querySelector("#nav-links");
const compactNav = matchMedia("(max-width: 1050px)");

function setMenu(open) {
  navToggle.setAttribute("aria-expanded", String(open));
  navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  navLinks.hidden = compactNav.matches && !open;
}

function syncMenu() {
  navToggle.hidden = !compactNav.matches;
  setMenu(false);
}

navToggle.addEventListener("click", () => setMenu(navLinks.hidden));
navLinks.addEventListener("click", event => {
  if (compactNav.matches && event.target.closest("a")) {
    const section = document.querySelector(event.target.closest("a").hash);
    setMenu(false);
    section.tabIndex = -1;
    section.focus({preventScroll: true});
  }
});
navToggle.closest("nav").addEventListener("keydown", event => {
  if (event.key === "Escape" && navToggle.getAttribute("aria-expanded") === "true") {
    setMenu(false);
    navToggle.focus();
  }
});
compactNav.addEventListener("change", syncMenu);
syncMenu();


const sectionLinks = Array.from(navLinks.querySelectorAll("a"));
const navSections = Array.from(document.querySelectorAll(sectionLinks.map(link => link.hash).join(",")));

function markCurrent(section) {
  sectionLinks.forEach(link => {
    if (link.hash === "#" + section?.id) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  });
}

function markVisibleSection() {
  const headerEdge = navToggle.closest("header").getBoundingClientRect().bottom + 45;
  const scroller = document.scrollingElement;
  const atBottom = scroller.scrollTop > 0 &&
    scroller.scrollHeight - scroller.clientHeight - scroller.scrollTop <= 2;

  // A short final section can reach the viewport without crossing the header.
  const current = atBottom
    ? navSections.at(-1)
    : navSections.findLast(section => section.getBoundingClientRect().top <= headerEdge);
  markCurrent(current);
}
window.addEventListener("scroll", markVisibleSection, {passive: true});
window.addEventListener("resize", markVisibleSection);
window.addEventListener("hashchange", markVisibleSection);
markVisibleSection();

