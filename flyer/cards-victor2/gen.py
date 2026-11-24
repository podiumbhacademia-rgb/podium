# Cards do app do Victor: título + explicação curta à esquerda, print do celular à direita com o botão destacado.
import json
from pathlib import Path
D = Path(__file__).parent
BOX = json.loads((D / 'boxes.json').read_text())

CSS = '''*{margin:0;padding:0;box-sizing:border-box}
:root{--cream:#FFF3E2;--ink:#16110E;--yellow:#FFC72C}
html,body{width:540px;height:675px}
body{font-family:Montserrat,sans-serif;color:var(--cream);-webkit-font-smoothing:antialiased}
.page{position:relative;width:540px;height:675px;overflow:hidden;background:radial-gradient(ellipse 120% 70% at 50% 20%,#EE0617 0%,#D20410 55%,#A80309 100%)}
.logo{position:absolute;right:26px;top:26px;height:30px;opacity:.95}
.num{position:absolute;left:26px;top:24px;width:50px;height:50px;border-radius:50%;background:var(--yellow);color:var(--ink);display:grid;place-items:center;font-weight:900;font-size:26px}
h1{position:absolute;left:26px;right:26px;top:84px;font-weight:900;font-style:italic;text-transform:uppercase;font-size:34px;line-height:.98;text-shadow:0 3px 0 rgba(90,0,5,.3)}
ul.ex{position:absolute;left:26px;width:236px;list-style:none;display:flex;flex-direction:column;gap:13px}
ul.ex li{position:relative;padding-left:22px;font-weight:600;font-size:15.5px;line-height:1.32}
ul.ex li::before{content:"";position:absolute;left:0;top:6px;width:11px;height:11px;border-radius:50%;background:var(--yellow)}
ul.ex b{color:var(--yellow);font-weight:800}
.ph{position:absolute;right:24px;border-radius:30px;background:#0d0a09;padding:8px;box-shadow:0 18px 40px rgba(40,0,0,.5)}
.scr{position:relative;overflow:hidden;border-radius:23px}
.scr>img{display:block}
.ring{position:absolute;border:4px solid var(--yellow);border-radius:11px;box-shadow:0 0 0 5px rgba(255,199,44,.35),0 0 22px rgba(255,199,44,.85)}
.tap{position:absolute;width:52px;height:52px;filter:drop-shadow(0 4px 6px rgba(0,0,0,.45))}
.chip{display:inline-block;background:var(--ink);color:var(--cream);border-radius:999px;padding:7px 14px;font-weight:800;font-size:14px;white-space:nowrap}
.chip b{color:var(--yellow)}
'''
FINGER = '<svg class="tap" viewBox="0 0 64 64" style="{s}"><circle cx="20" cy="18" r="13" fill="rgba(255,199,44,.35)"/><path d="M20 18v22l-6-5c-3-2-7 1-5 5l11 13c2 3 5 5 9 5h11c6 0 10-5 10-10V33c0-3-2-5-5-5-2 0-3 1-4 2 0-3-2-5-5-5-2 0-3 1-4 2 0-3-2-5-5-5-2 0-3 1-3 2V18c0-3-2-5-4-5s-4 2-4 5z" fill="#FFF3E2" stroke="#16110E" stroke-width="2.5" stroke-linejoin="round"/></svg>'

def phone(img, box=None, top=186, w=228, finger=True, pad=5):
    sc = w / 390; h = round(760 * sc)
    out = f'<div class="ph" style="top:{top}px"><div class="scr" style="width:{w}px;height:{h}px"><img src="{img}" style="width:{w}px;height:{h}px" alt="">'
    if box:
        x, y, bw, bh = BOX[box]
        out += f'<div class="ring" style="left:{x*sc-pad}px;top:{y*sc-pad}px;width:{bw*sc+2*pad}px;height:{bh*sc+2*pad}px"></div>'
        if finger:
            out += FINGER.format(s=f'left:{(x+bw*0.6)*sc}px;top:{(y+bh*0.5)*sc}px')
    return out + '</div></div>'

def card(name, num, title, items, img, box=None, finger=True, ex_top=196, extra=''):
    n = f'<div class="num">{num}</div>' if num else ''
    li = ''.join(f'<li>{t}</li>' for t in items)
    html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{name}</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,600;0,700;0,800;0,900;1,900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="page"><img class="logo" src="logo.png" alt="">{n}
