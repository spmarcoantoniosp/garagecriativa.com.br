# Snapshot da zona DNS · garagecriativa.com.br

Capturado de `ns8.wixdns.net` em 2026-09-12 04:11 -03, **antes** de qualquer
alteração. Serve para reconstruir a zona caso os nameservers sejam trocados.

```
; apex
    
; <<>> DiG 9.10.6 <<>>
; (1 server found) 
;; global options: +cmd 
garagecriativa.com.br. 3600 IN A 185.230.63.171
garagecriativa.com.br. 3600 IN A 185.230.63.107
garagecriativa.com.br. 3600 IN A 185.230.63.186
; www
    
; <<>> DiG 9.10.6 <<>>
; (1 server found) 
;; global options: +cmd 
www.garagecriativa.com.br. 3600 IN CNAME cdn3.wixdns.net.
; MX — e-mail Google Workspace
     
; (1 server found)  
; <<>> DiG 9.10.6 <<>> @ns8.wixdns.net
;; global options: +cmd  
garagecriativa.com.br. 3600 IN MX 1 aspmx.l.google.com.
garagecriativa.com.br. 3600 IN MX 5 alt1.aspmx.l.google.com.
garagecriativa.com.br. 3600 IN MX 5 alt2.aspmx.l.google.com.
garagecriativa.com.br. 3600 IN MX 10 alt3.aspmx.l.google.com.
garagecriativa.com.br. 3600 IN MX 10 alt4.aspmx.l.google.com.
; TXT

; <<>> DiG 9.10.6 <<>> @ns8.wixdns.net garagecriativa.com.br TXT +noall +answer
; (1 server found)
;; global options: +cmd
garagecriativa.com.br.	TXT	"google-site-verification=aLA3BZbg3nDxK_LRfG0ck5WKBSI3vDvm5ydTrgDnroM"
; _dmarc

; <<>> DiG 9.10.6 <<>> @ns8.wixdns.net _dmarc.garagecriativa.com.br TXT +noall +answer
; (1 server found)
;; global options: +cmd
_dmarc.garagecriativa.com.br. 3600 IN
_dmarc.garagecriativa.com.br. 3600 IN
_dmarc.garagecriativa.com.br. 3600 IN
```
