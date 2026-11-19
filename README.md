# 9 Anos de Podium · ingressos

Site de venda de ingressos da confraternização de fim de ano da Podium Academia (13/12, 14h).
Publicado em **https://podium9anos.netlify.app** (Netlify, projeto `podium9anos`).

| Painel | Endereço | Quem usa |
|---|---|---|
| Compra | `/` | alunos e convidados |
| Administração | `/admin/` | equipe (PIN admin ou do Victor) |
| Caixa do Victor | `/caixa/` | só o Victor (entradas em dinheiro e gastos da festa) |
| Portaria | `/portaria/` | quem estiver na porta (lê QR pela câmera) |
| Ingresso | `/i/?t=TOKEN` | QR individual de cada pessoa |
| Pedido | `/pedido/?id=…&k=…` | comprador acompanha o pedido |

- Os PINs ficam nas variáveis de ambiente do Netlify (`ADMIN_PIN`, `VICTOR_PIN`, `PORTARIA_PIN`), não no código.
- Dados (pedidos, ingressos, gastos, comprovantes) ficam no Netlify Blobs.
- Preços, chave Pix e links de cartão: `public/assets/app.js` (objeto `EVENT`) e `netlify/functions/api.mts` (`PRICES`).
- Flyer A4: `flyer/` (`flyer-podium-9anos-A4.pdf` para impressão).
