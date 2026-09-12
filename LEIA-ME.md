# GARAGE · SITE V4

Direção Hora Azul, escuro dominante, com sistema de movimento.
Abra `index.html`. Abra `sistema.html` para ver as regras do sistema de design.

## Seis páginas, zero link quebrado

| Arquivo | Papel |
|---|---|
| `index.html` | Home. Única variante — a versão com imagem foi descartada. |
| `workshops.html` | Onze workshops em quatro trilhas + mentoria + formulário. |
| `hub.html` | Consultoria: cinco situações, método em seis etapas, formulário. |
| `cases.html` | Índice de cases, com estado explícito do que está publicado. |
| `case-inrad.html` | Case INRAD · HCFMUSP, em superfície clara de leitura. |
| `sistema.html` | Documentação do design system: tokens, tipografia, movimento, componentes, dívida aberta. |

## O que entrou na V4

**Bloqueantes corrigidos**
- Menu em celular: botão e painel navegável. Antes o menu simplesmente sumia abaixo de 900px.
- Formulários funcionam: validação nativa + envio por e-mail com os campos preenchidos. Provisório até haver endpoint.
- Linhas de workshop: título e descrição estavam colados. `.wcard__t` e `.wcard__d` eram `span` inline.
- Cases não publicados deixaram de fingir que são link. Viraram estado "em preparação".
- Todas as âncoras quebradas corrigidas.

**Mecânica comercial restituída**
- Bloco de contato na home, com WhatsApp e e-mail.
- Redes sociais no rodapé: Instagram, LinkedIn, YouTube.
- `og:image` 1200×630 em todas as páginas.
- `sitemap.xml` e `robots.txt`.
- Dados estruturados: Organization na home, ItemList/Course em workshops, Service no Hub, Article no case.

**Consistência**
- Um menu só, um rótulo de CTA só ("Traga seu desafio"), em todas as páginas.
- "Formações" (nomenclatura revogada) eliminado.
- Verde #8FA37E, que estava fora da paleta, removido.
- As cinco situações do Hub passaram a ter marcador único — são cinco instâncias da mesma coisa, não cinco categorias.

**Acessibilidade**
- Zero falha de contraste em 772 nós de texto verificados (antes: 3 por página).
- Piso tipográfico de 13px. Antes havia texto em 11,5px.
- Alvos de toque em 44px.

**Movimento**
- Ver `sistema.html` seção 04 e `assets/motion.js`.
- Uma direção, uma curva, uma vez só. Desligado sob `prefers-reduced-motion`.
- Sem JavaScript, o site nasce inteiramente visível: o movimento é camada, não condição de leitura.

## Pendente — depende de você

1. **SVG da marca Garage Hub.** Enquanto não existe, o cabeçalho do Hub usa lockup tipográfico, porque a página do Hub não pode assinar como Garage Criativa.
2. **Marca-mãe Garage**, se existir.
3. **Seis campos comerciais por workshop**: investimento, próxima turma, certificação, número de encontros.
4. **Endpoint de formulário.** Hoje abre o cliente de e-mail. Trocar o handler em `motion.js` (bloco 3).
5. **Quatro cases restantes**, com autorização de publicação nominal.
6. **Redirect 301** de `garagehub.com.br` para `/hub`, se o domínio ainda estiver ativo.

## Checagem de saída

```
python3 checagem-de-saida.py
```

Verifica links, âncoras, contraste em todos os nós de texto, alvos de toque, piso
tipográfico e menu em celular. Nenhuma versão sai sem passar. Foi a ausência dessa
checagem que deixou passar a regressão de contraste entre a V1.1 e a V3.

## Build

`build.py` regera head, cabeçalho e rodapé canônicos em todas as páginas a partir de
uma fonte única. O `<main>` de cada página é preservado. Rodar após editar navegação,
rodapé ou metadados:

```
python3 build.py index.html workshops.html hub.html cases.html case-inrad.html sistema.html
```


---

# V5 — prancha e fotografia

## Prancha conceitual do case INRAD
`assets/img/prancha-inrad.svg`, embutida em `case-inrad.html`. Cinco fases, sete
camadas, curva de experiência com quatro quedas nomeadas por categoria, e a
camada de indicador desenhada em branco — prevista no mapa e não instrumentada
no projeto. Gerada por `prancha.py`.

**Não entra na prancha:** nome de sistema, nome de sala, dor específica de campo
e minuto medido. A camada de tempo é largura relativa, sem número.

## Ano do case corrigido
Os mapas do projeto dizem 2020. O site dizia 2019 em quatro lugares. Corrigido.
Vale conferir a origem dos outros quatro anos da lista de cases.

## Fotografia
Cinco imagens de banco em duotone Garage (#17110E → #E8DCD0), em
`assets/img/`. Procedência completa em `assets/img/proveniencia.txt`.

| Arquivo | Onde |
|---|---|
| `cases-abertura.jpg` | banda de abertura de `cases.html` |
| `tres-tempos.jpg` | faixa Três Tempos, na home |
| `hub-metodo.jpg` | ao lado do método, em `hub.html` |
| `workshops.jpg` | antes das trilhas, em `workshops.html` |
| `case-fecho.jpg` | fecho de `case-inrad.html` |
| `textura.jpg` | selecionada, ainda sem vaga |

**Regra:** imagem de banco entra sem legenda que a atribua a um projeto da Garage.
Registro real de workshop entra separado, com legenda datada. Critério de seleção
aplicado: sem rosto identificável, sem marca ou texto legível, sobrevive ao
escurecimento.


---

# V6 — ajustes de contato e imagem

- **E-mail institucional** `facilitadores@garagecriativa.com.br` em todo o site:
  rodapé, bloco de contato, `mailto` e os dois formulários.
- **Botão flutuante de WhatsApp** fixo no canto inferior direito das seis páginas,
  com rótulo que aparece no hover. Classe `.wa`. Glifo em SVG inline, sem
  dependência externa. Na paleta do site, não no verde padrão do WhatsApp —
  para trocar, basta mudar `background` e `fill` da regra `.wa`.
- **"Sistema de design" saiu do rodapé.** A página `sistema.html` continua no
  pacote como documentação interna, sem link público.
- **Bloco de contato reescrito.** Os rótulos "Formação · Formulário de workshops"
  e "Projeto · Formulário de consultoria" viraram dois botões em linguagem de
  quem compra: "Quero capacitar meu time" e "Quero resolver um serviço que trava".
- **Faixa Três Tempos** trocada pela foto do cronômetro de facilitação, recortada
  em 3,27:1 para caber na banda sem corte, e enquadrada de modo a excluir a marca
  do fabricante visível no aparelho.


---

# Notas de publicação

- **Canonical e sitemap usam `.html`.** Funciona em qualquer hospedagem estática.
  Se o servidor for configurado para URLs limpas (`/workshops` em vez de
  `/workshops.html`), troque nos seis arquivos e no `sitemap.xml` — senão o
  canonical aponta para uma página que retorna 404.
- **`sistema.html` está com `noindex,nofollow` e fora do sitemap.** É documentação
  interna, não deve ser indexada.
- **Os formulários ainda não têm endpoint.** Hoje abrem o cliente de e-mail do
  visitante. Em celular sem app de e-mail configurado, o envio falha em silêncio
  e o lead se perde. O canal que funciona sem depender de nada é o WhatsApp.
  Para resolver: trocar o handler no bloco 3 de `assets/motion.js`.
