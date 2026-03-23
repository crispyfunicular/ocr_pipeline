/* ── script.js — Showcase interactions ── */

document.addEventListener('DOMContentLoaded', () => {
  // ── Scroll reveal ──
  const reveals = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  reveals.forEach((el) => observer.observe(el));

  // ── Active nav highlight ──
  const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');
  const sections = [...navLinks].map((link) => {
    const id = link.getAttribute('href').slice(1);
    return { link, section: document.getElementById(id) };
  }).filter((item) => item.section);

  function updateActiveNav() {
    const scrollY = window.scrollY + 120;
    let current = sections[0];
    for (const item of sections) {
      if (item.section.offsetTop <= scrollY) {
        current = item;
      }
    }
    navLinks.forEach((l) => l.classList.remove('active'));
    if (current) current.link.classList.add('active');
  }
  window.addEventListener('scroll', updateActiveNav, { passive: true });
  updateActiveNav();

  // ── Mobile nav toggle ──
  const toggle = document.getElementById('nav-toggle');
  const navLinksContainer = document.querySelector('.nav-links');
  if (toggle && navLinksContainer) {
    toggle.addEventListener('click', () => {
      navLinksContainer.classList.toggle('open');
      toggle.textContent = navLinksContainer.classList.contains('open') ? '✕' : '☰';
    });
    // Close on link click
    navLinksContainer.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', () => {
        navLinksContainer.classList.remove('open');
        toggle.textContent = '☰';
      });
    });
  }

  // ── Stat counter animation ──
  const statNumbers = document.querySelectorAll('.stat-number[data-target]');
  const statObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          statObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );
  statNumbers.forEach((el) => statObserver.observe(el));

  function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    const duration = 1500;
    const startTime = performance.now();

    function tick(now) {
      const progress = Math.min((now - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      const value = Math.round(eased * target);
      el.textContent = value.toLocaleString('fr-FR');
      if (progress < 1) requestAnimationFrame(tick);
      else el.textContent = target.toLocaleString('fr-FR') + (target > 100 ? '+' : '');
    }
    requestAnimationFrame(tick);
  }

  // ── JSONL typewriter effect ──
  const jsonlLines = [
    '{"breton": "a wrie", "français": "cousait"}',
    '{"breton": "a zo bet broudet", "français": "a été piqué"}',
    '{"breton": "ar c\'hazh", "français": "le chat"}',
    '{"breton": "demat", "français": "bonjour"}',
    '{"breton": "ur vamm", "français": "une mère"}',
  ];

  const typewriterEl = document.getElementById('jsonl-typewriter');
  if (typewriterEl) {
    const typeObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            startTypewriter(typewriterEl, jsonlLines);
            typeObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );
    typeObserver.observe(typewriterEl);
  }

  function startTypewriter(el, lines) {
    let lineIdx = 0;
    let charIdx = 0;
    let currentText = '';

    function type() {
      if (lineIdx >= lines.length) return;

      const line = lines[lineIdx];
      if (charIdx < line.length) {
        currentText += line[charIdx];
        el.textContent = currentText + '▌';
        charIdx++;
        setTimeout(type, 18 + Math.random() * 22);
      } else {
        currentText += '\n';
        el.textContent = currentText + '▌';
        lineIdx++;
        charIdx = 0;
        if (lineIdx < lines.length) {
          setTimeout(type, 400);
        } else {
          el.textContent = currentText.trimEnd();
        }
      }
    }
    type();
  }
});
