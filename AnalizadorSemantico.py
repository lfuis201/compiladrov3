import ll1
class simbolo:
  def __init__(self,t,lex,type,pos,line,scope,type_date=None):
    self.token=t
    self.lexema=lex
    self.tipo=type
    self.posicion=pos
    self.lineea=line
    self.scope=scope
    self.tipo_dato=type_date

def buscar_simbolo_td(tabla,elemento):
  for i in tabla:
    if i.lexema==elemento and (i.tipo == "variable" or i.tipo == "func"):
      return i.tipo_dato

def buscar_simbolo_tipo(tabla,elemento):
  for i in tabla:
    if i.lexema==elemento and (i.tipo == "variable" or i.tipo == "func"):
      return i.tipo

def imprimir_tds(tabla):
  for i in tabla:
    print(i.token,i.lexema,i.tipo,i.posicion,i.lineea,i.scope)

def buscar_mision(arbol,i):
  if arbol.elemento == "DeclaracionFuncion" and arbol.hijos[1].token.value == i:
    return arbol
  for subarbol in arbol.hijos:
    arbolBuscado = buscar_mision(subarbol, i)
    if (arbolBuscado != None):
        return arbolBuscado
  return None

def obtener_tipo_mision(arbol):
  if arbol.hijos[6].hijos[1].hijos[0].elemento == "''":
    return None
  else:
    tipo = verificar_tipo_Ex(arbol.hijos[6].hijos[1].hijos[1].hijos[0])
    return tipo


n=0
es_ciclo=False
tabla_de_simbolos=[]
#ll1.arbol.imprimirArbol(ll1.arbolito)
funcion_actual=None
funcion_actual_aux=None
errores = False

def verificar_tipo_de_dato_id(node_tx):
  tipo_de_dato = buscar_simbolo_td(tabla_de_simbolos,node_tx.hijos[0].token.value)
  return tipo_de_dato

def verificar_tipo_de_termino(node_t):
  tipo_de_dato = None
  if node_t.elemento == "lnum":
    tipo_de_dato = "num"
  elif node_t.elemento == "lstring":
    tipo_de_dato = "string"
  elif node_t.elemento == "ldecimal":
    tipo_de_dato = "decimal"
  return tipo_de_dato

def verificar_tipo_Ex_prima(node_Ex_prima):
  global errores
  tipo_de_dato_Ex_prima = "None"
  if node_Ex_prima.hijos[0].elemento=="''":
    tipo_de_dato_Ex_prima = "None"
  elif node_Ex_prima.hijos[0].elemento=="Simbolo":
    tipo_de_dato_T = verificar_tipo_Tx(node_Ex_prima.hijos[1])
    tipo_de_dato_Ex_prima = verificar_tipo_Ex_prima(node_Ex_prima.hijos[2])
    
    if tipo_de_dato_Ex_prima == "None":
      tipo_de_dato_Ex_prima = tipo_de_dato_T
    else:
      if tipo_de_dato_T == tipo_de_dato_Ex_prima:
        tipo_de_dato_Ex_prima = tipo_de_dato_T
      else:
        print("Error de asiganción 3 en la línea " + str(node_Ex_prima.hijos[1].hijos[0].hijos[0].token.lineno) + ": los tipos no coinciden")
        errores = True
  return tipo_de_dato_Ex_prima

def verificar_tipo_Tx(node_Tx):
  tipo_de_dato=None
  if node_Tx.hijos[0].elemento == "string":
    tipo_de_dato = verificar_tipo_de_termino(node_Tx.hijos[0].hijos[0])
  elif node_Tx.hijos[0].elemento == "identificador":
    tipo_de_dato = verificar_tipo_de_dato_id(node_Tx)
  return tipo_de_dato
  
    

def verificar_tipo_Tx_Ex_prima(node_Tx, node_Ex_prima):
  global errores
  type_Tx = verificar_tipo_Tx(node_Tx)
  type_Ex_prima= verificar_tipo_Ex_prima(node_Ex_prima)
  if str(type_Ex_prima) == "None":
    return type_Tx
  else:
    if type_Tx ==  type_Ex_prima:
      return type_Tx
    else:
      print("Error de asiganción 2 en la línea " + str(node_Tx.hijos[0].hijos[0].token.lineno) + ": los tipos no coinciden")
      errores = True

