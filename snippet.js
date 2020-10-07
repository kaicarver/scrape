

urls = Array.from(document.querySelectorAll('.rg_di .rg_meta'))
  .map(el => JSON.parse(el.textContent).ou);

urls = Array.from(document.querySelectorAll('.wXeWr'))
  .map(el => el.href);
