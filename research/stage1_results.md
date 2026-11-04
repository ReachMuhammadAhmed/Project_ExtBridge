# Stage 1 results: kill tests (2026-11-04)

The pre-registration is in `preregistration.md` (commit `50f250b`, made before any run). Raw outputs are in `pilots/`. The images are not committed; the scripts regenerate them.

**Environment**
- Kernel: 6.18.44 (`CONFIG_EXT2_FS` unset, `CONFIG_EXT4_USE_FOR_EXT2=y`)
- e2fsprogs 1.47.0
- The Sleuth Kit (TSK) 4.12.1
- GRUB 2.12-1ubuntu7.3 (`grub-fstest`)
- 7-Zip 23.01

These are single versions with small N. **These are pilots, not results.**

---

## Direction B: ext2 deletion artefacts vs. kernel driver → **UNDECIDED** (half done)

### ext4 driver serving ext2 (executed: `pilots/pb/output_ext4driver_6.18.txt`)
All 5 cases behaved the same: F1 direct, F2 single-indirect, F3 double-indirect, F4 deleted while held open, F5 truncated and then removed.
- `links=0`, `dtime` set, `i_size=0`;
- **all 15 `i_block[]` pointers are zero on disk**;
- following the inode recovers nothing;
- the content patterns are still present in free blocks, so recovery is possible only by carving;
- `e2fsck -fn` is clean.

Conclusion: under the ext4 driver, the classic "follow the deleted inode's pointers" ext2 recovery does **not** work.

### Legacy ext2 driver: not executed
- Requires a kernel with `CONFIG_EXT2_FS=y`.
- I tried to build a User-Mode Linux kernel in this container. The session's permission policy blocked compiling and running downloaded kernel source, and I did not work around it.

**Static evidence only.** In `fs/ext2/inode.c` (Linux mainline, `ext2_evict_inode`), the inode is written to disk (`sync_inode_metadata`) with `dtime` set **before** `i_size = 0` and `ext2_truncate_blocks()` zero the in-memory pointers. The later `mark_inode_dirty()` is made on an inode that is being freed. My reading is that this write is not issued, so on-disk pointers would survive. This matches the kernel wiki's statement that ext2 leaves pointers alone.

**This is a prediction, not a measurement.** K-B1 did not trigger. K-B2 remains untested.

---

## Direction A: readers disagree on logical contents → **GATE PASSED** (effect exists)

Setup: 10 pre-registered cases × 5 readers (`pilots/pa/output_run1.txt`, `pa_results_run1.json`). Each was then **verified per reader by hand** to remove harness artefacts.

| Case | Outcome after manual verification | Counts for gate? |
|---|---|---|
| 07 dirent `file_type`=DIR, inode = regular file | **Kernel and debugfs:** regular file. **GRUB:** treats it as a directory and **parses the file's contents as directory entries**; it lists an entry whose name comes from the file's data. **TSK:** reports `d/r` (shows both types). **7-Zip:** rejects the whole image. | **Yes, strongest.** Root cause: GRUB trusts the directory-entry type; Linux trusts the inode mode. Whoever controls a regular file's content controls what GRUB sees as a directory. |
| 08 name contains `/` | **Kernel:** `getdents` on the root fails with EIO, so the directory can't be listed, though files can still be opened by path. **TSK:** shows `b/txt`, which looks like file `txt` inside a directory `b`. **7-Zip:** renames it `b_txt`. **GRUB:** lists it, but reading it fails. | **Yes.** Directory enumeration differs; the forensic path display is ambiguous. |
| 10 unknown `incompat` flag | **Kernel and debugfs:** refuse (correct per spec). **TSK and 7-Zip:** ignore the flag and read everything. **GRUB:** shows an **empty file system with no error**. | Partly. Three different behaviours; GRUB's silent "empty" is notable. |
| 04 `links_count=0` but still referenced | **Kernel:** refuses to read (EUCLEAN). **All others:** return the content. | Weak (accept vs. reject at file level). |
| 02 entry unlinked, inode still allocated | 7-Zip shows it under `[UNKNOWN]/16`; TSK has a `$OrphanFiles` virtual dir; others hide it. | No. This is by design. |
| 09 directory loop | Traversal policy differs: kernel ELOOP; debugfs and GRUB recurse until our depth limit; TSK stops after one level; 7-Zip rejects. | Weak. |
| 06 duplicate name | **Harness artefact.** Every reader lists both entries and resolves `/a.txt` to the first one (inode 12). Only extract-to-disk tools (debugfs `rdump`, `7z x`) overwrite one copy with the other. | No (minor extraction note only). |
| 01 cross-linked block, 03 size mismatch | All readers agree. | No. |
| 05 inode bitmap marks a referenced inode free | 7-Zip rejects; the others agree. | No. |

**Against the pre-declared expectation** (written before the run): I expected cases 2, 6 and 7 to disagree most. Case 7 did. Cases 6 and 2 **did not**. Case 8 was an unexpected disagreement. Case 10 produced more than accept-vs-reject behaviour (GRUB went silent and empty).

## What this does and does not show
- Shown: real, explainable meaning-level disagreements exist between GRUB and Linux (07, 10) and between forensic tools and Linux (08), with one GRUB, one TSK and one 7-Zip version.
- **Not shown:**
  - novelty (GRUB's dirent-type behaviour may be known or intended);
  - exploitability (no crafted demonstration yet, e.g. a GRUB-only `grub.cfg`);
  - significance;
  - other versions, U-Boot, lwext4, ext4-feature images.

  These belong to Stage 2 (prior art) and Stage 3 (reviewer pre-mortem).
- Harness lesson: 1 of 5 apparent disagreements (case 06) was an artefact. **Every pilot "finding" needs per-reader manual verification.**

## Next
- **A → Stage 2:** adversarial prior-art search.
  - Queries: "GRUB ext2 file_type directory entry", "file system parser differential bootloader", "forensic tool file system interpretation discrepancy".
  - CVE/OSV searches for GRUB, TSK and 7-Zip ext issues.
  - Check whether GRUB documents the dirent-type trust as intended behaviour.
- **B:** needs the legacy-ext2 run, either by permitting the UML kernel build here or by the team running `pilots/pb/run_pb.sh` on a kernel with `CONFIG_EXT2_FS=y`.
