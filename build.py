#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GARAGE V4 — reconstrói head / cabeçalho / rodapé canônicos em todas as páginas.
O <main> de cada página é preservado; só a moldura é regerada."""
import re, io, os

SITE = "https://www.garagecriativa.com.br"
MAIL = "facilitadores@garagecriativa.com.br"
WPP  = "5511944828226"
WPP_LABEL = "(11) 94482-8226"

NAV = [
    ("Workshops",   "workshops.html",        "workshops"),
    ("Consultoria", "hub.html",              "hub"),
    ("Cases",       "cases.html",            "cases"),
    ("3 Tempos",    "index.html#formato",    None),
    ("Mentoria",    "workshops.html#mentoria", None),
    ("Loja",        "https://www.garagelab.com.br", None),
]

# A que mundo cada item pertence. O menu colore por aqui: Criativa, Hub e a
# loja (Garage Labs, outro domínio) são coisas diferentes e devem ler assim.
MUNDO = {
    "Workshops": "cri", "3 Tempos": "cri", "Mentoria": "cri",
    "Consultoria": "hub", "Cases": "hub",
    "Loja": "lab",
}

SOCIAL = [
    ("Instagram", "https://www.instagram.com/garagecriativa/",
     '<path d="M12 2.2c3.2 0 3.6 0 4.9.07 1.2.05 1.8.25 2.2.42.6.22 1 .48 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c0 1.2-.2 1.8-.4 2.2a3.7 3.7 0 0 1-.9 1.4c-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2 0-1.8-.2-2.2-.4a3.7 3.7 0 0 1-1.4-.9 3.7 3.7 0 0 1-.9-1.4c-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c0-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2Zm0 1.8c-3.1 0-3.5 0-4.8.07-1.1.05-1.7.24-2.1.4-.5.2-.9.44-1.2.78-.34.33-.57.7-.78 1.2-.16.4-.35 1-.4 2.1C2.7 9.8 2.7 10.2 2.7 12s0 2.2.07 3.5c.05 1.1.24 1.7.4 2.1.2.5.44.9.78 1.2.33.34.7.57 1.2.78.4.16 1 .35 2.1.4 1.3.07 1.7.07 4.8.07s3.5 0 4.8-.07c1.1-.05 1.7-.24 2.1-.4.5-.2.9-.44 1.2-.78.34-.33.57-.7.78-1.2.16-.4.35-1 .4-2.1.07-1.3.07-1.7.07-3.5s0-2.2-.07-3.5c-.05-1.1-.24-1.7-.4-2.1a3 3 0 0 0-.78-1.2 3 3 0 0 0-1.2-.78c-.4-.16-1-.35-2.1-.4C15.5 4 15.1 4 12 4Zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8Zm0 8a3.1 3.1 0 1 0 0-6.2 3.1 3.1 0 0 0 0 6.2Zm6.2-8.2a1.15 1.15 0 1 1-2.3 0 1.15 1.15 0 0 1 2.3 0Z"/>'),
    ("LinkedIn", "https://www.linkedin.com/company/15260165/",
     '<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3V9Zm6.5 0h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C21 8.65 22 10.9 22 14.1V21h-4v-6.1c0-1.45-.03-3.3-2-3.3-2 0-2.3 1.57-2.3 3.2V21h-4V9Z"/>'),
    ("YouTube", "https://www.youtube.com/c/GarageCriativa",
     '<path d="M21.6 7.2a2.5 2.5 0 0 0-1.76-1.77C18.25 5 12 5 12 5s-6.25 0-7.84.43A2.5 2.5 0 0 0 2.4 7.2C2 8.8 2 12 2 12s0 3.2.4 4.8a2.5 2.5 0 0 0 1.76 1.77C5.75 19 12 19 12 19s6.25 0 7.84-.43a2.5 2.5 0 0 0 1.76-1.77C22 15.2 22 12 22 12s0-3.2-.4-4.8ZM10 15.2V8.8l5.2 3.2-5.2 3.2Z"/>'),
]

HEAD_TPL = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32">
<link rel="icon" href="assets/favicon-512.png" sizes="512x512">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="{ogtype}">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Garage">
<meta property="og:image" content="{site}/assets/og-garage.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{site}/assets/og-garage.png">
{robots}<meta name="theme-color" content="#17110E">
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/cooper-hewitt-latin-700-normal.woff2" crossorigin>
<link rel="stylesheet" href="assets/garage.css">
{schema}</head>
"""

