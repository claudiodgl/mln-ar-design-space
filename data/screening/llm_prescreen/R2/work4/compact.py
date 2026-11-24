import sys,re
L=open(sys.argv[1],encoding='utf-8').read().splitlines()
out=[];cur=None
for l in L:
    if l.startswith('['):
        cur=[l,'']; out.append(cur)
    elif l.strip().startswith("ABS:") and cur: cur[1]=l.strip()[4:].strip()
for i,(t,a) in enumerate(out):
    print(i, t[:200], '||', a[:int(sys.argv[2])])
