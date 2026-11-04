#!/usr/bin/env python3
"""Stage 1 re-cut: score every reachable grid cell on data usability and write intersection_map.md.

All per-source facts below were collected on 2026-11-04 (see PROVENANCE notes). Re-running this
script reproduces intersection_map.md exactly; change a fact here, never by hand in the map.

Usability score (methodology Stage 1, step 5), 0-2 per criterion, max 10:
  unit      clear unit of analysis                       (per cell, judged)
  labels    labels / ground truth obtainable             (per cell, judged)
  history   >=3 years = 2, 1-3 = 1, <1 = 0; unverified start = 1 (conservative)
  licence   2 explicit open licence / public domain / stated research permission;
            1 platform terms only or unverified; 0 prohibits research use (cell dropped)
  mining    OpenAlex count tercile over the distinct sources scored: bottom third = 2,
            middle = 1, top third (heavily mined) = 0
Short list: cells scoring >= 6, highest first; ties prefer a source not yet on the list, then the less-mined source; each source
counts at most twice (further cells from it become alternates); max 12.
"""
import os
from datetime import date

YEAR = 2026
D, G, GIT, U = "direct", "GitHub API", "git clone", "unreachable"

# id: (name, url, access, licence_score, licence_note, history_start_year_or_None, openalex_count, openalex_query)
S = {
 # --- documentation (kernel docs etc.)
 "F8": ("Kernel filesystems docs", "https://docs.kernel.org/filesystems/index.html", D, 1, "licence not verified", None, 4, '"Linux kernel documentation"'),
 "SC7": ("Kernel scheduler docs", "https://docs.kernel.org/scheduler/index.html", D, 1, "licence not verified", None, 4, '"Linux kernel documentation"'),
 "M5": ("Kernel MM admin docs", "https://docs.kernel.org/admin-guide/mm/index.html", D, 1, "licence not verified", None, 4, '"Linux kernel documentation"'),
 "K10": ("Kernel documentation", "https://docs.kernel.org/", D, 1, "licence not verified", None, 4, '"Linux kernel documentation"'),
 "D5": ("Kernel driver-API docs", "https://docs.kernel.org/driver-api/index.html", D, 1, "licence not verified", None, 4, '"Linux kernel documentation"'),
 "C3": ("Kernel sysctl docs", "https://docs.kernel.org/admin-guide/sysctl/index.html", D, 1, "licence not verified", None, 4, '"sysctl" "Linux kernel"'),
 "S10": ("NVM Express specifications", "https://nvmexpress.org/specifications/", D, 1, "terms not verified", None, 7, '"NVMe specification"'),
 "B9": ("UEFI specifications", "https://uefi.org/specifications", D, 1, "terms not verified; some downloads need a form", None, 7, '"UEFI specification"'),
 "V7": ("OCI runtime specification", "https://github.com/opencontainers/runtime-spec", G, 2, "Apache-2.0 (GitHub API)", 2015, 2, '"OCI runtime specification"'),
 # --- code / git history / test suites
 "K2": ("Linux kernel git history (GitHub mirror)", "https://github.com/torvalds/linux", G, 2, "GPL-2.0 kernel source (GitHub shows NOASSERTION: multiple licences)", 2005, 386, '"Linux kernel" patches'),
 "F1": ("fstests (xfstests) git", "https://git.kernel.org/pub/scm/fs/xfs/xfstests-dev.git", GIT, 1, "licence not verified", None, 2, '"xfstests"'),
 "K13": ("Stable-kernel queue git", "https://git.kernel.org/pub/scm/linux/kernel/git/stable/stable-queue.git", GIT, 1, "licence not verified", None, 1, '"stable kernel" patches'),
 "SC5": ("rt-tests git", "https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git", GIT, 1, "licence not verified", None, 20, '"cyclictest"'),
 "S4": ("fio repository history", "https://github.com/axboe/fio", G, 2, "GPL-2.0 (GitHub API)", 2012, 187, '"fio" "I/O"'),
 "S5": ("blktests", "https://github.com/linux-blktests/blktests", G, 1, "no licence stated (GitHub API)", 2017, 0, '"blktests"'),
 "M2": ("Linux Test Project (LTP)", "https://github.com/linux-test-project/ltp", G, 2, "GPL-2.0 (GitHub API)", 2012, 15, '"Linux Test Project"'),
 "M3": ("mmtests", "https://github.com/gormanm/mmtests", G, 2, "GPL-2.0 (GitHub API)", 2012, 3, '"mmtests"'),
 "B5": ("EDK2 (UEFI reference) repo", "https://github.com/tianocore/edk2", G, 1, "NOASSERTION (GitHub API)", 2011, 13, '"EDK II"'),
 # --- issue trackers (issue text is governed by platform terms, not the code licence)
 "F4": ("e2fsprogs GitHub issues", "https://github.com/tytso/e2fsprogs/issues", G, 1, "GitHub Terms govern issue text", 2011, 0, '"e2fsprogs"'),
 "F5": ("OpenZFS GitHub issues", "https://github.com/openzfs/zfs/issues", G, 1, "GitHub Terms govern issue text", 2009, 4, '"OpenZFS"'),
 "F7": ("libfuse GitHub issues", "https://github.com/libfuse/libfuse/issues", G, 1, "GitHub Terms govern issue text", 2015, 1, '"libfuse"'),
 "S7": ("SPDK GitHub issues", "https://github.com/spdk/spdk/issues", G, 1, "GitHub Terms govern issue text", 2015, 133, '"SPDK"'),
 "S9": ("nvme-cli GitHub issues", "https://github.com/linux-nvme/nvme-cli/issues", G, 1, "GitHub Terms govern issue text", 2015, 1, '"nvme-cli"'),
 "SC1": ("sched_ext (scx) issues & PRs", "https://github.com/sched-ext/scx", G, 1, "GitHub Terms govern issue/PR text", 2023, 16, '"sched_ext"'),
 "M4": ("jemalloc GitHub issues", "https://github.com/jemalloc/jemalloc/issues", G, 1, "GitHub Terms govern issue text", 2013, 27, '"jemalloc"'),
 "B3": ("fwupd GitHub issues", "https://github.com/fwupd/fwupd/issues", G, 1, "GitHub Terms govern issue text", 2015, 3, '"fwupd"'),
 "B8": ("systemd GitHub issues", "https://github.com/systemd/systemd/issues", G, 1, "GitHub Terms govern issue text", 2015, 425, '"systemd"'),
 "V3": ("moby (Docker) GitHub issues", "https://github.com/moby/moby/issues", G, 1, "GitHub Terms govern issue text", 2013, 30, '"Docker" "GitHub issues"'),
 "V4": ("Kubernetes GitHub issues", "https://github.com/kubernetes/kubernetes/issues", G, 1, "GitHub Terms govern issue text", 2014, 916, '"Kubernetes" "issues"'),
 "V5": ("runc GitHub issues", "https://github.com/opencontainers/runc/issues", G, 1, "GitHub Terms govern issue text", 2015, 437, '"runc"'),
 "V6": ("Firecracker GitHub issues", "https://github.com/firecracker-microvm/firecracker/issues", G, 1, "GitHub Terms govern issue text", 2017, 25, '"Firecracker" "microVM"'),
 "S8": ("Ceph issue tracker", "https://tracker.ceph.com/", D, 1, "terms not readable from here", None, 4, '"Ceph" "bug"'),
 "B6": ("GRUB bug tracker (Savannah)", "https://savannah.gnu.org/bugs/?group=grub", D, 1, "terms not verified", None, 14, '"GRUB" "bootloader"'),
 "R3": ("Launchpad: Ubuntu kernel bugs", "https://bugs.launchpad.net/ubuntu/+source/linux", D, 1, "terms not readable from here", None, 1, '"Launchpad" "bug reports"'),
 # --- mailing lists as lore.kernel.org git clones (web pages block scripts; git works)
 "L-ext4": ("linux-ext4 list (lore git, 1 epoch)", "https://lore.kernel.org/linux-ext4/git/0.git", GIT, 1, "public archive; no stated reuse licence", 2006, 19, '"Linux kernel mailing list"'),
 "L-block": ("linux-block list (lore git, 1 epoch)", "https://lore.kernel.org/linux-block/git/0.git", GIT, 1, "public archive; no stated reuse licence", 2015, 19, '"Linux kernel mailing list"'),
 "L-mm": ("linux-mm list (lore git, epochs 0-2)", "https://lore.kernel.org/linux-mm/git/0.git", GIT, 1, "public archive; no stated reuse licence", 1997, 19, '"Linux kernel mailing list"'),
 "L-dri": ("dri-devel list (lore git, epochs 0-2)", "https://lore.kernel.org/dri-devel/git/0.git", GIT, 1, "public archive; no stated reuse licence", 2010, 19, '"Linux kernel mailing list"'),
 "L-kvm": ("kvm list (lore git, epochs 0-1)", "https://lore.kernel.org/kvm/git/0.git", GIT, 1, "public archive; no stated reuse licence", 2006, 19, '"Linux kernel mailing list"'),
 "L-lkml": ("LKML (lore git, epochs 0-20)", "https://lore.kernel.org/lkml/git/0.git", GIT, 1, "public archive; no stated reuse licence", None, 19, '"Linux kernel mailing list"'),
 "L-lkp": ("Kernel test robot reports, oe-lkp (lore git)", "https://lore.kernel.org/oe-lkp/git/0.git", GIT, 1, "public archive; no stated reuse licence", 2022, 0, '"kernel test robot"'),
 # --- vulnerability / bug infrastructure
 "K6": ("syzbot upstream dashboard", "https://syzkaller.appspot.com/upstream", D, 1, "no licence stated", 2017, 78, '"syzkaller"'),
 "K8": ("NVD CVE API", "https://services.nvd.nist.gov/rest/json/cves/2.0", D, 1, "US-government data; terms page not readable from here", 1997, 12, '"National Vulnerability Database" "Linux kernel"'),
 "K9": ("OSV vulnerability database", "https://osv.dev/list?ecosystem=Linux", D, 1, "per-source licences (secondary sources)", None, 10, '"OSV" "vulnerability database"'),
 "K12": ("regzbot regression tracker", "https://linux-regtracking.leemhuis.info/regzbot/mainline/", D, 1, "no licence stated", None, 1, '"regzbot"'),
 # --- datasets
 "S1": ("Backblaze Drive Stats", "https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data", D, 2, "official page: open, cite Backblaze, no resale", 2013, 137, '"Backblaze"'),
 "S3": ("Alibaba block traces", "https://github.com/alibaba/block-traces", G, 1, "no licence stated (GitHub API)", 2020, 2, '"Alibaba" "block traces"'),
 "SC2": ("Google cluster-data traces", "https://github.com/google/cluster-data", G, 1, "no licence stated on repo (GitHub API)", 2015, 279, '"Google cluster trace"'),
 "SC4": ("Azure Public Dataset", "https://github.com/Azure/AzurePublicDataset", G, 2, "CC-BY-4.0 (GitHub API)", 2017, 14, '"Azure public dataset"'),
 "R1": ("Loghub system-log datasets", "https://github.com/logpai/loghub", G, 1, "NOASSERTION (GitHub API)", 2016, 117, '"Loghub"'),
 "R2": ("Public postmortems collection", "https://github.com/danluu/post-mortems", G, 1, "no licence stated (GitHub API)", 2015, 610, '"postmortems" "incidents"'),
 "R4": ("Ubuntu error tracker", "https://errors.ubuntu.com/", D, 1, "terms not verified", None, 0, '"Ubuntu error tracker"'),
 "D1": ("Linux Hardware probes DB", "https://linux-hardware.org/", D, 1, "no data licence found", None, 0, '"linux-hardware.org"'),
 "B1": ("coreboot Gerrit code review", "https://review.coreboot.org/", D, 1, "review metadata terms not verified", None, 23, '"coreboot"'),
 "B4": ("LVFS firmware service", "https://fwupd.org/", D, 1, "terms not verified", None, 2, '"Linux Vendor Firmware Service"'),
 "V8": ("Kubernetes TestGrid (CI results)", "https://testgrid.k8s.io/", D, 1, "terms not verified", None, 6, '"flaky tests" "Kubernetes"'),
 "C4": ("Unix & Linux Stack Exchange", "https://unix.stackexchange.com/", D, 2, "CC BY-SA (site footer)", 2008, 0, '"Unix & Linux Stack Exchange"'),
 "C5": ("Server Fault", "https://serverfault.com/", D, 2, "CC BY-SA (Stack Exchange network licence)", 2008, 1, '"Server Fault" "Stack Exchange"'),
}