def logo(page):
    """Marca no cabeçalho. O Hub ainda não tem SVG próprio — usa lockup tipográfico."""
    if page == "hub":
        return ('<a class="nav__word" href="index.html" aria-label="Garage Hub">'
                'garage<i>hub</i></a>')
    return ('<a class="nav__logo" href="index.html" aria-label="Garage">'
            '<img src="assets/logo/gc-horizontal-negativo.svg" alt="Garage" width="158" height="44"></a>')

def header(page, cta_href):
    items_d, items_m = [], []
    for label, href, key in NAV:
        cur = ' aria-current="page"' if key and key == page else ''
        w = ' data-w="%s"' % MUNDO[label] if label in MUNDO else ''
        items_d.append('        <li><a href="%s"%s%s>%s</a></li>' % (href, w, cur, label))
        items_m.append('      <li><a href="%s"%s%s>%s</a></li>' % (href, w, cur, label))
    return """<a class="skip" href="#main">Ir para o conteúdo</a>
<div class="dusk"></div>

<header class="nav">
  <div class="wrap nav__in">
    {logo}
    <nav aria-label="Principal">
      <ul class="nav__links">
{itemsd}
      </ul>
    </nav>
    <a class="nav__cta" href="{cta}">Traga seu desafio</a>
    <button class="nav__burger" type="button" aria-expanded="false"
            aria-controls="nav-panel" aria-label="Abrir menu"><span></span></button>
  </div>
  <div class="nav__panel" id="nav-panel">
    <ul>
{itemsm}
    </ul>
    <a class="nav__panel-cta" href="{cta}">Traga seu desafio</a>
  </div>
</header>
""".format(logo=logo(page), itemsd="\n".join(items_d), itemsm="\n".join(items_m), cta=cta_href)

def footer():
    soc = "\n".join(
        '        <a href="%s" aria-label="%s" rel="noopener" target="_blank">'
        '<svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></a>' % (url, name, path)
        for name, url, path in SOCIAL)
    return """<footer class="foot">
  <div class="wrap">
    <div class="foot__grid">
      <div>
        <img src="assets/logo/gc-horizontal-negativo.svg" alt="Garage" width="180" height="40">
        <p style="color:#C3B6AD;font-weight:400;max-width:32ch;margin:0">Formação e consultoria em design de serviço. São Paulo, desde 2016.</p>
        <div class="foot__social">
{soc}
        </div>
      </div>
      <div><h5>Criativa</h5><ul>
        <li><a href="workshops.html">Onze workshops</a></li>
        <li><a href="index.html#formato">Três Tempos</a></li>
        <li><a href="workshops.html#mentoria">Mentoria</a></li>
      </ul></div>
      <div><h5>Hub</h5><ul>
        <li><a href="hub.html">Consultoria</a></li>
        <li><a href="hub.html#metodo">Método</a></li>
        <li><a href="cases.html">Cases</a></li>
      </ul></div>
      <div><h5>Contato</h5><ul>
        <li><a href="https://wa.me/{wpp}" rel="noopener" target="_blank">WhatsApp {wppl}</a></li>
        <li><a href="mailto:{mail}">{mail}</a></li>
      </ul></div>
    </div>
    <div class="foot__legal"><span>© 2026 Garage · São Paulo</span><span>garagecriativa.com.br</span></div>
  </div>
</footer>
<a class="wa" href="https://wa.me/5511944828226" target="_blank" rel="noopener noreferrer" aria-label="Falar com a Garage no WhatsApp">
  <span class="wa__t">Falar no WhatsApp</span>
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.74-.86-2.01-.96-.27-.1-.47-.15-.66.15-.2.3-.76.96-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.25-.46-2.38-1.47-.88-.78-1.47-1.75-1.65-2.05-.17-.3-.02-.46.13-.6.14-.14.3-.35.45-.53.15-.18.2-.3.3-.5.1-.2.05-.38-.02-.53-.08-.15-.66-1.6-.9-2.19-.24-.57-.48-.5-.66-.5l-.56-.01c-.2 0-.51.07-.78.37-.27.3-1.02 1-1.02 2.43s1.05 2.82 1.2 3.02c.15.2 2.06 3.15 5 4.42.7.3 1.24.48 1.67.62.7.22 1.34.19 1.84.12.56-.09 1.74-.71 1.98-1.4.25-.69.25-1.28.17-1.4-.07-.13-.27-.2-.56-.35M12.05 21.7h-.02a9.6 9.6 0 0 1-4.9-1.34l-.35-.21-3.64.96.97-3.55-.23-.36a9.58 9.58 0 0 1-1.47-5.12c0-5.3 4.32-9.6 9.63-9.6a9.56 9.56 0 0 1 6.8 2.82 9.5 9.5 0 0 1 2.82 6.79c0 5.3-4.32 9.61-9.61 9.61M20.5 3.5A11.9 11.9 0 0 0 12.05.02C5.46.02.1 5.38.1 11.97c0 2.1.55 4.16 1.6 5.98L0 24l6.2-1.63a11.93 11.93 0 0 0 5.85 1.5h.01c6.58 0 11.94-5.36 11.95-11.95a11.87 11.87 0 0 0-3.5-8.42"/></svg>
</a>
<script src="assets/motion.js" defer></script>
</body>
</html>
""".format(soc=soc, mail=MAIL, wpp=WPP, wppl=WPP_LABEL)

