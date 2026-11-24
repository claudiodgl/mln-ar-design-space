import sys,re
src,dst=sys.argv[1],sys.argv[2]
out=[];cur=None
for line in open(src,encoding='utf-8'):
    line=line.rstrip('\n')
    if line.startswith('['):
        cur=[line,''];out.append(cur)
    elif line.strip().startswith('ABS:') and cur: cur[1]=line.strip()[4:].strip()
    elif cur and cur[1]: cur[1]+=' '+line.strip()
with open(dst,'w',encoding='utf-8') as f:
    for t,a in out:
        f.write(t+'\n   '+a[:260]+'\n')
print(len(out))
