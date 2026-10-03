import re, json, datetime, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
A = open('../dancesoul-icons/Actions.dc.html').read()
base_css = re.search(r'<style>(.*?)</style>', A, re.S).group(1)
base_css = re.sub(r'body\{[^}]*\}', 'body{margin:0;font-family:"Nunito Sans",sans-serif;background:#F3F4F7}', base_css)
base_css += '''.a-wavex{transform-box:fill-box}
@keyframes fi-wavex{0%,100%{transform:translateX(0)}50%{transform:translateX(-1.5px)}}
.m-loop .a-wavex,.m-hover .fi-card:hover .a-wavex{animation:fi-wavex 1.2s ease-in-out infinite}
'''
NAVY = '#1F4566'; SAND = '#E9C46A'


def C(cx, cy, r, cls, extra=''):
    return f'<circle class="{cls}{extra}" cx="{cx}" cy="{cy}" r="{r}"/>'


def L(d, cls='sp', w=2.2, extra=''):
    pl = ' pathLength="1"' if 'a-draw' in extra else ''
    return f'<path class="{cls}{extra}"{pl} fill="none" stroke-width="{w}" d="{d}"/>'


def Wv(x0, y, n, cls='ss', w=1.8, extra='', step=3, amp=1.6):
    d = f'M{x0} {y}q{step/2} -{amp} {step} 0' + ''.join(f't{step} 0' for _ in range(n - 1))
    return L(d, cls, w, extra)


cal_base = ('<rect class="fp" x="3" y="5" width="18" height="16" rx="2.5"/>'
            '<path class="fs" d="M3 7.5A2.5 2.5 0 0 1 5.5 5h13A2.5 2.5 0 0 1 21 7.5V10H3z"/>' + L("M8 3v4M16 3v4", 'sp', 2))
board = ('<path class="fp" d="M5.2 18.8C3.6 17.2 5.6 10.9 10.2 6.3S19.7 2.6 20.6 3.5s.4 6.2-4.2 10.8-9.6 6.1-11.2 4.5z"/>'
         + L("M6.8 17.2L18.4 5.6", 'sw', 1.1))

