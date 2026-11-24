import sys, csv, re, os
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
D = {}
def s(ids, dec, code, note=''):
    for i in ids.split():
        k = 'R2-C' + i
        assert k not in D, k
        D[k] = (dec, code, note)
inc = lambda i, c, n: s(i, 'include', c, n)
uns = lambda i, n: s(i, 'unsure', '', n)
bg = lambda i, n: s(i, 'background', 'B', n)

# includes
inc('13491','I4','situated/embedded AR vis for medical guidance')
inc('13553','I4','AR XCT data alongside real objects; possible preprint of C14102')
inc('14102','I4','AR XCT material data anchored on real objects')
inc('13555','I4','in situ MR visualizations in physical architectural space')
inc('13580','I4','physical landmarks for AR vis spatial memory')
inc('13586','I4','AR overviews for spatially distributed physical tasks')
inc('13599','I4','hybrid UI for immersive situated analytics')
inc('13604','I4','interaction design for situated vis in public spaces')
inc('13637','I4','situated AR air-quality visualization')
inc('13696','I4','in-situ AR robot visualization authoring')
inc('13740','I4','tangible authoring of embedded-object vis in MR')
inc('13760','I4','situated vs proxied immersive dam visualization')
inc('13811','I4','mobile AR in-situ data vis embedded in videos')
inc('13812','I4','handheld-projector situated analytics')
inc('13816','I4','situated brushing and linking highlighting')
inc('13826','I4','AR situated multimodal sensor data visualization')
inc('13829','I4','AR co-located IA, physical space partitioning')
inc('13900','I4','design space of abstract/concrete immersive vis transitions')
inc('13916','I4','AR blended with shape-changing data physicalization')
inc('14005','I4','situated AR labels 2D vs 3D in maintenance')
inc('14044','I4','proxsituated XR football visualizations')
inc('14047','I4','situated AR visualization for TCM formulas')
inc('14196','I4','selection of physical referents in situated AR')
inc('14225','I4','AR in-situ vis of autonomous factory processes')
inc('14255','I4','situated AR vis for maintenance; scoping review + study')
inc('14291','I4','tangible interface for MR cutaway vis (no abstract)')
inc('14357','I4','AR motion-intent vis anchored to real robots')
inc('14413','I4','ambient AR vis embedded in surroundings')
inc('14427','I4','AR situated analytics obstruction mitigation in HRC')
inc('14467','I4','ground-anchored situated AR visualizations')
inc('14513','I4','embedded vs situated AR feedback comparison')
inc('14531','I4','AR overlay of mechanisms on physical observations')
inc('14550','I4','situated temporal filtering mobile AR photos')
inc('14602','I4','in-situ AR thermal mesh on urban trees')
inc('14631','I4','tangible active proxies for physical data referents')
inc('14675','I4','AR privacy info anchored to smart-home devices')
inc('14681','I4','AR glasses radio environment situated vis')
inc('14706','I4','design space tangible media immersive data exploration')
inc('14708','I4','AR inter-object relationship graph anchored to physical objects')
inc('14710','I4','situated brushing and linking in VR/AR')
inc('14720','I4','situated AR windshield cues; dissertation, check E5')
inc('14775','I4','situated feedforward vis for AR target selection')
inc('14795','I4','AR visual cues anchored on phantom for needle insertion')
inc('14799','I4','AR visualization of wireless propagation in situ')
inc('13804','I2','VR exploration of AI-generated graphs (quantum optics)')
inc('13886','I2','AR graph algorithm visualization (education)')
inc('13890','I2','Graph2VR linked-data graphs in VR')
inc('14166','I2','MR knowledge graph visualization')
inc('14377','I2','AR node-link problem diagrams')
inc('14480','I2','VR network topology visualization')
inc('14737','I2','projection-AR tangible graph mind-map')
inc('14804','I2','immersive collaborative ontology graph manipulation')
inc('14359','I1','dynamic historical networks as small multiples (juxtaposed slices)')
inc('14448','I5','hybrid matrix/node-link model for clustered networks')

