const bootLines = [
  "> booting mompy...",
  "> loading python training console...",
  "> mission system online",
  "> ready"
];

const bootLog = document.querySelector("#boot-log");
const revealTargets = document.querySelectorAll("[data-reveal]");

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function typeBootLine(line) {
  if (!bootLog) return;
  for (const char of line) {
    bootLog.textContent += char;
    await sleep(28);
  }
  bootLog.textContent += "\n";
  await sleep(260);
}

async function runBootSequence() {
  if (!bootLog) return;
  bootLog.textContent = "";
  await sleep(400);
  for (const line of bootLines) {
    await typeBootLine(line);
  }
}

function setupRevealObserver() {
  if (!("IntersectionObserver" in window)) {
    revealTargets.forEach((target) => target.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  revealTargets.forEach((target) => observer.observe(target));
}

function setupHeaderState() {
  const header = document.querySelector(".site-header");
  if (!header) return;

  const update = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 20);
  };

  update();
  window.addEventListener("scroll", update, { passive: true });
}

setupRevealObserver();
setupHeaderState();
runBootSequence();
