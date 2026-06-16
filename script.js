// تثبيت شريط التنقل عند التمرير
const navbar = document.getElementById("navbar");
window.addEventListener("scroll", () => {
  navbar.classList.toggle("scrolled", window.scrollY > 40);
});

// قائمة الجوال
const navToggle = document.getElementById("navToggle");
const navLinks = document.getElementById("navLinks");
navToggle.addEventListener("click", () => navLinks.classList.toggle("open"));
navLinks.querySelectorAll("a").forEach((a) =>
  a.addEventListener("click", () => navLinks.classList.remove("open"))
);

// حركة ظهور العناصر عند التمرير
const revealEls = document.querySelectorAll(
  ".product-card, .feature, .gallery-item, .section-head, .contact-form, .contact-info"
);
revealEls.forEach((el) => el.classList.add("reveal"));

const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("show");
        io.unobserve(e.target);
      }
    });
  },
  { threshold: 0.15 }
);
revealEls.forEach((el) => io.observe(el));

// عدّاد الأرقام في القسم الرئيسي
const counters = document.querySelectorAll(".stat b[data-count]");
const countObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      const el = e.target;
      const target = +el.dataset.count;
      let cur = 0;
      const step = Math.max(1, Math.ceil(target / 60));
      const tick = () => {
        cur += step;
        if (cur >= target) {
          el.textContent = target.toLocaleString("ar-EG");
        } else {
          el.textContent = cur.toLocaleString("ar-EG");
          requestAnimationFrame(tick);
        }
      };
      tick();
      countObserver.unobserve(el);
    });
  },
  { threshold: 0.5 }
);
counters.forEach((c) => countObserver.observe(c));