ORG = ('<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"Organization",'
       '"name":"Garage","url":"%s/","foundingDate":"2016","email":"%s","areaServed":"BR",'
       '"logo":"%s/assets/og-garage.png",'
       '"description":"Escola de inovação e consultoria de design de serviço.",'
       '"sameAs":["https://www.instagram.com/garagecriativa/","https://www.linkedin.com/company/15260165/","https://www.youtube.com/c/GarageCriativa"],'
       '"subOrganization":[{"@type":"Organization","name":"Garage Criativa","description":"Escola de inovação — formação in-company em design de serviço, produto e agilidade."},'
       '{"@type":"Organization","name":"Garage Hub","description":"Consultoria de design de serviço e inovação organizacional."}]}\n</script>\n') % (SITE, MAIL, SITE)

# JSON-LD específico de página. Cada bloco reproduz, byte a byte, o que já está
# publicado — mexer aqui é mexer no que o Google lê.
ROBOTS_NOINDEX = '<meta name="robots" content="noindex,nofollow">\n'

SERVICE_HUB = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","name":"Consultoria de design de servico","serviceType":"Design de servico e inovacao organizacional","provider":{"@type":"Organization","name":"Garage Hub","url":"https://www.garagecriativa.com.br/hub"},"areaServed":{"@type":"Country","name":"Brasil"},"hasOfferCatalog":{"@type":"OfferCatalog","name":"Metodo em seis etapas","itemListElement":[
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Pesquisar"}},
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Definir"}},
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Idear"}},
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Prototipar"}},
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Testar"}},
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Entregar"}}]}}
</script>
"""

COURSE_LIST = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ItemList","name":"Workshops in-company Garage Criativa","numberOfItems":11,"itemListElement":[
{"@type":"ListItem","position":1,"item":{"@type":"Course","name":"IA Design Thinking","description":"Enquadramento do problema antes do investimento.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT13H"}}},
{"@type":"ListItem","position":2,"item":{"@type":"Course","name":"Sprint Research com IA","description":"Descoberta de usuario em dias, nao em semanas.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT13H"}}},
{"@type":"ListItem","position":3,"item":{"@type":"Course","name":"IA Service Design","description":"Redesenho de servico de ponta a ponta.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT13H"}}},
{"@type":"ListItem","position":4,"item":{"@type":"Course","name":"AI Design Sprint","description":"Decisao com evidencia sobre uma aposta grande.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT21H"}}},
{"@type":"ListItem","position":5,"item":{"@type":"Course","name":"Sprint Data-Driven com IA","description":"Do dado bruto ao diagnostico acionavel.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT13H"}}},
{"@type":"ListItem","position":6,"item":{"@type":"Course","name":"Business Design com IA","description":"Modelo de negocio e viabilidade antes do capital.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT13H"}}},
{"@type":"ListItem","position":7,"item":{"@type":"Course","name":"Sprint Strategic Plan com IA","description":"Do norte a execucao, com OKR auditado.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT21H"}}},
{"@type":"ListItem","position":8,"item":{"@type":"Course","name":"Design de Futuros com IA","description":"Antecipacao de ruptura em horizonte de 3 a 10 anos.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT13H"}}},
{"@type":"ListItem","position":9,"item":{"@type":"Course","name":"Lideranca de Produtos com IA","description":"Criterio de priorizacao que sobrevive a pressao.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT13H"}}},
{"@type":"ListItem","position":10,"item":{"@type":"Course","name":"Gestao de Projetos com IA","description":"Escolha de abordagem e previsibilidade de entrega.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT13H"}}},
{"@type":"ListItem","position":11,"item":{"@type":"Course","name":"Lideranca Agil com IA","description":"Formacao e conducao de times de alta performance.","provider":{"@type":"Organization","name":"Garage Criativa"},"hasCourseInstance":{"@type":"CourseInstance","courseMode":"blended","courseWorkload":"PT13H"}}}]}
</script>
"""

