# Gera flyer.build.html com o QR Code embutido (depois renderize para PDF com o navegador).
from pathlib import Path
d = Path(__file__).parent
(d / "flyer.build.html").write_text((d / "flyer.html").read_text().replace("QRCODE", (d / "qr.svg").read_text()))
