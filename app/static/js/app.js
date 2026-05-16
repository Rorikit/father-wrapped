const story = document.querySelector("#story");
const sections = [...document.querySelectorAll(".story-section")];
const progressBar = document.querySelector("#progressBar");
const startButton = document.querySelector("#startButton");
const restartButton = document.querySelector("#restartButton");
const musicToggle = document.querySelector("#musicToggle");
const backgroundMusic = document.querySelector("#backgroundMusic");
const typewriter = document.querySelector("#typewriter");
const modal = document.querySelector("#photoModal");
const modalImage = document.querySelector("#modalImage");
const modalTitle = document.querySelector("#modalTitle");
const closeModal = document.querySelector("#closeModal");

const markMissingImages = () => {
  document.querySelectorAll(".media-frame img").forEach((image) => {
    image.addEventListener("error", () => {
      image.classList.add("is-missing");
    });
  });
};

const updateProgress = () => {
  const maxScroll = story.scrollHeight - story.clientHeight;
  const percent = maxScroll > 0 ? (story.scrollTop / maxScroll) * 100 : 0;
  progressBar.style.width = `${Math.min(100, Math.max(0, percent))}%`;
};

const animateCounters = (section) => {
  section.querySelectorAll(".counter:not(.is-counted)").forEach((counter) => {
    counter.classList.add("is-counted");
    const target = Number(counter.dataset.target || 0);
    const duration = 1500;
    const startTime = performance.now();

    const tick = (now) => {
      const progress = Math.min((now - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      counter.textContent = Math.floor(target * eased).toLocaleString("ru-RU");

      if (progress < 1) {
        requestAnimationFrame(tick);
      }
    };

    requestAnimationFrame(tick);
  });
};

let quoteIndex = 0;
let quoteTimer;

const runTypewriter = () => {
  if (!typewriter || typewriter.dataset.started === "true") return;

  typewriter.dataset.started = "true";
  const quotes = JSON.parse(typewriter.dataset.quotes || "[]");
  if (!quotes.length) return;

  const typeQuote = () => {
    const quote = quotes[quoteIndex % quotes.length];
    let cursor = 0;
    typewriter.textContent = "";

    clearInterval(quoteTimer);
    quoteTimer = setInterval(() => {
      typewriter.textContent = quote.slice(0, cursor);
      cursor += 1;

      if (cursor > quote.length) {
        clearInterval(quoteTimer);
        quoteIndex += 1;
        setTimeout(typeQuote, 1800);
      }
    }, 42);
  };

  typeQuote();
};

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      animateCounters(entry.target);

      if (entry.target.contains(typewriter)) {
        runTypewriter();
      }
    });
  },
  {
    root: story,
    threshold: 0.45,
  }
);

sections.forEach((section) => observer.observe(section));

startButton?.addEventListener("click", () => {
  sections[1]?.scrollIntoView({ behavior: "smooth" });
});

restartButton?.addEventListener("click", () => {
  sections[0]?.scrollIntoView({ behavior: "smooth" });
});

musicToggle?.addEventListener("click", async () => {
  try {
    if (backgroundMusic.paused) {
      await backgroundMusic.play();
      musicToggle.textContent = "Выключить музыку";
    } else {
      backgroundMusic.pause();
      musicToggle.textContent = "Включить музыку";
    }
  } catch (error) {
    musicToggle.textContent = "Добавьте музыку";
  }
});

document.querySelectorAll(".gallery-item").forEach((button) => {
  button.addEventListener("click", () => {
    modalImage.src = button.dataset.full;
    modalImage.alt = button.dataset.title;
    modalTitle.textContent = button.dataset.title;

    if (typeof modal.showModal === "function") {
      modal.showModal();
    }
  });
});

closeModal?.addEventListener("click", () => modal.close());

modal?.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.close();
  }
});

story.addEventListener("scroll", updateProgress, { passive: true });
window.addEventListener("resize", updateProgress);

markMissingImages();
updateProgress();
sections[0]?.classList.add("is-visible");
