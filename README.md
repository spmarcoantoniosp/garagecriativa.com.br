# garagecriativa.com.br

Site da Garage Criativa, versão **V6.1**. Seis páginas estáticas, fontes e
imagens locais, sem dependência de CDN.

A documentação completa do pacote está em [LEIA-ME.md](LEIA-ME.md): o que mudou
em cada versão, o design system, a checagem de saída e as pendências.

## Verificação feita antes de publicar

| Item | Resultado |
|---|---|
| Arquivos locais referenciados e ausentes | **0** |
| Âncoras internas quebradas | **0** |
| Dependências de CDN externo | **nenhuma** |
| `sistema.html` com `noindex` e fora do sitemap | ✅ |
| Segredos nos scripts | nenhum |

## ⚠️ Este domínio NÃO é como os outros

`garagecriativa.com.br` tem **site em produção e e-mail corporativo ativos**.
A migração não é equivalente à dos domínios novos.

- **Site atual:** hospedado no **Wix** e no ar agora.
- **Nameservers:** `ns8.wixdns.net` / `ns9.wixdns.net` — o DNS é gerenciado
  **no Wix**, não na GoDaddy.
- **E-mail:** Google Workspace (MX `aspmx.l.google.com`), servido por esse
  mesmo DNS.

### O risco concreto

Trocar os nameservers do Wix para outro provedor **sem recriar os registros MX**
derruba o e-mail da empresa no mesmo instante — inclusive
`facilitadores@garagecriativa.com.br`. O e-mail não migra junto com o site;
ele vive no DNS que está sendo trocado.

Antes de qualquer mudança de DNS: exportar a zona atual do Wix inteira
(MX, TXT, CNAME de verificação do Google) e recriar tudo no destino.

### Lacuna encontrada

O domínio **não tem registro SPF**, apesar de enviar e-mail por Google
Workspace. Isso prejudica entregabilidade e facilita falsificação do domínio.
Corrigir é um registro TXT:

```
v=spf1 include:_spf.google.com ~all
```

## Pendência que afeta vendas

Os formulários **não têm endpoint**: abrem o cliente de e-mail do visitante.
Em celular sem app de e-mail configurado, o envio falha em silêncio e o
contato se perde. O LEIA-ME já registra isso. O canal que funciona hoje sem
depender de nada é o botão de WhatsApp.

Para resolver: trocar o handler no bloco 3 de `assets/motion.js`.

## URLs com `.html`

Canonical e `sitemap.xml` usam a extensão (`/workshops.html`), o que funciona
no GitHub Pages sem configuração. Não trocar para URLs limpas sem ajustar os
seis arquivos e o sitemap juntos.

## Ferramentas no repositório

`build.py`, `prancha.py` e `checagem-de-saida.py` são utilitários de
desenvolvimento e ficam versionados junto. Rodam a partir da raiz do projeto;
mover de lugar quebra os comandos documentados no LEIA-ME.
