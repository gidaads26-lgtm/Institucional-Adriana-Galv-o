#!/usr/bin/env python3
"""Monta index.html a partir de template.html, embutindo fotos em base64."""
import base64, io, os, re, html, json
from urllib.parse import quote
from PIL import Image, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "..", "index.html")
FOTOS = os.path.join(AQUI, "fotos")

# ===== Dados (troque aqui) =====
DOMINIO = "https://www.seudominio.com.br"   # a definir
CIDADE = "Guarulhos"
UF = "SP"
ENDERECO = []        # 3 linhas, ex.: ["Rua X, 123, sala 4", "Bairro, São Paulo, SP", "CEP 00000-000"]
FORMACAO = ""        # ex.: "Formada em Hipnoterapia Clínica pelo INSTITUTO e em Neuropsicopedagogia pela INSTITUICAO."
HERO_TITULO = 'Se a ansiedade tem tirado a sua paz, <span class="acento">você não precisa enfrentar isso sem apoio</span>'
HERO_SUB = "Vou com você até a raiz do que dói e te ajudo a levar a mudança para a sua rotina."
DEPOIMENTOS = []     # [{"nome":..., "tema":..., "texto":..., "foto":"depo1.jpg" ou None}]

def pend(txt):
    return f'<span class="pendente">{txt}</span>'

# ===== Icones (traco fino) =====
def ic(body, extra=""):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"{extra}>{body}</svg>')

ICONES = {
 "IC_WA": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5 5.15-1.35A9.9 9.9 0 1 0 12.04 2Zm0 18.1a8.2 8.2 0 0 1-4.18-1.15l-.3-.18-3.06.8.82-2.98-.2-.31a8.2 8.2 0 1 1 6.92 3.82Zm4.5-6.14c-.25-.12-1.46-.72-1.69-.8-.23-.08-.39-.12-.55.12-.16.25-.63.8-.78.97-.14.16-.29.18-.53.06a6.7 6.7 0 0 1-3.32-2.9c-.25-.43.25-.4.72-1.33.08-.16.04-.3-.02-.43-.06-.12-.55-1.33-.76-1.82-.2-.48-.4-.41-.55-.42h-.47a.9.9 0 0 0-.65.3 2.74 2.74 0 0 0-.86 2.04c0 1.2.88 2.37 1 2.53.12.16 1.73 2.64 4.2 3.7 1.56.67 2.17.73 2.95.61.47-.07 1.46-.6 1.66-1.17.2-.58.2-1.07.15-1.17-.06-.1-.22-.16-.47-.28Z"/></svg>',
 "IC_INSTA": ic('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r=".9" fill="currentColor" stroke="none"/>'),
 "IC_PINO": ic('<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.6"/>'),
 "IC_ESPIRAL": ic('<path d="M12 12.2c0-.6.5-1 1-1 .9 0 1.4.9 1.3 1.8-.2 1.4-1.6 2.2-3 2-1.9-.3-3-2.1-2.6-4 .4-2.4 2.8-3.8 5.1-3.3 2.9.6 4.6 3.5 3.9 6.4-.8 3.3-4.3 5.3-7.6 4.4C6.3 17.5 4 13.4 5 9.5 6.1 5 10.9 2.5 15.3 3.8"/>'),
 "IC_CEREBRO": ic('<path d="M9.5 4.5A2.5 2.5 0 0 0 7 7a2.6 2.6 0 0 0-2 4.3A2.8 2.8 0 0 0 6.5 16 2.6 2.6 0 0 0 9.5 19.5c1.1 0 2-.7 2.5-1.5V6c-.4-.9-1.4-1.5-2.5-1.5Z"/><path d="M14.5 4.5A2.5 2.5 0 0 1 17 7a2.6 2.6 0 0 1 2 4.3 2.8 2.8 0 0 1-1.5 4.7 2.6 2.6 0 0 1-3 3.5c-1.1 0-2-.7-2.5-1.5"/><path d="M9 9.5c1 0 1.8.5 2.2 1.3M15 9.5c-1 0-1.8.5-2.2 1.3M8.5 14c.9.2 1.8 0 2.5-.6M15.5 14c-.9.2-1.8 0-2.5-.6"/>'),
 "IC_FOLHA": ic('<path d="M5 19c0-8 5-13.5 14-14-.3 9-6 14-14 14Z"/><path d="M5 19c3-4 6-6.5 9.5-8.5"/>'),
 "IC_VENTO": ic('<path d="M3 8.5h10.5a2.5 2.5 0 1 0-2.5-2.5"/><path d="M3 12.5h15a2.5 2.5 0 1 1-2.5 2.5"/><path d="M3 16.5h7"/>'),
 "IC_RAIZ": ic('<path d="M12 3v9"/><path d="M8 6.5c1.5 0 4 1 4 3.5M16 5.5c-1.5 0-4 1.2-4 4"/><path d="M4 12h16"/><path d="M12 12c0 3-2.5 4-4.5 6.5M12 12c0 3 2.5 4 4.5 6.5M12 12v8.5"/>'),
 "IC_CORACAO": ic('<path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.1a4.3 4.3 0 0 1 7.5 2.7C19.5 15.4 12 20 12 20Z"/><path d="M8.5 11.5c.5-1 1.3-1.6 2.3-1.7"/>'),
 "IC_SOL": ic('<circle cx="12" cy="12" r="3.8"/><path d="M12 2.8v2M12 19.2v2M2.8 12h2M19.2 12h2M5.5 5.5l1.4 1.4M17.1 17.1l1.4 1.4M5.5 18.5l1.4-1.4M17.1 6.9l1.4-1.4"/>'),
 "IC_NUVEM": ic('<path d="M7 17.5h10a4 4 0 0 0 .6-8 5.5 5.5 0 0 0-10.5 1.5A3.3 3.3 0 0 0 7 17.5Z"/><path d="M12 13.5c1 .8 2 .8 3 0"/>'),
 "IC_FLECHA": '<svg viewBox="0 0 32 12" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M1 6h29M25 1l5 5-5 5"/></svg>',
 "IC_BRILHO": ic('<path d="M12 3.5l1.9 5.1 5.1 1.9-5.1 1.9L12 17.5l-1.9-5.1L5 10.5l5.1-1.9L12 3.5Z"/><path d="M18.5 15.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7.7-1.8Z"/>'),
 "IC_SETA": ic('<path d="M5 12h14M13 6l6 6-6 6"/>'),
 "IC_MAIS": ic('<path d="M12 5v14M5 12h14"/>', ' stroke-width="2"'),
}

