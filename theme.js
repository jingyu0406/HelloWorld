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
  stylesheet.href = 'theme.css?v=2';
  document.head.append(stylesheet);

  document.addEventListener('DOMContentLoaded', () => {
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
