"""Link oe-lkp perf reports to mainline commits. Usage: python3 -I label_perf.py lkp_msgs.jsonl linux_msgs.txt out.json"""
import sys,json,re,collections
R=[json.loads(l) for l in open(sys.argv[1])]
perf=[r for r in R if r.get('perf') and r['robot']]
byid={r['mid']:r for r in perf}
commits=[c.split('\x1f',2) for c in open(sys.argv[2],encoding='utf-8',errors='replace').read().split('\x1e')[1:]]
lore=re.compile(r'lore\.kernel\.org/[\w.-]+/([^/\s>]+@[^/\s>]+)')
rev=re.compile(r'This reverts commit ([0-9a-f]{12,40})'); fx=re.compile(r'^Fixes:\s*([0-9a-f]{8,40})',re.M)
cited=collections.defaultdict(list); revset=set(); fixc=collections.Counter()
for h,d,b in commits:
    for m in lore.findall(b):
        m=m.rstrip('/.')
        if m in byid: cited[m].append(dict(h=h[:12],d=d,revert=b.startswith('Revert')))
    for x in rev.findall(b): revset.add(x[:12])
    for x in fx.findall(b): fixc[x[:12]]+=1
mids=set(byid); human=collections.Counter()
for r in R:
    if r['reply'] and not r['robot']:
        t=next((x for x in [r['irt']]+r['refs'] if x in mids),None)
        if t: human[t]+=1
rows=[]
for r in perf:
    b=(r['blamed'] or '')[:12]
    rows.append(dict(mid=r['mid'],date=r['date'],dir=r['dir'],pct=r['pct'],metric=r['metric'],branch=r['branch'],
        cited=r['mid'] in cited, reverted=b in revset, fixes_tag=fixc[b]>0, human_replies=human[r['mid']],
        has_closes=bool(r['closes_mid']),n_other=r['n_other_tests'],n_prof=r['n_perf_profile']))
json.dump(rows,open(sys.argv[3],'w'))
print('mainline commits',len(commits),commits[-1][1],'..',commits[0][1])
def summ(sel,name):
    n=len(sel); c=sum(x['cited'] for x in sel); rv=sum(x['reverted'] for x in sel); f=sum(x['fixes_tag'] for x in sel); h=sum(x['human_replies']>0 for x in sel)
    strong=sum(x['cited'] or x['reverted'] for x in sel)
    print(f"{name}: n={n} cited={c} reverted={rv} strong(cited|reverted)={strong} fixes_tag_on_blamed={f} any_human_reply={h}")
regs=[x for x in rows if x['dir']=='regression']
summ(regs,'all regression reports')
for y in ['2016','2018','2020','2022','2024','2026']:
    pass
by=collections.defaultdict(list)
for x in regs: by[(x['date'] or '????')[:4]].append(x)
for y in sorted(by): summ(by[y],'  '+y)
summ([x for x in regs if x['branch']=='linus:master'],'regressions on linus:master')
summ([x for x in rows if x['dir']=='improvement'],'improvement reports')