COLS = ["Spec & docs", "Testing", "Debugging & diagnosis", "Repair", "Maintenance & evolution",
        "Config mgmt", "Performance eng.", "Security & vulns", "Code review", "CI & release"]

# Each cell: (source, unit 0-2, labels 0-2, reason) or None = shaded (no public source found).
C = {
 "File systems": [
  ("F8", 1, 0, "doc pages; no outcome labels"), ("F1", 2, 1, "test cases/commits; 'regression test for' links are heuristic"),
  ("F5", 2, 2, "issue; state and type labels recorded"), ("F4", 2, 1, "issue; few labels"),
  ("K2", 2, 2, "commit in fs/; Fixes: tags record bug-introducing commits"), ("F5", 2, 1, "config issues found by keyword"),
  ("F7", 2, 1, "perf issues found by keyword"), ("K8", 2, 2, "CVE; CWE/CVSS fields recorded"),
  ("L-ext4", 2, 1, "patch thread; acceptance inferred by matching commits"), ("K12", 2, 2, "regression entry; status and culprit commit recorded")],
 "Storage": [
  ("S10", 1, 0, "spec sections; no labels"), ("S5", 2, 1, "test/commit; heuristic links"),
  ("S7", 2, 2, "issue; labels and state recorded"), ("S9", 2, 1, "issue; few labels"),
  ("S4", 2, 1, "commit; fix intent from messages"), ("S8", 2, 2, "Redmine issue; status/category/severity fields"),
  ("S3", 2, 0, "I/O request trace; no ground truth"), ("K8", 2, 2, "CVE; CWE/CVSS fields recorded"),
  ("L-block", 2, 1, "patch thread; acceptance inferred"), ("K12", 2, 2, "regression entry; status recorded")],
 "Scheduling": [
  ("SC7", 1, 0, "doc pages"), ("SC5", 2, 1, "test tool commits; heuristic"),
  ("SC1", 2, 1, "issue; young repo, few labels"), ("K2", 2, 2, "commit in kernel/sched; Fixes: tags"),
  ("K2", 2, 2, "commit history of kernel/sched"), ("V4", 2, 2, "issue; sig/kind labels recorded"),
  ("SC2", 2, 2, "task/job events incl. failures and evictions"), None,
  ("SC1", 2, 1, "PR review; merge state recorded, review quality heuristic"), ("L-lkp", 2, 2, "robot report; regression % and bisected commit recorded")],
 "Memory management": [
  ("M5", 1, 0, "doc pages"), ("M2", 2, 1, "test case; heuristic links to bugs"),
  ("M4", 2, 1, "issue; few labels"), ("K6", 2, 2, "syzbot bug; fix commit and status recorded"),
  ("K2", 2, 2, "commit in mm/; Fixes: tags"), ("C3", 1, 0, "sysctl doc entries; no labels"),
  ("M3", 1, 0, "benchmark configs; results not a public dataset"), ("K9", 2, 2, "advisory; affected/fixed versions recorded"),
  ("L-mm", 2, 1, "patch thread; acceptance inferred"), ("M2", 2, 1, "CI runs; pass/fail per test, history heuristic")],
 "Kernel code": [
  ("K10", 1, 0, "doc pages"), ("K2", 2, 1, "selftests in tree; heuristic links"),
  ("K6", 2, 2, "crash report; status, fix, bisection recorded"), ("K13", 2, 2, "backported patch; upstream commit and Fixes: recorded"),
  ("K2", 2, 2, "commit; Fixes: tags"), ("K2", 2, 1, "Kconfig option; no outcome labels"),
  ("L-lkp", 2, 2, "perf regression report; bisected commit recorded"), ("K9", 2, 2, "advisory; versions recorded"),
  ("L-lkml", 2, 1, "patch thread; acceptance inferred"), ("K12", 2, 2, "regression entry; status recorded")],
 "Drivers": [
  ("D5", 1, 0, "doc pages"), ("D1", 2, 1, "hardware probe; device status (to verify)"),
  ("R3", 2, 2, "bug; status/importance recorded"), ("K2", 2, 2, "commit in drivers/; Fixes: tags"),
  ("K2", 2, 2, "commit history of drivers/"), ("D1", 2, 1, "probe config; heuristic"),
  None, ("K8", 2, 2, "CVE; CWE/CVSS fields"),
  ("L-dri", 2, 1, "patch thread; acceptance inferred"), None],
 "Boot & firmware": [
  ("B9", 1, 0, "spec sections"), ("B5", 2, 1, "CI tests/commits; heuristic"),
  ("B6", 2, 2, "bug; status fields recorded"), ("B3", 2, 1, "issue; few labels"),
  ("B5", 2, 1, "commit; no Fixes: convention"), ("B8", 2, 2, "issue; bug/RFE/component labels"),
  None, ("B4", 1, 1, "firmware release / security attribute"),
  ("B1", 2, 2, "Gerrit change; merged/abandoned and votes recorded"), None],
 "Virtualization & containers": [
  ("V7", 1, 0, "spec sections"), ("V6", 2, 1, "test/issue; heuristic"),
  ("V3", 2, 2, "issue; kind/area labels"), ("V5", 2, 1, "issue; few labels"),
  ("V4", 2, 2, "commit/PR history with labels"), ("V4", 2, 2, "issue; config-related labels"),
  ("SC4", 2, 2, "VM/function records with utilisation/lifetime"), ("K9", 2, 2, "advisory; versions recorded"),
  ("L-kvm", 2, 1, "patch thread; acceptance inferred"), ("V8", 2, 2, "test run; pass/fail recorded")],
 "Reliability & observability": [
  None, None, ("R1", 2, 2, "log line/session; anomaly labels in several datasets"),
  ("R3", 2, 2, "bug; status recorded"), ("S1", 2, 2, "drive-day; failure flag recorded"),
  ("R2", 1, 1, "incident write-up; categories heuristic"), None, None, None, ("R4", 1, 1, "crash bucket; views need JavaScript")],
 "Configuration": [
  ("C3", 1, 0, "doc entries"), None, ("C4", 2, 2, "question; accepted answer/score/tags recorded"),
  ("C5", 2, 2, "question; accepted answer/score/tags recorded"), ("K2", 2, 2, "Kconfig change history"),
  ("K2", 2, 1, "Kconfig option; no outcome labels"), None, None, None, None],
}


