#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRANCHA 01 · JORNADA DO PACIENTE — case INRAD · HCFMUSP
Esquema conceitual autoral. Representa a estrutura do trabalho e os pontos
de decisão. Não reproduz o mapa entregue ao cliente.

Regras de cor (uma família neutra + duas cores semânticas):
  grafite  -> estrutura, passo, sistema, retaguarda
  tijolo   -> dor e queda da curva de experiência
  âmbar    -> tempo e espera
Nenhum nome de sistema, sala ou dor específica do cliente.
Nenhum número de duração: a camada de tempo é largura relativa.
"""
import io

# ---------------------------------------------------------------- paleta
INK      = "#17110E"
INK2     = "#4A3F38"
DIM      = "#6B5C51"
PAPER    = "#F5F1ED"
SURF     = "#EFEAE3"
RULE     = "#DFD7CE"
RULE2    = "#C9BFB3"
BRICK    = "#9C5233"
BRICK_L  = "#C4785A"
AMBER    = "#E0A64A"
AMBER_D  = "#8A5C12"

SANS = "Cooper Hewitt, system-ui, -apple-system, sans-serif"
MONO = "Plex Mono, ui-monospace, Menlo, monospace"

W, H = 1240, 818
L    = 208            # coluna de rótulos
R    = 1204           # borda direita da malha
CW   = (R - L) / 5.0  # largura de fase

# ------------------------------------------------------- dados da jornada
# Contagens abstraídas da estrutura observada nas duas jornadas.
FASES = [
    dict(n="01", nome="Atração",    sub="convocação",
         passos=1, contato=1, retag=1, sist=1, tempo=.34, mais=False),
    dict(n="02", nome="Onboarding", sub="chegada e ficha",
         passos=4, contato=3, retag=4, sist=3, tempo=1.0, mais=False),
    dict(n="03", nome="Preparo",    sub="avaliação",
         passos=4, contato=3, retag=5, sist=2, tempo=.88, mais=True),
    dict(n="04", nome="Exame",      sub="execução",
         passos=3, contato=3, retag=4, sist=2, tempo=.74, mais=False),
    dict(n="05", nome="Saída",      sub="liberação",
         passos=2, contato=2, retag=2, sist=0, tempo=.30, mais=True),
]
ESTADOS = ["contato", "uso", "erro", "desist."]

# curva de experiência: (x relativo 0-5, profundidade 0 topo .. 1 fundo)
CURVA = [(0.00,.30),(0.42,.26),(0.78,.62),(1.10,.46),(1.52,.78),(1.88,.58),
         (2.20,.44),(2.55,.86),(2.90,.66),(3.20,.52),(3.58,.80),(3.92,.60),
         (4.22,.48),(4.58,.88),(4.92,.70),(5.00,.72)]
# quedas nomeadas por categoria (vocabulário genérico de service design)
QUEDAS = [(0.78,.62,"sem confirmação"),
          (1.52,.78,"espera sem informação"),
          (2.55,.86,"orientação ausente"),
          (4.58,.88,"saída sem próximo passo")]

# ------------------------------------------------------------ utilidades
o = []
def a(s): o.append(s)

def txt(x, y, s, size=12, fill=INK2, font=MONO, weight=500,
        anchor="start", ls=".09em", op=None):
    extra = ' opacity="%s"' % op if op else ""
    a('<text x="%.1f" y="%.1f" fill="%s" font-family="%s" font-size="%s" '
      'font-weight="%s" letter-spacing="%s" text-anchor="%s"%s>%s</text>'
      % (x, y, fill, font, size, weight, ls, anchor, extra, s))

def line(x1, y1, x2, y2, stroke=RULE, w=1, dash=None, cap="butt"):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    a('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
      'stroke-width="%s" stroke-linecap="%s"%s/>' % (x1, y1, x2, y2, stroke, w, cap, d))

def rect(x, y, w, h, fill="none", stroke=None, sw=1, dash=None, rx=0):
    s = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    a('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s"%s%s/>'
      % (x, y, w, h, rx, fill, s, d))

def dot(x, y, r=4.2, fill=INK):
    a('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (x, y, r, fill))

def ring(x, y, r=6, stroke=INK, sw=1.8, fill=PAPER):
    a('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
      % (x, y, r, fill, stroke, sw))

def sq(x, y, s=8, fill=INK2):
    a('<rect x="%.1f" y="%.1f" width="%s" height="%s" fill="%s"/>'
      % (x - s/2, y - s/2, s, s, fill))

def spread(i, n, pad=34):
    """n marcas distribuídas dentro da fase i"""
    x0 = L + i*CW + pad
    x1 = L + (i+1)*CW - pad
    if n <= 0:  return []
    if n == 1:  return [(x0 + x1)/2]
    step = (x1 - x0) / (n - 1)
    return [x0 + k*step for k in range(n)]

def rowlabel(y, s, sub=None):
    txt(24, y, s, 12.5, INK2, MONO, 700, "start", ".14em")
    if sub:
        txt(24, y + 15, sub, 12, DIM, MONO, 400, "start", ".08em")

# ================================================================== faixas
Y_HEAD   = 96     # cabeçalho das fases
Y_STATE  = 138    # estados
Y_PASSO  = 196
Y_CONT   = 254
Y_VIS    = 292
Y_RETAG  = 336
Y_SIST   = 394
Y_CURV0  = 434    # topo da faixa de curva
Y_CURVH  = 104    # altura da faixa
Y_TEMPO  = 584
Y_IND    = 638
Y_LEG    = 698

a('<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" '
  'aria-labelledby="pr-t pr-d" width="100%%">' % (W, H))
a('<title id="pr-t">Prancha conceitual da jornada do paciente em exames de imagem</title>')
a('<desc id="pr-d">Esquema autoral em cinco fases e sete camadas: passo de ação, '
  'ponto de contato, linha de visibilidade, retaguarda, sistema, curva de '
  'experiência, tempo observado e a camada de indicador prevista e não '
  'instrumentada. Não reproduz o artefato entregue ao cliente.</desc>')

# fundo
rect(0, 0, W, H, PAPER)
rect(0, 0, W, 56, INK)
txt(24, 34, "PRANCHA 01 · JORNADA DO PACIENTE · CINCO FASES, SETE CAMADAS",
    13, PAPER, MONO, 500, "start", ".15em")
txt(R, 34, "ESQUEMA CONCEITUAL AUTORAL", 12, "#A2938A", MONO, 400, "end", ".15em")

# ---------------------------------------------------------- cabeçalho fase
for i, f in enumerate(FASES):
    x = L + i*CW
    if i:  line(x, 72, x, Y_IND + 30, RULE, 1)
    txt(x + 22, Y_HEAD - 26, f["n"], 12.5, BRICK, MONO, 700, "start", ".16em")
    txt(x + 22, Y_HEAD, f["nome"], 22, INK, SANS, 700, "start", "-.02em")
    txt(x + 22, Y_HEAD + 19, f["sub"], 13, DIM, MONO, 400, "start", ".05em")
line(L, 72, R, 72, INK, 2)
line(L, Y_IND + 30, R, Y_IND + 30, RULE2, 1)

# quatro estados por fase
for i in range(5):
    for k, e in enumerate(ESTADOS):
        x = L + i*CW + 30 + k*((CW - 66) / 3.0)
        line(x, Y_STATE - 8, x, Y_STATE - 2, RULE2, 1.4)
        txt(x, Y_STATE + 8, e, 10.5, DIM, MONO, 400, "middle", ".02em")
rowlabel(Y_STATE + 2, "ESTADOS", "por fase")

# --------------------------------------------------------- passo de ação
rowlabel(Y_PASSO + 4, "PASSO DE AÇÃO", "o que a pessoa faz")
for i, f in enumerate(FASES):
    for x in spread(i, f["passos"]):
        dot(x, Y_PASSO)

# ------------------------------------------------------- ponto de contato
rowlabel(Y_CONT + 4, "PONTO DE CONTATO", "onde o serviço aparece")
line(L + 18, Y_CONT, R - 18, Y_CONT, INK, 1.4)
for i, f in enumerate(FASES):
    for x in spread(i, f["contato"]):
        ring(x, Y_CONT)

# --------------------------------------------------- linha de visibilidade
line(L, Y_VIS, R, Y_VIS, BRICK, 1.6, dash="9 7")
txt(24, Y_VIS + 4, "VISIBILIDADE", 12.5, BRICK, MONO, 700, "start", ".14em")
txt(R, Y_VIS - 9, "acima, o que a pessoa vê", 12, DIM, MONO, 400, "end", ".05em")
txt(R, Y_VIS + 19, "abaixo, o que a operação faz", 12, DIM, MONO, 400, "end", ".05em")

# ------------------------------------------------------------- retaguarda
rowlabel(Y_RETAG + 4, "RETAGUARDA", "passo não automatizado")
for i, f in enumerate(FASES):
    for x in spread(i, f["retag"]):
        a('<circle cx="%.1f" cy="%.1f" r="4.2" fill="%s" fill-opacity="1"/>'
          % (x, Y_RETAG, INK2))

# ----------------------------------------------------------------- sistema
rowlabel(Y_SIST + 4, "SISTEMA", "registro em sistema")
for i, f in enumerate(FASES):
    if f["sist"] == 0:
        x = L + i*CW + CW/2
        txt(x, Y_SIST + 4, "—", 14, RULE2, MONO, 400, "middle", "0")
    for x in spread(i, f["sist"]):
        sq(x, Y_SIST)

# -------------------------------------------------------- curva de exp.
rect(L, Y_CURV0, R - L, Y_CURVH, SURF)
rowlabel(Y_CURV0 + 30, "CURVA DE", "EXPERIÊNCIA")
def cx(v):  return L + (v/5.0) * (R - L)
def cy(v):  return Y_CURV0 + 20 + v * (Y_CURVH - 46)
pts = " ".join("%.1f,%.1f" % (cx(x), cy(y)) for x, y in CURVA)
a('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4" '
  'stroke-linejoin="round" stroke-linecap="round"/>' % (pts, BRICK))
line(L, cy(.30), R, cy(.30), RULE2, 1, dash="3 5")
txt(R - 8, cy(.30) - 8, "referência de entrada", 11.5, DIM, MONO, 400, "end", ".05em")
for x, y, lab in QUEDAS:
    dot(cx(x), cy(y), 5, BRICK)
    a('<circle cx="%.1f" cy="%.1f" r="9" fill="none" stroke="%s" '
      'stroke-width="1" stroke-opacity=".5"/>' % (cx(x), cy(y), BRICK))
    lx = min(max(cx(x), L + 80), R - 104)
    txt(lx, cy(y) + 27, lab, 11.5, BRICK, MONO, 500, "middle", ".03em")

# ---------------------------------------------------------------- tempo
rowlabel(Y_TEMPO + 2, "TEMPO OBSERVADO", "largura relativa")
BARH = 14
for i, f in enumerate(FASES):
    x0 = L + i*CW + 22
    full = CW - 44
    line(x0, Y_TEMPO, x0 + full, Y_TEMPO, RULE, 1, dash="2 4")
    rect(x0, Y_TEMPO - BARH/2, full * f["tempo"], BARH, AMBER, AMBER_D, 1)

# ------------------------------------------------------------- indicador
rowlabel(Y_IND + 2, "INDICADOR", "camada prevista")
for i in range(5):
    x0 = L + i*CW + 22
    rect(x0, Y_IND - 11, CW - 44, 22, "none", RULE2, 1, dash="4 5")
_nt = "camada prevista no mapa e não instrumentada no projeto"
rect(L + (R-L)/2 - 210, Y_IND - 9, 420, 18, PAPER)
txt(L + (R-L)/2, Y_IND + 4, _nt, 12, DIM, MONO, 400, "middle", ".05em")

# --------------------------------------- marca das etapas extras (tomografia)
for i, f in enumerate(FASES):
    if not f["mais"]:  continue
    x = L + i*CW + 58
    a('<circle cx="%.1f" cy="%.1f" r="8.5" fill="%s"/>' % (x, Y_HEAD - 30, BRICK))
    txt(x, Y_HEAD - 26, "+", 13, PAPER, SANS, 700, "middle", "0")

# ---------------------------------------------------------------- legenda
line(0, Y_LEG - 26, W, Y_LEG - 26, RULE, 1)
lg = [("dot",  "passo de ação", 0),
      ("ring", "ponto de contato", 0),
      ("dotg", "passo de retaguarda", 0),
      ("sq",   "registro em sistema", 0),
      ("bar",  "tempo relativo", 1),
      ("brick","queda de experiência", 1),
      ("plus", "etapa a mais na tomografia", 1)]
xs = {0: 24, 1: 24}
for kind, lab, rowi in lg:
    x = xs[rowi]
    Y_LEG_R = Y_LEG + rowi * 26
    if   kind == "dot":   dot(x + 6, Y_LEG_R)
    elif kind == "ring":  ring(x + 6, Y_LEG_R, 5.4)
    elif kind == "dotg":  dot(x + 6, Y_LEG_R, 4.2, INK2)
    elif kind == "sq":    sq(x + 6, Y_LEG_R)
    elif kind == "bar":   rect(x, Y_LEG_R - 5, 20, 10, AMBER, AMBER_D, 1)
    elif kind == "brick": dot(x + 6, Y_LEG_R, 5, BRICK)
    elif kind == "plus":
        a('<circle cx="%.1f" cy="%.1f" r="7.5" fill="%s"/>' % (x + 6, Y_LEG_R, BRICK))
        txt(x + 6, Y_LEG_R + 4, "+", 12, PAPER, SANS, 700, "middle", "0")
    txt(x + (26 if kind == "bar" else 20), Y_LEG_R + 4, lab, 11.5, INK2,
        MONO, 400, "start", ".04em")
    xs[rowi] = x + 24 + len(lab) * 6.6 + 28

# ------------------------------------------------------------------ nota
txt(24, H - 26,
    "Esquema conceitual autoral. Representa a estrutura do trabalho e os pontos de "
    "decisão; não reproduz o mapa entregue ao cliente.",
    12, DIM, MONO, 400, "start", ".03em")
txt(R, H - 26, "INRAD · HCFMUSP · 2020", 12, DIM, MONO, 500, "end", ".12em")

a('</svg>')

svg = "\n".join(o)
io.open("assets/img/prancha-inrad.svg", "w", encoding="utf8").write(svg)
print("ok — %d bytes" % len(svg))
