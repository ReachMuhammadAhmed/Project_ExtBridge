# Stage 1: SE × AI × OS intersection map

Built 2026-11-04 following Stage 1 of `methodology.md`. The **AI-method axis is deliberately left blank**: methods are chosen in Stage 3 from the shape of the data.

**Legend**
- ✅ = source confirmed reachable by a direct page fetch from the research environment.
- ✅ᴳ = public GitHub repository confirmed through the GitHub search API (visibility, activity, issue count). Direct page fetches of GitHub were blocked by the research sandbox's network policy, not by GitHub.
- ❌ = unreachable from the research environment (anti-bot challenge, DNS failure or HTTP error). These usually work in a normal browser, but they **do not count toward the gate** until confirmed.
- ▒ = shaded: no specific public data source identified. Out of scope for a laptop-only, single-author project unless a source is found later.

Each cell names one primary source (ID → catalogue below). A source may serve several cells, e.g. the kernel's git history covers maintenance, repair (via `Fixes:` tags) and configuration (Kconfig files).

## Grid

| OS concern \ SE activity | Spec & docs | Testing | Debugging & diagnosis | Repair | Maintenance & evolution | Config mgmt | Performance eng. | Security & vulns | Code review | CI & release |
|---|---|---|---|---|---|---|---|---|---|---|
| **File systems** | ✅ F8 | ❌ F1 | ✅ᴳ F5 | ✅ᴳ F4 | ✅ᴳ K2 | ✅ᴳ F5 | ✅ᴳ F7 | ✅ K8 | ✅ᴳ F6 | ✅ K12 |
| **Storage** | ✅ S10 | ✅ᴳ S5 | ✅ᴳ S7 | ✅ᴳ S9 | ✅ᴳ S4 | ✅ S8 | ✅ᴳ S3 | ✅ K8 | ✅ᴳ S4 | ✅ K12 |
| **Scheduling** | ✅ SC7 | ✅ᴳ M2 | ✅ᴳ SC1 | ✅ᴳ K2 | ✅ᴳ K2 | ✅ᴳ V4 | ✅ᴳ SC2 | ▒ — | ✅ᴳ SC1 | ✅ V8 |
| **Memory management** | ✅ M5 | ✅ᴳ M2 | ✅ᴳ M4 | ✅ K6 | ✅ᴳ K2 | ✅ C3 | ✅ᴳ M3 | ✅ K9 | ✅ᴳ M4 | ✅ᴳ M2 |
| **Kernel code** | ✅ K10 | ✅ᴳ K2 | ✅ K6 | ✅ᴳ K2 | ✅ᴳ K2 | ✅ᴳ K2 | ▒ — | ✅ K9 | ❌ K4 | ✅ K12 |
| **Drivers** | ✅ D5 | ✅ D1 | ✅ R3 | ✅ᴳ K2 | ✅ᴳ K2 | ✅ D1 | ▒ — | ✅ K8 | ❌ D4 | ▒ — |
| **Boot & firmware** | ✅ B9 | ✅ᴳ B5 | ✅ B6 | ✅ᴳ B3 | ✅ᴳ B5 | ✅ᴳ B8 | ▒ — | ✅ B4 | ✅ B1 | ▒ — |
| **Virtualization & containers** | ✅ᴳ V7 | ✅ᴳ V6 | ✅ᴳ V3 | ✅ᴳ V5 | ✅ᴳ V4 | ✅ᴳ V4 | ✅ᴳ SC4 | ✅ K9 | ✅ᴳ V3 | ✅ V8 |
| **Reliability & observability** | ▒ — | ▒ — | ✅ᴳ R1 | ✅ R3 | ✅ S1 | ✅ᴳ R2 | ▒ — | ▒ — | ▒ — | ✅ R4 |
| **Configuration** | ✅ C3 | ▒ — | ✅ C4 | ✅ C5 | ✅ᴳ K2 | ✅ᴳ K2 | ▒ — | ▒ — | ▒ — | ▒ — |

## Gate count (Stage 1 exit criterion: ≥ 8 cells with a named, accessible public data source)

| Count | Cells |
|---|---|
| Confirmed reachable, direct fetch (✅) | 34 |
| Confirmed reachable, GitHub API (✅ᴳ) | 47 |
| **Total confirmed (counts toward gate)** | **81** |
| Named source, unreachable from here (❌, not counted) | 3 |
| Shaded (no source) | 16 |

Confirmed cells per OS concern: File systems: 9, Storage: 10, Scheduling: 9, Memory management: 10, Kernel code: 8, Drivers: 7, Boot & firmware: 8, Virtualization & containers: 10, Reliability & observability: 5, Configuration: 5.