NAV = [
    ('Dashboard', 'painel', '<path class="fp" d="M4 10.6L12 4l8 6.6v8.9a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 19.5z"/>' + Wv(6.5, 16.8, 4, 'sw', 1.6, ' a-wavex')),
    ('Aulas', 'aulas', '<g class="a-bob">' + board + '<path class="fs" d="M8.4 16.4l.8 3.6 1.9-2.6z"/></g>'),
    ('Calendário', 'calendario', cal_base + Wv(6, 15.5, 4, 'sw', 1.6) + C(16.5, 18.3, 1.3, 'fs', ' a-pulse')),
    ('Alunos', 'alunos', '<path class="fs" d="M1.5 19a4.4 4.4 0 0 1 6-4.1A7.6 7.6 0 0 0 5.4 19z"/><path class="fs" d="M22.5 19a4.4 4.4 0 0 0-6-4.1 7.6 7.6 0 0 1 2.1 4.1z"/>'
     + C(5, 9.5, 1.9, 'fs') + C(19, 9.5, 1.9, 'fs') + '<g class="a-bob">' + C(12, 7, 2.7, 'fp') + '<path class="fp" d="M5.8 20.5a6.2 6.2 0 0 1 12.4 0z"/></g>'),
    ('Ferramentas', 'ferramentas', ''.join(f'<rect class="{"fs a-pulse" if (x, y) == (9.5, 9.5) else "fp"}" x="{x}" y="{y}" width="5" height="5" rx="1.3"/>' for y in (3, 9.5, 16) for x in (3, 9.5, 16))),
    ('Perfil', 'perfil', C(12, 12, 10, 'fp') + '<g class="a-bob">' + C(12, 9.5, 3, 'fw') + '<path class="fw" d="M6.3 18.6a6.6 6.6 0 0 1 11.4 0 8 8 0 0 1-11.4 0z"/></g>'),
    ('Relatórios', 'relatorios', C(7, 7.5, 2.7, 'fp') + '<path class="fp" d="M2.5 19a4.5 4.5 0 0 1 9 0z"/>' + L("M14 7.5h7M14 11.5h7", 'sp', 2) + Wv(14, 16, 2, 'ss', 2, ' a-draw', step=3.5)),
    ('Sócios', 'socios', '<rect class="fp" x="2.5" y="5" width="19" height="14" rx="2.5"/><g class="a-pulse">' + C(8, 10.6, 2.4, 'fs')
     + '<path class="fs" d="M4.8 16.6a3.2 3.2 0 0 1 6.4 0z"/></g>' + L("M13.5 10h5M13.5 13h5M13.5 16h3", 'sw', 1.4)),
    ('Site público', 'site', '<rect class="fp" x="2.5" y="4" width="19" height="16" rx="2.5"/><path class="fs" d="M2.5 6.5A2.5 2.5 0 0 1 5 4h14a2.5 2.5 0 0 1 2.5 2.5V8.5h-19z"/>'
     + C(5.3, 6.3, .8, 'fw') + C(7.6, 6.3, .8, 'fw') + Wv(5.5, 14.5, 4, 'sw', 1.7, ' a-wavex')),
    ('Criar conteúdo', 'conteudo', '<path class="fp" d="M4 10v4a1 1 0 0 0 1 1h2l7 4.5V4.5L7 9H5a1 1 0 0 0-1 1z"/><g class="a-blink">' + L("M17 9a4 4 0 0 1 0 6M19.5 6.5a7.5 7.5 0 0 1 0 11", 'ss', 1.8) + '</g>'),
    ('Enviar e-mail', 'email', '<rect class="fp" x="2.5" y="5" width="17" height="13" rx="2.5"/>' + L("M3.5 6.5l7.5 5.8 7.5-5.8", 'sw', 1.5)
     + '<g class="a-nudge-r">' + C(18.5, 17.5, 4.2, 'fs') + L("M16.6 17.5h3.6M18.6 15.7l1.8 1.8-1.8 1.8", 'sw', 1.4) + '</g>'),
    ('Spam bloqueado', 'spam', '<path class="fp" d="M12 2.8l8 3.2v5.6c0 5-3.3 8.8-8 10.4-4.7-1.6-8-5.4-8-10.4V6z"/><g class="a-pulse">'
     + L("M12 7.9a3.6 3.6 0 1 0 0 7.2 3.6 3.6 0 0 0 0-7.2zM9.5 14l5-5", 'sw', 1.6) + '</g>'),
    ('Nova aula', 'nova_aula', cal_base + Wv(6, 15.5, 3, 'sw', 1.6) + '<g class="a-pulse">' + C(18, 18, 4.3, 'fs') + L("M18 16v4M16 18h4", 'sw', 1.6) + '</g>'),
    ('Todas as aulas', 'todas_aulas', ''.join(f'<rect class="fp" x="3" y="{y}" width="18" height="4.4" rx="2.2"/>' + C(5.6, round(y + 2.2, 1), 1.2, 'fs', ' a-blink' if i == 0 else '')
                                             + L(f"M8.5 {round(y + 2.2, 1)}h9", 'sw', 1.3) for i, y in enumerate((3.5, 9.8, 16.1)))),
    ('Sem aulas', 'sem_aulas', cal_base + '<g class="a-shake">' + L("M9.5 13l5 5M14.5 13l-5 5", 'sw', 2.2) + '</g>'),
]

