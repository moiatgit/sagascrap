#! /bin/python
# encoding: utf-8

# Aquest script extreu estadístics del picke generat per extractinfo
#
# IMPORTANT: aquest script encara no funciona.
# Presenta un problema de disseny: no es pot extreure la informació de
# la matrícula d'enguany dels continguts descarregats del SAGA. La
# informació guardada com a ant/act només fa referència a si la nota
# ha estat definida en aquesta avaluació o en una anterior.
# Caldrà doncs trobar la manera (encara que sigui amb la incorporació
# externa d'un csv) per poder finalitzar aquest script. Mentrestant,
# finalitza l'execució amb un error 1

import sys
print "CRITICAL: script sense finalitzar"
sys.exit(1)

import re
from collections import defaultdict
import pickle


picklefilename = "notessaga.pickle"         # it will load the computations on this pickle

# recupera les dades del fitxer pickle
picklef = open(picklefilename,"r")
moduls, matricules = pickle.load(picklef)
picklef.close()

print "XXX n matricules: ", len(matricules)

# conforma la jerarquia de mòduls
class Modul:
    """ encapsula la informació d'un mòdul """
    def __init__(self, codi):
        self.codi = codi
        self.nom = 'desconegut'
        self.hores = -1
        self.ufs = []
        self.alumnes_presentats_a_alguna_uf = set()
        self.alumnes_amb_ufs_suspeses = dict() # nombre de UFs suspeses en aquests mòdul
        self.alumnes_amb_modul_superat = 0  # Es considera els que tenen nota de mòdul
                                            # i estan matriculats
                                            # aquest any (és a dir,
                                            # han aprovat el mòdul
                                            # aquest curs)

    def add_alumne_amb_uf_suspesa(self, codi_matricula):
        """ afegeix l'alumne amb uf suspesa """
        if codi_matricula not in self.alumnes_amb_ufs_suspeses:
            self.alumnes_amb_ufs_suspeses[codi_matricula] = 0
        self.alumnes_amb_ufs_suspeses[codi_matricula] += 1
        print "XXX ara el mòdul té suspens", self.alumnes_amb_ufs_suspeses


    def __unicode__(self):
        alumnes_amb_una_uf_suspesa = 0
        alumnes_amb_mes_duna_uf_suspesa = 0
        print "XXX alumnes amb ufs suspeses ", self.alumnes_amb_ufs_suspeses.values()
        for v in self.alumnes_amb_ufs_suspeses.values():
            if v == 1:
                alumnes_amb_una_uf_suspesa += 1
            elif v > 1:
                alumnes_amb_mes_duna_uf_suspesa += 1

        s = '{ "codi":%s, "nom":"%s", "hores":%s, "ufs":['%(self.codi,
                                                   self.nom,
                                                   self.hores)
        s += ", ".join(uf.__unicode__() for uf in self.ufs)
        s += ', "alumnes presentats a alguna uf": %s, "alumnes amb mòdul superat":%s, "alumnes amb una uf suspesa":%s, "alumnes amb més d\'una uf suspesa":%s'%(
            len(self.alumnes_presentats_a_alguna_uf), self.alumnes_amb_modul_superat, alumnes_amb_una_uf_suspesa, alumnes_amb_mes_duna_uf_suspesa)
        s += "]}"
        return s

class UnitatFormativa:
    """ encapsula una unitat formativa """
    def __init__(self, codi, nom, hores):
        self.codi = codi
        self.nom = nom
        self.hores = hores
        self.notes_alumnes = []     # Llista de notes dels alumnes que
                                    # estaven matriculats a aquesta UF
                                    # Només notes numèriques
    def __unicode__(self):
        s = '{ "codi":%s, "nom":"%s", "hores":%s, notes: ['%(self.codi,
                                                   self.nom,
                                                   self.hores)
        s += ", ".join(str(n) for n in self.notes_alumnes)
        s += ']}'
        return s


jerarquiamoduls = dict()        # { codi_modul: Modul }
for codi, valors in moduls.iteritems():
    nom = valors[0]
    hores = valors[1]
    if len(codi)==3:
        jerarquiamoduls[codi] = Modul(codi)
        jerarquiamoduls[codi].nom = nom
        jerarquiamoduls[codi].hores = hores
    else:
        codimodul = codi[:3]
        if codi[:3] not in jerarquiamoduls:
            jerarquiamoduls[codimodul] = Modul(codi)
        uf = UnitatFormativa(codi, nom, hores)
        jerarquiamoduls[codimodul].ufs.append(uf)

# computa estadístics
for codimodul, modul in jerarquiamoduls.iteritems():
    for matricula in matricules.values():
        actual, nota = matricula["notes"][codimodul]
        if actual != "act":
            continue
        if nota.isdigit() and int(nota)>=5:
            modul.alumnes_amb_modul_superat += 1

    for uf in modul.ufs:
        for matricula in matricules.values():
            actual, nota = matricula["notes"][uf.codi]
            if actual != "act":
                continue
            if nota.isdigit():
                val = int(nota)
                uf.notes_alumnes.append(val)
                modul.alumnes_presentats_a_alguna_uf.add(matricula["alumne"])
                if val < 5:
                    modul.add_alumne_amb_uf_suspesa(matricula["alumne"])


# mostra estadístics per mòdul
codismoduls = sorted(jerarquiamoduls.keys())
for codi in codismoduls:
    if codi == '002':
        modul = jerarquiamoduls[codi]
        # print modul.codi,
        # print modul.alumnes_amb_modul_superat,
        print modul.__unicode__()
        print