<h1>{title}</h1><ul class="ex" style="top:{ex_top}px">{li}</ul>{extra}{phone(img, box, finger=finger) if img else ''}</div></body></html>'''
    (D / f'{name}.html').write_text(html)

# capa
(D / 'c0.html').write_text(f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>capa</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,600;0,700;0,800;0,900;1,900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="page"><img class="logo" src="logo.png" alt="">
<h1 style="top:34px;font-size:42px">Victor,<br>seu app<br>da festa</h1>
<ul class="ex" style="top:200px;width:230px">
<li>Gerar o <b>ingresso</b> de cada pessoa e mandar no WhatsApp</li>
<li>Ver a <b>lista</b> de quem já comprou</li>
<li>Anotar quem te <b>pagou</b> e o que você <b>gastou</b></li>
<li>Ver o <b>saldo</b> da festa</li></ul>
<img src="n_ticket.png" style="position:absolute;right:22px;top:150px;width:236px;transform:rotate(4deg);border-radius:12px;box-shadow:0 18px 40px rgba(40,0,0,.55)" alt="">
<div style="position:absolute;left:26px;bottom:30px"><div class="chip">podium9anos.netlify.app<b>/caixa</b></div></div>
</div></body></html>''')

card('c1', 1, 'Como entrar', [
    'Abra o link <b>podium9anos.<br>netlify.app/caixa</b>',
    'Usuário: <b>victor</b>',
    'Senha: <b>a que eu te mandei</b>',
    'Toque em <b>Entrar</b>. Da próxima vez o celular já lembra de você'], 'n0.png', 'n0')

card('c2', 2, 'Seu menu', [
    'Tudo começa aqui. Cada botão abre uma parte do app',
    'O <b>vermelho</b> é o mais importante: gerar os ingressos',
    'Embaixo de cada botão tem um resumo (quantos nomes, quantos enviados…)',
    'Pra voltar ao menu, toque em <b>← Voltar</b>'], 'n1.png', 'n1')

card('c3', 3, 'Gerar ingresso', [
    'Aqui aparece <b>todo mundo que já pagou</b>, pelo site ou direto com você',
    'Toque em <b>Gerar ingresso</b> no nome da pessoa',
    'O app cria a <b>imagem do ingresso</b> com o nome e o QR Code dela'], 'n2.png', 'n2')

card('c4', 4, 'Mandar no WhatsApp', [
    'Toque em <b>Enviar imagem</b>',
    'Escolha o <b>WhatsApp</b> e a conversa da pessoa',
    'Se ela deixou o número, <b>Abrir conversa</b> já leva direto pra ela',
    'Na festa, ela mostra esse <b>QR Code na portaria</b>'], 'n3.png', 'n3')

card('c5', 5, 'Enviou?<br>Marca ✔', [
    'Depois de mandar, marque <b>Enviado</b>',
    'O nome sai de <b>A enviar</b> e vai pra <b>Já enviados</b>',
    'Assim você não esquece ninguém nem manda repetido',
    'A equipe vê o mesmo ✔ no celular dela'], 'n4.png', 'n4', ex_top=230)

card('c6', 6, 'Lista de nomes', [
    'Todo mundo que já está <b>confirmado</b> na festa',
    'Use a <b>busca</b> pra achar alguém rápido',
    '<b>entrou</b> = já passou pela portaria',
    'Embaixo: quem comprou no site e o pagamento ainda falta confirmar'], 'n5.png', 'n5', finger=False)

card('c7', 7, 'Registrar venda', [
    'Alguém te pagou em <b>dinheiro, Pix ou maquininha</b>?',
    'Coloque o <b>nome completo</b> de cada pessoa',
    'Escolha <b>como recebeu</b> (o valor já vem calculado)',
    'Toque em <b>Registrar venda</b>. O ingresso já aparece pra gerar'], 'n6.png', 'n6')

card('c8', 8, 'Registrar gasto', [
    'Gastou alguma coisa da festa?',
    'Escolha o tipo: <b>comida, bebida, DJ, decoração…</b>',
    'Coloque o <b>valor</b> e, se quiser, uma descrição',
    'Toque em <b>Registrar gasto</b>'], 'n7.png', 'n7')

card('c9', 9, 'Caixa da festa', [
    '<b>Saldo</b> = tudo que entrou − tudo que saiu',
    'Logo abaixo: quanto entrou, quanto saiu e quantas pessoas pagaram',
    'Rolando a tela: gastos por tipo, últimos gastos e vendas',
    'Errou? Dá pra <b>apagar</b> o gasto ou <b>cancelar</b> a venda'], 'n8.png', 'n8', finger=False)
print('ok')
