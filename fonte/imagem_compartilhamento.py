#!/usr/bin/env python3
"""Gera a imagem de compartilhamento 1200x630 do site."""
import asyncio, base64, sys
from playwright.async_api import async_playwright

import os
AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "..", "og-image.jpg")
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
img, tin = b64(os.path.join(AQUI, "fotos", "hero.jpg")), b64(os.path.join(AQUI, "fotos", "tinta.jpg"))

HTML = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box}}
body{{margin:0;width:1200px;height:630px;background:#F7F1EA;font-family:"Jost",sans-serif;color:#22323A;position:relative;overflow:hidden}}
/* faixa de tinta na direita, por tras da foto */
.tinta{{position:absolute;right:0;top:0;bottom:0;width:330px;background:url(data:image/jpeg;base64,{tin}) 30% 50%/cover;border-radius:44px 0 0 44px}}
.tinta::after{{content:"";position:absolute;inset:0;border-radius:inherit;background:rgba(21,42,51,.42)}}
.foto{{position:absolute;left:640px;top:54px;width:420px;height:522px}}
.foto::before{{content:"";position:absolute;inset:0;border:1.5px solid #B08A3E;border-radius:40px;transform:translate(-18px,18px)}}
.foto div{{position:absolute;inset:0;border-radius:40px;overflow:hidden;box-shadow:0 34px 60px -30px rgba(21,42,51,.65)}}
.foto img{{width:100%;height:100%;object-fit:cover;object-position:52% 18%}}
.txt{{position:absolute;left:72px;top:64px;width:530px}}
.sobre{{display:flex;align-items:center;gap:14px;font-size:15px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;color:#3D6878}}
.sobre::before{{content:"";width:36px;height:1px;background:#B08A3E}}
h1{{font-family:"Newsreader",serif;font-weight:300;font-size:92px;line-height:.98;letter-spacing:-.02em;margin:26px 0 0}}
h1 i{{color:#4A7A8C;font-weight:300}}
.frase{{font-family:"Newsreader",serif;font-style:italic;font-weight:300;font-size:29px;line-height:1.3;color:#1D3742;margin-top:28px;max-width:500px}}
.rodape{{position:absolute;left:72px;bottom:58px;display:flex;align-items:center;gap:22px}}
.selo{{display:flex;align-items:center;gap:12px;background:#4A7A8C;color:#fff;font-weight:500;font-size:16px;letter-spacing:.16em;text-transform:uppercase;padding:17px 28px;border-radius:999px}}
.selo svg{{width:22px;height:22px}}
.local{{font-size:17px;color:#56636A;line-height:1.35}}
.local b{{display:block;font-weight:500;color:#22323A;letter-spacing:.04em}}
</style></head><body>
<div class="tinta"></div>
<div class="foto"><div><img src="data:image/jpeg;base64,{img}"></div></div>
<div class="txt">
  <div class="sobre">Hipnoterapeuta Clínica</div>
  <h1>Adriana<br><i>Galvão</i></h1>
  <div class="frase">Se a ansiedade tem tirado a sua paz, você não precisa enfrentar isso sem apoio.</div>
</div>
<div class="rodape">
  <div class="selo"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5 5.15-1.35A9.9 9.9 0 1 0 12.04 2Zm0 18.1a8.2 8.2 0 0 1-4.18-1.15l-.3-.18-3.06.8.82-2.98-.2-.31a8.2 8.2 0 1 1 6.92 3.82Zm4.5-6.14c-.25-.12-1.46-.72-1.69-.8-.23-.08-.39-.12-.55.12-.16.25-.63.8-.78.97-.14.16-.29.18-.53.06a6.7 6.7 0 0 1-3.32-2.9c-.25-.43.25-.4.72-1.33.08-.16.04-.3-.02-.43-.06-.12-.55-1.33-.76-1.82-.2-.48-.4-.41-.55-.42h-.47a.9.9 0 0 0-.65.3 2.74 2.74 0 0 0-.86 2.04c0 1.2.88 2.37 1 2.53.12.16 1.73 2.64 4.2 3.7 1.56.67 2.17.73 2.95.61.47-.07 1.46-.6 1.66-1.17.2-.58.2-1.07.15-1.17-.06-.1-.22-.16-.47-.28Z"/></svg>Agende pelo WhatsApp</div>
  <div class="local"><b>Guarulhos/SP</b>Presencial e online</div>
</div>
</body></html>'''

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        await pg.set_content(HTML); await pg.wait_for_timeout(400)
        await pg.screenshot(path=os.path.join(AQUI, "og-tmp.png"))
        await b.close()
asyncio.run(main())
from PIL import Image
im = Image.open(os.path.join(AQUI, "og-tmp.png")).convert("RGB")
im.save(OUT, quality=88, optimize=True, progressive=True)
os.remove(os.path.join(AQUI, "og-tmp.png"))
# simula o recorte quadrado da miniatura do WhatsApp
print(os.path.abspath(OUT))
