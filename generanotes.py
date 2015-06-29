#! /bin/python
# encoding: utf-8

# Aquest script extreu les notes  del picke generat per extractinfo

import sys
import pickle

picklefilename = "notessaga.pickle"         # it will load the computations on this pickle

def separaentrades(xs, val='"-"'):
    """ donada una llista d'elements, i un valor de duplicació,
    retorna la llista amb cada element seguit d'un val
    Ex. si xs = [1, 2, 3]
    la sortida serà:
        [1, "-", 2, "-", 3, "-"]
    """
    return [x for pair in [ (elem, val) for elem in xs] for x in pair]

# recupera les dades del fitxer pickle
picklef = open(picklefilename,"r")
moduls, matricules = pickle.load(picklef)
picklef.close()


# mostra resultats generals
codis = sorted([codi for codi in moduls])
nomsmoduls = ['"%s"'%moduls[codi][0] for codi in codis]
horesmoduls = [moduls[codi][1] for codi in codis]
# capçaleres
# print ", ".join(["alumne"] + separaentrades(codis))
# print ", ".join([""] + separaentrades(nomsmoduls))
# print ", ".join([""] + separaentrades(horesmoduls))
print ", ".join(["alumne"] + codis)
print ", ".join([""] + nomsmoduls)
print ", ".join([""] + horesmoduls)

for id_matricula in matricules:
    matricula = matricules[id_matricula]
    entrada = ['"%s"'%matricula["alumne"]]
    for codi in codis:
#        entrada.append(matricula["notes"][codi][0])
        entrada.append(matricula["notes"][codi][1])
    print ", ".join(entrada)