def hist_score(start):
    if start is None:
        return 1  # unverified: conservative middle score
    span = YEAR - start
    return 2 if span >= 3 else (1 if span >= 1 else 0)


used = sorted({c[0] for row in C.values() for c in row if c})
counts = sorted(S[s][6] for s in used)
t1, t2 = counts[len(counts) // 3], counts[(2 * len(counts)) // 3]


def mining_score(n):
    return 2 if n < t1 else (1 if n < t2 else 0)


rows = []
for concern, cells in C.items():
    for col, cell in zip(COLS, cells):
        if cell is None:
            continue
        sid, unit, lab, why = cell
        name, url, access, lic, licnote, start, oa, q = S[sid]
        if access == U:
            continue
        h, m = hist_score(start), mining_score(oa)
        total = unit + lab + h + lic + m
        rows.append(dict(concern=concern, col=col, sid=sid, unit=unit, lab=lab, hist=h, lic=lic, mine=m,
                         total=total, why=why, oa=oa))

eligible = [r for r in rows if r["total"] >= 6 and r["lic"] > 0]
remaining = sorted(eligible, key=lambda r: -r["total"])
short, seen = [], set()
MAX_PER_SOURCE = 2
uses = {}
alternates = []
while remaining and len(short) < 12:
    top = remaining[0]["total"]
    tier = [r for r in remaining if r["total"] == top]
    tier.sort(key=lambda r: (r["sid"] in seen, r["oa"]))  # unseen source first, then less-mined source
    pick = tier[0]
    remaining.remove(pick)
    if uses.get(pick["sid"], 0) >= MAX_PER_SOURCE:
        alternates.append(pick)
        continue
    short.append(pick); seen.add(pick["sid"]); uses[pick["sid"]] = uses.get(pick["sid"], 0) + 1

# ---------- write intersection_map.md
L = []
w = L.append
w("# Stage 1: SE × AI × OS intersection map (re-cut with data usability)\n")
w(f"Generated by `tools/score_stage1.py` (facts collected 2026-11-04). Do not edit by hand: change the data in the script and rerun it. "
  "The **AI-method axis is deliberately blank**: methods are chosen in Stage 3 from the shape of the data.\n")
w("**Access legend:** direct = page loads from the research environment; GitHub API = public repository confirmed via the GitHub search API "
  "(the sandbox blocked direct GitHub pages); git clone = repository answers `git ls-remote` (kernel.org web pages block scripts, git does not).\n")
w("## Grid (cell = source ID and usability score out of 10; ▒ = no public source)\n")
w("| OS concern \\ SE activity | " + " | ".join(COLS) + " |")
w("|" + "---|" * (len(COLS) + 1))
byc = {(r["concern"], r["col"]): r for r in rows}
for concern, cells in C.items():
    out = []
    for col, cell in zip(COLS, cells):
        r = byc.get((concern, col))
        out.append("▒" if cell is None else f"{cell[0]} · **{r['total']}**" + (" ★" if r in short else ""))
    w(f"| **{concern}** | " + " | ".join(out) + " |")
w("\n★ = on the short list.\n")
w("## Scoring table (every reachable cell)\n")
w(f"Mining-saturation terciles over the {len(used)} distinct sources used: OpenAlex count < {t1} → 2, {t1}–{t2 - 1} → 1, ≥ {t2} → 0.\n")
w("| # | OS concern | SE activity | Source | Unit | Labels | History | Licence | Mining (OpenAlex n) | **Total** | Why (unit/labels) |")
w("|---|---|---|---|---|---|---|---|---|---|---|")
for i, r in enumerate(sorted(rows, key=lambda r: (-r["total"], r["concern"], COLS.index(r["col"]))), 1):
    w(f"| {i} | {r['concern']} | {r['col']} | {r['sid']} | {r['unit']} | {r['lab']} | {r['hist']} | {r['lic']} | {r['mine']} ({r['oa']}) | **{r['total']}** | {r['why']} |")
w("")
w(f"Cells scored: {len(rows)} · scoring ≥ 6 with licence > 0: {len(eligible)} · shaded: {sum(c is None for row in C.values() for c in row)}.\n")
w("## Short list (Stage 1 gate)\n")
w("| # | Cell | Source | Access | Score | Licence note |")
w("|---|---|---|---|---|---|")
for i, r in enumerate(short, 1):
    n = S[r["sid"]]
    w(f"| {i} | {r['concern']} × {r['col']} | {r['sid']}: [{n[0]}]({n[1]}) | {n[2]} | {r['total']} | {n[4]} |")
dist = sorted({r["sid"] for r in short})
w(f"\n**{len(short)} cells, {len(dist)} distinct sources** ({', '.join(dist)}). Each source counts at most twice.\n")
if alternates:
    w("Alternates (high-scoring cells excluded only by the two-per-source cap): " +
      "; ".join(f"{r['concern']} × {r['col']} [{r['sid']}, {r['total']}]" for r in alternates) + ".\n")
w("**AI-side gate result:** " + (f"PASS: {len(eligible)} cells score ≥ 6 (at least 8 needed), the short list holds {len(short)} (8–12 allowed), and none scores 0 on licence. "
  if 8 <= len(short) <= 12 else "RESHAPE: fewer than 8 qualifying cells. ") +
  "The gate becomes final only after the student has opened every short-listed source (methodology Stage 1 exit criteria). "
  "Licence scores of 1 must be confirmed before Stage 6.\n")
w("## Source catalogue\n")
w("| ID | Source | URL | Access | Licence (score) | History from | OpenAlex query → count |")
w("|---|---|---|---|---|---|---|")
for sid in used:
    n = S[sid]
    w(f"| {sid} | {n[0]} | {n[1]} | {n[2]} | {n[4]} ({n[3]}) | {n[5] or 'unverified'} | `{n[7]}` → {n[6]} |")
w("""
**Notes**
- **History:** GitHub "created" dates can be later than the project's real history (e.g., the kernel mirror holds history from 2005). Lore start dates are the first message in epoch 0, measured from blob-free clones. Those clones are large (about 0.3–1.1 GB per epoch), so plan the disk space.
- **OpenAlex counts** are phrase searches over titles and abstracts. They are a rough saturation signal only, never proof of a gap. Generic names (e.g., "systemd", "runc") also match papers that merely mention the tool.
- **Licence 1** means the reuse terms couldn't be confirmed or only platform terms apply. Report mined data in aggregate (Stage 2 ethics note), and confirm the terms before Stage 6.
- Six cells now use lore git clones: code review in file systems, storage, memory management, kernel code, drivers, and virtualization (kvm). Two more do too: scheduling CI and kernel performance (kernel test robot reports). Earlier, these lists were unreachable through their web pages. fstests, the stable queue and rt-tests are reached as git clones.
""")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "intersection_map.md")
open(out, "w").write("\n".join(L))
print(f"rows={len(rows)} eligible={len(eligible)} short={len(short)} distinct={len(dist)} terciles={t1},{t2}")
for r in short:
    print(f"  {r['total']}  {r['concern']} × {r['col']}  [{r['sid']}]")
