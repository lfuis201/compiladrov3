import AnalizadorSemantico

data = ".data\n\nendl: .asciiz " + '"' + "\\n" +'"' + "\n"
total = 0
parametros = []


def generar_terminal(node_t):
  if node_t.elemento == "lnum":
    return "li $a0 " + str(node_t.token.value) + "\n"
  elif node_t.elemento == "ldecimal":
    return "li $a0 " + str(node_t.token.value) + "\n"

def generar_Ex_prima(node_Ex_prima):
  resultado=""
  if node_Ex_prima.hijos[0].elemento=="''":
    return ""
  elif node_Ex_prima.hijos[0].elemento=="Simbolo":
    resultado = "sw $a0 0($sp)\naddiu $sp $sp -4\n"
    resultado += generar_Tx(node_Ex_prima.hijos[1])
    resultado += "lw $t1 4($sp)\n"
    if node_Ex_prima.hijos[0].hijos[0].elemento == "mas":
      resultado += "add $a0 $t1 $a0\naddiu $sp $sp 4\n"
    elif node_Ex_prima.hijos[0].hijos[0].elemento == "menos":
      resultado += "sub $a0 $t1 $a0\naddiu $sp $sp 4\n"
    elif node_Ex_prima.hijos[0].hijos[0].elemento == "por":
      resultado += "mul $a0 $t1 $a0\naddiu $sp $sp 4\n"
    elif node_Ex_prima.hijos[0].hijos[0].elemento == "dividir":
      resultado += "div $t1 $a0\n"
      resultado += "mflo $a0\n"
      resultado += "addiu $sp $sp 4\n"

    elif node_Ex_prima.hijos[0].hijos[0].elemento == "modulo":
      resultado += "div $t1 $a0\n"
      resultado += "mfhi $a0\n"
      resultado += "addiu $sp $sp 4\n"
    elif node_Ex_prima.hijos[0].hijos[0].elemento == "comparacion":
      resultado += "addiu $sp $sp 4\n"
    elif node_Ex_prima.hijos[0].hijos[0].elemento == "diferente":
      resultado += "addiu $sp $sp 4\n"
    resultado += generar_Ex_prima(node_Ex_prima.hijos[2])
  return resultado

def obtener_id_parametro (valor):
  return (len(parametros) - parametros.index(valor)) * 4

def generar_Tx(node_Tx):
  resultado=""
  if node_Tx.hijos[0].elemento == "String":
    resultado = generar_terminal(node_Tx.hijos[0].hijos[0])
  elif node_Tx.hijos[0].elemento == "identificador" and node_Tx.hijos[1].hijos[0].elemento == "''":
    if node_Tx.hijos[0].token.value in parametros:
      resultado = "lw $a0 "+ str(obtener_id_parametro(node_Tx.hijos[0].token.value)) + "($fp)\n"
    else:
      resultado = "lw $a0 " + node_Tx.hijos[0].token.value + "\n"
  elif node_Tx.hijos[0].elemento == "identificador" and node_Tx.hijos[1].hijos[0].elemento != "''":
    resultado = generar_mainda_de_mision(node_Tx)
  return resultado

def generar_Tx_Ex_prima(node_Tx, node_Ex_prima):
  resultado = generar_Tx(node_Tx)
  resultado += generar_Ex_prima(node_Ex_prima)
  return resultado

def generar_ex(node_e):
  resultado = generar_Tx_Ex_prima(node_e.hijos[0],node_e.hijos[1])
  return resultado


def generar_variable(node):
  global data
  data += str(node.hijos[1].token.value) + ": .word	0:1\n"
  if node.hijos[3].hijos[0].elemento == "''":
      return ""
  else:
      return generar_ex(node.hijos[3].hijos[1].hijos[0]) + "sw $a0 " + str(node.hijos[1].token.value) + "\n"

def generar_asignacion_de_variable(arbol):
    codigo = generar_ex(arbol.hijos[1].hijos[1].hijos[0]) + "sw $a0 " + str(arbol.hijos[0].token.value) + "\n"
    return codigo


def generar_if(arbol):
  codigo = generar_ex(arbol.hijos[2].hijos[0])
  codigo += "beq $a0 $t1 label_true\n"
  codigo += "label_false:\n"
  codigo += generar_codigo(arbol.hijos[6])
  codigo += "b label_end\n"
  codigo += "label_true:\n"
  codigo += generar_codigo(arbol.hijos[4])
  codigo += "label_end:\n"
  return codigo

