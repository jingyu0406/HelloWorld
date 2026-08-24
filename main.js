const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reduced && 'IntersectionObserver' in window) {
  const sections = document.querySelectorAll('.featured-project, .project-card, .case-head, .case-layout, .about > *, .contact > *');
  sections.forEach((element) => element.classList.add('reveal'));
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  sections.forEach((element) => observer.observe(element));
}
