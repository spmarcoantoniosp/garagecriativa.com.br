# Zona para recriar no Registro.br · garagecriativa.com.br

Gerado em 2026-09-12 09:53 -03 a partir do que está publicado no Wix,
já **sem** os registros mortos (SendGrid, criaenvio, RD Station, subdomínios Wix).

Total: **14 registros**.

---

## A · site (4 registros) — **campo Nome VAZIO**

| Nome | Valor |
|---|---|
| *(vazio)* | 185.199.108.153 |
| *(vazio)* | 185.199.109.153 |
| *(vazio)* | 185.199.110.153 |
| *(vazio)* | 185.199.111.153 |

## CNAME · www (1)

| Nome | Valor |
|---|---|
| www | spmarcoantoniosp.github.io. |

## MX · e-mail Google Workspace (5) — **campo Nome VAZIO** · os mais críticos

| Nome | Prioridade | Valor |
|---|---|---|
| *(vazio)* | 1 | aspmx.l.google.com. |
| *(vazio)* | 5 | alt1.aspmx.l.google.com. |
| *(vazio)* | 5 | alt2.aspmx.l.google.com. |
| *(vazio)* | 10 | alt3.aspmx.l.google.com. |
| *(vazio)* | 10 | alt4.aspmx.l.google.com. |

## TXT (4)

**SPF** — campo Nome **vazio**
```
v=spf1 include:_spf.google.com ~all
```

**Verificação do Google** — campo Nome **vazio**
```
google-site-verification=aLA3BZbg3nDxK_LRfG0ck5WKBSI3vDvm5ydTrgDnroM
```

**DMARC** — nome `_dmarc`
```
v=DMARC1; p=none; rua=mailto:dmarc@garagecriativa.com.br; fo=1
```

**DKIM** — nome `google._domainkey`
```
v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA19fQq2pecfieIhTSDp/qa0ElhQ2xK8xBOcXy1ZY6q8oeRzrF7ZTrhxmUpcYu1frCOeCmhs6BqPw4AJdXVNY/mz2UbYB6/bAqNEARrVnpOXXZ7pn+s7BX1nYpQS9ZFVl5SkiOOywKkUgV3tpBj199nP5x3v+P67kiTmVHOUT6Tt2oS2junQ1yqTVWn8VemVZtORcBaV7OfvkExwR2Ek0k9cw7GIB5Qr/mTuw969bHQbJgQbi7OHjb2eSbanMIcb1NShDdzCOSEUfAp8Pb0v/fRot9nLPEuJWJPi37rcxV20xd9ePN7P3EeK7jTnNXQMrGp2M5DqXQZwa+Ghx+/FthDwIDAQAB
```

---

## Formato de arquivo de zona

Se o painel aceitar colar zona pronta:

```
@                    IN  A     185.199.108.153
@                    IN  A     185.199.109.153
@                    IN  A     185.199.110.153
@                    IN  A     185.199.111.153
www                  IN  CNAME spmarcoantoniosp.github.io.
@                    IN  MX    1  aspmx.l.google.com.
@                    IN  MX    5  alt1.aspmx.l.google.com.
@                    IN  MX    5  alt2.aspmx.l.google.com.
@                    IN  MX    10 alt3.aspmx.l.google.com.
@                    IN  MX    10 alt4.aspmx.l.google.com.
@                    IN  TXT   "v=spf1 include:_spf.google.com ~all"
@                    IN  TXT   "google-site-verification=aLA3BZbg3nDxK_LRfG0ck5WKBSI3vDvm5ydTrgDnroM"
_dmarc               IN  TXT   "v=DMARC1; p=none; rua=mailto:dmarc@garagecriativa.com.br; fo=1"
google._domainkey    IN  TXT   "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA19fQq2pecfieIhTSDp/qa0ElhQ2xK8xBOcXy1ZY6q8oeRzrF7ZTrhxmUpcYu1frCOeCmhs6BqPw4AJdXVNY/mz2UbYB6/bAqNEARrVnpOXXZ7pn+s7BX1nYpQS9ZFVl5SkiOOywKkUgV3tpBj199nP5x3v+P67kiTmVHOUT6Tt2oS2junQ1yqTVWn8VemVZtORcBaV7OfvkExwR2Ek0k9cw7GIB5Qr/mTuw969bHQbJgQbi7OHjb2eSbanMIcb1NShDdzCOSEUfAp8Pb0v/fRot9nLPEuJWJPi37rcxV20xd9ePN7P3EeK7jTnNXQMrGp2M5DqXQZwa+Ghx+/FthDwIDAQAB"
```

---

## ⚠️ No painel do Registro.br

O campo **Nome** da raiz fica **em branco** — não aceita `@`, nem aspas, nem o
nome do domínio. Só `www`, `_dmarc` e `google._domainkey` levam texto.

Valores de TXT: cole **sem aspas**.

## Ordem segura

1. Criar os 14 registros no Registro.br **com a delegação ainda no Wix**
2. Conferir consultando os servidores do Registro.br diretamente
3. **Só então** trocar os nameservers
4. Acompanhar o e-mail por 48h antes de cancelar o Wix
