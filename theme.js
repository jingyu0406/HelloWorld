(() => {
  const storageKey = 'jingyu-theme';
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  let saved = null;
  try { saved = localStorage.getItem(storageKey); } catch (_) {}

  const applyTheme = (theme) => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#11110f' : '#f5f1e8');
    const button = document.querySelector('.theme-toggle');
    if (button) {
      const isDark = theme === 'dark';
      button.setAttribute('aria-label', isDark ? '切換至淺色模式' : '切換至深色模式');
      button.setAttribute('title', isDark ? '切換至淺色模式' : '切換至深色模式');
      button.querySelector('.theme-icon').textContent = isDark ? '☀' : '☾';
      button.querySelector('.theme-label').textContent = isDark ? 'Light' : 'Dark';
    }
  };

  applyTheme(saved === 'dark' || saved === 'light' ? saved : (media.matches ? 'dark' : 'light'));
  const stylesheet = document.createElement('link');
  stylesheet.rel = 'stylesheet';
  stylesheet.href = 'theme.css?v=3';
  document.head.append(stylesheet);
  const motionStylesheet = document.createElement('link');
  motionStylesheet.rel = 'stylesheet';
  motionStylesheet.href = 'motion.css?v=2';
  document.head.append(motionStylesheet);
  const pointerStylesheet = document.createElement('link');
  pointerStylesheet.rel = 'stylesheet';
  pointerStylesheet.href = 'pointer.css?v=1';
  document.head.append(pointerStylesheet);
  const motionScript = document.createElement('script');
  motionScript.src = 'motion.js?v=2';
  motionScript.async = false;
  document.head.append(motionScript);

  document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.site-header');
    const siteNav = header?.querySelector('nav');
    if (header && siteNav) {
      siteNav.id = 'site-navigation';
      const navButton = document.createElement('button');
      navButton.className = 'menu-toggle';
      navButton.type = 'button';
      navButton.setAttribute('aria-controls', siteNav.id);
      navButton.setAttribute('aria-expanded', 'false');
      navButton.setAttribute('aria-label', '開啟導覽選單');
      navButton.innerHTML = '<span></span><span></span><span></span>';
      header.insertBefore(navButton, siteNav);
      const closeNavigation = () => {
        document.body.classList.remove('nav-open');
        navButton.setAttribute('aria-expanded', 'false');
        navButton.setAttribute('aria-label', '開啟導覽選單');
      };
      navButton.addEventListener('click', () => {
        const open = document.body.classList.toggle('nav-open');
        navButton.setAttribute('aria-expanded', String(open));
        navButton.setAttribute('aria-label', open ? '關閉導覽選單' : '開啟導覽選單');
      });
      siteNav.addEventListener('click', (event) => { if (event.target.closest('a')) closeNavigation(); });
      document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && document.body.classList.contains('nav-open')) { closeNavigation(); navButton.focus(); } });
      window.matchMedia('(min-width: 801px)').addEventListener?.('change', (event) => { if (event.matches) closeNavigation(); });
    }
    const dropdown = document.querySelector('.nav-projects');
    if (dropdown) {
      const workLink = dropdown.querySelector('a[href="index.html"]');
      const menuButton = dropdown.querySelector('.projects-menu-button');
      menuButton.addEventListener('click', () => {
        const open = dropdown.classList.toggle('is-open');
        menuButton.setAttribute('aria-expanded', String(open));
      });
      document.addEventListener('click', (event) => {
        if (!dropdown.contains(event.target)) { dropdown.classList.remove('is-open'); menuButton.setAttribute('aria-expanded', 'false'); }
      });
      dropdown.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') { dropdown.classList.remove('is-open'); menuButton.setAttribute('aria-expanded', 'false'); workLink?.focus(); }
      });
    }
    const button = document.createElement('button');
    button.className = 'theme-toggle';
    button.type = 'button';
    button.innerHTML = '<span class="theme-icon" aria-hidden="true"></span><span class="theme-label"></span>';
    (document.querySelector('.site-header nav') || document.querySelector('.site-header'))?.append(button);
    applyTheme(document.documentElement.dataset.theme);
    button.addEventListener('click', () => {
      const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(storageKey, next); } catch (_) {}
      applyTheme(next);
    });
  });

  media.addEventListener?.('change', (event) => {
    try { if (localStorage.getItem(storageKey)) return; } catch (_) {}
    applyTheme(event.matches ? 'dark' : 'light');
  });
})();
