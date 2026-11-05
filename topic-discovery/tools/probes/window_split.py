"""Post-2020 analysis window and time split sizes for I-001. Usage: python3 -I window_split.py <perf_labels.json from label_perf.py>"""
import sys,json
rows=json.load(open(sys.argv[1]))
r=sorted([x for x in rows if x['dir']=='regression' and (x['date'] or '')>='2020'],key=lambda x:x['date'])
pos=lambda x: x['cited'] or x['reverted']
print('2020+ regression reports',len(r),'| strong positives',sum(map(pos,r)),'| threads with human reply',sum(x['human_replies']>0 for x in r),'| no reply',sum(x['human_replies']==0 for x in r))
cut=int(len(r)*0.7); t=r[cut:]
print('time split 70/30: train',cut,'test',len(t),'| test positives',sum(map(pos,t)),'| test starts',t[0]['date'])
