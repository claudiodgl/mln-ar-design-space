import sys
sys.stdout.reconfigure(encoding="utf-8")
ids=set(sys.argv[1].split(','))
t=open('batch8.txt',encoding='utf-8').read().split('\n')
cur=None
for l in t:
    if l.startswith('['):
        cid=l[1:l.index(']')].replace('R2-C','')
        cur = cid in ids
        if cur: print('\n'+l[:120])
    elif cur and l.strip(): print(l.strip()[4:1100] if l.strip().startswith('ABS:') else l.strip()[:600])
