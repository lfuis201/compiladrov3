class Arbol:
  def __init__(self,ele,i,tok=None,type=None):
    self.id = i
    self.elemento=ele
    self.hijos = []
    self.token = tok
    self.typeo = type
    
  def agregarhijo(self,arbol,elemento,padre,i,tok=None,type=None):
    subarbol = buscarSubarbol(arbol, padre)
    subarbol.hijos.append(Arbol(elemento,i,tok,type))

def buscarSubarbol(arbol, i):
  if arbol.id == i:
    return arbol
  for subarbol in arbol.hijos:
    arbolBuscado = buscarSubarbol(subarbol, i)
    if (arbolBuscado != None):
        return arbolBuscado
  return None

def imprimirArbol(arbol):
  print(arbol.elemento)
  for subarbol in arbol.hijos:
    imprimirArbol(subarbol)

def recorrerArbol(arbol,pila):
  if(arbol.elemento==arbol.elemento.lower() and arbol.elemento != "''"):
    arbol.token=pila.pop(0)
  for subarbol in arbol.hijos:
    recorrerArbol(subarbol,pila)