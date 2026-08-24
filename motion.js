(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) return;

  const start = () => {
    document.documentElement.classList.add('motion-ready');

    const progress = document.createElement('div');
    progress.className = 'scroll-progress';
    progress.setAttribute('aria-hidden', 'true');
    document.body.append(progress);
    let scrollQueued = false;
    const updateScroll = () => {
      const range = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = `scaleX(${range > 0 ? Math.min(window.scrollY / range, 1) : 0})`;
      document.documentElement.style.setProperty('--scroll-y', `${window.scrollY}px`);
      scrollQueued = false;
    };
    window.addEventListener('scroll', () => { if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(updateScroll); } }, { passive: true });
    updateScroll();

    const revealTargets = document.querySelectorAll('.section-heading, .profile-heading, .profile-stats, .section-label, .capability-grid article, .experience-list article, .directory-card, .project-hero > *, .project-cover, .project-details > *, .story-block, .about > *, .contact-heading > *, .contact-form, .page-cta > *, footer > *');
    revealTargets.forEach((element, index) => {
      element.classList.add('motion-reveal');
      element.style.setProperty('--motion-delay', `${Math.min(index % 4, 3) * 70}ms`);
    });
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { entry.target.classList.add('motion-visible'); observer.unobserve(entry.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -4% 0px' });
    revealTargets.forEach((element) => observer.observe(element));

    if (window.matchMedia('(pointer: fine) and (min-width: 801px)').matches) {
      document.querySelectorAll('.directory-card, .capability-grid article').forEach((card) => {
        card.classList.add('motion-tilt');
        card.addEventListener('pointermove', (event) => {
          const bounds = card.getBoundingClientRect();
          const x = (event.clientX - bounds.left) / bounds.width - 0.5;
          const y = (event.clientY - bounds.top) / bounds.height - 0.5;
          card.style.setProperty('--tilt-x', `${(-y * 3.5).toFixed(2)}deg`);
          card.style.setProperty('--tilt-y', `${(x * 3.5).toFixed(2)}deg`);
          card.style.setProperty('--glow-x', `${((x + 0.5) * 100).toFixed(0)}%`);
          card.style.setProperty('--glow-y', `${((y + 0.5) * 100).toFixed(0)}%`);
        });
        card.addEventListener('pointerleave', () => { card.style.removeProperty('--tilt-x'); card.style.removeProperty('--tilt-y'); });
      });

      document.querySelectorAll('.button').forEach((button) => {
        button.addEventListener('pointermove', (event) => {
          const bounds = button.getBoundingClientRect();
          button.style.setProperty('--magnet-x', `${(event.clientX - bounds.left - bounds.width / 2) * 0.12}px`);
          button.style.setProperty('--magnet-y', `${(event.clientY - bounds.top - bounds.height / 2) * 0.18}px`);
        });
        button.addEventListener('pointerleave', () => { button.style.removeProperty('--magnet-x'); button.style.removeProperty('--magnet-y'); });
      });
    }

    const parallaxImage = document.querySelector('.portrait-frame img, .project-cover img');
    if (parallaxImage && window.matchMedia('(min-width: 801px)').matches) {
      window.addEventListener('scroll', () => {
        const bounds = parallaxImage.parentElement.getBoundingClientRect();
        const offset = Math.max(-18, Math.min(18, (window.innerHeight / 2 - (bounds.top + bounds.height / 2)) * 0.035));
        parallaxImage.style.setProperty('--parallax-y', `${offset}px`);
      }, { passive: true });
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
