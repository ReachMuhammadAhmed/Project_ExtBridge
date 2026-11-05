"""Parse regzbot HTML pages into per-regression rows (no names kept). Usage: python3 -I regzbot_parse.py <page.html> ... > out.jsonl"""
import sys,re,json,datetime,html
for f in sys.argv[1:]:
    t=open(f,encoding='utf-8',errors='replace').read()
    for e in t.split('<tr style="vertical-align:top;">')[1:]:
        tds=e.split('</td>',1)
        first=tds[0]
        culprit=bool(re.search(r'id=[0-9a-f]{40}',first))
        ftxt=' '.join(html.unescape(re.sub(r'<[^>]+>',' ',first)).split())
        rng=('..' in ftxt) and not culprit
        ts=[int(x) for x in re.findall(r'timeAgo\((\d{13})\)',e)]
        body=' '.join(html.unescape(re.sub(r'<[^>]+>',' ',e)).split())
        res=re.search(r'Resolution:\s*(.{0,160})',body)
        rtxt=res.group(1) if res else ''
        kind=('revert' if re.search(r'\bRevert',rtxt) else 'commit' if re.search(r'\b[0-9a-f]{12}\b',rtxt) else ('other' if rtxt else 'none'))
        src='bugzilla' if 'bugzilla.kernel.org' in e[:3000] else ('gitlab' if 'gitlab.freedesktop.org' in e[:3000] else ('github' if 'github.com' in e[:3000] else 'lore'))
        nact=len(re.findall(r'timeAgo\(',e))
        implicit='implicit due to Link/Closes tag' in e
        print(json.dumps(dict(page=f.split('/')[-1],culprit=culprit,range=rng,first=min(ts) if ts else None,last=max(ts) if ts else None,
              res_kind=kind,src=src,n_events=nact,implicit_fix=implicit,stable=('stable' in ftxt.lower()))))
