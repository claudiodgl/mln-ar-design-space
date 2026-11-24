"""Manual venue corrections for OpenAlex-generated supplement.bib entries."""
import re, sys
p = sys.argv[1]
t = open(p, encoding="utf8").read()

def setfield(key, field, value, kind=None):
    global t
    m = re.search(r"@(\w+)\{" + re.escape(key) + r",(.*?)\n\}", t, re.S)
    assert m, key
    body = m.group(2)
    body = re.sub(r"\n  (booktitle|journal|howpublished) = \{.*?\},?", "", body)
    body = body.rstrip(",") + f",\n  {field} = {{{value}}}"
    k = kind or m.group(1)
    t = t[:m.start()] + f"@{k}{{{key},{body}\n}}" + t[m.end():]

setfield("Page2021prisma", "journal", "BMJ", "article")
t = t.replace("pages = {n71--n71}", "volume = {372},\n  pages = {n71}")
setfield("Manshaei2019bionets", "journal", "Proceedings of the ACM on Human-Computer Interaction (EICS)", "article")
setfield("Drochtert2015magiclens", "booktitle", "SIGGRAPH Asia 2015 Mobile Graphics and Interactive Applications")
setfield("Durant2024hybrid", "booktitle", "EuroVis 2024 Posters")
setfield("Kyaw2026mindmap", "booktitle", "ACM SIGGRAPH 2026 Posters")
setfield("Bhattacharya2026nodebots", "booktitle", "Adjunct Proceedings of the ACM Symposium on User Interface Software and Technology (UIST)")
setfield("Tanhaei2023datar", "booktitle", "Proceedings of the ACM International Conference on Interactive Media Experiences (IMX), Demos")
setfield("Zhao2017egocentric", "booktitle", "SIGGRAPH Asia 2017 Symposium on Visualization")
open(p, "w", encoding="utf8").write(t)
print("fixed")
