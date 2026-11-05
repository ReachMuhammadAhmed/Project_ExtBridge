"""Keyword counts in human replies to robot perf-regression reports (aggregate only).
Usage: python3 -I reply_kw.py <oe-lkp git dir> <lkp_msgs.jsonl>"""
import sys,json,subprocess,email,email.policy,re,collections
G=sys.argv[1]; R=[json.loads(l) for l in open(sys.argv[2])]
regs={r['mid'] for r in R if r.get('perf') and r['robot'] and r['dir']=='regression'}
want={}
for r in R:
    if r['reply'] and not r['robot']:
        t=next((x for x in [r['irt']]+r['refs'] if x in regs),None)
        if t: want[r['mid']]=t
revs=subprocess.run(["git","-C",G,"rev-list","--all"],capture_output=True,text=True).stdout.split()
p=subprocess.Popen(["git","-C",G,"cat-file","--batch"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
KW={'noise/noisy':r'\bnois(e|y)\b','alignment':r'\balign(ment|ed)?\b','cannot reproduce':r"(can'?not|can't|couldn'?t|unable to|not able to) (reproduce|see|confirm)",
    'unrelated/nothing to do':r"(unrelated|nothing to do with|not related|doesn'?t make sense|makes no sense)",'false positive':r'false (positive|alarm)',
    'revert':r'\brevert','fix/patch':r'\b(fix(ed)?|patch)\b','thanks/thank':r'\bthank','expected/intended':r'\b(expected|intended|by design|trade-?off)\b'}
thread_hits=collections.defaultdict(set); nrep=0
for rv in revs:
    p.stdin.write((rv+":m\n").encode()); p.stdin.flush(); h=p.stdout.readline().split()
    if len(h)<3 or h[1]==b'missing': continue
    data=p.stdout.read(int(h[2])); p.stdout.read(1)
    m=email.message_from_bytes(data,policy=email.policy.compat32); mid=str(m.get('Message-ID','')).strip().strip('<>')
    if mid not in want: continue
    nrep+=1
    part=m
    if m.is_multipart():
        part=next((x for x in m.walk() if x.get_content_type()=='text/plain'),m)
    try: body=part.get_payload(decode=True).decode('utf-8','replace')
    except Exception: body=str(part.get_payload())
    own='\n'.join(l for l in body.splitlines() if not l.lstrip().startswith('>'))  # drop quoted text
    for k,rx in KW.items():
        if re.search(rx,own,re.I): thread_hits[k].add(want[mid])
threads=set(want.values())
print('human replies',nrep,'threads (regression reports with a human reply)',len(threads))
for k in KW: print(f'  {k}: {len(thread_hits[k])} threads ({100*len(thread_hits[k])/len(threads):.0f}%)')