**AI-side result: PASS** (81 ≥ 8; even counting only direct fetches, 34 ≥ 8).
**Still required by the methodology before the gate is final:** the student must personally open each source used in the cells they intend to pursue. The gate criterion says "that you've opened at least once", and the "AI vs. you" rule says AI-named datasets must be opened by the student.

## Source catalogue (checked 2026-11-04)

Status values: reachable / reachable (GitHub API) / needs registration / unreachable from here.

| ID | Source | URL | Status | Note |
|---|---|---|---|---|
| F1 | fstests (xfstests) git | https://git.kernel.org/pub/scm/fs/xfs/xfstests-dev.git | unreachable from here | anti-bot challenge (Anubis); open in browser |
| F3 | linux-ext4 mailing list | https://lore.kernel.org/linux-ext4/ | unreachable from here | anti-bot challenge; open in browser |
| F4 | e2fsprogs GitHub issues | https://github.com/tytso/e2fsprogs/issues | reachable (GitHub API) | public; 126 open issues |
| F5 | OpenZFS GitHub issues | https://github.com/openzfs/zfs/issues | reachable (GitHub API) | public; 1,576 open issues |
| F6 | btrfs-progs GitHub issues & PRs | https://github.com/kdave/btrfs-progs | reachable (GitHub API) | public; 344 open issues |
| F7 | libfuse GitHub issues | https://github.com/libfuse/libfuse/issues | reachable (GitHub API) | public; 61 open issues |
| F8 | Kernel filesystems documentation | https://docs.kernel.org/filesystems/index.html | reachable |  |
| F9 | OpenBenchmarking.org results | https://openbenchmarking.org/ | unreachable from here | Cloudflare challenge; open in browser |
| S1 | Backblaze Drive Stats | https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data | reachable | download links present (not downloaded) |
| S2 | SNIA IOTTA traces | http://iotta.snia.org/ | unreachable from here | DNS failure here; downloads reportedly need licence acceptance + name/email |
| S3 | Alibaba block traces | https://github.com/alibaba/block-traces | reachable (GitHub API) | public; last push 2022 (data may be hosted elsewhere) |
| S4 | fio GitHub repo, issues & PRs | https://github.com/axboe/fio | reachable (GitHub API) | public; 241 open issues |
| S5 | blktests (moved) | https://github.com/linux-blktests/blktests | reachable (GitHub API) | public; old osandov/blktests URL no longer valid |
| S6 | linux-block mailing list | https://lore.kernel.org/linux-block/ | unreachable from here | anti-bot challenge; open in browser |
| S7 | SPDK GitHub issues | https://github.com/spdk/spdk/issues | reachable (GitHub API) | public; 235 open issues |
| S8 | Ceph issue tracker | https://tracker.ceph.com/ | reachable | public browsing; sign-in optional |
| S9 | nvme-cli GitHub issues | https://github.com/linux-nvme/nvme-cli/issues | reachable (GitHub API) | public; 50 open issues |
| S10 | NVM Express specifications | https://nvmexpress.org/specifications/ | reachable | page public; some documents may need membership |
| SC1 | sched_ext (scx) GitHub issues & PRs | https://github.com/sched-ext/scx | reachable (GitHub API) | public; 99 open issues |
| SC2 | Google cluster-data traces | https://github.com/google/cluster-data | reachable (GitHub API) | public; trace files hosted separately (check access) |
| SC4 | Azure Public Dataset | https://github.com/Azure/AzurePublicDataset | reachable (GitHub API) | public |
| SC5 | rt-tests git | https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git | unreachable from here | anti-bot challenge |
| SC6 | Kernel test robot (LKP) reports | https://lore.kernel.org/oe-lkp/ | unreachable from here | anti-bot challenge |
| SC7 | Kernel scheduler documentation | https://docs.kernel.org/scheduler/index.html | reachable |  |
| M1 | linux-mm mailing list | https://lore.kernel.org/linux-mm/ | unreachable from here | anti-bot challenge |
| M2 | Linux Test Project (LTP) | https://github.com/linux-test-project/ltp | reachable (GitHub API) | public; 186 open issues |
| M3 | mmtests | https://github.com/gormanm/mmtests | reachable (GitHub API) | public |
| M4 | jemalloc GitHub issues & PRs | https://github.com/jemalloc/jemalloc | reachable (GitHub API) | public; 370 open issues |
| M5 | Kernel memory-management admin docs | https://docs.kernel.org/admin-guide/mm/index.html | reachable |  |
| K2 | Linux kernel GitHub mirror (git history) | https://github.com/torvalds/linux | reachable (GitHub API) | public mirror; issues disabled (use for code/history only) |
| K4 | Patchwork (kernel patch review) | https://patchwork.kernel.org/ | unreachable from here | anti-bot challenge |
| K6 | syzbot upstream dashboard | https://syzkaller.appspot.com/upstream | reachable |  |
| K8 | NVD CVE API | https://services.nvd.nist.gov/rest/json/cves/2.0 | reachable | JSON; unauthenticated is rate-limited |
| K9 | OSV vulnerability database | https://osv.dev/list?ecosystem=Linux | reachable |  |
| K10 | Kernel documentation | https://docs.kernel.org/ | reachable |  |
| K11 | KernelCI dashboard | https://dashboard.kernelci.org/ | unreachable from here | anti-bot challenge |
| K12 | regzbot regression tracker | https://linux-regtracking.leemhuis.info/regzbot/mainline/ | reachable |  |
| D1 | Linux Hardware probes database | https://linux-hardware.org/ | reachable |  |
| D4 | dri-devel mailing list | https://lore.kernel.org/dri-devel/ | unreachable from here | anti-bot challenge |
| D5 | Kernel driver-API docs | https://docs.kernel.org/driver-api/index.html | reachable |  |
| B1 | coreboot Gerrit code review | https://review.coreboot.org/ | reachable | UI needs JavaScript; public REST /changes/ returns JSON |
| B3 | fwupd GitHub issues | https://github.com/fwupd/fwupd/issues | reachable (GitHub API) | public; 145 open issues |
| B4 | LVFS firmware service | https://fwupd.org/ | reachable |  |
| B5 | EDK2 (UEFI reference) GitHub | https://github.com/tianocore/edk2 | reachable (GitHub API) | public; 1,458 open issues |
| B6 | GRUB bug tracker | https://savannah.gnu.org/bugs/?group=grub | reachable |  |
| B8 | systemd GitHub issues | https://github.com/systemd/systemd/issues | reachable (GitHub API) | public; 3,387 open issues |
| B9 | UEFI specifications | https://uefi.org/specifications | reachable | some downloads may require a form |
| V1 | QEMU GitLab issues | https://gitlab.com/qemu-project/qemu/-/issues | unreachable from here | HTTP 404 from here (cause unknown); open in browser |
| V3 | moby (Docker engine) GitHub issues & PRs | https://github.com/moby/moby | reachable (GitHub API) | public; 3,953 open issues |
| V4 | Kubernetes GitHub issues | https://github.com/kubernetes/kubernetes/issues | reachable (GitHub API) | public; 3,223 open issues |
| V5 | runc GitHub issues | https://github.com/opencontainers/runc/issues | reachable (GitHub API) | public; 203 open issues |
| V6 | Firecracker GitHub issues | https://github.com/firecracker-microvm/firecracker/issues | reachable (GitHub API) | public; 124 open issues |
| V7 | OCI runtime specification | https://github.com/opencontainers/runtime-spec | reachable (GitHub API) | public |
| V8 | Kubernetes TestGrid (CI results) | https://testgrid.k8s.io/ | reachable |  |
| R1 | Loghub system-log datasets | https://github.com/logpai/loghub | reachable (GitHub API) | public |
| R2 | Public postmortems collection | https://github.com/danluu/post-mortems | reachable (GitHub API) | public |
| R3 | Launchpad: Ubuntu kernel bugs | https://bugs.launchpad.net/ubuntu/+source/linux | reachable |  |
| R4 | Ubuntu error tracker | https://errors.ubuntu.com/ | reachable | page loads; data views need JavaScript |
| C1 | Kernel Kconfig source (Elixir) | https://elixir.bootlin.com/linux/latest/source/Kconfig | unreachable from here | anti-bot challenge; use K2 instead |
| C3 | Kernel sysctl documentation | https://docs.kernel.org/admin-guide/sysctl/index.html | reachable |  |
| C4 | Unix & Linux Stack Exchange | https://unix.stackexchange.com/ | reachable |  |
| C5 | Server Fault | https://serverfault.com/ | reachable |  |
| C6 | Stack Exchange API | https://api.stackexchange.com/2.3/questions?site=unix&tagged=linux-kernel | reachable | JSON; free without key (lower quota) |

**Notes on the checks**
- *Unreachable from here* reflects the research sandbox's network (anti-bot pages on kernel.org, lore, Elixir and freedesktop GitLab; Cloudflare on OpenBenchmarking; DNS failure for SNIA IOTTA). It does not mean the source is offline.
- **None was classified as "needs registration"** from a confirmed page. SNIA IOTTA reportedly requires licence acceptance plus name and email (secondary sources only). Some UEFI and NVMe documents may need a form or membership.
- For data hosted outside GitHub (Google cluster-data, Alibaba traces, Azure dataset, Backblaze downloads), only the landing page was confirmed. Check download access when you open them.
- Sources used in the grid: 52 of 63 catalogued.
