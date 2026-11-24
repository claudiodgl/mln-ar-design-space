import csv
from collections import Counter
base = r'C:\Users\TestAnvändare\Documents\MLN_method\screening_ai\R2'
t = open(base + r'\batch9.txt', encoding='utf-8').read().splitlines()
cids = [l[1:l.index(']')] for l in t if l.startswith('[')]
def rng(s): return [int(x) for x in s.split()]
D = {}
for i in rng("46 32 45 103 64 117 56 78 202 256 295 361 532 203 348 171 325 135 197 227 133 74 88 104 125 38 248 258 261 179 243 391 345 499 352 344 324 169"): D[i] = ('exclude', 'E1', '')
for i in rng("3 48 51 52 54 59 62 66 68 69 75 77 89 90 91 95 97 99 100 106 107 111 113 131 134 136 137 140 143 145 146 149 155 157 158 164 173 174 176 177 178 189 196 217 224 234 266 273 275 277 280 285 288 291 358 363 364 368 373 401 420 433 448 461 465 466 469 493 511 30 31"): D[i] = ('exclude', 'E3', '')
for i in rng("1 19 20 26 29 34 35 36 37 39 43 44 50 76 151 232 294 284 296 270 238 455 198 250 186 187 188 208 223 259 263 366 384 431 477 513 534 316 236 205"): D[i] = ('exclude', 'E5', '')
for i in rng("8 25 16 42 84 110 156 221 253 257 365 407"): D[i] = ('exclude', 'E6', '')
for i in rng("172 255 271 374 412 444 460 478 536"): D[i] = ('exclude', 'E7', '')
B = {12: 'Systematic review/design space of immersive analytics', 147: 'Review of data vis in mobile AR apps', 181: 'Big data vis with AR/VR: challenges, agenda',
     212: 'Situated analytics chapter, Immersive Analytics book', 228: 'Immersive Analytics book (LNCS 11190)', 314: 'Systematic review of AR maritime data visualisation',
     346: 'Systematic review of AR data visualization in education', 518: 'Interaction model for ubiquitous/cross-device analytics'}
for k, v in B.items(): D[k] = ('background', 'B', v)
I = {58: ('I2', 'Semi-immersive 3D environment for phylogenetic trees'), 322: ('I2', 'VR browser visualizing page link structure (history tree)'),
     387: ('I2', 'Immersive AR tool for brain region-disease relations'), 482: ('I2', 'VR vs 2D visualization of package dependency ecosystem'),
     123: ('I1', 'GraphTrail-like heterogeneous network exploration; verify identity'),
     2: ('I4', 'View layout for situated analytics in immersive vis'), 6: ('I4', 'AR visualization bound to physical objects in smart environments'),
     11: ('I4', 'Proxsituated visualization model with physical referents'), 23: ('I4', 'Situated visualizations of environmental footprints in urban space'),
     79: ('I4', 'AR situated media and timelines registered to historic sites'), 87: ('I4', 'In-situ medical AR visualization method (anchored)'),
     96: ('I4', 'Context-aware AR visualization of pervasive services in place'), 163: ('I4', 'AR sensor data visualization anchored on sailboat'),
     194: ('I4', 'MR thermal data overlaid on physical experiment'), 220: ('I4', 'AR visualization of hidden underground facilities in situ'),
     225: ('I4', 'Situated analytics app augmenting physical products'), 340: ('I4', 'AR in-field situated observation visualization'),
     341: ('I4', 'Context-aware AR explanation visualizations on physical objects'), 349: ('I4', 'AR sailing navigation data interface evaluation'),
     362: ('I4', 'Role-based AR HMD sailing data visualizations'), 381: ('I4', 'MR weather data placed on real trees'),
     382: ('I4', 'AR rowing coach situated data visualization'), 395: ('I4', 'Adaptive multi-view layout for situated visualizations'),
     405: ('I4', 'AR thermal data overlaid on hot physical surfaces'), 410: ('I4', 'Adaptive OST AR volume rendering using real background'),
     421: ('I4', 'AR postural visualization anchored on skier body'), 423: ('I4', 'Head- vs boat-stabilized AR data placement (anchoring)'),
     426: ('I4', 'AR on-body vs detached stroke visualization'), 427: ('I4', 'Body-based AR data visualization next to people'),
     458: ('I4', 'Situated visualization attached to moving swimmers'), 471: ('I4', 'Room-scale AR visualizations using physical space'),
     491: ('I4', 'Spatially situated AR motion guidance encodings'), 535: ('I4', 'AR timelines: relative position and situatedness')}
