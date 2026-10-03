"""Build showcase.html from the three Silver Surf artboards in this folder."""
import html
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
rd = lambda f: open(f).read()
CARD = r'<div class="fi-card" style="display: flex; align-items: center; gap: 12px; padding: 12px; background: #FFFFFF; border: 1px solid #E3E7EE; border-radius: 14px">.*?(<svg.*?</svg>).*?color: #16324A">(.*?)</div>\s*<div[^>]*>(si-[^<]*)</div>'


def parse(f):
    return [(m.group(2), m.group(3), m.group(1)) for m in re.finditer(CARD, rd(f), re.S)]


nav, surf, acts = parse('Main.dc.html'), parse('Surf.dc.html'), parse('Actions.dc.html')
icon_css = re.search(r'<style>(.*?)</style>', rd('Actions.dc.html'), re.S).group(1)
icon_css = re.sub(r'body\{[^}]*\}', '', icon_css)
icon_css = re.sub(r'@media \(prefers-reduced-motion: reduce\)\{.*?\}\}', '', icon_css, flags=re.S)


def card(name, key, svg):
    key, _, bi = key.partition(' · ')
    svg = re.sub(r' width="\d+" height="\d+"', '', svg, 1)
    q = html.escape(f'{name} {key} {bi}'.lower())
    sub = f'<span class="tile-sub">{bi}</span>' if bi else ''
    return (f'<button type="button" class="fi-card tile" data-q="{q}" aria-label="Copiar SVG de {html.escape(name)}">'
            f'<span class="tile-ico">{svg}</span><span class="tile-name">{name}</span><span class="tile-key">{key}</span>{sub}</button>')


