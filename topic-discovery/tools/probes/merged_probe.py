"""For robot perf-regression reports on non-mainline branches: did the blamed commit's subject later appear in mainline?
Usage: python3 -I merged_probe.py <oe-lkp git> <lkp_msgs.jsonl> <linux_msgs.txt>"""
import sys,json,subprocess,re,collections
G,MSG,LIN=sys.argv[1:4]
R=[json.loads(l) for l in open(MSG)]
regs={r['mid']:r for r in R if r.get('perf') and r['robot'] and r['dir']=='regression'}
p=subprocess.Popen(["git","-C",G,"cat-file","--batch"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
subj={}
for rv in subprocess.run(["git","-C",G,"rev-list","--all"],capture_output=True,text=True).stdout.split():
    p.stdin.write((rv+":m\n").encode()); p.stdin.flush(); h=p.stdout.readline().split()
    if len(h)<3 or h[1]==b'missing': continue
    d=p.stdout.read(int(h[2])); p.stdout.read(1)
    m=re.search(rb'^Message-ID:\s*<([^>]+)>',d,re.M|re.I)
    if not m or m.group(1).decode() not in regs: continue
    c=re.search(rb'^commit:\s*[0-9a-f]{40}\s*\("(.+?)"\)',d,re.M)
    if c: subj[m.group(1).decode()]=c.group(1).decode('utf-8','replace')
main=set()
for x in open(LIN,encoding='utf-8',errors='replace').read().split('\x1e')[1:]:
    h,dt,b=x.split('\x1f',2); main.add(b.split('\n',1)[0].strip())
cnt=collections.Counter()
for mid,r in regs.items():
    if (r['date'] or '')<'2016-06': continue
    mainline=r['branch'] in ('linus:master',)
    s=subj.get(mid)
    if s is None: cnt[('mainline' if mainline else 'dev','no subject parsed')]+=1; continue
    cnt[('mainline' if mainline else 'dev','merged' if s in main else 'not in mainline')]+=1
for k,v in sorted(cnt.items()): print(k,v)