# ===== FAQ =====
cidade_txt = CIDADE if CIDADE else None
FAQ = [
 ("A hipnose faz eu perder o controle?",
  ["Não. Na hipnose clínica você fica consciente o tempo todo, escuta a minha voz e pode abrir os olhos ou interromper a sessão quando quiser. "
   "É um estado de atenção concentrada e relaxamento, parecido com aquele momento em que um bom filme prende tanto a nossa atenção que o resto some. "
   "Nada acontece contra a sua vontade, e a hipnose só começa quando você se sentir à vontade."]),
 ("Quantas sessões eu vou precisar?",
  ["Depende do tema, da sua história e de como você responde ao processo. Na consulta de avaliação eu consigo te dar uma ideia mais clara, "
   "e vamos revendo ao longo do caminho."]),
 ("O atendimento é só online?",
  ["Não. Atendo presencialmente no consultório em " + (CIDADE if CIDADE else pend("[cidade]")) + " e também online, por videochamada. "
   "No online seguimos as mesmas etapas. Você só precisa de um lugar tranquilo, internet estável e, se possível, fones de ouvido."]),
 ("Serve para ansiedade, depressão e traumas emocionais?",
  ["Sim, são os temas que mais atendo. A hipnoterapia é um cuidado complementar: ela pode caminhar junto com o acompanhamento médico, psiquiátrico ou psicológico, mas não substitui nenhum deles. "
   "Se você usa medicação, não interrompa sem conversar com quem acompanha o seu tratamento. E, se na avaliação eu perceber que outro tipo de cuidado é mais indicado para você, eu vou te dizer."]),
 ("A consulta de avaliação já é o tratamento completo?",
  ["Não. Ela é o primeiro passo. Conversamos sobre o que trouxe você, a sua história e o que você deseja, eu explico como a hipnoterapia funciona "
   "e respondo às suas dúvidas. A partir dela, montamos o plano terapêutico em conjunto."]),
 ("Em quanto tempo eu vejo alguma mudança?",
  ["Cada pessoa tem o seu ritmo. Algumas percebem pequenas diferenças logo no começo, como dormir melhor ou reagir com mais calma, e outras precisam de mais tempo. "
   "Não existe um prazo igual para todo mundo, e eu acompanho com você cada passo."]),
]

