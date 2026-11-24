# Gera os cards explicando o Caixa da festa para o Victor.
from pathlib import Path
D = Path(__file__).parent

CSS = '''*{margin:0;padding:0;box-sizing:border-box}
:root{--cream:#FFF3E2;--ink:#16110E;--yellow:#FFC72C;--red:#D20410}
html,body{width:540px;height:675px}
body{font-family:Montserrat,sans-serif;color:var(--cream);-webkit-font-smoothing:antialiased}
.page{position:relative;width:540px;height:675px;overflow:hidden;background:radial-gradient(ellipse 120% 70% at 50% 25%,#EE0617 0%,#D20410 55%,#A80309 100%)}
.top{position:absolute;left:34px;right:34px;top:30px;display:flex;align-items:center;justify-content:space-between}
.top img{height:34px}
.top span{font-weight:800;font-size:11px;letter-spacing:.12em;text-transform:uppercase;opacity:.8}
.num{position:absolute;left:34px;top:84px;width:44px;height:44px;border-radius:50%;background:var(--yellow);color:var(--ink);display:grid;place-items:center;font-weight:900;font-size:22px}
h1{position:absolute;left:34px;right:34px;top:136px;font-weight:900;font-style:italic;text-transform:uppercase;font-size:31px;line-height:1.02;text-shadow:0 3px 0 rgba(90,0,5,.3)}
.txt{position:absolute;left:34px;right:34px;font-weight:600;font-size:15.5px;line-height:1.4}
.txt b{color:var(--yellow);font-weight:800}
ol.txt{list-style:none;counter-reset:s;display:flex;flex-direction:column;gap:6px}
ol.txt li{counter-increment:s;display:grid;grid-template-columns:22px 1fr;gap:6px}
ol.txt li::before{content:counter(s)".";font-weight:900;color:var(--yellow)}
.phone{position:absolute;left:50%;transform:translateX(-50%);width:262px;border-radius:30px;background:#0d0a09;padding:9px;box-shadow:0 18px 40px rgba(40,0,0,.5)}
.phone img{display:block;width:100%;border-radius:22px}
.fade{position:absolute;left:0;right:0;bottom:0;height:70px;background:linear-gradient(transparent,#A80309)}
.tip{position:absolute;left:34px;right:34px;bottom:26px;background:var(--ink);border-radius:12px;padding:10px 14px;font-weight:700;font-size:13.5px;line-height:1.35;z-index:3}
.tip b{color:var(--yellow)}
'''

def card(n, name, body):
    html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Card {n}</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,600;0,700;0,800;0,900;1,900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="page">
<div class="top"><img src="logo.png" alt=""><span>Caixa da festa · 9 anos</span></div>
{body}
</div></body></html>'''
    (D / f'{name}.html').write_text(html)

def phone(img, top, crop=None):
    # crop: altura visível do print (em px do card); o resto some na borda de baixo
    style = f'top:{top}px'
    return f'<div class="phone" style="{style}"><img src="{img}" alt=""></div><div class="fade"></div>'

card(0, 'card-0', '''
<h1 style="top:96px;font-size:40px">Victor,<br>esse é o seu<br>caixa da festa</h1>
<p class="txt" style="top:262px">Aqui você registra <b>quem pagou direto pra você</b> (dinheiro, Pix ou maquininha), anota <b>todo gasto da festa</b> e vê o <b>saldo</b> na hora.</p>
''' + phone('cx1.png', 380) + '''
<div class="tip">Link: <b>podium9anos.netlify.app/caixa</b><br>O PIN é só seu. Não passe pra ninguém.</div>''')

card(1, 'card-1', '''<div class="num">1</div><h1>Como entrar</h1>
<ol class="txt" style="top:184px"><li><span>Abra o link <b>podium9anos.netlify.app/caixa</b></span></li><li><span>Digite o seu PIN e toque em <b>Entrar</b></span></li><li><span>Pronto! O celular lembra de você nas próximas vezes.</span></li></ol>
''' + phone('cx0c.png', 330) + '''
<div class="tip">Dica: salve o link na tela inicial do celular pra abrir com um toque.</div>''')

card(2, 'card-2', '''<div class="num">2</div><h1>O resumo lá em cima</h1>
<p class="txt" style="top:184px"><b>Saldo da festa</b> = tudo que entrou menos tudo que saiu.<br>Embaixo: quanto entrou, quanto saiu, quantas pessoas já pagaram e quantos pedidos do site estão esperando confirmação.</p>
''' + phone('cx1.png', 330))

card(3, 'card-3', '''<div class="num">3</div><h1>Alguém te pagou?<br>Registre a venda</h1>
<ol class="txt" style="top:218px"><li><span>Toque em <b>Entrada</b></span></li><li><span>Nome completo de cada pessoa + faixa de idade</span></li><li><span>Como recebeu: <b>dinheiro, Pix direto ou maquininha</b></span></li><li><span>Confira o valor (ele calcula sozinho) e toque em <b>Registrar venda</b></span></li></ol>
''' + phone('cx2.png', 410))

card(4, 'card-4', '''<div class="num">4</div><h1>Mande os ingressos</h1>
<p class="txt" style="top:184px">Na hora aparece o <b>QR Code de cada pessoa</b>. Se você colocou o WhatsApp, toque em <b>Mandar ingressos no WhatsApp</b> e a mensagem já vai pronta.<br>Sem WhatsApp? Toque em <b>Copiar mensagem</b> e cole onde quiser.</p>
''' + phone('cx3c.png', 368))

card(5, 'card-5', '''<div class="num">5</div><h1>Gastou com a festa?<br>Registre a saída</h1>
<ol class="txt" style="top:218px"><li><span>Toque em <b>Saída</b></span></li><li><span>Escolha o tipo: alimentação, bebida, DJ, decoração…</span></li><li><span>Coloque o valor e, se quiser, uma descrição</span></li><li><span>Confira a data, como pagou e toque em <b>Registrar gasto</b></span></li></ol>
''' + phone('cx4.png', 410))

card(6, 'card-6', '''<div class="num">6</div><h1>Acompanhe e corrija</h1>
<p class="txt" style="top:184px">Role a página pra ver os <b>gastos por categoria</b>, os <b>últimos gastos</b> e as <b>vendas</b> que você registrou.<br>Errou? Toque em <b>Apagar</b> no gasto ou <b>Cancelar</b> na venda (o QR daquela venda deixa de valer).</p>
''' + phone('cx5.png', 368))

card(7, 'card-7', '''<div class="num">+</div><h1>Pagamentos<br>feitos pelo site</h1>
<p class="txt" style="top:218px">Quem compra pelo site aparece em <b>podium9anos.netlify.app/admin</b>. O seu PIN também abre essa página.</p>
<ol class="txt" style="top:300px"><li><span>Confira no app do banco se o dinheiro caiu</span></li><li><span>Toque em <b>Confirmar pagamento</b>: os QR Codes são gerados</span></li><li><span>Toque em <b>Enviar no WhatsApp</b> pra mandar os ingressos</span></li></ol>
<div class="tip" style="bottom:auto;top:470px">Combinado: os ingressos chegam pro cliente <b>em até 24h</b> depois do pagamento.</div>
<p class="txt" style="top:560px;text-align:center;font-weight:900;font-style:italic;font-size:22px;text-transform:uppercase">Bora fazer a melhor<br>festa dos 9 anos!</p>''')
print('ok')
