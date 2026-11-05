"""Check that quotes occur verbatim (whitespace/quote-mark normalised) on pages. Usage: python3 -I quotecheck.py <tsv url<TAB>quote>"""
import sys,urllib.request,re,html,unicodedata
cache={}
def norm(s):
    s=unicodedata.normalize('NFKC',s).replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('—','-').replace('–','-')
    return ' '.join(s.split()).lower()
for line in open(sys.argv[1]):
    if not line.strip(): continue
    u,q=line.rstrip('\n').split('\t')
    if u not in cache:
        try:
            req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (research quote check)'})
            t=urllib.request.urlopen(req,timeout=60).read().decode('utf-8','replace')
            t=re.sub(r'(?s)<(script|style).*?</\1>',' ',t); t=html.unescape(re.sub(r'<[^>]+>',' ',t)); cache[u]=norm(t)
        except Exception as e: cache[u]='ERR '+str(e)
    page=cache[u]
    ok = norm(q) in page
    print('OK  ' if ok else ('ERR ' if page.startswith('ERR') else 'MISS'), u, '|', q[:90], '' if not page.startswith('ERR') else page[:80])
