#! /bin/python
# encoding: utf-8

# Aquest script extreu les dades del bolcat de notes en junta del saga

from bs4 import BeautifulSoup
import re, sys
import pickle

# regex per trobar els alumnes i les notes
re_expected_script = re.compile('<script type="text/javascript">')  # Contingut d'inici d'un script d'interés

re_nota = re.compile('\s*new NotaCFLOE')                # Línia d'inici d'una nota

re_matricula = re.compile("\s*var matricula = '(.*)';") # extractor del nr de matrícula de l'alumne

re_prenomalumne = re.compile('\s*<input type="hidden" name="idMatricula" value="(.*)">')
re_nomalumne = re.compile('\s*<input type="hidden" name="nomAlumne" value="(.*)">')

# fitxer a tractar
# TODO: recollir-ho de sys.argv o millor, directament de SAGA!
fitxer = "bolcat.notes.junta.html"
picklefilename = "notessaga.pickle"         # it will leave the computations on this pickle

# obté el font en html
f = open(fitxer)
html = f.read()
f.close()

# utilitats
def neteja(s):
    """ utilitat per netejar l'entrada obtinguda dels camps dels
    scripts"""
    return s.strip().strip(",").strip('"')

def separaentrades(xs, val='"-"'):
    """ donada una llista d'elements, i un valor de duplicació,
    retorna la llista amb cada element seguit d'un val
    Ex. si xs = [1, 2, 3]
    la sortida serà:
        [1, "-", 2, "-", 3, "-"]
    """
    return [x for pair in [ (elem, val) for elem in xs] for x in pair]

# base de dades
matricules = dict()  # { id_matricula: { "alumne":xxx, "notes": {codi_modul : ( matricula, nota} }
moduls = dict()      # { codi_modul : (nom, hores) }

# crea la sopa
soup = BeautifulSoup(html)

# extracció de la informació dels mòduls
scripts = soup(["script"])
#print '"id", "mòdul/uf", "nom mòdul", "hores", "matrícula", "nota"'
for script in scripts:
    text = str(script)
    lines = text.split('\n')
    num_lines = len(lines)
    if num_lines < 4:
        continue

    # extreu l'id de matrícula de l'alumne
    m = re_matricula.match(lines[5])
    if m == None:
        print "WARNING: format incorrecte. S'esperava matricula i s'ha trobat %s"%lines[5]
        print "\tContext:\n" + "-"*30
        print text
        sys.exit(1)
    id_matricula = m.group(1)
    if id_matricula not in matricules:
        matricules[id_matricula]={ "alumne":"desconegut", "notes": dict() }
    else:
        print "WARNING: matrícula repetida"

    # extreu notes
    nlin = 10
    while nlin < num_lines:
        line = lines[nlin]
        if re_nota.match(line): # comença una nota
            codi_modul = neteja(lines[nlin+8])
            nom_modul = neteja(lines[nlin+9])
            matricula_modul = neteja(lines[nlin+1]) # si coincideix amb id_matricula és d'aquest curs
            hores_modul = neteja(lines[nlin+15])
            nota_nova = neteja(lines[nlin+5])
            nota_antiga = neteja(lines[nlin+17])

            matricula_modul = "act" if matricula_modul == id_matricula else "ant"
            nota = nota_nova if nota_antiga == "null" else nota_antiga
            nota = "pendent" if nota == "null" else nota
#            print '%s, "%s", "%s", %s, "%s", "%s"'%(id_matricula,
#                                                    codi_modul,
#                                                    nom_modul,
#                                                    hores_modul,
#                                                    matricula_modul,
#                                                    nota)
            if codi_modul not in moduls:
                moduls[codi_modul]=(nom_modul, hores_modul)
            matricules[id_matricula]["notes"][codi_modul] = (matricula_modul, nota)

            nlin += 20
            continue
        # seguim buscant
        nlin += 1

# troba el nom dels alumnes amb els ids de matrícula
# print "\n"*10
# print '"id_matricula", "nom_alumne"'
forms = soup(["form"])
for form in forms:
    id_matricula = None
    nom_alumne = None
    for inp in form.findAll("input"):
        if not id_matricula and inp["name"] == "idMatricula":
            id_matricula = inp["value"]
        if not nom_alumne and inp["name"] == "nomAlumne":
            nom_alumne = inp["value"]
    if id_matricula and nom_alumne:
#        print '%s, "%s"'%(id_matricula, nom_alumne.encode("utf8"))
        matricules[id_matricula]["alumne"]=nom_alumne.encode("utf8")

# guarda dades en un picle
picklef = open(picklefilename,"wb")
pickle.dump((moduls, matricules), picklef)
picklef.close()

print "Fet"
