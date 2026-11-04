#!/usr/bin/env bash
# P-B: ext2 deletion artefacts under whichever driver this kernel uses for ext2.
# Usage: sudo ./run_pb.sh <workdir>   (needs root + loop devices)
set -euo pipefail
W=${1:-./pb_work}; mkdir -p "$W"; IMG="$W/pb.img"; MNT="$W/mnt"; mkdir -p "$MNT"
pat(){ python3 -c "import sys;n=int(sys.argv[1]);s=sys.argv[2].encode();sys.stdout.buffer.write((s*(n//len(s)+1))[:n])" "$1" "$2"; }
rm -f "$IMG"; dd if=/dev/zero of="$IMG" bs=1M count=8 status=none
mke2fs -q -t ext2 -b 1024 -F "$IMG"
echo "kernel: $(uname -r)"; zcat /proc/config.gz 2>/dev/null | grep -E 'CONFIG_EXT2_FS=|CONFIG_EXT4_USE_FOR_EXT2' || echo "config: unavailable"
mount -o loop -t ext2 "$IMG" "$MNT"; echo "driver serving mount: $(grep " $(realpath $MNT) " /proc/mounts | awk '{print $3}') ($(dmesg 2>/dev/null | grep -i 'ext[24]' | tail -1 | sed 's/^.*\] //'))"
pat 5120   "F1-direct-"   > "$MNT/f1"
pat 102400 "F2-single-ind-" > "$MNT/f2"
pat 409600 "F3-double-ind-" > "$MNT/f3"
pat 5120   "F4-open-fd-"  > "$MNT/f4"
pat 102400 "F5-truncated-" > "$MNT/f5"
sync
for f in f1 f2 f3 f4 f5; do echo "$f $(stat -c %i "$MNT/$f") $(sha256sum < "$MNT/$f" | cut -c1-16)"; done > "$W/inodes.txt"
umount "$MNT"; mount -o loop -t ext2 "$IMG" "$MNT"
exec 3<"$MNT/f4"            # hold f4 open across its unlink
rm "$MNT/f1" "$MNT/f2" "$MNT/f3" "$MNT/f4"
: > "$MNT/f5"; rm "$MNT/f5"
exec 3<&-                   # close -> f4 really freed now
sync; umount "$MNT"
echo "== per-file results (inode: links dtime size nonzero_i_block recovered_sha) =="
while read -r f ino sha; do
  st=$(debugfs -R "stat <$ino>" "$IMG" 2>/dev/null)
  links=$(grep -o 'Links: [0-9]*' <<<"$st" | awk '{print $2}')
  dtime=$(grep -q 'dtime:' <<<"$st" && echo set || echo none)
  size=$(grep -o 'Size: [0-9]*' <<<"$st" | head -1 | awk '{print $2}')
  # raw i_block[] read straight from the inode table (location via debugfs imap)
  loc=$(debugfs -R "imap <$ino>" "$IMG" 2>/dev/null | grep -o 'located at block [0-9]*, offset 0x[0-9a-f]*')
  blk=$(awk '{print $4}' <<<"$loc" | tr -d ,); off=$(awk '{print $6}' <<<"$loc")
  nz=$(python3 -c "
import sys
img,blk,off=sys.argv[1],int(sys.argv[2]),int(sys.argv[3],16)
with open(img,'rb') as fh: fh.seek(blk*1024+off); b=fh.read(128)
ib=[int.from_bytes(b[40+4*i:44+4*i],'little') for i in range(15)]
print(f'{sum(1 for x in ib if x)}/15 direct0={ib[0]} ind={ib[12]} dind={ib[13]}')" "$IMG" "$blk" "$off")
  # attempt recovery: follow surviving pointers with debugfs (works only if pointers present)
  rec=$(debugfs -R "cat <$ino>" "$IMG" 2>/dev/null | sha256sum | cut -c1-16)
  tag=$(case $f in f1) echo F1-direct-;; f2) echo F2-single-ind-;; f3) echo F3-double-ind-;; f4) echo F4-open-fd-;; f5) echo F5-truncated-;; esac)
  onDisk=$(grep -c -a -o -- "$tag" "$IMG" || true)
  echo "$f ino=$ino links=$links dtime=$dtime size=$size nonzero_iblock=$nz orig_sha=$sha inode_follow_sha=$rec pattern_occurrences_left_on_disk=$onDisk"
done < "$W/inodes.txt"
e2fsck -fn "$IMG" >/dev/null 2>&1; echo "e2fsck -fn exit: $?"
