"""Usage: python3 -I verify_batch.py <in.tsv> <out.jsonl>; in: key<TAB>idtype<TAB>id<TAB>title<TAB>family<TAB>year"""
import sys,json,os,urllib.request,time
K=os.environ["SCHOLAR_API_KEY"]
def post(path,body):
    req=urllib.request.Request("https://scholar-sidekick.com"+path,data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+K,"Content-Type":"application/json"})
    for i in range(3):
        try: return json.load(urllib.request.urlopen(req,timeout=60))
        except Exception as e: err=str(e); time.sleep(3)
    return {"error":err}
out=open(sys.argv[2],"w")
for line in open(sys.argv[1]):
    if not line.strip() or line.startswith("#"): continue
    k,t,i,title,fam,yr=line.rstrip("\n").split("\t")
    c={"title":title,"authors":[{"family":fam}]}
    if yr: c["year"]=int(yr)
    c[t]=i
    v=post("/api/verify",{"claimed":c})
    rt=post("/api/retraction-check",{"id":i}) if t=="doi" else {}
    m=v.get("matched") or {}
    rec=dict(key=k,id=i,verdict=v.get("verdict"),conf=v.get("confidence"),mism=v.get("mismatches"),
             rec_title=m.get("title"),rec_year=(m.get("issued") or {}).get("year"),rec_container=m.get("container-title") or m.get("container"),
             rec_first=((m.get("authors") or [{}])[0].get("family") or (m.get("authors") or [{}])[0].get("literal")),
             retracted=(rt.get("result") or {}).get("isRetracted") if rt else None, err=v.get("error"))
    out.write(json.dumps(rec)+"\n"); out.flush()
    print(k,rec["verdict"],rec["conf"],rec["mism"],"|",rec["rec_title"],"|",rec["rec_first"],rec["rec_year"],"| retracted:",rec["retracted"])
