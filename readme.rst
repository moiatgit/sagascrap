############
SAGA Scratch
############

Aquest projecte és un intent d'extreure informació del SAGA per part
d'un tutor **desesperat**.

Si no saps que és SAGA (felicitats per a tu!) o bé no ets un tutor
desesperat, probablement aquest projecte no tingui res a veure amb tu
i el pots ignorar.

Tot el que apareix en aquest projecte el deixo sota llicència GPL 3 o
superior. 

Estat
=====

El projecte actualment permet, si et descarregues la informació
pertinent del SAGA, extreure alumnes/notes/UFs/mòduls de manera
tabular en un format csv que puguis manipular, per exemple, amb un
full de càlcul.

Això implica:

- pots donar les notes als teus alumnes en el format que t'interessi
  (ex. penjant-les individualment al Moodle)

- pots omplir part de la memòria de tutors que et demanen a final de
  curs sense requerir introduccions de notes massives o demanar
  aquestes als teus companys d'equip docent.

- pots analitzar les dades pels teus usos de tutor

Futur
=====

En un futur (potser llunyà) hi haurà un script que podrà connectar-se
i baixar ell solet la informació del SAGA. No és ciència ficció doncs
ho he aconseguit ja. El problema és que el SAGA es comporta molt
diferent depenent de l'estat en que es troba (ex. en junta) i el meu
temps (a diferència del que part de la humanitat sembla creure dels
profes) és bé escars.

Per suposat, està obert a la participació de tothom. Us animo a
fer un fork i adaptar-lo a les vostres necessitats. Em fareu saltar
llàgrimes d'alegria si, a més, us animeu a col·laborar per crear una
petita *suite* d'utilitats.

Guia d'utilització
==================

Per a obtenir el codi font

1. entra en SAGA

2. entra en junta del grup d'interés

3. alumne per alumne clica amb botó dret en la capçalera "modul" de la
   taula amb les notes -> this frame -> view frame source

   copy el contingut que es mostra i enganxa'l al document on reculls
   tots. Si no vols canviar el programa extractinfo.py, caldrà que
   anomenis aquest fitxer bolcat.notes.junta.html

   Notes:

   - sí, és un pal

   - no, no és etern: 30 alumnes en menys de 10 minuts

   - compte d'agafar el contingut del frame de la taula. Ha de contenir
     línies de l'estil: ::

       new ContingutCFLOE("276644795", "00303", "UF3.  Fonaments de gestió de fitxers",

4. elimina info d'html que confon a BeautifulSoup ::

    $ sed -i '/<\/\?html/d' bolcat.notes.junta.html

5. executa ::

    $ python extractinfo.py

6. si et calen les dades (notes per alumne i uf) ::

       $ python generanotes.py > info.csv

   incorpora com a csv info.csv a un full de càlcul i ja pots començar
   a jugar amb les dades

   Si el que vols són els estadístics (ex. per la memòria de tutors)
   prova amb: ::

       $ python generastats.py

   **Nota**: aquest script està encara sense acabar i **no funciona**.
   Mira la capçalera del seu codi font per més detalls


