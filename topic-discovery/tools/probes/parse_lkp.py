"""Parse oe-lkp public-inbox clone into one JSON line per message (no names/emails kept except robot flag).
Usage: python3 -I parse_lkp.py <oe-lkp git dir> <out.jsonl>"""
import sys, subprocess, json, re, email, email.policy, email.utils
from email.header import decode_header, make_header
G, OUT = sys.argv[1], sys.argv[2]
revs = subprocess.run(["git","-C",G,"rev-list","--all"],capture_output=True,text=True).stdout.split()
p = subprocess.Popen(["git","-C",G,"cat-file","--batch"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
def get(obj):
    p.stdin.write((obj+"\n").encode()); p.stdin.flush()
    hdr = p.stdout.readline().split()
    if len(hdr) < 3 or hdr[1] == b"missing": return None
    n = int(hdr[2]); data = p.stdout.read(n); p.stdout.read(1); return data
SUBJ = re.compile(r':\s+(?P<metric>\S+)\s+(?P<pct>-?\d+(?:\.\d+)?)%\s+(?P<dir>regression|improvement)\s*$')
HASH = re.compile(r'^commit:\s*([0-9a-f]{40})', re.M)
CLOSES = re.compile(r'Closes:\s*https?://lore\.kernel\.org/\S+?/([^/\s]+@[^/\s]+?)/?\s*$', re.M)
out = open(OUT, "w"); n = 0
for r in revs:
    blob = get(r + ":m")
    if blob is None: continue
    m = email.message_from_bytes(blob, policy=email.policy.compat32)
    try: subj = str(make_header(decode_header(m.get("Subject","")))).replace("\n"," ")
    except Exception: subj = m.get("Subject","")
    subj = " ".join(subj.split())
    frm = str(m.get("From","") or "")
    robot = "kernel test robot" in frm.lower() or "lkp@intel.com" in frm.lower()
    try: dt = email.utils.parsedate_to_datetime(m.get("Date")).astimezone().isoformat()[:10]
    except Exception: dt = None
    body = ""
    part = m
    if m.is_multipart():
        for pp in m.walk():
            if pp.get_content_type() == "text/plain": part = pp; break
    try: body = part.get_payload(decode=True).decode("utf-8","replace")
    except Exception: body = str(part.get_payload())
    rec = dict(mid=str(m.get("Message-ID","") or "").strip().strip("<>"), date=dt, robot=robot,
               irt=str(m.get("In-Reply-To","") or "").strip().strip("<>"),
               refs=[x.strip("<>") for x in str(m.get("References","") or "").split()],
               reply=subj.lower().startswith("re:"), subj=subj)
    s = SUBJ.search(str(subj))
    if s and not rec["reply"]:
        rec.update(perf=True, metric=s["metric"], pct=float(s["pct"]), dir=s["dir"])
        h = HASH.search(body); rec["blamed"] = h.group(1) if h else None
        c = CLOSES.search(body); rec["closes_mid"] = c.group(1) if c else None
        rec["branch"] = (re.match(r'\[([^\]]+)\]', subj) or [None, None])[1]
        rec["n_other_tests"] = body.count("| testcase: change |")
        rec["has_stddev"] = "%stddev" in body
        rec["n_perf_profile"] = len(re.findall(r'perf-profile\.\S+', body))
        rec["body_len"] = len(body)
        # stddev of the headline metric on the blamed side, if printed as "± x%"
        line = next((l for l in body.splitlines() if l.rstrip().endswith(rec["metric"])), "")
        rec["metric_line"] = " ".join(line.split())[:200]
    out.write(json.dumps(rec) + "\n"); n += 1
print("messages", n)
