# Remove a sombra vermelha escura em volta das letras de "9 ANOS DE PODIUM"
# e reconstrói o fundo vermelho liso por trás, mantendo letras, X amarelos, nuvens e logo.
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from pathlib import Path

D = Path(__file__).parent
im = np.asarray(Image.open(D / 'hero.jpg').convert('RGB')).astype(np.float32) / 255
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]
mx, mn = im.max(-1), im.min(-1)
sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
val = mx

# o que fica: letras/nuvens/logo (claros e pouco saturados) e o amarelo dos X
claro = (sat < 0.40) & (val > 0.55)
amarelo = (r > 0.75) & (g > 0.55) & (b < 0.45)
fica = claro | amarelo

# região do título
roi = np.zeros((H, W), bool); roi[560:H, 200:W - 160] = True
# letras = áreas claras e sólidas (a abertura apaga a textura pontilhada das nuvens)
semente = ndi.binary_opening(claro & roi, iterations=7)
letras = ndi.binary_propagation(semente, mask=claro) & roi
nuvens = claro & ~letras
zona = (ndi.binary_dilation(letras, iterations=80) & roi
        & ~ndi.binary_dilation(fica, iterations=1)
        & ~ndi.binary_dilation(nuvens, iterations=45))

# fundo: o vermelho vivo limpo do próprio flyer (mediana dos pixels vermelhos claros fora da sombra)
valido = roi & ~zona & ~ndi.binary_dilation(fica, iterations=8) & (sat > 0.85) & (val > 0.80)
cor = np.median(im[valido], axis=0)
bg = np.broadcast_to(cor, im.shape).astype(np.float32).copy()
rng = np.random.default_rng(7)
ruido = ndi.gaussian_filter(rng.normal(0, 1, (H, W)), 0.8).astype(np.float32)
bg = bg + (ruido * 0.012)[..., None]
print('cor do fundo', (cor*255).round())

# borda suave da zona trocada
alpha = ndi.gaussian_filter(zona.astype(np.float32), 22)
alpha = np.where(ndi.binary_dilation(fica, iterations=1), 0, alpha)[..., None]
out = im * (1 - alpha) + bg * alpha

# bordinha das letras: pixels de transição (meio saturados) viram mistura creme + fundo novo
borda = ndi.binary_dilation(letras, iterations=3) & ~claro & roi
a = np.clip((0.80 - sat) / 0.45, 0, 1)[..., None]
creme = np.array([0.99, 0.955, 0.925], np.float32)
out = np.where(borda[..., None], a * creme + (1 - a) * bg, out)

Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(D / 'hero-sem-sombra.png')
print('ok', zona.sum(), letras.sum())
