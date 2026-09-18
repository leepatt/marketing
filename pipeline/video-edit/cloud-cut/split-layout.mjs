// shared: turn the Formwork Builder page into a 1080x1920 split — viewer top, config panel bottom (close up)
export const CSS = `
  #__viewer{position:fixed!important;top:0;left:0;width:1080px;height:960px;background:#f6f6f4;z-index:2147483000;border-radius:0;margin:0}
  #__viewer *:not(canvas):not(:has(canvas)){display:none!important}
  #__viewer canvas{width:1080px!important;height:960px!important}
  #__wrap{position:fixed!important;top:960px;left:0;width:1080px;height:960px;overflow:hidden;background:#fff;z-index:2147483001;margin:0}
  #__panel{zoom:2;width:540px!important;max-width:540px!important;padding:14px 20px 40px;box-sizing:border-box;margin:0}
  #__panel > *{border:0!important;box-shadow:none!important;border-radius:0!important}
  main, main *{visibility:hidden!important}   /* the view-cube and home icon live in main, outside the moved viewer */
`;
export async function applySplit(p) {
  await p.addStyleTag({ content: CSS });
  const info = await p.evaluate(() => {
    let host = document.querySelector('canvas'); for (let i=0;i<3;i++) host = host.parentElement; host.id='__viewer';
    const aside = document.querySelector('aside'); const panel = aside.firstElementChild || aside;
    const wrap = document.createElement('div'); wrap.id='__wrap'; wrap.appendChild(panel); panel.id='__panel';
    document.body.appendChild(host); document.body.appendChild(wrap);
    window.dispatchEvent(new Event('resize'));
    const c = document.querySelector('canvas').getBoundingClientRect(), r = panel.getBoundingClientRect();
    return `canvas ${Math.round(c.width)}x${Math.round(c.height)}@${Math.round(c.y)} | panel ${Math.round(r.width)}x${Math.round(r.height)}@${Math.round(r.y)}`;
  });
  return info;
}
export async function scrollPanelTo(p, label, off=20) {
  await p.evaluate(([t,off]) => { const w=document.getElementById('__wrap'); const el=[...w.querySelectorAll('*')].find(e=>e.children.length<6 && (e.innerText||'').trim().toUpperCase().startsWith(t.toUpperCase())); if (el){ w.scrollTo({ top: w.scrollTop + (el.getBoundingClientRect().top - w.getBoundingClientRect().top) - off, behavior: 'smooth' }); } }, [label, off]);
}
