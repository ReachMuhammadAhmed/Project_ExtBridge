"""Per year: mainline commits crediting the kernel test robot (Reported-by) and how many carry a lore Link:/Closes: tag.
Usage: python3 -I robot_tags.py <linux_msgs.txt from git log --format='%x1e%H%x1f%ad%x1f%B' --date=short>"""
import sys,re,collections
c=collections.Counter(); l=collections.Counter()
for x in open(sys.argv[1],encoding='utf-8',errors='replace').read().split('\x1e')[1:]:
    h,d,b=x.split('\x1f',2)
    if 'Reported-by: kernel test robot' in b:
        c[d[:4]]+=1
        if re.search(r'^(Link|Closes):.*lore\.kernel\.org',b,re.M): l[d[:4]]+=1
print('year | commits with "Reported-by: kernel test robot" | of which with a lore Link:/Closes: tag')
for y in sorted(c): print(y,'|',c[y],'|',l[y])
