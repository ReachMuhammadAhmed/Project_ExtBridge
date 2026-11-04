#!/usr/bin/env python3
"""P-A pilot: do ext readers disagree on the logical contents of the same image?

Builds the 10 pre-registered image cases (research/preregistration.md), extracts a
logical view {path: (type, size, sha256[:12])} from each reader, and diffs them.

Readers: debugfs (libext2fs), kernel (loop mount, ro; ext4 driver on this host),
grub-fstest (GRUB 2), TSK (fls+icat), 7-Zip. e2fsck -fn gives a verdict only.
Usage (root): python3 pa_harness.py <workdir>
"""
import hashlib, json, os, re, shutil, struct, subprocess, sys, tempfile

W = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "pa_work")
os.makedirs(W, exist_ok=True)
BS = 1024
FILES = {"a.txt": b"AAAA-alpha-" * 50, "b.txt": b"BBBB-bravo-" * 50,
         "dir/c.txt": b"CCCC-charlie-" * 30, "x.txt": b"XXXX-xray-" * 20}

def sh(cmd, inp=None, timeout=60):
    r = subprocess.run(cmd, input=inp, capture_output=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr

def h(b): return hashlib.sha256(b).hexdigest()[:12]

def dfs(img, req, write=False):
    return sh(["debugfs"] + (["-w"] if write else []) + ["-R", req, img])[1].decode(errors="replace")

def ino_of(img, path):
    m = re.search(r"Inode:\s*(\d+)", dfs(img, f"stat /{path}"))
    return int(m.group(1)) if m else None

def base_image(path):
    sh(["dd", "if=/dev/zero", f"of={path}", "bs=1M", "count=4"])
    src = tempfile.mkdtemp()
    for p, data in FILES.items():
        os.makedirs(os.path.dirname(os.path.join(src, p)), exist_ok=True)
        open(os.path.join(src, p), "wb").write(data)
    sh(["mke2fs", "-q", "-F", "-t", "ext2", "-b", str(BS), "-d", src, path])
    shutil.rmtree(src)

# ---- raw helpers -----------------------------------------------------------
def sb(img):
    with open(img, "rb") as f: f.seek(1024); return f.read(1024)

def dir_block(img, path):
    m = re.search(r"\(0\):(\d+)", dfs(img, f"stat /{path}" if path else "stat /"))
    return int(m.group(1))

def edit_dirent(img, dirpath, name, fn):
    """Find entry `name` in first block of dirpath, let fn(buf, off) mutate it."""
    blk = dir_block(img, dirpath)
    with open(img, "r+b") as f:
        f.seek(blk * BS); buf = bytearray(f.read(BS)); off = 0
        while off < BS:
            ino, rl, nl, ft = struct.unpack_from("<IHBB", buf, off)
            if buf[off + 8: off + 8 + nl] == name.encode():
                fn(buf, off); f.seek(blk * BS); f.write(buf); return True
            if rl == 0: break
            off += rl
    return False

# ---- the 10 pre-registered cases ------------------------------------------
def c01_crosslink(img):
    a, b = ino_of(img, "a.txt"), ino_of(img, "b.txt")
    blk = int(re.search(r"\(0\):(\d+)", dfs(img, f"stat <{a}>")).group(1))
    dfs(img, f"sif <{b}> block[0] {blk}", True)
def c02_hidden_entry(img):
    dfs(img, "unlink /x.txt", True)          # name merged into prev rec_len; inode stays allocated
def c03_size_mismatch(img):
    a, b = ino_of(img, "a.txt"), ino_of(img, "b.txt")
    dfs(img, f"sif <{a}> size 5000", True)    # larger than allocated -> implicit hole
    dfs(img, f"sif <{b}> size 10", True)      # smaller than data
def c04_links_zero(img):
    a = ino_of(img, "a.txt")
    dfs(img, f"sif <{a}> links_count 0", True); dfs(img, f"sif <{a}> dtime 1700000000", True)
def c05_bitmap_free(img):
    dfs(img, f"freei <{ino_of(img, 'a.txt')}>", True)
def c06_duplicate_name(img):
    b = ino_of(img, "b.txt")
    edit_dirent(img, "", "b.txt", lambda buf, o: buf.__setitem__(slice(o + 8, o + 13), b"a.txt"))
def c07_filetype_mismatch(img):
    edit_dirent(img, "", "a.txt", lambda buf, o: buf.__setitem__(o + 7, 2))   # claims directory
def c08_illegal_name(img):
    edit_dirent(img, "", "b.txt", lambda buf, o: buf.__setitem__(o + 9, ord("/")))  # "b/txt"
def c09_dir_loop(img):
    dfs(img, "link <2> /dir/loop", True)
def c10_unknown_incompat(img):
    with open(img, "r+b") as f:
        f.seek(1024 + 0x60); v = struct.unpack("<I", f.read(4))[0]
        f.seek(1024 + 0x60); f.write(struct.pack("<I", v | 0x80000000))

CASES = [c01_crosslink, c02_hidden_entry, c03_size_mismatch, c04_links_zero, c05_bitmap_free,
         c06_duplicate_name, c07_filetype_mismatch, c08_illegal_name, c09_dir_loop, c10_unknown_incompat]

# ---- readers ---------------------------------------------------------------
MAXDEPTH = 6
def walk_dir(root):
    view, seen = {}, set()
    def rec(d, rel, depth):
        if depth > MAXDEPTH: view[rel + "/…"] = ("depth-limit", 0, ""); return
        try: names = sorted(os.listdir(d))
        except OSError as e: view[rel or "/"] = ("err:" + e.strerror, 0, ""); return
        for n in names:
            p, r = os.path.join(d, n), (rel + "/" + n).lstrip("/")
            try:
                st = os.lstat(p)
                if os.path.isdir(p) and not os.path.islink(p):
                    view[r] = ("d", 0, "")
                    if (st.st_dev, st.st_ino) in seen: view[r] = ("d-loop", 0, ""); continue
                    seen.add((st.st_dev, st.st_ino)); rec(p, r, depth + 1)
                else:
                    data = open(p, "rb").read(); view[r] = ("f", len(data), h(data))
            except OSError as e: view[r] = ("err:" + (e.strerror or "?"), 0, "")
    rec(root, "", 0); return view

def r_kernel(img):
    mnt = tempfile.mkdtemp()
    rc, _, err = sh(["mount", "-o", "ro,loop", "-t", "ext2", img, mnt], timeout=30)
    if rc: os.rmdir(mnt); return {"!REJECT": err.decode().strip()[-120:]}
    try: return walk_dir(mnt)
    finally: sh(["umount", mnt]); os.rmdir(mnt)

def r_debugfs(img):
    out = tempfile.mkdtemp()
    rc, _, err = sh(["debugfs", "-R", f"rdump / {out}", img], timeout=60)
    v = walk_dir(out); shutil.rmtree(out)
    if not v and re.search(rb"(?i)unsupported|bad magic|corrupt", err): return {"!REJECT": err.decode()[-120:]}
    return v

def r_7z(img):
    out = tempfile.mkdtemp()
    rc, so, se = sh(["7z", "x", "-y", f"-o{out}", "-tExt", img], timeout=60)
    v = walk_dir(out); shutil.rmtree(out)
    if rc and not v: return {"!REJECT": (so + se).decode(errors="replace").strip().splitlines()[-1][:120]}
    return v

def r_grub(img, path="", depth=0):
    # grub-fstest `ls` prints space-separated names; directories end in "/"
    rc, so, se = sh(["grub-fstest", img, "ls", "(loop0)/" + path], timeout=30)
    if depth == 0 and (rc or b"error" in se.lower()):
        return {"!REJECT": (se or so).decode(errors="replace").strip()[:120]}
    view = {}
    if depth > MAXDEPTH: return {path + "/…": ("depth-limit", 0, "")}
    for tok in so.decode(errors="replace").split():
        isdir = tok.endswith("/"); name = tok.rstrip("/")
        if name in (".", "..", ""): continue
        rel = (path + "/" + name).lstrip("/")
        if isdir:
            view[rel] = ("d", 0, ""); view.update(r_grub(img, rel, depth + 1))
        else:
            rc2, data, _ = sh(["grub-fstest", img, "cat", "(loop0)/" + rel], timeout=30)
            view[rel] = ("f", len(data), h(data)) if rc2 == 0 else ("err", 0, "")
    return view

def r_tsk(img):
    rc, so, se = sh(["fls", "-r", "-p", "-f", "ext2", img], timeout=60)
    if rc: return {"!REJECT": se.decode(errors="replace").strip()[:120]}
    view = {}
    for line in so.decode(errors="replace").splitlines():
        m = re.match(r"^(\S)/(\S)\s+(\*?)\s*(\d+)(?:\(realloc\))?:\s+(.*)$", line)
        if not m: continue
        typ, deleted, ino, name = m.group(1), m.group(3), m.group(4), m.group(5)
        if deleted or name.endswith("/..") or name.endswith("/.") or name in (".", ".."): continue
        if typ == "d": view[name] = ("d", 0, "")
        elif typ == "r":
            rc2, data, _ = sh(["icat", "-f", "ext2", img, ino], timeout=30)
            view[name] = ("f", len(data), h(data))
    return view

READERS = {"kernel": r_kernel, "debugfs": r_debugfs, "grub": r_grub, "tsk": r_tsk, "7zip": r_7z}

def main():
    results = {}
    for case in CASES:
        img = os.path.join(W, case.__name__ + ".img"); base_image(img); case(img)
        rc, so, _ = sh(["e2fsck", "-fn", img])
        views = {}
        for name, fn in READERS.items():
            try: views[name] = fn(img)
            except subprocess.TimeoutExpired: views[name] = {"!TIMEOUT": ""}
            except Exception as e: views[name] = {"!CRASH": repr(e)[:120]}
        accepted = {k: v for k, v in views.items() if not any(x.startswith("!") for x in v)}
        paths = sorted(set().union(*[v.keys() for v in accepted.values()])) if accepted else []
        diffs = {}
        for p in paths:
            vals = {k: tuple(v.get(p, ("absent", 0, ""))) for k, v in accepted.items()}
            if len(set(vals.values())) > 1: diffs[p] = vals
        results[case.__name__] = {"e2fsck_exit": rc, "rejected": {k: list(v.values())[0] for k, v in views.items() if k not in accepted},
                                  "semantic_disagreements": diffs, "views": views}
        print(f"\n### {case.__name__}  e2fsck_exit={rc}  accepted={sorted(accepted)}  rejected={sorted(set(views)-set(accepted))}")
        for p, vals in diffs.items():
            print(f"  DIFF {p}: " + "; ".join(f"{k}={v[0]},{v[1]},{v[2]}" for k, v in vals.items()))
        if not diffs: print("  (no semantic disagreement among accepting readers)")
    json.dump(results, open(os.path.join(W, "pa_results.json"), "w"), indent=1, default=list)

if __name__ == "__main__":
    main()