def faq_html():
    out = []
    for q, ps in FAQ:
        corpo = "".join(f"<p>{p}</p>" for p in ps)
        out.append(f'<details><summary>{q}<span class="mais" aria-hidden="true">{ICONES["IC_MAIS"]}</span></summary><div class="resp">{corpo}</div></details>')
    return "\n      ".join(out)

# ===== Imagens =====
def placeholder_svg(rotulo, w, h):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
           f'<rect width="{w}" height="{h}" fill="#EEE4D8"/>'
           f'<rect x="24" y="24" width="{w-48}" height="{h-48}" fill="none" stroke="#B48A4E" stroke-width="3" stroke-dasharray="14 10" rx="18"/>'
           f'<text x="50%" y="48%" text-anchor="middle" font-family="Georgia,serif" font-size="{int(w/16)}" fill="#4A7A8C">{rotulo}</text>'
           f'<text x="50%" y="56%" text-anchor="middle" font-family="sans-serif" font-size="{int(w/28)}" fill="#56636B">foto a inserir</text></svg>')
    return "data:image/svg+xml," + quote(svg)

def foto(nome, rotulo, w, h, larg_max=1000, qual=78):
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG"):
        p = os.path.join(FOTOS, nome + ext)
        if os.path.exists(p):
            im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
            if im.width > larg_max:
                im = im.resize((larg_max, round(im.height * larg_max / im.width)), Image.LANCZOS)
            b = io.BytesIO(); im.save(b, "JPEG", quality=qual, optimize=True, progressive=True)
            return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode(), True
    return placeholder_svg(rotulo, w, h), False

# ===== Favicon =====
RAMINHO = ('<path d="M32 54 C31 42 33 30 31 18 C30 12 32 8 35 5" fill="none" stroke="#FFD5CA" stroke-width="2.6" stroke-linecap="round"/>'
           '<path d="M31.5 44 C25 42 20 37 18 30 C25 31 30 36 31.5 42Z M32 34 C38 31 43 26 45 19 C38 21 33 27 32 32Z M31 24 C26 22 23 17 22 12 C27 13 30 17 31 22Z" fill="#FFD5CA"/>')
FAV_SVG = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#4A7A8C"/>{RAMINHO}</svg>'

