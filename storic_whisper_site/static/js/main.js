/* ═══════════════════════════════════════════════════════════
   STORIC WHISPER — main.js
   Custom cursor • Scroll reveal • Navbar • Mobile menu
   ═══════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── 1. Custom Cursor ─────────────────────────────────── */
  const cursor     = document.getElementById('sw-cursor');
  const cursorRing = document.getElementById('sw-cursor-ring');

  if (cursor && cursorRing && window.matchMedia('(pointer:fine)').matches) {
    let mx = window.innerWidth / 2;
    let my = window.innerHeight / 2;
    let rx = mx, ry = my;

    document.addEventListener('mousemove', (e) => {
      mx = e.clientX;
      my = e.clientY;
      cursor.style.left = mx + 'px';
      cursor.style.top  = my + 'px';
    });

    function animateRing() {
      rx += (mx - rx) * 0.13;
      ry += (my - ry) * 0.13;
      cursorRing.style.left = rx + 'px';
      cursorRing.style.top  = ry + 'px';
      requestAnimationFrame(animateRing);
    }
    animateRing();

    document.addEventListener('mousedown', () => {
      cursor.style.transform = 'translate(-50%,-50%) scale(0.7)';
    });
    document.addEventListener('mouseup', () => {
      cursor.style.transform = 'translate(-50%,-50%) scale(1)';
    });
  } else if (cursor && cursorRing) {
    cursor.style.display = cursorRing.style.display = 'none';
  }

  /* ── 2. Navbar scroll effect ──────────────────────────── */
  const nav = document.getElementById('sw-nav');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 40) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── 3. Mobile menu ───────────────────────────────────── */
  const hamburger   = document.getElementById('sw-hamburger');
  const mobileMenu  = document.getElementById('sw-mobile-menu');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('open');
      hamburger.classList.toggle('open', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('open');
        document.body.style.overflow = '';
      });
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }

  /* ── 4. Scroll Reveal ─────────────────────────────────── */
  function initReveal() {
    const els = document.querySelectorAll('.sw-reveal');
    if (!els.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('sw-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    els.forEach(el => observer.observe(el));
  }
  initReveal();

  /* ── 5. Active nav link ───────────────────────────────── */
  function setActiveNav() {
    const path = window.location.pathname;
    document.querySelectorAll('.sw-nav-link').forEach(link => {
      const href = link.getAttribute('href') || '';
      link.classList.toggle('active', path === href || (href !== '/' && path.startsWith(href)));
    });
  }
  setActiveNav();

  /* ── 6. Newsletter form ───────────────────────────────── */
  document.querySelectorAll('.sw-newsletter-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = form.querySelector('.sw-newsletter-input');
      const btn   = form.querySelector('.sw-newsletter-btn');
      if (!input || !input.value.includes('@')) return;

      const original = btn.textContent;
      btn.textContent = 'शुक्रिया! ✓';
      btn.style.background = '#2d6a4f';
      input.value = '';
      setTimeout(() => {
        btn.textContent = original;
        btn.style.background = '';
      }, 4000);
    });
  });

  /* ── 7. Smooth scroll for anchor links ────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ── 8. Lazy load images ──────────────────────────────── */
  if ('IntersectionObserver' in window) {
    const lazyImgs = document.querySelectorAll('img[data-src]');
    const imgObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imgObserver.unobserve(img);
        }
      });
    });
    lazyImgs.forEach(img => imgObserver.observe(img));
  }

  /* ── 9. LUPPI chat: see static/js/luppi-chat.js (ai_assistant page only) ── */

  /* ── 10. Article category filter ─────────────────────── */
  const filterBtns = document.querySelectorAll('.sw-filter-btn');
  if (filterBtns.length) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.cat;
        document.querySelectorAll('.sw-article-card-wrap').forEach(card => {
          const cardCat = card.dataset.cat;
          card.style.display = (cat === 'all' || cardCat === cat) ? '' : 'none';
        });
      });
    });
  }

  /* ── 11. Reading progress bar ─────────────────────────── */
  const progressBar = document.getElementById('sw-progress');
  if (progressBar) {
    window.addEventListener('scroll', () => {
      const scrollTop = document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      progressBar.style.width = ((scrollTop / height) * 100) + '%';
    }, { passive: true });
  }

  /* ── 12. Estimated reading time ───────────────────────── */
  const articleContent = document.getElementById('sw-article-content');
  const readingTimeEl  = document.getElementById('sw-reading-time');
  if (articleContent && readingTimeEl) {
    const words   = articleContent.innerText.split(/\s+/).length;
    const minutes = Math.max(1, Math.round(words / 220));
    readingTimeEl.textContent = minutes + ' मिनट पढ़ने में';
  }

  console.log('%cStoric Whisper 🌙', 'color:#c9a84c;font-size:18px;font-weight:bold;');
  console.log('%cPsychology Without Noise', 'color:#7a7874;font-size:13px;');

})();