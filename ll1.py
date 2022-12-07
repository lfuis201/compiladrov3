from AnalizadorLexico import tokens,tokens_info

import pandas as pd
import numpy as np
from graphviz import Digraph
from arbol import Arbol, recorrerArbol

dot = Digraph()
filas = {"Inicio"	:1	,
"E"	:2	,
"E'"	:3	,
"DeclaracionFuncion"	:4	,
"FuncionPrincipal"	:5	,
"K"	:6	,
"Parametros"	:7	,
"Y'"	:8	,
"Y"	:9	,
"TipoDato"	:10	,
"C"	:11	,
"CuerpoF"	:12	,
"J"	:13	,
"Cuerpo"	:14	,
"D'"	:15	,
"DeclaracionVariables"	:16	,
"Dc'"	:17	,
"Sentencias"	:18	,
"OPS"	:19	,
"MuchasSentenciasCiclo"	:20	,
"M'"	:21	,
"SentenciasCiclo"	:22	,
"MuchasSentencias"	:23	,
"S'"	:24	,
"DeclaracionVariable"	:25	,
"Corchetes"	:26	,
"OPI"	:27	,
"Expresion"	:28	,
"Ex"	:29	,
"Ex'"	:30	,
"Tx"	:31	,
"String"	:32	,
"Op"	:33	,
"ParaLLamados"	:34	,
"PL'"	:35	,
"PL"	:36	,
"Simbolo"	:37
}

columnas={"func"	:1	,
"identificador"	:2	,
"pizquierdo"	:3	,
"pderecho"	:4	,
"lizquierdo"	:5	,
"lderecho"	:6	,
"main"	:7	,
"coma"	:8	,
"num"	:9	,
"decimal"	:10	,
"string"	:11	,
"cizquierdo"	:12	,
"cderecho"	:13	,
"return"	:14	,
"si"	:15	,
"sino"	:16	,
"ciclo"	:17	,
"print"	:18	,
"igual"	:19	,
"lnum"	:20	,
"lstring"	:21	,
"ldecimal"	:22	,
"true"	:23	,
"false"	:24	,
"mas"	:25	,
"menos"	:26	,
"por"	:27	,
"or"	:28	,
"and"	:29	,
"mayor_igual"	:30	,
"diferente"	:31	,
"menor_igual"	:32	,
"comparacion"	:33	,
"menor"	:34	,
"mayor"	:35	,
"modulo"	:36	,
"dividir"	:37	,
"$"	:38
}
df = pd.read_excel("tabla4.xlsx", 'Hoja1',  header=None)
tablita_parse = df.values

pila = ["Inicio","$"]
entrada = tokens
entrada.append("$")
pila_tokens = tokens_info
linea_tokens = tokens_info.copy()

continuar=True
i=0
j=0
p=0
aux=[]
pendientes=[]
tree = Arbol(pila[0],0)
dot.node(str(j), pila[0])
padres=[0,-1]
#print("Inicio:")
#print(pila)
#print(entrada)

while continuar:
  #print("Vuelta",i)
  if pila[0]=="$" and entrada[0]=="$":
    continuar=False
    #print(pila)
    #print(entrada)
    #print("Cadena aceptada")
  elif pila[0] == entrada[0]:
    #print(pila)
    #print(entrada)
    pila = pila[1:]
    entrada.pop(0)
    linea_tokens.pop(0)
  elif pila[0][0]==(pila[0][0]).lower() and entrada[0][0]==(entrada[0][0]).lower():
    continuar=False
    #print(pila)
    #print(entrada)
    print("Error sintáctico en la línea " + str(linea_tokens[0].lineno) + ": Cadena rechazada")
    raise SystemExit
  else:
    if entrada[0] in columnas:
      reemplazo = tablita_parse[filas[pila[0]]][columnas[entrada[0]]]
      p=int(padres[0])
    else:
      continuar=False
      #print(pila)
      #print(entrada)
      print("Error sintáctico en la línea " + str(linea_tokens[0].lineno) + ": Cadena rechazada")
      raise SystemExit
      break
    if reemplazo == "vacio":
      j=j+1
      h=j
      dot.node(str(h), "''")
      dot.edge(str(p),str(h))
      tree.agregarhijo(tree,"''",p,h)
      pila=pila[1:]
      padres=padres[1:]
      #print(pila)
      #print(entrada)
    else:
      if str(reemplazo) == 'nan':
        print("Error sintáctico en la línea " + str(linea_tokens[0].lineno) + ": Cadena rechazada")
        raise SystemExit
      array_aux=reemplazo.split()
      pila = np.concatenate((array_aux,pila[1:]),axis=0)
      hijos = len(array_aux)
      aux.clear()
      for e in range(hijos):
        j=j+1
        if array_aux[e][0]==array_aux[e][0].upper():
          aux.append(j)
          tree.agregarhijo(tree,array_aux[e],p,j)
        else:
          tree.agregarhijo(tree,array_aux[e],p,j)
        h=j
        dot.node(str(h), array_aux[e])
        dot.edge(str(p),str(h))
      padres = np.concatenate((aux,padres[1:]),axis=0)
      #print(pila)
      #print(entrada)
  i=i+1
print(dot.source)
recorrerArbol(tree,pila_tokens)