def apple_icon():
    from PIL import ImageDraw
    s = 180
    im = Image.new("RGB", (s, s), "#4A7A8C"); d = ImageDraw.Draw(im)
    k = s / 64
    # caule
    pts = [(32, 54), (31.6, 44), (32, 34), (31, 24), (31, 18), (33, 10), (35, 5)]
    d.line([(x*k, y*k) for x, y in pts], fill="#FFD5CA", width=int(2.6*k), joint="curve")
    for poly in ([(31.5,44),(25,42),(20,37),(18,30),(25,31),(30,36)],
                 [(32,34),(38,31),(43,26),(45,19),(38,21),(33,27)],
                 [(31,24),(26,22),(23,17),(22,12),(27,13),(30,17)]):
        d.polygon([(x*k, y*k) for x, y in poly], fill="#FFD5CA")
    b = io.BytesIO(); im.save(b, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

# ===== Depoimentos =====
def depos_html():
    cards = []
    for i in range(3):
        d = DEPOIMENTOS[i] if i < len(DEPOIMENTOS) else None
        if d:
            if d.get("foto"):
                src, ok = foto(os.path.splitext(d["foto"])[0], "", 200, 200, larg_max=200, qual=80)
                av = f'<span class="avatar"><img src="{src}" alt="Foto de {html.escape(d["nome"])}" loading="lazy" width="200" height="200"></span>'
            else:
                av = f'<span class="avatar" aria-hidden="true">{html.escape(d["nome"][0])}</span>'
            cards.append(f'<figure class="depo-card" style="--i:{i}"><span class="aspas" aria-hidden="true">“</span>'
                         f'<blockquote>{html.escape(d["texto"])}</blockquote>'
                         f'<footer>{av}<figcaption><strong>{html.escape(d["nome"])}</strong><small>{html.escape(d["tema"])}</small></figcaption></footer></figure>')
        else:
            cards.append(f'<figure class="depo-card a-inserir" style="--i:{i}"><span class="aspas" aria-hidden="true">“</span>'
                         f'<blockquote>A inserir: depoimento real, autorizado pela pessoa.</blockquote>'
                         f'<footer><span class="avatar" aria-hidden="true">?</span><figcaption><strong>A inserir</strong><small>Tema do atendimento</small></figcaption></footer></figure>')
    return "\n      ".join(cards)

RUA, CEP = "", ""   # ex.: "Rua X, 123, sala 4", "00000-000"
def endereco_json():
    d = {"@type": "PostalAddress", "streetAddress": RUA, "addressLocality": CIDADE,
         "addressRegion": UF, "postalCode": CEP, "addressCountry": "BR"}
    return json.dumps({k: v for k, v in d.items() if v}, ensure_ascii=False)

def main():
    t = open(os.path.join(AQUI, "template.html"), encoding="utf-8").read()
    hero, ok_h = foto("hero", "Foto da Hero", 800, 1000)
    sobre, ok_s = foto("sobre", "Foto Quem sou eu", 750, 1000)
    local, ok_l = foto("consultorio", "Foto do consultório", 1000, 750)

    cidade_uf = f"{CIDADE}/{UF}" if CIDADE else "[Cidade, UF]"
    subs = {
        "DOMINIO": DOMINIO,
        "EM_CIDADE": f" em {CIDADE}/{UF}" if CIDADE else "",
        "CIDADE": CIDADE, "UF": UF,
        "CIDADE_UF_HTML": cidade_uf if CIDADE else pend(cidade_uf),
        "CIDADE_HTML": CIDADE if CIDADE else pend("[Cidade]"),
        "ENDERECO_3L": "<br>".join(ENDERECO) if ENDERECO else pend("Rua e número a definir") + "<br>" + pend("Bairro") + f", {CIDADE}/{UF}<br>" + pend("CEP"),
        "ENDERECO_1L": ", ".join(ENDERECO) if ENDERECO else f"Consultório em {CIDADE}/{UF}",
        "FORMACAO": FORMACAO if FORMACAO else pend("[Formação: onde se formou em Hipnoterapia Clínica e em Neuropsicopedagogia]"),
        "HERO_TITULO": HERO_TITULO, "HERO_SUB": HERO_SUB,
        "IMG_HERO": hero, "IMG_SOBRE": sobre, "IMG_LOCAL": local,
        "ENDERECO_JSON": endereco_json(),
        "TINTA": foto("tinta", "", 1600, 1000, larg_max=1600, qual=78)[0],
        "FAQ": faq_html(), "DEPOIMENTOS": depos_html(),
        "FAVICON_SVG": "data:image/svg+xml," + quote(FAV_SVG), "APPLE_ICON": apple_icon(),
    }
    subs.update(ICONES)
    def rep(m):
        k = m.group(1)
        if k not in subs: raise KeyError(k)
        return subs[k]
    out = re.sub(r"%%([A-Z0-9_]+)%%", rep, t)
    open(SAIDA, "w", encoding="utf-8").write(out)
    print("ok", len(out)//1024, "KB | fotos:", dict(hero=ok_h, sobre=ok_s, consultorio=ok_l))

if __name__ == "__main__":
    main()
