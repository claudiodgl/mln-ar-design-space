import sys
L=open(sys.argv[1],encoding='utf-8').read().splitlines()
out=[];cur=None
for l in L:
    if l.startswith('['): cur=[l,'']; out.append(cur)
    elif l.strip().startswith('ABS:') and cur: cur[1]=l.strip()[4:].strip()
for i in map(int,sys.argv[2:]):
    print(i,out[i][0][:120]); print('   ',out[i][1][int(__import__("os").environ.get("N","900")):int(__import__("os").environ.get("M","2500"))]); print()