def generar_devuelve(arbol):
  codigo = ""
  if arbol.hijos[0].elemento != "''":
    codigo = generar_ex(arbol.hijos[1].hijos[0])
  return codigo

def generar_imprimir(arbol):
    codigo=""
    if arbol.hijos[2].typeo == "num":
        codigo = generar_ex(arbol.hijos[2].hijos[0])
        codigo += "li $v0 1\n"
        codigo += "syscall\n"
        codigo += "li $v0 4\nla $a0 endl\nsyscall\n"
    if arbol.hijos[2].typeo == "decimal":
        codigo = generar_ex(arbol.hijos[2].hijos[0])
        #codigo += "lw $f12 $a0"
        codigo += "li $v0 2\n"
        codigo += "syscall\n"
        codigo += "li $v0 4\nla $a0 endl\nsyscall\n"
    return codigo

def generar_PL_prima(PL_prima):
  codigo = ""
  if PL_prima.hijos[0].elemento != "''":
    codigo = generar_PL_PL_prima(PL_prima.hijos[1],PL_prima.hijos[2])
  return codigo

def generar_PL(PL):
  codigo = generar_ex(PL.hijos[0].hijos[0])
  codigo += "sw $a0 0($sp)\naddiu $sp $sp-4\n"
  return codigo

def generar_PL_PL_prima(PL,PL_prima):
  codigo = generar_PL (PL)
  codigo += generar_PL_prima (PL_prima)
  return codigo

def generar_parametros(arbol):
  codigo = generar_PL_PL_prima(arbol.hijos[0],arbol.hijos[1])
  return codigo

def generar_mainda_de_mision(arbol):
  codigo = "sw $fp 0($sp)\naddiu $sp $sp-4\n"
  if arbol.hijos[1].hijos[1].hijos[0].elemento != "''":
    codigo += generar_parametros(arbol.hijos[1].hijos[1])
  codigo += "jal " + arbol.hijos[0].token.value + "\n"
  return codigo

def contar_Y(Y):
  global total
  total = total + 1
  parametros.append(Y.hijos[1].token.value)

def contar_Y_prima(Y_prima):
  if Y_prima.hijos[0].elemento != "''":
    contar_Y(Y_prima.hijos[1])
    contar_Y_prima(Y_prima.hijos[2])

def contar_parametros(arbol):
  global total
  total = 0
  contar_Y(arbol.hijos[0])
  contar_Y_prima(arbol.hijos[1])
  return total


def generar_main(arbol):
    codigo=""
    for subarbol in arbol.hijos:
      if subarbol.elemento=="FuncionPrincipal":
          codigo = generar_codigo(subarbol)
    codigo += "li $v0 10\nsyscall\n"
    return codigo

def generar_codigo(arbol):
  codigo = ""
  if arbol.elemento == "FuncionPrincipal":
    codigo += "main:\n"
  if arbol.elemento == "DeclaracionVariable":
    codigo += generar_variable(arbol)
  if (arbol.elemento=="SentenciasCiclo" or arbol.elemento == "Sentencias") and arbol.hijos[0].elemento == "print":
    codigo += generar_imprimir(arbol)
  if arbol.elemento == "J":
    codigo += generar_devuelve(arbol)
  if (arbol.elemento=="SentenciasCiclo" or arbol.elemento == "Sentencias") and arbol.hijos[0].elemento=="identificador"and arbol.hijos[1].hijos[0].elemento=="igual":
    codigo += generar_asignacion_de_variable(arbol)
  if ((arbol.elemento=="SentenciasCiclo" or arbol.elemento == "Sentencias") and (arbol.hijos[0].elemento=="si" or arbol.hijos[0].elemento=="ciclo")) or arbol.elemento == "DeclaracionFuncion":
    if arbol.hijos[0].elemento=="si":
      codigo += generar_if(arbol)
  else:
    for subarbol in arbol.hijos:
      if subarbol.elemento!="FuncionPrincipal":
        codigo += generar_codigo(subarbol)

  return codigo

codigo_text = generar_main(AnalizadorSemantico.ll1.tree)
codigo_text += generar_codigo(AnalizadorSemantico.ll1.tree)
codigo = data+"\n.text\n\n" + codigo_text

file=open('codigo.s','w')
file.write(codigo)
file.close()