SURF = [
    ('Aula de grupo', 'grupo', C(5.5, 7.5, 2, 'fs') + C(18.5, 7.5, 2, 'fs') + '<path class="fs" d="M2.8 15.5a2.7 2.7 0 0 1 5.4 0z"/><path class="fs" d="M15.8 15.5a2.7 2.7 0 0 1 5.4 0z"/><g class="a-bob">'
     + C(12, 6, 2.5, 'fp') + '<path class="fp" d="M8.3 15.5a3.7 3.7 0 0 1 7.4 0z"/></g>' + Wv(2, 19.5, 7, 'ss', 1.9, ' a-wavex', step=2.86)),
    ('Aula privada', 'privada', C(8, 5, 2.5, 'fp') + '<path class="fp" d="M5 18v-6a3 3 0 0 1 6 0v6z"/><g class="a-sway"><path class="fs" d="M16.5 2.5c2 0 3.3 4.2 3.3 9.5s-1.3 9.5-3.3 9.5-3.3-4.2-3.3-9.5 1.3-9.5 3.3-9.5z"/>'
     + L("M16.5 4v15", 'sw', 1) + '</g>' + Wv(2, 21, 3, 'ss', 1.6)),
    ('Surf infantil', 'infantil', '<g class="a-bounce">' + C(12, 6.5, 3.3, 'fp') + '<path class="fp" d="M8.5 17.5v-3.2a3.5 3.5 0 0 1 7 0v3.2z"/>'
     + L("M9 12.5L6 9.5M15 12.5l3-3", 'sp', 1.8) + '</g>' + Wv(3, 20.5, 6, 'ss', 1.9) + C(19.5, 4, 1.3, 'fs', ' a-blink')),
    ('Bodyboard', 'bodyboard', '<g class="a-bob"><rect class="fp" x="5" y="3.5" width="11" height="16" rx="3.5" transform="rotate(-14 10.5 11.5)"/><rect class="fw" x="7" y="6" width="7" height="2" rx="1" transform="rotate(-14 10.5 11.5)"/></g>'
     + L("M15.8 5.5c3 0 5.2 2.4 4.6 5.5", 'ss', 1.5) + C(20.2, 12.4, 1.5, 'fs')),
    ('Stand up paddle', 'sup', '<path class="fp" d="M2 18c0-1.2 4.5-2 10-2s10 .8 10 2-4.5 2-10 2-10-.8-10-2z"/><g class="a-sway">' + L("M9 3l6 12", 'sp', 1.8)
     + '<ellipse class="fs" cx="15.6" cy="15.6" rx="1.4" ry="2.6" transform="rotate(-27 15.6 15.6)"/></g>' + Wv(2, 22, 7, 'ss', 1.4, '', step=2.86, amp=1.2)),
    ('Surfskate', 'surfskate', Wv(5, 6.5, 5, 'ss', 1.8, ' a-wavex') + '<g class="a-bob"><path class="fp" d="M2.5 11.8c.3 1.6 1.4 2.7 3 2.7h13c1.6 0 2.7-1.1 3-2.7z"/>'
     + C(7, 17.6, 1.9, 'fs') + C(17, 17.6, 1.9, 'fs') + '</g>'),
    ('Aluguer de prancha', 'aluguer_prancha', board + '<g class="a-swing"><path class="fs" d="M13.2 13h5.2l2.4 2.5-2.4 2.5h-5.2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1z"/>' + C(14.3, 15.5, .8, 'fw') + '</g>'),
    ('Aluguer de fato', 'aluguer_fato', '<path class="fp" d="M9 2.5h6l1.2 2.4 3.6 1.6 1.2 8.3-2.3.6-1.2-6.1-1.5 1.1V21h-3.2l-.8-6.6-.8 6.6H7.8V10.4L6.3 9.3l-1.2 6.1-2.3-.6 1.2-8.3 3.6-1.6z"/>'
     + L("M12 4.5v7.5", 'sw', 1.2) + C(12, 13.2, .9, 'fs', ' a-blink')),
    ('Condições do mar', 'ondas', '<path class="fp" d="M2 20.5c.8-6.2 4.9-11 10.8-11 4 0 7.2 2.4 7.2 5.8 0 2.2-1.6 3.6-3.6 3.6-1.7 0-2.8-1.1-2.8-2.5 0-1 .6-1.8 1.5-2.1-1-.9-2.6-1.3-4.1-1.1-3.5.6-5.6 3.9-6 7.3z"/>'
     + L("M2 21h20", 'ss', 1.8) + C(19, 5, 2.4, 'fs', ' a-pulse')),
    ('Maré', 'mare', Wv(2, 15.5, 7, 'ss', 1.8, ' a-wavex', step=2.86) + Wv(2, 20, 7, 'ss', 1.8, '', step=2.86)
     + '<g class="a-bob"><path class="fp" d="M8 2.5L4.5 6.5h2.4V11h2.2V6.5h2.4z"/></g><path class="fp" d="M16 11.5l3.5-4h-2.4V3h-2.2v4.5h-2.4z"/>'),
    ('Vento', 'vento', '<g class="a-nudge-r">' + L("M3 8h10.5a2.5 2.5 0 1 0-2.5-2.5M3 12h15a2.5 2.5 0 1 1-2.5 2.5", 'sp', 2.1) + '</g>' + L("M3 16.5h7", 'ss', 2.1) + C(20, 19.5, 1.3, 'fs')),
    ('Nível', 'nivel', '<rect class="fp" x="3" y="15" width="4.5" height="6" rx="1.2"/><rect class="fp" x="9.75" y="11" width="4.5" height="10" rx="1.2"/><rect class="fp" x="16.5" y="7" width="4.5" height="14" rx="1.2"/>'
     + Wv(3, 5, 4, 'ss', 1.7, ' a-wavex', step=3.5) + C(18.8, 3.6, 1.3, 'fs')),
    ('Surf camp', 'camp', '<path class="fp" stroke-linejoin="round" d="M2.5 20L12 4.5 21.5 20z"/><path class="fw" d="M12 20l-2.6-5.2h5.2z"/>' + L("M1 20.7h22", 'sp', 1.6) + C(19.5, 5, 2.2, 'fs', ' a-pulse')),
    ('Fotos e vídeo', 'fotos', '<rect class="fp" x="2.5" y="7" width="19" height="13" rx="2.5"/><rect class="fp" x="8" y="4.5" width="7" height="4" rx="1.2"/>'
     + C(12, 13.5, 4.2, 'fw') + C(12, 13.5, 2.2, 'fs', ' a-pulse') + '<rect class="fs" x="16.5" y="9" width="2.5" height="1.6" rx=".8"/>'),
]


