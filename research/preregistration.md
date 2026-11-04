# Pre-registration — Stage 1 kill tests

Written and committed **before** any experiment was run. Results go in `research/stage1_results.md`; this file is not edited afterwards (changes would show up in git history).

Both directions below were proposed by an AI assistant. Per the plan, they are treated as hypotheses only, and must survive execution before any literature work.

---

## Direction B — ext2 deletion artefacts depend on the kernel driver

**Background (to be verified, not assumed):** the ext4 wiki states that ext2 leaves block pointers in a deleted inode, while ext3 zeroes them. Modern kernels can serve ext2 through the ext4 driver (`CONFIG_EXT4_USE_FOR_EXT2=y`). This container's kernel (6.18) has `CONFIG_EXT2_FS` unset, so it uses the ext4 driver.

**Hypothesis H-B.** After `rm` on an ext2 image, the on-disk deleted inode has zeroed `i_block[]` pointers when the ext4 driver performed the delete, but intact pointers when the legacy ext2 driver did.

**Procedure.**
- Fresh image: `mke2fs -t ext2 -b 1024`.
- Test files:
  - F1: 5 KiB (direct blocks only);
  - F2: 100 KiB (single indirect);
  - F3: 400 KiB (double indirect);
  - F4: 5 KiB, deleted while another process holds it open;
  - F5: 100 KiB, truncated to 0 and then removed.
- Each file has known content (deterministic pattern), and its SHA-256 is recorded.
- Steps: mount, write, sync, unmount → mount, delete, unmount → inspect with `debugfs` (`stat <ino>`, `blocks`, `dump`) and a raw read of the inode table.

**Measurements, per file:**
- `i_dtime` set;
- `i_links_count`;
- `i_size`;
- number of non-zero `i_block[0..14]`;
- whether the indirect blocks still contain pointers;
- whether the original content can be recovered byte-exact by following the surviving pointers.

**Kill criteria:**
- **K-B1:** the ext4 driver leaves pointers intact for F1–F3. Then the driver does not change the artefact and B is dead.
- **K-B2:** the legacy ext2 driver also zeroes pointers. Same conclusion.
- Only "ext4 zeroes, ext2 keeps" (or a measurable difference in recoverability) passes.

**Split:** the ext4-driver half runs in this container. The legacy-ext2 half needs a kernel with `CONFIG_EXT2_FS=y` (team WSL2 or QEMU). Until that half runs, B is **undecided**.

---

## Direction A — ext readers disagree on the logical contents of the same image

**Hypothesis H-A.** For at least one hand-crafted ext2 image, two readers that both *accept* the image report a different logical view: a different file list, or different content for the same path. The root cause must be explainable from the on-disk structures.

**Readers (whatever installs here):**
- `debugfs` (libext2fs);
- `e2fsck -fn` (consistency verdict only);
- Linux kernel via the ext4 driver (loop mount, read-only);
- GRUB (`grub-fstest`);
- The Sleuth Kit (`fls` + `icat`);
- 7-Zip.

**Logical view** = sorted list of `(path, type, size, sha256)`.

**Image cases, fixed in advance** (each made by editing a clean `mke2fs` image with `debugfs -w` or raw byte edits):
1. **Cross-linked block:** two files share a data block.
2. **Hidden entry:** a live directory entry placed inside the previous entry's `rec_len` slack.
3. **Size mismatch:** `i_size` larger than allocated blocks (implicit hole) vs. smaller than the data.
4. **Link count:** `links_count = 0` with `dtime` set, but still referenced from a directory.
5. **Bitmap mismatch:** inode bitmap marks a referenced inode free.
6. **Duplicate name:** the same name appears twice in one directory, pointing to different inodes.
7. **File type mismatch:** directory entry `file_type` disagrees with inode `i_mode`.
8. **Illegal name byte:** a name containing `/` or NUL.
9. **Directory loop:** a subdirectory entry points to an ancestor.
10. **Unknown flag:** an unknown `incompat` feature flag is set (expected: some readers reject, others ignore).

**What counts:** only *semantic* disagreements between readers that accept the image. Crashes, rejections and `e2fsck` complaints are recorded but do **not** count toward the gate. Crash-finding is already crowded; see the plan.

**Kill criterion K-A:** zero semantic disagreements across all cases that could be built. Then A is dead or much weaker than claimed.

**Pre-declared expectation** (written down so we can't rationalise afterwards): I expect cases 2, 6 and 7 to be the most likely to produce disagreements, and case 10 to produce only accept-vs-reject differences.

---

## What Stage 1 cannot show
- Passing a kill test only shows **the effect exists**. It says nothing about novelty or significance. Those are Stages 2–3.
- A single kernel version, single tool versions, small N. These are pilots, not results.
