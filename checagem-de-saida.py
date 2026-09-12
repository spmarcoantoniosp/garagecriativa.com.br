from playwright.sync_api import sync_playwright
import os, re, json
import pathlib
d=str(pathlib.Path(__file__).resolve().parent)+"/"
base="file://"+d
pages=["index.html","workshops.html","hub.html","cases.html","case-inrad.html","sistema.html"]
files=set(os.listdir(d))
print("=== LINKS E ÂNCORAS ===")
tot=0
for p in pages:
    html=open(d+p,encoding="utf8").read()
    hrefs=re.findall(r'href="([^"]+)"',html); ids=set(re.findall(r'id="([^"]+)"',html))
    bad=[]
    for h in hrefs:
        if h.startswith(("http","mailto:","assets/")): continue
        if h=="#": bad.append((h,"âncora vazia"))
        elif h.startswith("#"):
            if h[1:] not in ids: bad.append((h,"âncora inexistente"))
        else:
            f=h.split("#")[0]
            if f not in files: bad.append((h,"arquivo inexistente"))
            elif "#" in h:
                t=open(d+f,encoding="utf8").read()
                if h.split("#")[1] not in set(re.findall(r'id="([^"]+)"',t)): bad.append((h,"âncora inexistente no destino"))
    tot+=len(bad); print(" %-18s %3d links  %d problemas %s"%(p,len(hrefs),len(bad),sorted(set(bad)) or ""))
print("TOTAL de links quebrados:",tot)

js="""() => {
function lum(c){const m=c.match(/\\d+(\\.\\d+)?/g).map(Number);const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2])}
function bg(el){let e=el;while(e){const c=getComputedStyle(e).backgroundColor;if(c&&!c.includes('rgba(0, 0, 0, 0)'))return c;e=e.parentElement}return 'rgb(255,255,255)'}
const out=[],tt=[];
document.querySelectorAll('body *').forEach(el=>{
 if(el.children.length && ![...el.childNodes].some(n=>n.nodeType===3 && n.textContent.trim())) return;
 const t=el.textContent.trim(); if(!t) return;
 const s=getComputedStyle(el); if(s.display==='none'||s.visibility==='hidden') return;
 const fs=parseFloat(s.fontSize), fw=parseInt(s.fontWeight)||400;
 const r=(Math.max(lum(s.color),lum(bg(el)))+.05)/(Math.min(lum(s.color),lum(bg(el)))+.05);
 const min=(fs>=24||(fs>=18.66&&fw>=700))?3:4.5;
 out.push({t:t.slice(0,40),fs:Math.round(fs*10)/10,r:Math.round(r*100)/100,ok:r>=min,min,c:s.color,b:bg(el)});
});
document.querySelectorAll('a,button,input,select,textarea').forEach(el=>{
 const b=el.getBoundingClientRect(); if(b.width===0||b.height===0) return;
 if(b.height<40) tt.push({t:(el.textContent.trim()||el.tagName).slice(0,28),h:Math.round(b.height)});
});
return {n:out.length, fails:out.filter(o=>!o.ok), tiny:out.filter(o=>o.fs<13).map(o=>o.fs), tt};
}"""
print("\n=== CONTRASTE · ALVOS · ESCALA (desktop 1440) ===")
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={"width":1440,"height":900})
    gt=gf=gtt=gti=0
    for f in pages:
        pg.goto(base+f); pg.wait_for_timeout(800)
        r=pg.evaluate(js); gt+=r['n']; gf+=len(r['fails']); gtt+=len(r['tt']); gti+=len(r['tiny'])
        print(" %-18s nós %3d | falhas %d | alvos<40px %2d | texto<13px %d"%(f,r['n'],len(r['fails']),len(r['tt']),len(r['tiny'])))
        for x in r['fails'][:6]: print("      ✗",x['r'],"min",x['min'],"|",x['fs'],"px |",x['t'],"|",x['c'],"sobre",x['b'])
        for x in r['tt'][:4]: print("      ·",x['h'],"px |",x['t'])
    print(" TOTAL: %d nós, %d falhas de contraste, %d alvos pequenos, %d textos <13px"%(gt,gf,gtt,gti))
    # mobile: menu existe?
    m=b.new_page(viewport={"width":390,"height":844})
    print("\n=== MOBILE 390 ===")
    for f in ["index.html","workshops.html"]:
        m.goto(base+f); m.wait_for_timeout(600)
        vis=m.evaluate("()=>{const b=document.querySelector('.nav__burger');return b?getComputedStyle(b).display:'ausente'}")
        m.click(".nav__burger"); m.wait_for_timeout(450)
        n=m.evaluate("()=>document.querySelectorAll('#nav-panel a').length")
        h=m.evaluate("()=>document.getElementById('nav-panel').getBoundingClientRect().height")
        print(" %-16s botão:%s | links no painel:%d | altura painel:%dpx"%(f,vis,n,h))
    b.close()
