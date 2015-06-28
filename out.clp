; couleur_maison((couleur(rouge) & couleur(jaune) & couleur(bleu) & couleur(vert) & couleur(blanc)))
(couleur rouge)
(couleur jaune)
(couleur bleu)
(couleur vert)
(couleur blanc)
;couleur_maison((CouleurRouge & CouleurJaune & CouleurBleu & CouleurVert & CouleurBlanc))

; habiter(nationalite(Anglais),couleur(rouge))
(nationalite Anglais)
(couleur rouge)
;habiter(NationaliteAnglais,CouleurRouge)

; avoir(nationalite(Suedois),animal(chien))
(nationalite Suedois)
(animal chien)
;avoir(NationaliteSuedois,AnimalChien)

; boire(nationalite(Danois),the)
(nationalite Danois)
;boire(NationaliteDanois,the)

; a_gauche(couleur(vert),couleur(blanc))
(couleur vert)
(couleur blanc)
;a_gauche(CouleurVert,CouleurBlanc)

; boire(couleur(vert),cafe)
(couleur vert)
;boire(CouleurVert,cafe)

; fumer(\x.avoir(x,animal(oiseau)),Pall_Mall)
(animal oiseau)
;fumer(\x.avoir(x,AnimalOiseau),Pall_Mall)

; fumer(couleur(jaune),Dunhill)
(couleur jaune)
;fumer(CouleurJaune,Dunhill)

; habiter(\x.boire(x,jus_d_orange),position(3))
(position 3)
;habiter(\x.boire(x,jus_d_orange),Position3)

; (habiter(nationalite(Norvegien),position(1)) & habiter(?np2,a_cote(couleur(bleu))))
(nationalite Norvegien)
(position 1)
(couleur bleu)
(a_cote CouleurBleu)
;(habiter(NationaliteNorvegien,Position1) & habiter(?np2,A_CoteCouleurbleu))

; fumer(\s.habiter(s,a_cote(\x.avoir(x,animal(chat)))),Blend)
(animal chat)
;fumer(\s.habiter(s,a_cote(\x.avoir(x,AnimalChat))),Blend)

; avoir(a_cote(\x.fumer(x,Dunhill)),animal(cheval))
(animal cheval)
;avoir(a_cote(\x.fumer(x,Dunhill)),AnimalCheval)

; fumer(\x.boire(x,biere),Blue_Master)
;fumer(\x.boire(x,biere),Blue_Master)

; fumer(nationalite(Allemand),Prince)
(nationalite Allemand)
;fumer(NationaliteAllemand,Prince)

; fumer(\x.avoir(x,a_cote(\x.boire(x,eau))),Blend)
;fumer(\x.avoir(x,a_cote(\x.boire(x,eau))),Blend)

