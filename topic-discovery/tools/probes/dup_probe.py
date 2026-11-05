"""Option B probe: how often does the robot send separate reports for one blamed commit, and how often is one signature blamed on several commits?
Usage: python3 -I dup_probe.py <lkp_msgs.jsonl>"""
import sys,json,re,collections
R=[json.loads(l) for l in open(sys.argv[1])]
roots=[r for r in R if r['robot'] and not r['reply']]
pat=re.compile(r'^(?:\[[^\]]*\]\s*)+([0-9a-f]{8,12}):\s+(.*)$')
rep=[(m.group(1)[:10],m.group(2),r) for r in roots for m in [pat.match(r['subj'])] if m]
print('robot root messages',len(roots),'with "<hash>: <signature>" subject',len(rep))
by=collections.Counter(h for h,s,r in rep)
print('distinct blamed commits',len(by),'with >1 separate root report',sum(1 for v in by.values() if v>1),'reports on such commits',sum(v for v in by.values() if v>1))
norm=lambda s: re.sub(r'\d+(\.\d+)?%?','#',s).strip()
sig=collections.defaultdict(set)
for h,s,r in rep:
    if not r.get('perf'): sig[norm(s)].add(h)
multi=[k for k,v in sig.items() if len(v)>1]
print('non-perf signatures',len(sig),'blamed on >1 distinct commit',len(multi),'reports involved',sum(len(sig[k]) for k in multi))
print('perf reports that already list other affected tests (robot-side grouping)',sum(1 for r in R if r.get('perf') and r['n_other_tests']>0))