inc('14649','I3','3D-printed tactile graph/tree diagrams for blind students')
uns('13920','AR on-site MEP installation framework; anchoring')
# background
bg('13707','situated analytics process framework/mantra')
bg('13931','overview of immersive analytics AR/VR (low venue)')
bg('13979','systematic review tangible vis widgets')
bg('14231','review situated visualization cultural heritage')
bg('14355','situated vis superpowers position paper, AR lens')
bg('14540','chapter on immersive interaction incl tangible/spatial')
bg('14701','framework quantifying diegesis in AR situated vis')

# unsure
uns('13475','embedded urban temporal vis, no abstract; likely AR (I4)')
uns('13482','AR complex spatial data vis, no abstract')
uns('13490','OST AR vis colour vs environment background (I4?)')
uns('14748','OST AR colour vis vs environment background (I4?)')
uns('13502','AR vis of topic relationships; likely graph (I2)')
uns('13506','mobile AR + large display on public maps (I4?)')
uns('13551','AR vs VR immersive analytics comparison')
uns('13552','AR lab with real-time measurement data; no abstract')
uns('13556','VR collaborative software vis; maybe graph (I2)')
uns('13610','AR wastewater infrastructure planning; no abstract')
uns('13655','AR brain MRI in-situ guidance; anchoring unclear')
uns('13701','AR flow streamlines; anchoring unclear')
uns('13711','mobile device + AR table vis hybrid')
uns('13724','STEP: graph sequence as juxtaposed edge plots (I1?)')
uns('13734','AR X-ray vision; no abstract')
uns('13753','KG maps/graphs/sets over time; data sculpture metaphor')
uns('13775','mobile AR geospatial vis collaboration')
uns('13787','in-situ referents for immersive scale perception')
uns('13813','comparative vis of multiple causal graphs (I1?)')
uns('13847','AR robot programming vis in robot frame')
uns('13869','mobile AR airflow vis on AC; no abstract')
uns('13891','AR/MR situated interface design method construction')
uns('13914','immersive WiFi vis in environmental context')
uns('13930','book chapter AR data visualization')
uns('13932','XR financial transactions; possibly network')
uns('13992','graph-based multi-domain urban data; maybe multilayer')
uns('13996','immersive brain DTB vis; network content unclear')
uns('14002','location-based multimodal vis; AR unclear')
uns('14029','VR digital threads (graphs?); no abstract')
uns('14049','VR visceralisation of box-and-arrow state-transition models')
uns('14085','MR history tool around physical screen')
uns('14095','IA hydropower; AR/situated unclear')
uns('14131','OST AR display limits in immersive analytics')
uns('14145','immersive literature sensemaking; maybe citation network')
uns('14165','tangible UI MR medical volume; no abstract')
uns('14186','RadTrix hybrid for bipartite diseasome (I5?)')
uns('14268','design space spatially-embedded lenses (I4?)')
uns('14340','AR figures for astronomy publications')
uns('14362','MR + 2D hybrid tissue maps')
uns('14367','VR node-link vis of ANN structure (I2?)')
uns('14399','MR game analytics with spatial reconstruction')
uns('14431','AR immersive analytics manufacturing; no abstract')
uns('14433','augmented tangible spatial interaction; no abstract')
uns('14563','tangible geospatial UI for migration flows (I3?)')
uns('14615','artists/exhibitions networks; possibly multilayer')
uns('14653','muxviz multilayer library; vis component? (I1)')
uns('14655','immersive navigation of connected engineering models')
uns('14661','brain networks across scales; multilevel?')
uns('14696','AR software structure + runtime profiling')
uns('14724','AR dense-target selection in data vis')
uns('14805','XR client for CIDOC-CRM linked-data graph (I2?)')