for k, (c, n) in I.items(): D[k] = ('include', c, n)
U = {5: 'Proxemic maps in immersive vis; check AR/spatial context', 9: 'Level-of-detail AR; no abstract, check AR viz technique',
     14: 'X-ray vision AR metaphors for occluded objects; check', 21: 'Real world as canvas; likely situated-vis position paper',
     28: 'Field sketch-based immersive geology analytics; check AR anchoring', 33: 'Mobile devices and AR for data analysis; no abstract',
     41: 'VR knowledge-database demonstrator; check graph visualization', 55: 'AR two-handed tangible panel interface; not vis-specific',
     86: 'AR interface for wireless sensor networks; check network vis', 161: 'AR surgical navigation depth visualization; medical anchoring',
     162: 'Medical AR distance coding visualization; check', 175: 'Matrix of diverse protein relation types; possibly multi-relational',
     184: 'See-through HMDs plus tiled display; check AR technique', 185: 'Gaze-directed AR/MR HMD immersive visualization; check',
     192: 'AR window showing machine data; check physical anchoring', 193: 'HoloLens bee drift analytics on 3D terrain; check anchoring',
     204: 'Software repositories in VR; check graph structure', 210: 'AR nature metaphor for factory data; no abstract',
     230: 'VR software module islands; check dependency graph', 242: 'OmicsNet 3D multi-omics network; possibly layered layout',
     249: 'AR augmented airtable motion physics; check situated vis', 264: 'Software vis metaphors in VR; check graph metaphors',
     267: 'MR visual programming anchored to IoT devices; node graph', 279: 'AR white matter pathway dissection; check anchoring',
     282: 'AR heat conduction lab visualization; situated data on rods', 286: 'Software analytics in immersive AR; check graph vis',
     292: 'Cyber security vis in VR; may include network graphs', 300: 'TGView3D theory graphs in 3D, reportedly VR',
     302: 'Software city plus call traces in VR; check graph', 303: 'Software architecture evolution in VR; check dependencies',
     347: 'AR literature topic relation explorer; check graph vis', 351: 'Situatedness of data representations; check AR/physical',
     392: 'Geo-constrained 3D graph over map; possibly layered', 393: 'Large geo climate networks, multiple types; check layers',
     398: 'Immersive analytics frame of reference design; check AR', 400: 'Free-hand no-code AR vis creation; check',
     403: 'AR interaction with tomography visualizations; check anchoring', 413: 'Immersive VR storyline (dynamic relations) visualization',
     416: 'AR recoloring using real-world context; check vis technique', 429: 'Egocentric visualization while running; check AR situated',
     430: 'Context-aware AR recoloring for maintenance; check', 432: 'Microservice dependency graph 2D vs 3D; check immersion',
     435: 'Microservice evolution visualization; check 3D/AR graph', 440: 'Mobile AR health data visualizations; check anchoring',
     446: 'Microservice architecture 3D/VR/AR graph model', 447: 'VR software visualization customization; check graph',
     454: '2D/3D kinase network vis; check VR export', 457: 'Situated sports guidance AR/VR; check',
     462: 'Mobile AR sports capture replay; check situated vis', 468: 'MR visualizations of future movement predictions; check',
     470: 'MR in-situ direct volume rendering; check anchoring', 492: 'AR vs desktop environmental visualizations; check situatedness',
     497: 'Microservice change-impact visualization; check 3D/AR graph', 508: 'Dynamic multivariate network communities; check time-slice layers',
     509: 'AR room-scale timeline authoring; spatial context', 515: 'AR data ribbon beyond frame; demo paper',
     521: 'XR authoring tool visualizing complex dependency graphs'}
for k, n in U.items(): D[k] = ('unsure', '', n)
assert all(1 <= k <= len(cids) for k in D)
with open(base + r'\batch9_decisions.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['cid', 'decision', 'code', 'note'])
    for i, c in enumerate(cids, 1):
        w.writerow([c, *D.get(i, ('exclude', 'E2', ''))])
rows = [D.get(i, ('exclude', 'E2', '')) for i in range(1, len(cids) + 1)]
print(len(cids), Counter(r[0] for r in rows), Counter(r[1] for r in rows))
print(sum(1 for _ in open(base + r'\batch9_decisions.csv', encoding='utf-8')) - 1)
