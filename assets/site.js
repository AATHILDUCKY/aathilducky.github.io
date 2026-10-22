(() => {
  'use strict';
  const legacySections = {
    about: '/about/', 'online-tools': '/tools/', projects: '/projects/',
    experience: '/about/#experience', 'freelance-projects': '/freelance/', contact: '/contact/',
  };
  const legacyTarget = legacySections[location.hash.slice(1)];
  if (document.body.dataset.page === 'home' && legacyTarget) {
    location.replace(legacyTarget);
    return;
  }

  const menuButton = document.getElementById('menu-toggle');
  const menu = document.getElementById('mobile-nav');
  if (menuButton && menu) {
    const setMenu = (open, restoreFocus = false) => {
      menu.hidden = !open;
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      menuButton.querySelector('use').setAttribute('href', open ? '#i-close' : '#i-menu');
      if (restoreFocus) menuButton.focus();
    };
    setMenu(false);
    menuButton.hidden = false;
    menuButton.addEventListener('click', () => setMenu(menu.hidden));
    menu.addEventListener('click', event => {
      if (event.target.closest('a[href]')) setMenu(false);
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !menu.hidden) setMenu(false, true);
    });
    document.addEventListener('click', event => {
      if (!menu.hidden && !event.target.closest('.site-header')) setMenu(false);
    });
    matchMedia('(min-width: 1001px)').addEventListener('change', event => {
      if (event.matches) setMenu(false);
    });
  }

  const search = document.getElementById('project-search');
  if (search) {
    const rows = [...document.querySelectorAll('[data-project]')];
    const filters = [...document.querySelectorAll('[data-filter]')];
    const count = document.getElementById('project-count');
    const reset = document.getElementById('project-reset');
    let category = 'all';
    const filterProjects = () => {
      const term = search.value.trim().toLowerCase();
      let visible = 0;
      rows.forEach(row => {
        const matches = (category === 'all' || row.dataset.category === category) && row.dataset.search.includes(term);
        row.hidden = !matches;
        if (matches) visible += 1;
      });
      count.textContent = `${visible} of ${rows.length} projects`;
      document.getElementById('project-empty').hidden = visible !== 0;
      reset.hidden = !term && category === 'all';
      filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    };
    document.getElementById('project-controls').hidden = false;
    search.addEventListener('input', filterProjects);
    filters.forEach(button => button.addEventListener('click', () => {
      category = button.dataset.filter;
      filterProjects();
    }));
    reset.addEventListener('click', () => {
      category = 'all';
      search.value = '';
      filterProjects();
      search.focus();
    });
    filterProjects();
  }

  const toolSearch = document.getElementById('tool-search');
  if (toolSearch) {
    const cards = [...document.querySelectorAll('[data-tool]')];
    const filters = [...document.querySelectorAll('[data-tool-filter]')];
    const count = document.getElementById('tool-count');
    const reset = document.getElementById('tool-reset');
    let category = 'all';
    const filterTools = () => {
      const terms = toolSearch.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
      let visible = 0;
      cards.forEach(card => {
        const matches = (category === 'all' || card.dataset.category === category) && terms.every(term => card.dataset.search.includes(term));
        card.hidden = !matches;
        if (matches) visible += 1;
      });
      count.textContent = `${visible} of ${cards.length} tools`;
      document.getElementById('tool-empty').hidden = visible !== 0;
      reset.hidden = terms.length === 0 && category === 'all';
      filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.toolFilter === category)));
    };
    document.getElementById('tool-controls').hidden = false;
    toolSearch.addEventListener('input', filterTools);
    filters.forEach(button => button.addEventListener('click', () => {
      category = button.dataset.toolFilter;
      filterTools();
    }));
    reset.addEventListener('click', () => {
      category = 'all';
      toolSearch.value = '';
      filterTools();
      toolSearch.focus();
    });
    filterTools();
  }

  const copyButton = document.getElementById('copy-email');
  if (copyButton && navigator.clipboard && window.isSecureContext) {
    copyButton.hidden = false;
    copyButton.addEventListener('click', async () => {
      const feedback = document.getElementById('copy-feedback');
      try {
        await navigator.clipboard.writeText('aathilducky@gmail.com');
        feedback.textContent = 'Email address copied.';
      } catch {
        feedback.textContent = 'Please use the email link above.';
      }
    });
  }
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