# excludes
s('13532 13719 14182 14320 14429 14633 14647 14650', 'exclude', 'E4')
s('13762 14680', 'exclude', 'E5')
s('14578', 'exclude', 'E6')
s('14032 14118 14138 14154 14160 14419 14532', 'exclude', 'E7')
s('''13488 13505 13511 13533 13535 13541 13562 13573 13596 13608 13639 13676 13702
13713 13726 13736 13754 13755 13772 13823 13827 13899 13924 13933 13956 13972 14026
14039 14062 14065 14069 14072 14081 14088 14132 14136 14161 14172 14183 14204 14205
14208 14244 14265 14319 14327 14344 14350 14351 14361 14372 14373 14403 14420 14442
14460 14462 14472 14522 14569 14583 14601 14619 14625 14659 14662 14665 14666 14669
14692 14704 14707 14726 14731 14776 14781 14792 14797 14806 14565''', 'exclude', 'E3')
s('''13481 13486 13499 13514 13529 13574 13591 13592 13625 13628 13629 13630 13631
13638 13640 13660 13671 13682 13694 13718 13722 13732 13742 13747 13751 13764 13777
13788 13794 13798 13814 13844 13849 13852 13853 13857 13862 13897 13901 13913 13915
13945 13946 13953 13961 13970 13973 13981 13987 13989 14010 14025 14064 14089 14090
14091 14092 14104 14108 14169 14174 14177 14178 14179 14181 14193 14218 14261 14281
14287 14289 14304 14332 14334 14368 14405 14438 14441 14449 14453 14463 14473 14474
14483 14509 14510 14517 14543 14549 14552 14567 14571 14574 14575 14579 14587 14588
14599 14605 14609 14614 14618 14626 14637 14663 14689 14693 14714 14727 14728 14733
14742 14743 14744 14752 14755 14761 14773 14788 14793 13859 14058 14406 14432''', 'exclude', 'E1')

t = open(os.path.join(HERE, '..', 'batch8.txt'), encoding='utf-8').read().split('\n')
cids = [l[1:l.index(']')] for l in t if l.startswith('[')]
# everything else -> E2 (checked manually: listed in E2 set below)
E2 = set('R2-C' + x for x in '''
13469 13477 13484 13489 13492 13495 13503 13509 13512 13518 13524 13531 13537 13546 13548
13554 13557 13566 13577 13578 13581 13583 13590 13598 13615 13635 13636 13648 13649 13663
13667 13675 13687 13689 13691 13693 13705 13715 13717 13739 13741 13743 13757 13761 13765
13767 13768 13770 13773 13774 13781 13785 13801 13802 13803 13805 13817 13821 13839 13841
13848 13863 13866 13880 13881 13888 13902 13907 13909 13912 13929 13935 13948 13983 13990
14003 14004 14011 14021 14024 14041 14048 14052 14061 14063 14066 14075 14096 14101 14107
14109 14113 14125 14129 14139 14146 14149 14156 14162 14163 14168 14190 14197 14209 14210
14216 14238 14239 14241 14247 14249 14256 14270 14276 14277 14279 14286 14295 14297 14301
14314 14315 14328 14331 14349 14353 14354 14360 14376 14385 14388 14392 14401 14402 14404
14436 14440 14444 14445 14447 14456 14457 14461 14465 14470 14478 14479 14482 14488 14496
14497 14505 14507 14511 14521 14529 14534 14535 14536 14537 14538 14544 14546 14548 14553
14555 14560 14576 14584 14589 14591 14593 14594 14600 14608 14617 14621 14623 14624 14632
14640 14667 14677 14700 14709 14715 14736 14739 14740 14758 14764 14767 14769 14777 14778
14784 14791 14798 14800 14801 14802 14803 14185 13644 13595 14481'''.split())
for k in E2:
    if k in cids:
        assert k not in D, ('dup', k)
        D[k] = ('exclude', 'E2', '')
missing = [c for c in cids if c not in D]
extra = [k for k in D if k not in cids]
print('records', len(cids), 'decided', len(D), 'missing', missing, 'extra', extra)
if not missing and not extra:
    with open(os.path.join(HERE, '..', 'batch8_decisions.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['cid', 'decision', 'code', 'note'])
        for c in cids:
            w.writerow([c, *D[c]])
    from collections import Counter
    print(Counter(v[0] for v in D.values()), Counter(v[1] for v in D.values() if v[0]=='include'))