PAGES = {
 "index.html": dict(page="home", brand=None, cta="#contato",
   title="Garage · Formação e consultoria em design de serviço | São Paulo",
   ogtitle="Garage · Formação e consultoria em design de serviço",
   desc="Escola de inovação e consultoria de design de serviço em São Paulo, desde 2016. Onze workshops in-company e projetos de redesenho de serviço em saúde, financeiro, imobiliário e indústria.",
   canon=SITE+"/", ogtype="website", schema=ORG),
 "workshops.html": dict(page="workshops", brand="criativa", cta="#contato",
   title="Onze workshops in-company · Garage Criativa | São Paulo",
   ogtitle="Onze workshops in-company, em quatro trilhas",
   desc="Onze workshops in-company em quatro trilhas, no formato Três Tempos: design thinking, service design, design sprint, dados, business design, futuros, produto, projetos e liderança — com IA aplicada.",
   canon=SITE+"/workshops.html", ogtype="website", schema=COURSE_LIST),
 "hub.html": dict(page="hub", brand="hub", cta="#contato",
   title="Consultoria de design de serviço · Garage Hub | São Paulo",
   ogtitle="Garage Hub · consultoria de design de serviço",
   desc="Mapeamos a jornada, localizamos onde o serviço quebra, redesenhamos o modelo operacional em service blueprint e acompanhamos a implementação com o time do cliente conduzindo.",
   canon=SITE+"/hub.html", ogtype="website", schema=SERVICE_HUB),
 "cases.html": dict(page="cases", brand="hub", cta="index.html#contato",
   title="Cases · projetos entregues | Garage",
   ogtitle="Cases · projetos entregues pela Garage",
   desc="Projetos de redesenho de serviço entregues pela Garage em saúde, imobiliário, financeiro, indústria e logística — com o desafio recebido, a condução e o que mudou depois.",
   canon=SITE+"/cases.html", ogtype="website"),
 "case-inrad.html": dict(page="cases", brand="hub", cta="index.html#contato",
   title="Jornada do paciente em tomografia e mamografia · INRAD HCFMUSP | Garage Hub",
   ogtitle="Case INRAD · HCFMUSP — jornada do paciente",
   desc="Case Garage Hub no INRAD do HCFMUSP: mapeamento da jornada do paciente em tomografia e mamografia, do agendamento à saída, com personas e pontos de oportunidade.",
   canon=SITE+"/case-inrad.html", ogtype="article"),
 "sistema.html": dict(page=None, brand=None, cta="index.html#contato",
   title="Sistema de design · Garage",
   ogtitle="Sistema de design · Garage",
   desc="Tokens, componentes, padrões e sistema de movimento do site da Garage. Documentação viva do design system.",
   canon=SITE+"/sistema.html", ogtype="website", robots=ROBOTS_NOINDEX),
}

def rebuild(fn, main_html):
    cfg = PAGES[fn]
    head = HEAD_TPL.format(title=cfg["title"], desc=cfg["desc"], canon=cfg["canon"],
                           ogtitle=cfg["ogtitle"], ogtype=cfg["ogtype"], site=SITE,
                           schema=cfg.get("schema", ""),
                           robots=cfg.get("robots", ""))
    body_attr = ' data-brand="%s"' % cfg["brand"] if cfg["brand"] else ""
    return head + "<body%s>\n" % body_attr + header(cfg["page"], cfg["cta"]) + "\n" + main_html + "\n" + footer()

def get_main(fn):
    s = io.open(fn, encoding="utf8").read()
    m = re.search(r'(<main id="main">.*?</main>)', s, re.S)
    return m.group(1)

if __name__ == "__main__":
    import sys
    for fn in sys.argv[1:]:
        out = rebuild(fn, get_main(fn))
        io.open(fn, "w", encoding="utf8").write(out)
        print("rebuilt", fn)
