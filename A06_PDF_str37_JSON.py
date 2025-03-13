# -*- coding: utf-8 -*-
#imports the json librari to code and decode json strings
import json
#creates the dictionary d
d = {}
#introduces three keys and values
d["campo1"]="valor1"          # TRANSLATION campo=polje  valor=vrednost    znotraj podatkovne strukture dictionary (slovar) imamo argument in njegovo vrednost
d["campo2"]="valor2"          # {"campo1": "valor1", "campo2": "valor2", "campo3": "valor3"}  oz. {"ime": "Maj", "priimek": "Čapelnik", "leto_rojstva": 2001}
d["campo3"]="valor3"
#converts the dictionary to a json string
d_json = json.dumps(d)
print("First json: {0}".format(d_json))
#creates other dictionary
d2={}                                          # d2={}
#introduces some keys and values
d2["ok"]=True                                  # d2={"ok": true}
d2["menssage"]="diccionariy 2"
#introduces the other json string as a value in this dictionary
d2["data"]=d                                   # d2={"ok": true, "data":{vstavljen zgornji dictionary}}
d2_json = json.dumps(d2)                       # dictionary -->JSON string 
print("Second json: {0}".format(d2_json))      # izpis JSON string

# OBRATNA POT IZ JSON stringa naredimo dictionary
strJson = '{"message": "diccionariy 2", "ok": true, "data": {"campo1": "valor1", "campo2": "valor2", "campo3": "valor3"}}'
#decodes the json string and creates a dictionary
d=json.loads(strJson)
#prints the keys of the dictionary
print(d.keys())                        # na malo čuden način smo jih izpisali. Posebej argumente (lastnosti) in posebej vrednosti
#print the values of the dictionary
print(d.values())
print("Standarden izpis: {0}".format(d))