def verificar_tipo_Ex(arbol):
  tipo_de_dato = verificar_tipo_Tx_Ex_prima(arbol.hijos[0],arbol.hijos[1])
  return tipo_de_dato

def comprobar_duplicado(valor,lineea):
  global errores
  for x in reversed(tabla_de_simbolos):
    if x.lexema==valor and (x.tipo=="func" or x.tipo == "variable"):
      print("Error errore semántico en línea "+ str(lineea) + ": " + x.lexema + " ya fue declarado")
      errores = True
      break

def comprobar_existencia(valor,tipo,lineea):
  global errores
  encontrado=False
  for x in reversed(tabla_de_simbolos):
    if x.lexema==valor and x.tipo==tipo:
      encontrado=True
      break
  if encontrado==False:
    print("Error semántico en línea "+ str(lineea) + ": Llamaste a la " + tipo + " " + valor + ", pero no fue declarada")
    errores = True


def verificar_declaracion_variable(arbol):
  global errores
  comprobar_duplicado(arbol.hijos[1].token.value,arbol.hijos[1].token.lineno)

  tabla_de_simbolos.append(simbolo(arbol.hijos[1].token,arbol.hijos[1].token.value,"variable",arbol.hijos[1].token.lexpos,arbol.hijos[1].token.lineno,funcion_actual,arbol.hijos[0].hijos[0].elemento))
  
  if arbol.hijos[3].hijos[0].elemento == "igual":
    td_asignacion = verificar_tipo_Ex(arbol.hijos[3].hijos[1].hijos[0])
    td_variable = buscar_simbolo_td(tabla_de_simbolos,arbol.hijos[1].token.value)
    if td_variable != td_asignacion:
      print ("Error de asignación en la línea " + str(arbol.hijos[1].token.lineno) + ": no coincienden los tipos")
      errores = True
    else:
      arbol.hijos[3].hijos[1].tipo=td_asignacion

def obtener_parametros_lmision(arbol,par):
  if arbol.elemento=="PL":
    tipo = verificar_tipo_Ex(arbol.hijos[0].hijos[0])
    par.append(tipo)
    arbol.hijos[0].tipo=tipo
  for x in arbol.hijos:
    obtener_parametros_lmision(x,par)

def obtener_parametros(arbol,par):
  if arbol.elemento=="Y":
    par.append(arbol.hijos[0].hijos[0].elemento)
  for x in arbol.hijos:
    obtener_parametros(x,par)

def insertar_parametros(arbol):
  if arbol.elemento=="Y":
    tabla_de_simbolos.append(simbolo(arbol.hijos[1].token,arbol.hijos[1].token.value,"variable",arbol.hijos[1].token.lexpos,arbol.hijos[1].token.lineno,funcion_actual,arbol.hijos[0].hijos[0].elemento))
  for x in arbol.hijos:
    insertar_parametros(x)

def verificar_mision(arbol):
  global funcion_actual
  global funcion_actual_aux
  comprobar_duplicado(arbol.hijos[1].token.value,arbol.hijos[1].token.lineno)
  funcion_actual=arbol.hijos[1].token.value
  funcion_actual_aux=funcion_actual
  
  if arbol.hijos[3].hijos[0] !="''":
      insertar_parametros(arbol.hijos[3])

  tipo_de_mision=obtener_tipo_mision(arbol)
  arbol.hijos[1].tipo = tipo_de_mision
  tabla_de_simbolos.append(simbolo(arbol.hijos[1].token,arbol.hijos[1].token.value,"func",arbol.hijos[1].token.lexpos,arbol.hijos[1].token.lineno,"global",tipo_de_mision))

def verificar_asignacion_de_variable(arbol):
  global errores
  comprobar_existencia(arbol.hijos[0].token.value,"variable",arbol.hijos[0].token.lineno)

  td_asignacion = verificar_tipo_Ex(arbol.hijos[1].hijos[1].hijos[0])
  td_variable = buscar_simbolo_td(tabla_de_simbolos,arbol.hijos[0].token.value)

  if td_variable != td_asignacion:
    print ("Error de asignación en la línea " + str(arbol.hijos[0].token.lineno) + ": no coincienden los tipos")
    errores = True
  else:
      arbol.hijos[1].hijos[1].tipo=td_asignacion
  
  tabla_de_simbolos.append(simbolo(arbol.hijos[0].token,arbol.hijos[0].token.value,"asignacion",arbol.hijos[0].token.lexpos,arbol.hijos[0].token.lineno,funcion_actual))

