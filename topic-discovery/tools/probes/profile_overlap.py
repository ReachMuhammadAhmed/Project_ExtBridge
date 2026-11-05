"""Sample probe: do functions in a report's perf-profile lines overlap functions changed by the blamed commit?
Usage: python3 -I profile_overlap.py <oe-lkp git> <linux git> <lkp_msgs.jsonl> <perf_labels.json> <N>"""
import sys,json,subprocess,re,random,email,email.policy
G,L,MSG,LAB,N=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5])
R={json.loads(l)['mid']:json.loads(l) for l in open(MSG)}
lab={x['mid']:x for x in json.load(open(LAB))}
# map mid -> public-inbox commit
revs=subprocess.run(["git","-C",G,"log","--all","--format=%H %s"],capture_output=True,text=True).stdout.splitlines()
cand=[m for m,x in lab.items() if x['dir']=='regression' and (x['date'] or '')>='2021' and R[m].get('blamed')]
random.seed(7); pos=[m for m in cand if lab[m]['cited'] or lab[m]['reverted']]; neg=[m for m in cand if m not in pos]
sample=random.sample(pos,min(N//2,len(pos)))+random.sample(neg,N-min(N//2,len(pos)))
# find blob by scanning messages once
need=set(sample); bodies={}
p=subprocess.Popen(["git","-C",G,"cat-file","--batch"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for line in subprocess.run(["git","-C",G,"rev-list","--all"],capture_output=True,text=True).stdout.split():
    p.stdin.write((line+":m\n").encode()); p.stdin.flush(); h=p.stdout.readline().split()
    if len(h)<3 or h[1]==b'missing': continue
    d=p.stdout.read(int(h[2])); p.stdout.read(1)
    mm=re.search(rb'^Message-ID:\s*<([^>]+)>',d,re.M|re.I)
    if mm and mm.group(1).decode() in need: bodies[mm.group(1).decode()]=d.decode('utf-8','replace')
    if len(bodies)==len(need): break
res=[]
for m in sample:
    body=bodies.get(m,'')
    prof=set(re.findall(r'perf-profile\.(?:self|children|calltrace)\.cycles-pp\.([A-Za-z_][\w.]*)',body))
    prof={f.split('.')[-1] for f in prof}
    h=R[m]['blamed']
    out=subprocess.run(["git","-C",L,"show","--format=","-U0",h],capture_output=True,text=True,timeout=300).stdout
    changed=set(re.findall(r'^@@[^@]*@@.*?\b([A-Za-z_]\w*)\s*\(',out,re.M))|set(re.findall(r'^[+-](?:static\s+)?(?:inline\s+)?[\w\s\*]+?\b([A-Za-z_]\w*)\s*\([^;]*$',out,re.M))
    ov=prof&changed
    res.append(dict(pos=m in pos,nprof=len(prof),nchanged=len(changed),overlap=len(ov)>0,diff_ok=bool(out)))
import statistics
for k in [True,False]:
    s=[r for r in res if r['pos']==k]
    print('acted-on' if k else 'other   ', 'n',len(s),'diff fetched',sum(r['diff_ok'] for r in s),'has profile',sum(r['nprof']>0 for r in s),'overlap>0',sum(r['overlap'] for r in s))