def svg(b, s):
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{b}</svg>'


def card(n, key, b):
    return (f'<div class="fi-card" style="display: flex; align-items: center; gap: 12px; padding: 12px; background: #FFFFFF; border: 1px solid #E3E7EE; border-radius: 14px">'
            f'<div style="width: 48px; height: 48px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; background: #EEF2F7; border-radius: 12px">{svg(b, 28)}</div>'
            f'<div style="display: flex; flex-direction: column; gap: 2px; min-width: 0"><div style="font-size: 13.5px; font-weight: 700; line-height: 1.25; color: #16324A">{n}</div>'
            f'<div style="font-family: \'DM Mono\', monospace; font-size: 11px; color: #5A6B7B">{key}</div></div></div>\n')


def grid(cards, cols):
    return f'<div style="display: grid; grid-template-columns: repeat({cols}, minmax(0, 1fr)); gap: 12px">\n' + ''.join(cards) + '</div>\n'


# Actions: reuse the Dance Soul geometry, swap the diamond accents for circles
acts = []
for m in re.finditer(r'<div class="fi-card" style="display: flex; align-items: center; gap: 12px; padding: 12px; background: #FFFFFF; border-radius: 14px">.*?(<svg.*?</svg>).*?color: #2A1A24">(.*?)</div><div[^>]*>fi-([^ <]*) · (bi-[^<]*)</div>', A, re.S):
    s = m.group(1)

    def dia2circ(mm):
        cls, extra, x1, y1, x2, y2 = mm.groups()
        w = 2 * (float(x2) - float(x1)); h = 2 * (float(y2) - float(y1)); r = min(w, h) / 2 * 0.95
        return f'<circle class="{ {"dp": "fp", "ds": "fs", "fw": "fw"}[cls] }{extra or ""}" cx="{x1}" cy="{y2}" r="{r:.2f}"/>'
    s = re.sub(r'<path class="(dp|ds|fw)( a-[\w-]+)?" stroke-width="1.1" stroke-linejoin="round" d="M([\d.]+) ([\d.]+)L([\d.]+) ([\d.]+)L[\d. ]+L[\d. ]+Z"/>', dia2circ, s)
    acts.append((m.group(2), f'si-{m.group(3)} · {m.group(4)}', re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)))
assert len(acts) == 25, len(acts)