def verificar_llamada_de_variable(arbol):
  comprobar_existencia(arbol.hijos[0].token.value,"variable",arbol.hijos[0].token.lineno)

def verificar_llamada_de_mision(arbol):
  global errores
  parametros=[]
  parametros_lmision=[]
  comprobar_existencia(arbol.hijos[0].token.value,"func",arbol.hijos[0].token.lineno)
  nodo_mision=buscar_mision(ll1.tree,arbol.hijos[0].token.value)
  obtener_parametros(nodo_mision.hijos[3],parametros)
  obtener_parametros_lmision(arbol.hijos[1].hijos[1],parametros_lmision)
  if len(parametros) != len(parametros_lmision):
    print("Error semántico en la línea "+ str(arbol.hijos[0].token.lineno) +": los parámentros no coinciden")
    errores = True
  else:
    for ra in range(len(parametros)):
      if parametros[ra] != parametros_lmision[ra]:
        print("Error semántico en la línea "+ str(arbol.hijos[0].token.lineno) +": los parametros no coinciden")
        errores = True

def verificar_mostrar(arbol):
  td_asignacion = verificar_tipo_Ex(arbol.hijos[2].hijos[0])
  arbol.hijos[2].tipo=td_asignacion


def eliminar_scope(scope):
  #imprimir_tds(tabla_de_simbolos)
  #print("")
  for item in reversed(tabla_de_simbolos):
    if item.scope == scope:
      tabla_de_simbolos.pop(tabla_de_simbolos.index(item))
  #imprimir_tds(tabla_de_simbolos)
  #print("")

def verificar_scope_llama(arbol):
  for subarbol in arbol.hijos:
    if subarbol.elemento=="FuncionPrincipal":
      verificar_scope(subarbol)

def verificar_scope(arbol):
  global funcion_actual
  global n
  global funcion_actual_aux
  global es_ciclo

  if arbol.elemento == "FuncionPrincipal":
    funcion_actual="main"
    funcion_actual_aux="main"
  
  if arbol.elemento == "ciclo":
    es_ciclo=True
  
  if len(arbol.hijos)>0 and arbol.hijos[0].elemento=="func":
    n=0
    verificar_mision(arbol)
  
  if arbol.elemento == "DeclaracionVariable":
    verificar_declaracion_variable(arbol)
  
  if (arbol.elemento=="SentenciasCiclo" or arbol.elemento == "Sentencias") and arbol.hijos[0].elemento=="identificador"and arbol.hijos[1].hijos[0].elemento=="igual":
    verificar_asignacion_de_variable(arbol)
  
  if (arbol.elemento=="SentenciasCiclo" or arbol.elemento == "Sentencias" or arbol.elemento =="Tx") and arbol.hijos[0].elemento=="identificador"and arbol.hijos[1].hijos[0].elemento=="pizquierdo":
    verificar_llamada_de_mision(arbol)
  
  if arbol.elemento == "Tx" and arbol.hijos[0].elemento == "identificador" and arbol.hijos[1].hijos[0].elemento == "''":
    verificar_llamada_de_variable(arbol)
  
  if (arbol.elemento=="SentenciasCiclo" or arbol.elemento == "Sentencias") and arbol.hijos[0].elemento == "print":
    verificar_mostrar(arbol)
  
  if (arbol.elemento=="SentenciasCiclo" or arbol.elemento == "Sentencias") and arbol.hijos[0].elemento=="lizquierdo":
    n=n+1
    funcion_actual= funcion_actual_aux + str(n)
  
  if arbol.elemento == "lderecho" and n==0:
    if es_ciclo==True:
      es_ciclo=False
    else:
      eliminar_scope(funcion_actual)

  if arbol.elemento == "lderecho" and n>0:
    if es_ciclo==True:
      es_ciclo=False
    else:
        n=n-1
        eliminar_scope(funcion_actual)
        if n!=0:
            funcion_actual= funcion_actual_aux + str(n)
        else:
            funcion_actual= funcion_actual_aux
  
    for subarbol in arbol.hijos:
        if subarbol.elemento!="FuncionPrincipal":
            verificar_scope(subarbol)

verificar_scope(ll1.tree)
#print("Scope")
verificar_scope_llama(ll1.tree)
#print("Final")
#imprimir_tds(tabla_de_simbolos)
if errores == True:
    raise SystemExit