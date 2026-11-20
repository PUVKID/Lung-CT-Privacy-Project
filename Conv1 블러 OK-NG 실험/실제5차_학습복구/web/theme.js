// 저장된 사용자 선택이 없으면 밝은 화면으로 시작합니다.
(() => {
  let selected = null;
  try { selected = localStorage.getItem('ct-lab-theme'); } catch {}
  if (!['light','dark'].includes(selected)) selected = null;
  function apply() {
    const theme = selected || 'light';
    document.documentElement.dataset.theme = theme;
    window.dispatchEvent(new CustomEvent('ct-theme-change', {detail:theme}));
  }
  window.ctTheme = {
    current: () => document.documentElement.dataset.theme,
    toggle: () => {selected = window.ctTheme.current()==='dark'?'light':'dark';try{localStorage.setItem('ct-lab-theme',selected);}catch{}apply();}
  };
  apply();
})();