wave = '<svg class="wave" viewBox="0 0 64 8" aria-hidden="true"><path d="M2 4q4-4 8 0t8 0t8 0t8 0t8 0t8 0t8 0"/></svg>'
grid = lambda items: '<div class="grid">' + ''.join(card(*i) for i in items) + '</div>'
total = len(nav) + len(surf) + len(acts)
page = f'''<title>Silver Surf Icons</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@500;600;700&family=Nunito+Sans:wght@400;600;700&family=DM+Mono&display=swap">
<style>
/* Layout: one centred column; sticky tool bar; three sections of button tiles in auto-fill grids */
:root{{--bg:#F3F4F7;--surface:#FFFFFF;--ink:#16324A;--muted:#5A6B7B;--tile:#EEF2F7;--line:#E3E7EE;--navy:#1F4566;--sand:#E9C46A;--sand-ink:#7A5A12;
--ip:var(--navy);--is:var(--sand);--iw:var(--tile);--sz:40px;
--f-display:Lexend,"Trebuchet MS",sans-serif;--f-body:"Nunito Sans",system-ui,sans-serif;--f-mono:"DM Mono",ui-monospace,monospace}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0F2133;--surface:#16304A;--ink:#EEF3F8;--muted:#A9BBCB;--tile:#1C3A57;--line:#24476A;--navy:#9CC7EA;--sand-ink:#F2D9A0;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0F2133;--surface:#16304A;--ink:#EEF3F8;--muted:#A9BBCB;--tile:#1C3A57;--line:#24476A;--navy:#9CC7EA;--sand-ink:#F2D9A0;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:15px;line-height:1.5}}
.wrap{{max-width:1180px;margin:0 auto;padding-inline:20px;padding-block:28px 64px;display:flex;flex-direction:column;gap:36px}}
.hero{{display:flex;flex-direction:column;gap:8px;padding:28px;border-radius:18px;background:#22476B;color:#F2D9A0}}
.hero .kicker{{font-family:var(--f-mono);font-size:13px;color:#C9D6E3}}
.hero h1{{margin:0;font-family:var(--f-display);font-weight:700;font-size:clamp(30px,5vw,46px);line-height:1.05;text-wrap:balance;color:#FFFFFF}}
.hero p{{margin:0;max-width:62ch;color:#DCE6EF}}
.wave{{width:64px;height:8px}}.wave path{{fill:none;stroke:#F2D9A0;stroke-width:2.4;stroke-linecap:round}}
.bar{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;padding:12px 16px;background:var(--surface);border:1px solid var(--line);border-radius:14px}}
.bar label{{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--muted)}}
#q{{min-width:0;width:200px;height:36px;padding:0 12px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink);font:inherit}}
.seg{{display:inline-flex;border:1px solid var(--line);border-radius:10px;overflow:hidden}}
.seg button{{border:0;background:transparent;color:var(--ink);font:inherit;font-size:13px;padding:7px 12px;cursor:pointer}}
.seg button[aria-pressed="true"]{{background:#1F4566;color:#FFFFFF}}
.swatches{{display:inline-flex;gap:6px}}
.swatch{{width:26px;height:26px;border-radius:8px;border:2px solid var(--line);cursor:pointer;padding:0}}
.swatch[aria-pressed="true"]{{border-color:var(--ink)}}
input[type=range]{{width:120px;accent-color:#1F4566}}
button:focus-visible,input:focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}
section{{display:flex;flex-direction:column;gap:14px}}
h2{{margin:0;font-family:var(--f-display);font-size:22px;font-weight:600;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}}
h2 small{{font-family:var(--f-body);font-size:13px;font-weight:400;color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
.tile{{display:flex;flex-direction:column;align-items:flex-start;gap:4px;padding:14px;background:var(--surface);border:1px solid var(--line);border-radius:14px;text-align:left;color:var(--ink);font:inherit;cursor:pointer;min-width:0}}
.tile:hover{{border-color:var(--sand)}}
.tile-ico{{width:100%;aspect-ratio:1.6;max-width:100%;display:flex;align-items:center;justify-content:center;border-radius:10px;background:var(--tbg,var(--tile));margin-bottom:6px}}
.tile-ico svg{{width:var(--sz);height:var(--sz)}}
.tile-name{{font-size:14px;font-weight:700;line-height:1.25}}
.tile-key,.tile-sub{{font-family:var(--f-mono);font-size:11.5px;color:var(--muted);overflow-wrap:anywhere}}
[data-bg="navy"]{{--tbg:#22476B;--ip:#F2D9A0;--is:#FFFFFF;--iw:#22476B}}
[data-bg="sand"]{{--tbg:#F2D9A0;--ip:#1F4566;--is:#FFFFFF;--iw:#F2D9A0}}
[data-bg="night"]{{--tbg:#0B1A29;--ip:#F2D9A0;--is:#5FB7D4;--iw:#0B1A29}}
.foot{{font-size:13px;color:var(--muted);display:flex;gap:12px;flex-wrap:wrap;align-items:center}}
.foot button{{font:inherit;font-size:13px;padding:7px 12px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer}}
#toast{{position:fixed;left:50%;bottom:calc(20px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:var(--ink);color:var(--bg);padding:10px 16px;border-radius:10px;font-size:14px}}
#fallback{{width:100%;min-height:120px;font-family:var(--f-mono);font-size:12px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink)}}
.m-off *{{animation:none!important}}
{icon_css}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<main class="wrap m-loop" id="app" data-bg="light">
<header class="hero">
<div class="kicker">silver.andmore.pt · si-*</div>
<h1>Silver Surf Culture · ícones</h1>
{wave}
<p>{total} ícones em SVG, azul-marinho e areia, com a onda do menu como motivo e animação só em CSS. Clica num ícone para copiar o SVG; o CSS das classes copia-se no fim da página.</p>
</header>
<div class="bar" role="toolbar" aria-label="Opções de visualização">
<label for="q">Procurar <input id="q" type="search" placeholder="prancha, maré, apagar…" autocomplete="off"></label>
<div class="seg" role="group" aria-label="Animação"><button type="button" data-motion="loop" aria-pressed="true">Sempre</button><button type="button" data-motion="hover" aria-pressed="false">Ao passar</button><button type="button" data-motion="off" aria-pressed="false">Parada</button></div>
<div class="swatches" role="group" aria-label="Fundo dos ícones">
<button type="button" class="swatch" data-bgv="light" aria-pressed="true" aria-label="Fundo claro" style="background:var(--tile)"></button>
<button type="button" class="swatch" data-bgv="navy" aria-pressed="false" aria-label="Fundo azul-marinho" style="background:#22476B"></button>
<button type="button" class="swatch" data-bgv="sand" aria-pressed="false" aria-label="Fundo areia" style="background:#F2D9A0"></button>
<button type="button" class="swatch" data-bgv="night" aria-pressed="false" aria-label="Fundo noite" style="background:#0B1A29"></button>
</div>
<label for="sz">Tamanho <input id="sz" type="range" min="16" max="64" step="4" value="40"><span id="szv" style="font-family:var(--f-mono);min-width:3ch">40px</span></label>
</div>
<section data-sec><h2>Navegação <small>{len(nav)} · menu, ferramentas, botões e estado vazio</small></h2>{grid(nav)}</section>
<section data-sec><h2>Surf <small>{len(surf)} · site público</small></h2>{grid(surf)}</section>
<section data-sec><h2>Ações <small>{len(acts)} · substituem os bi-*</small></h2>{grid(acts)}</section>
<div class="foot"><button type="button" id="copycss">Copiar CSS dos ícones</button><span>Grelha 24×24 · cores por classes (.fp .fs .fw .sp .ss .sw) e variáveis --ip / --is / --iw · a animação desliga-se com "reduzir movimento".</span></div>
<textarea id="fallback" readonly hidden aria-label="Código para copiar"></textarea>
</main>
<div id="toast" role="status" hidden></div>
<style id="si-css-src" media="not all">{icon_css}</style>
<script>
(function(){{
var app=document.getElementById('app'),toast=document.getElementById('toast'),fb=document.getElementById('fallback'),t;
function say(m){{toast.textContent=m;toast.hidden=false;clearTimeout(t);t=setTimeout(function(){{toast.hidden=true}},1800)}}
function copy(text,label){{
  var done=function(){{fb.hidden=true;say(label+' copiado')}};
  var fail=function(){{fb.value=text;fb.hidden=false;fb.focus();fb.select();say('Seleciona e copia o código abaixo')}};
  try{{navigator.clipboard.writeText(text).then(done,fail)}}catch(e){{fail()}}
}}
document.querySelectorAll('.tile').forEach(function(b){{b.addEventListener('click',function(){{
  var svg=b.querySelector('svg').cloneNode(true);svg.setAttribute('width','24');svg.setAttribute('height','24');
  copy(svg.outerHTML,'SVG de '+b.querySelector('.tile-name').textContent);
}})}});
document.getElementById('copycss').addEventListener('click',function(){{copy(document.getElementById('si-css-src').textContent.trim(),'CSS')}});
document.querySelectorAll('[data-motion]').forEach(function(b){{b.addEventListener('click',function(){{
  app.classList.remove('m-hover','m-loop','m-off');app.classList.add('m-'+b.dataset.motion);
  document.querySelectorAll('[data-motion]').forEach(function(x){{x.setAttribute('aria-pressed',x===b)}});
}})}});
document.querySelectorAll('[data-bgv]').forEach(function(b){{b.addEventListener('click',function(){{
  app.dataset.bg=b.dataset.bgv;document.querySelectorAll('[data-bgv]').forEach(function(x){{x.setAttribute('aria-pressed',x===b)}});
}})}});
var sz=document.getElementById('sz'),szv=document.getElementById('szv');
sz.addEventListener('input',function(){{app.style.setProperty('--sz',sz.value+'px');szv.textContent=sz.value+'px'}});
document.getElementById('q').addEventListener('input',function(e){{
  var q=e.target.value.trim().toLowerCase();
  document.querySelectorAll('.tile').forEach(function(b){{b.hidden=!!q&&b.dataset.q.indexOf(q)<0}});
  document.querySelectorAll('[data-sec]').forEach(function(g){{g.hidden=!!q&&!g.querySelector('.tile:not([hidden])')}});
}});
}})();
</script>
'''
open('showcase.html', 'w').write(page)
print(len(nav), len(surf), len(acts), len(page) // 1024, 'KB')
