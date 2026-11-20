# Gera as 5 opções de flyer (HTML) a partir de blocos comuns.
from pathlib import Path
D = Path(__file__).parent

HEAD = '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{t}</title>
<link href="https://fonts.googleapis.com/css2?family=Titan+One&family=Montserrat:ital,wght@0,600;0,700;0,800;0,900;1,800;1,900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="base.css"><style>{css}</style></head><body><div class="page">
<img class="abs palm" src="coqueiro.svg" style="left:-70px;top:420px" alt="">
<img class="abs palm" src="coqueiro.svg" style="right:-70px;top:400px;transform:scaleX(-1)" alt="">
<img class="abs hero" src="hero.jpg" alt="">
'''
TAIL = '</div></body></html>'

ICON = {
 'grill': '<svg class="ico" viewBox="0 0 24 24"><path d="M4 11h16a8 8 0 0 1-16 0z"/><path d="M8 19l-2 3M16 19l2 3"/><path d="M9 3c1 1.5-1 2.5 0 4M13 3c1 1.5-1 2.5 0 4M17 4c.8 1.2-.8 2 0 3"/></svg>',
 'dj': '<svg class="ico" viewBox="0 0 24 24"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1v-6h3zM3 19a2 2 0 0 0 2 2h1v-6H3z"/></svg>',
 'drink': '<svg class="ico" viewBox="0 0 24 24"><path d="M8 2h8l-1 7a3 3 0 0 1-6 0z"/><path d="M12 12v8M8 22h8"/></svg>',
 'pin': '<svg class="ico" viewBox="0 0 24 24"><path d="M12 22s7-7.2 7-12.5A7 7 0 0 0 5 9.5C5 14.8 12 22 12 22z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 'cal': '<svg class="ico" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
 'phone': '<svg class="ico" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
}
QR = '<div class="qrbox" style="width:{s}px;height:{s}px"><img src="qr-dark.svg" alt="QR Code"></div>'
DECK = '<img class="abs deck" src="deck.jpg" alt="">'

def page(name, title, css, body, deck=True):
    html = HEAD.format(t=title, css=css) + body + (DECK if deck else '') + TAIL
    (D / f'{name}.html').write_text(html)

# ---------- 1 · Faixas coloridas ----------
page('op1', 'Opção 1', '''
.top{left:0;right:0;top:470px;display:flex;flex-direction:column;align-items:center;gap:12px}
.date{font-size:34px;line-height:1;text-shadow:0 3px 0 rgba(90,0,5,.35)}
.loc{background:var(--ink);color:var(--cream);border-radius:999px;padding:6px 22px;font-size:17px;letter-spacing:.12em}
.tiles{left:44px;right:44px;top:690px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.tile{border-radius:12px;padding:12px 12px 11px;color:var(--ink);display:flex;align-items:center;gap:10px;font-size:15px;line-height:1.1}
.bot{left:44px;right:44px;top:772px;display:flex;gap:18px;align-items:flex-start}
.prices{flex:1;background:var(--cream);color:var(--ink);border-radius:12px;padding:12px 16px 10px}
.prices h4{font-size:15px;color:var(--red);margin-bottom:4px}
.prices div{display:flex;justify-content:space-between;align-items:baseline;padding:5px 0;border-bottom:1px solid rgba(22,17,14,.12);font-weight:700;font-size:15px}
.prices div:last-of-type{border-bottom:0}
.prices b{font-family:"Titan One";font-weight:400;font-size:21px}
.side{display:flex;flex-direction:column;align-items:center;gap:8px}
.side .lab{font-size:13px;text-align:center;line-height:1.15}
.info{left:44px;right:230px;top:944px;text-align:left;font-size:14px}
''', '''
<div class="abs top">
  <div class="band mb">Confraternização de fim de ano</div>
  <div class="pill mx">Vendas abertas!</div>
  <div class="date mx">Domingo · 13 dez · 14h</div>
  <div class="loc mb">Boa Vista · BH</div>
</div>
<div class="abs tiles">
  <div class="tile mb" style="background:var(--yellow)">''' + ICON['grill'] + '''Churrasco + tropeiro</div>
  <div class="tile mb" style="background:var(--orange)">''' + ICON['dj'] + '''DJ a tarde toda</div>
  <div class="tile mb" style="background:var(--cream)">''' + ICON['drink'] + '''Leve sua bebida</div>
</div>
<div class="abs bot">
  <div class="prices"><h4 class="mx">Ingressos</h4>
    <div><span>Inteira</span><b>R$ 99,90</b></div>
    <div><span>De 11 a 15 anos</span><b>R$ 50,00</b></div>
    <div><span>Até 10 anos</span><b style="color:var(--red)">Não paga</b></div>
  </div>
  <div class="side">''' + QR.format(s=150) + '''<div class="lab mx">Escaneie e<br>garanta o seu</div></div>
</div>
<div class="abs info mb">Vem comemorar com a gente! · Info (31) 99622-1198</div>
''')

# ---------- 2 · Ingresso ----------
page('op2', 'Opção 2', '''
.head{left:0;right:0;top:468px;display:flex;flex-direction:column;align-items:center;gap:10px}
.ticket{left:40px;right:40px;top:592px;height:330px;background:var(--cream);color:var(--ink);border-radius:16px;display:grid;grid-template-columns:1fr 210px;box-shadow:0 10px 30px rgba(60,0,4,.35)}
.ticket::before,.ticket::after{content:"";position:absolute;right:198px;width:24px;height:24px;border-radius:50%;background:#C9030D}
.ticket::before{top:-12px}.ticket::after{bottom:-12px}
.l{padding:20px 22px;display:flex;flex-direction:column;gap:12px}
.r{border-left:3px dashed rgba(22,17,14,.22);padding:18px 16px;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center}
.date{display:flex;align-items:center;gap:14px}
.date .big{font-family:"Titan One";font-size:58px;line-height:.9;color:var(--red)}
.date .sm{font-size:16px;line-height:1.2}
.it{display:flex;align-items:center;gap:10px;font-size:16px;font-weight:700}
.it .ico{color:var(--red);width:26px;height:26px}
.pr{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:2px}
.pr div{background:var(--red);color:var(--cream);border-radius:8px;padding:7px 4px;text-align:center;font-size:11px;font-weight:700;line-height:1.2}
.pr div:first-child{background:var(--ink)}
.pr b{display:block;font-family:"Titan One";font-weight:400;font-size:17px}
.r .lab{font-size:14px;line-height:1.15}
.r .tel{font-size:12px;font-weight:700;line-height:1.3}
''', '''
<div class="abs head">
  <div class="band mb">Confraternização de fim de ano</div>
  <div class="pill mx">Vendas abertas!</div>
</div>
<div class="abs ticket">
  <div class="l">
    <div class="date"><span class="big">13 DEZ</span><span class="sm mb">Domingo<br>a partir das 14h</span></div>
    <div class="it">''' + ICON['pin'] + '''Boa Vista · Belo Horizonte</div>
    <div class="it">''' + ICON['grill'] + '''Churrasco + tropeiro</div>
    <div class="it">''' + ICON['dj'] + '''DJ e leve sua bebida favorita</div>
    <div class="pr"><div>Inteira<b>R$ 99,90</b></div><div>11 a 15 anos<b>R$ 50,00</b></div><div>Até 10 anos<b>Grátis</b></div></div>
  </div>
  <div class="r">
    <div class="lab mx" style="color:var(--red)">Escaneie e garanta seu ingresso</div>''' + QR.format(s=150) + '''
    <div class="tel">Mais informações<br>(31) 99622-1198</div>
    <div class="tel" style="color:var(--red)">Vem comemorar<br>com a gente!</div>
  </div>
</div>
''')

# ---------- 3 · Pôr do sol ----------
page('op3', 'Opção 3', '''
.page{background:linear-gradient(180deg,#D20410 0%,#D20410 42%,#EE3A12 58%,#FF7A1A 74%,#FFB02E 100%)}
.palm{opacity:.45;filter:brightness(.6)}
.top{left:0;right:0;top:470px;display:flex;flex-direction:column;align-items:center;gap:12px}
.date{font-size:36px;line-height:1;color:var(--cream);text-shadow:0 3px 0 rgba(90,0,5,.3)}
.loc{font-size:18px;letter-spacing:.14em;color:var(--cream)}
.mid{left:44px;right:44px;top:690px;display:flex;justify-content:center;gap:28px;color:var(--ink)}
.mid div{display:flex;align-items:center;gap:8px;font-size:15px}
.bot{left:44px;right:44px;top:752px;display:grid;grid-template-columns:1fr auto;gap:20px;align-items:center}
.prices{display:flex;flex-direction:column;gap:8px}
.prices div{background:rgba(255,243,226,.94);color:var(--ink);border-radius:999px;padding:8px 18px;display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:15px}
.prices b{font-family:"Titan One";font-weight:400;font-size:21px;color:var(--red)}
.qrw{display:flex;flex-direction:column;align-items:center;gap:8px;color:var(--ink)}
.qrw .lab{font-size:13px;text-align:center}
.info{left:44px;right:44px;top:938px;text-align:center;font-size:15px;color:var(--ink)}
''', '''
<div class="abs top">
  <div class="band mb">Confraternização de fim de ano</div>
  <div class="pill mx">Vendas abertas!</div>
  <div class="date mx">Domingo · 13 dez · 14h</div>
  <div class="loc mb">Boa Vista · BH</div>
</div>
<div class="abs mid mb"><div>''' + ICON['grill'] + '''Churrasco + tropeiro</div><div>''' + ICON['dj'] + '''DJ</div><div>''' + ICON['drink'] + '''Leve sua bebida</div></div>
<div class="abs bot">
  <div class="prices"><div><span>Inteira</span><b>R$ 99,90</b></div><div><span>De 11 a 15 anos</span><b>R$ 50,00</b></div><div><span>Até 10 anos</span><b>Não paga</b></div></div>
  <div class="qrw">''' + QR.format(s=158) + '''<div class="lab mx">Escaneie e garanta</div></div>
</div>
<div class="abs info mb">Vem comemorar com a gente! · Info (31) 99622-1198</div>
''')

# ---------- 4 · Painel amarelo ----------
page('op4', 'Opção 4', '''
.top{left:0;right:0;top:468px;display:flex;flex-direction:column;align-items:center;gap:10px}
.panel{left:0;right:0;top:600px;height:400px;background:var(--yellow);color:var(--ink)}
.wave{left:0;top:576px;width:794px;height:40px}
.grid{color:var(--ink);left:44px;right:44px;top:622px;display:grid;grid-template-columns:1fr 1fr;gap:26px}
.grid h4{font-size:17px;margin-bottom:8px;color:var(--red)}
.k{display:flex;align-items:center;gap:9px;font-weight:700;font-size:15px;padding:5px 0}
.k .ico{width:24px;height:24px}
.pz{display:flex;justify-content:space-between;align-items:baseline;font-weight:700;font-size:15px;padding:5px 0;border-bottom:2px solid rgba(22,17,14,.15)}
.pz:last-child{border-bottom:0}
.pz b{font-family:"Titan One";font-weight:400;font-size:21px}
.foot{color:var(--ink);left:44px;right:44px;top:812px;display:flex;align-items:center;gap:20px}
.foot .t{font-size:24px;line-height:1.05}
.foot .s{font-size:14px;font-weight:700;margin-top:8px}
''', '''
<div class="abs top">
  <div class="band mb">Confraternização de fim de ano</div>
  <div class="pill mx">Vendas abertas!</div>
</div>
<svg class="abs wave" viewBox="0 0 794 40" preserveAspectRatio="none"><path d="M0 24 C 130 4 260 40 400 22 C 540 4 660 36 794 16 L794 40 L0 40Z" fill="#FFC72C"/></svg>
<div class="abs panel"></div>
<div class="abs grid">
  <div><h4 class="mx">Quando e onde</h4>
    <div class="k">''' + ICON['cal'] + '''Domingo, 13 de dezembro, 14h</div>
    <div class="k">''' + ICON['pin'] + '''Boa Vista · Belo Horizonte</div>
    <div class="k">''' + ICON['grill'] + '''Churrasco + tropeiro</div>
    <div class="k">''' + ICON['dj'] + '''DJ · leve sua bebida</div>
  </div>
  <div><h4 class="mx">Ingressos</h4>
    <div class="pz"><span>Inteira</span><b>R$ 99,90</b></div>
    <div class="pz"><span>De 11 a 15 anos</span><b>R$ 50,00</b></div>
    <div class="pz"><span>Até 10 anos</span><b style="color:var(--red)">Não paga</b></div>
  </div>
</div>
<div class="abs foot">''' + QR.format(s=140) + '''
  <div><div class="t mx">Escaneie e garanta<br>seu ingresso</div><div class="s">Vem comemorar com a gente!<br>Mais informações · (31) 99622-1198</div></div>
</div>
''')

# ---------- 5 · Calendário ----------
page('op5', 'Opção 5', '''
.top{left:0;right:0;top:470px;display:flex;justify-content:center}
.wrap{left:44px;right:44px;top:528px;display:grid;grid-template-columns:200px 1fr;gap:22px}
.cal{background:var(--cream);color:var(--ink);border-radius:14px;overflow:hidden;text-align:center;box-shadow:0 8px 22px rgba(60,0,4,.35)}
.cal .m{background:var(--ink);color:var(--cream);font-size:22px;padding:8px 0}
.cal .d{font-family:"Titan One";font-size:96px;line-height:1;color:var(--red);padding-top:6px}
.cal .w{font-size:17px;padding:2px 0 14px}
.det{display:flex;flex-direction:column;gap:10px;justify-content:center}
.det .pill{font-size:28px;align-self:flex-start;padding:8px 26px 7px}
.det .it{display:flex;align-items:center;gap:10px;font-size:17px;font-weight:700}
.det .it .ico{color:var(--yellow)}
.bar{left:44px;right:44px;top:782px;background:var(--ink);border-radius:14px;padding:14px 16px;display:flex;align-items:center;gap:18px}
.bar .pz{flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:8px;text-align:center}
.bar .pz span{display:block;font-size:12px;font-weight:700;color:rgba(255,243,226,.8)}
.bar .pz b{font-family:"Titan One";font-weight:400;font-size:22px;color:var(--yellow)}
.bar .lab{font-size:12px;color:var(--cream);text-align:center;margin-top:6px}
.info{left:44px;right:44px;top:956px;text-align:center;font-size:15px}
''', '''
<div class="abs top"><div class="band mb">Confraternização de fim de ano</div></div>
<div class="abs wrap">
  <div class="cal"><div class="m mb">Dezembro</div><div class="d">13</div><div class="w mb">Domingo · 14h</div></div>
  <div class="det">
    <div class="pill mx">Vendas abertas!</div>
    <div class="it">''' + ICON['pin'] + '''Boa Vista · Belo Horizonte</div>
    <div class="it">''' + ICON['grill'] + '''Churrasco + tropeiro</div>
    <div class="it">''' + ICON['dj'] + '''DJ a tarde toda</div>
    <div class="it">''' + ICON['drink'] + '''Leve sua bebida favorita</div>
  </div>
</div>
<div class="abs bar">
  <div class="pz"><div><span>Inteira</span><b>R$ 99,90</b></div><div><span>11 a 15 anos</span><b>R$ 50,00</b></div><div><span>Até 10 anos</span><b>Grátis</b></div></div>
  <div>''' + QR.format(s=122) + '''<div class="lab mx">Escaneie e garanta</div></div>
</div>
<div class="abs info mb">Vem comemorar com a gente! · Info (31) 99622-1198</div>
''')
print('ok')
