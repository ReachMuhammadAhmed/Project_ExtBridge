"""Option C/D probe summary over regzbot_parse.py output. Usage: python3 -I regzbot_summary.py <rz_rows.jsonl> <resolved.html>"""
import sys,json,collections,re
R=[json.loads(l) for l in open(sys.argv[1])]
for p in ['rz_resolved.html','rz_inconclusive.html']:
    s=[r for r in R if r['page']==p]
    print(p,'entries',len(s),'culprit commit in first column',sum(r['culprit'] for r in s),'version range',sum(r['range'] for r in s),'neither (parse unknown)',sum(not r['culprit'] and not r['range'] for r in s))
    print('   resolution kind',dict(collections.Counter(r['res_kind'] for r in s)),'channel',dict(collections.Counter(r['src'] for r in s)))
res=[r for r in R if r['page']=='rz_resolved.html']; inc=[r for r in R if r['page']=='rz_inconclusive.html']
for k in [True,False]:
    a=sum(1 for r in res if r['culprit']==k); b=sum(1 for r in inc if r['culprit']==k)
    print('culprit known' if k else 'culprit not shown','resolved',a,'inconclusive',b,'inconclusive share %.1f%%'%(100*b/(a+b)))
t=open(sys.argv[2],encoding='utf-8',errors='replace').read().split('<tr style="vertical-align:top;">')[1:]
imp=sum(1 for e in t if 'implicit due to Link/Closes tag' in e)
man=sum(1 for e in t if re.search(r'Regzbot command history:.*?\bfix(ed)?:',re.sub(r'<[^>]+>',' ',e),re.S))
print('resolved entries with a fix matched via Link/Closes tag',imp,'| with a manual "fix:" regzbot command',man,'(heuristic; categories can overlap)')
