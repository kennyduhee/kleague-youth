import re
LABEL={"U11":"U11 (초5)","U12":"U12 (초6)","U14":"U14 (중2)","U15":"U15 (중3)","U17":"U17 (고2)","U18":"U18 (고3)"}
D={}
cur=None
for ln in open('/home/claude/seoul_raw.txt',encoding='utf-8').read().split('\n'):
    if not ln.strip(): continue
    if ln[0]=='@':
        k,i=ln[1:].split('|'); cur=D[k]={"id":int(i),"label":LABEL[k],"years":[]}
    elif ln[0]=='#':
        a=ln[1:].split('|'); cur["years"].append([int(x) for x in a]+[[]])
    else:
        ty,name,res,p,w,d,l,gf,ga,per=ln.split('|')
        m=re.match(r'\[([^\]]+)\]\s*(.*)',name); br,rest=m.group(1),m.group(2).strip()
        rest=re.sub(r'^20\d\d\s+','',rest)
        br=re.sub(r'^U1\d_','',br)
        if ty=='C':
            loc=br.split('/')[-1].strip()
            nm=f"{rest}({loc})"
        else:
            nm=f"{rest} [{br}]"
        s,e=per.split('-')
        f=lambda x:f"{x[:2]}.{x[2:]}" if x else ''
        cur["years"][-1][7].append([ty,nm,res or '-',int(p),int(w),int(d),int(l),int(gf),int(ga),f(s)+'~'+f(e)])
SHEETS=[("u11","U11","초5 · 초등부",["U11"]),("u12","U12","초6 · 초등부",["U12"]),("u14","U14","중2 · 오산중",["U14"]),("u15","U15","중3 · 오산중",["U15"]),("u17","U17","고2 · 오산고",["U17"]),("u18","U18","고3 · 오산고",["U18"])]