def page(title, inner, W, H, motion='loop'):
    props = {"motion": {"editor": "enum", "options": ["hover", "loop", "off"], "default": motion},
             "primary": {"editor": "color", "default": NAVY, "options": [NAVY, "#0E7490", "#16324A"]},
             "secondary": {"editor": "color", "default": SAND, "options": [SAND, "#F2D9A0", "#5FB7D4"]},
             "$preview": {"width": W, "height": H}}
    return f'''<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@500;600;700&amp;family=Nunito+Sans:wght@400;600;700&amp;family=DM+Mono&amp;display=swap">
<style>
{base_css}
</style>
</helmet>
<div class="m-{{{{motion}}}}" style="--ip: {{{{primary}}}}; --is: {{{{secondary}}}}; --iw: #FFFFFF; width: {W}px; height: {H}px; box-sizing: border-box; padding: 56px 64px; display: flex; flex-direction: column; gap: 28px; background: #F3F4F7; font-family: 'Nunito Sans', sans-serif">
{inner}</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{json.dumps(props, ensure_ascii=False)}'>
class Component extends DCLogic {{
renderVals() {{
return {{ motion: this.props.motion ?? '{motion}', primary: this.props.primary ?? '{NAVY}', secondary: this.props.secondary ?? '{SAND}' }};
}}
}}
</script>
</body>
</html>
'''


WAVE_SM = '<svg width="34" height="5" viewBox="0 0 34 5" aria-hidden="true"><path d="M1 2.5q2-2.5 4 0t4 0t4 0t4 0t4 0t4 0t4 0t4 0" fill="none" stroke="#F2D9A0" stroke-width="1.6" stroke-linecap="round"/></svg>'


def head(kicker, h1, sub):
    return (f'<div style="display: flex; flex-direction: column; gap: 6px"><div style="font-family: \'DM Mono\', monospace; font-size: 13px; color: #1F4566">{kicker}</div>'
            f'<h1 style="margin: 0; font-family: Lexend, sans-serif; font-weight: 700; font-size: 44px; line-height: 1.05; color: #16324A">{h1}</h1>'
            '<svg width="64" height="8" viewBox="0 0 64 8" aria-hidden="true"><path d="M2 4q4-4 8 0t8 0t8 0t8 0t8 0t8 0t8 0" fill="none" stroke="{{secondary}}" stroke-width="2.4" stroke-linecap="round"/></svg>'
            f'<div style="font-size: 14px; color: #5A6B7B">{sub}</div></div>\n')


nv = {k: b for n, k, b in NAV}
navbar = ''
for i, (n, k) in enumerate([('Dashboard', 'painel'), ('Aulas', 'aulas'), ('Calendário', 'calendario'), ('Alunos', 'alunos'), ('Ferramentas', 'ferramentas')]):
    active = i == 0
    navbar += (f'<a class="fi-card" href="#" style="display: flex; align-items: center; gap: 7px; padding: 8px 12px; border-radius: 8px; text-decoration: none; font-family: Lexend, sans-serif; font-weight: 600; font-size: 15px; color: #F2D9A0;'
               + (' background: rgba(255,255,255,.08);' if active else '') + f'">{svg(nv[k], 18)}<span style="display: flex; flex-direction: column; align-items: center">{n}{WAVE_SM if active else ""}</span></a>')
drop = ''.join(f'<a class="fi-card" href="#" style="display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; text-decoration: none; font-size: 14px; color: #16324A">{svg(nv[k], 18)}{n}</a>'
               for n, k in [('Relatórios', 'relatorios'), ('Sócios', 'socios'), ('Site público', 'site'), ('Criar conteúdo', 'conteudo'), ('Enviar e-mail', 'email'), ('Spam bloqueado', 'spam')])
