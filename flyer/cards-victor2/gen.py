# Cards visuais do app do Victor: pouco texto, print grande e destaque no botão.
import json
from pathlib import Path
D = Path(__file__).parent
BOX = json.loads((D / 'boxes.json').read_text())

CSS = '''*{margin:0;padding:0;box-sizing:border-box}
:root{--cream:#FFF3E2;--ink:#16110E;--yellow:#FFC72C}
html,body{width:540px;height:675px}
body{font-family:Montserrat,sans-serif;color:var(--cream);-webkit-font-smoothing:antialiased}
.page{position:relative;width:540px;height:675px;overflow:hidden;background:radial-gradient(ellipse 120% 70% at 50% 20%,#EE0617 0%,#D20410 55%,#A80309 100%)}
.logo{position:absolute;right:28px;top:26px;height:30px;opacity:.95}
.num{position:absolute;left:28px;top:24px;width:52px;height:52px;border-radius:50%;background:var(--yellow);color:var(--ink);display:grid;place-items:center;font-weight:900;font-size:27px}
h1{position:absolute;left:28px;right:28px;top:86px;font-weight:900;font-style:italic;text-transform:uppercase;font-size:38px;line-height:.98;text-shadow:0 3px 0 rgba(90,0,5,.3)}
.ph{position:absolute;left:50%;transform:translateX(-50%);border-radius:34px;background:#0d0a09;padding:9px;box-shadow:0 20px 44px rgba(40,0,0,.5)}
.scr{position:relative;overflow:hidden;border-radius:26px}
.scr>img{display:block}
.ring{position:absolute;border:4px solid var(--yellow);border-radius:12px;box-shadow:0 0 0 6px rgba(255,199,44,.35),0 0 24px rgba(255,199,44,.8)}
.tap{position:absolute;width:62px;height:62px;filter:drop-shadow(0 4px 6px rgba(0,0,0,.45))}
.fade{position:absolute;left:0;right:0;bottom:0;height:60px;background:linear-gradient(transparent,#A80309)}
.chip{position:absolute;background:var(--ink);color:var(--cream);border-radius:999px;padding:8px 16px;font-weight:800;font-size:15px;white-space:nowrap;box-shadow:0 6px 14px rgba(40,0,0,.4)}
.chip b{color:var(--yellow)}
'''
FINGER = '<svg class="tap" viewBox="0 0 64 64" style="{s}"><circle cx="20" cy="18" r="13" fill="rgba(255,199,44,.35)"/><path d="M20 18v22l-6-5c-3-2-7 1-5 5l11 13c2 3 5 5 9 5h11c6 0 10-5 10-10V33c0-3-2-5-5-5-2 0-3 1-4 2 0-3-2-5-5-5-2 0-3 1-4 2 0-3-2-5-5-5-2 0-3 1-3 2V18c0-3-2-5-4-5s-4 2-4 5z" fill="#FFF3E2" stroke="#16110E" stroke-width="2.5" stroke-linejoin="round"/></svg>'

def phone(img, box=None, top=150, w=300, finger=True, pad=6, extra=''):
    sc = w / 390
    h = round(760 * sc)
    out = f'<div class="ph" style="top:{top}px"><div class="scr" style="width:{w}px;height:{h}px"><img src="{img}" style="width:{w}px;height:{h}px" alt="">'
    if box:
        x, y, bw, bh = BOX[box]
        out += f'<div class="ring" style="left:{x*sc-pad}px;top:{y*sc-pad}px;width:{bw*sc+2*pad}px;height:{bh*sc+2*pad}px"></div>'
        if finger:
            out += FINGER.format(s=f'left:{(x+bw*0.62)*sc}px;top:{(y+bh*0.55)*sc}px')
    out += extra + '</div></div><div class="fade"></div>'
    return out

def card(name, body, num=None):
    n = f'<div class="num">{num}</div>' if num else ''
    html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{name}</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,700;0,800;0,900;1,900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="page"><img class="logo" src="logo.png" alt="">{n}{body}</div></body></html>'''
    (D / f'{name}.html').write_text(html)

# capa: o ingresso que ele vai gerar
card('c0', '''<h1 style="top:34px;font-size:44px">Seu app<br>da festa</h1>
<img src="n_ticket.png" style="position:absolute;left:50%;top:170px;width:330px;transform:translateX(-50%) rotate(-4deg);border-radius:14px;box-shadow:0 20px 44px rgba(40,0,0,.55)" alt="">
<div class="chip" style="left:50%;transform:translateX(-50%);bottom:26px">podium9anos.netlify.app<b>/caixa</b></div>''')

card('c1', '<h1>Entrar</h1>' + phone('n0.png', 'n0', top=190) +
     '<div class="chip" style="left:28px;top:138px">usuário <b>victor</b> + sua senha</div>', 1)
card('c2', '<h1>Seu menu</h1>' + phone('n1.png', 'n1'), 2)
card('c3', '<h1>Gerar<br>ingresso</h1>' + phone('n2.png', 'n2', top=180), 3)
card('c4', '<h1>Mandar no<br>WhatsApp</h1>' + phone('n3.png', 'n3', top=180), 4)
card('c5', '<h1>Enviou?<br>Marca ✔</h1>' + phone('n4.png', 'n4', top=180, pad=5), 5)
card('c6', '<h1>Quem já<br>comprou</h1>' + phone('n5.png', 'n5', top=180, finger=False), 6)

# recebeu / gastou lado a lado
def mini(img, box, left, label, color):
    sc = 220 / 390; h = round(760 * sc); x, y, bw, bh = BOX[box]
    return f'''<div class="ph" style="top:206px;left:{left}px;transform:none;padding:7px;border-radius:26px"><div class="scr" style="width:220px;height:{h}px;border-radius:20px"><img src="{img}" style="width:220px;height:{h}px" alt="">
<div class="ring" style="left:{x*sc-4}px;top:{y*sc-4}px;width:{bw*sc+8}px;height:{bh*sc+8}px"></div></div></div>
<div class="chip" style="left:{left+117}px;transform:translateX(-50%);top:156px;background:{color};color:#16110E;font-size:18px;font-weight:900">{label}</div>'''
card('c7', '<h1 style="font-size:34px">Recebeu?<br>Gastou?</h1>' + mini('n6.png', 'n6', 28, '+ Venda', '#FFC72C') + mini('n7.png', 'n7', 278, '− Gasto', '#FFF3E2') + '<div class="fade"></div>', 7)
print('ok')