BTN = "display: flex; align-items: center; gap: 8px; padding: 10px 16px; border-radius: 8px; font-family: Lexend, sans-serif; font-weight: 600; font-size: 14px;"
mock = f'''<div style="display: flex; flex-direction: column; border-radius: 18px; overflow: hidden; background: #F3F4F7; border: 1px solid #E3E7EE">
<div style="--ip: #F2D9A0; --is: #FFFFFF; --iw: #22476B; display: flex; align-items: center; gap: 16px; padding: 14px 24px; background: #22476B; border-bottom: 2px solid #F2D9A0">
<div style="width: 56px; height: 56px; flex-shrink: 0; border-radius: 50%; border: 2px dashed #F2D9A0; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #F2D9A0; text-align: center; line-height: 1.1">[logótipo]</div>
<nav aria-label="Menu principal" style="flex-grow: 1; display: flex; justify-content: flex-end; gap: 4px">{navbar}</nav>
<div class="fi-card" style="display: flex; align-items: center; gap: 8px; font-family: Lexend, sans-serif; font-weight: 600; color: #F2D9A0">{svg(nv['perfil'], 22)}Andre Moreira</div>
</div>
<div style="display: flex; gap: 24px; align-items: flex-start; padding: 22px 24px">
<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 16px">
<div style="display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; background: #1B3A56; border-radius: 14px">
<div><div style="font-family: Lexend, sans-serif; font-weight: 700; font-size: 22px; color: #FFFFFF">Olá, Andre</div><div style="font-size: 13px; color: #C9D6E3">Sáb, 3 Out</div></div>
<div style="display: flex; gap: 10px"><button class="fi-card" type="button" style="{BTN} border: 0; background: #FFFFFF; color: #16324A">{svg(nv['nova_aula'], 18)}Nova Aula</button>
<button class="fi-card" type="button" style="--ip: #FFFFFF; --is: #F2D9A0; --iw: #1B3A56; {BTN} border: 1px solid #FFFFFF; background: transparent; color: #FFFFFF">{svg(nv['todas_aulas'], 18)}Todas as aulas</button></div>
</div>
<div class="fi-card" style="display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 36px; background: #FFFFFF; border-radius: 14px; border: 1px solid #E3E7EE">{svg(nv['sem_aulas'], 56)}
<div style="font-family: Lexend, sans-serif; font-weight: 700; font-size: 16px; color: #16324A">Não há aulas agendadas</div>
<div style="font-size: 14px; color: #5A6B7B">Comece por criar uma nova aula para os seus alunos.</div>
<button type="button" style="--ip: #FFFFFF; --is: #F2D9A0; --iw: #1F4566; margin-top: 6px; {BTN} border: 0; background: #1F4566; color: #FFFFFF">{svg(nv['nova_aula'], 18)}Criar primeira aula</button></div>
</div>
<div style="width: 230px; flex-shrink: 0; display: flex; flex-direction: column; gap: 2px; padding: 8px; background: #FFFFFF; border-radius: 12px; border: 1px solid #E3E7EE"><div style="padding: 6px 12px; font-size: 12px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: #5A6B7B">Ferramentas</div>{drop}</div>
</div>
</div>
'''
main = (head('silver.andmore.pt · si-*', 'Ícones de navegação', 'Menu, ferramentas, botões e estado vazio · a onda do sublinhado como motivo · animação contínua (ou ao passar o rato, nos ajustes)')
        + mock + grid([card(n, 'si-' + k.replace('_', '-'), b) for n, k, b in NAV], 5))
surf = head('silver.andmore.pt · site público', 'Ícones de surf', 'Modalidades, aluguer e condições do mar') + grid([card(n, 'si-' + k.replace('_', '-'), b) for n, k, b in SURF], 4)
acth = head('silver.andmore.pt · ações', 'Ícones de ações', '25 ações que substituem os bi-* · mesma geometria da Dance Soul, acentos em círculo') + grid([card(n, k, b) for n, k, b in acts], 5)
pass
open('Main.dc.html', 'w').write(page('Ícones de navegação', main, 1280, 1340))
open('Surf.dc.html', 'w').write(page('Ícones de surf', surf, 1280, 820))
open('Actions.dc.html', 'w').write(page('Ícones de ações', acth, 1280, 840))
idx = 'canvas.json'
if not os.path.exists(idx):
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    json.dump({"v": 3, "createdOnFiles": {"v": 1, "at": now}, "title": "Silver Surf Icons", "launch": {"view": "canvas"}, "pages": [],
               "boards": {"Main.dc.html": {"x": 0, "y": 0, "w": 1280, "h": 1340, "title": "Ícones de navegação"},
                          "Surf.dc.html": {"x": 1360, "y": 0, "w": 1280, "h": 820, "title": "Ícones de surf"},
                          "Actions.dc.html": {"x": 1360, "y": 940, "w": 1280, "h": 840, "title": "Ícones de ações"}},
               "order": ["Main.dc.html", "Surf.dc.html", "Actions.dc.html"], "notes": {}, "designSystems": []}, open(idx, 'w'), ensure_ascii=False)
print(len(NAV), len(SURF), len(acts))
