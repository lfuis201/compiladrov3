import ply.lex as lex

tokens = ('func',
          'si',
          'sino',
          'num',
          'lnum',
          'decimal',
          'ldecimal',
          'print',
          'string',
          'lstring',
          'ciclo',
          'return',
          'mas',
          'menos',
          'por',
          'and',
          'or',
          'dividir',
          'mayor',
          'menor',
          'pizquierdo',
          'pderecho',
          'cizquierdo',
          'cderecho',
          'coma',
          'igual',
          'menor_igual',
          'mayor_igual',
          'diferente',
          'identificador',
          'lizquierdo',
          'lderecho',
          'division',
          'true',
          'false',
          'modulo',
          'main',
          'comparacion')


t_func = r'func'
t_si = r'si'
t_sino = r'sino'
t_num = r'num'
t_decimal = r'decimal'
t_print = r'print'
t_string = r'string'
t_ciclo = r'ciclo'
t_return = r'return'
t_main = r'main'
t_comparacion = r'\=\='

t_mas = r'\+'
t_menos = r'\-'
t_por = r'\*'
t_dividir = r'\/'
t_modulo = r'\%'

t_and = r'\#and'
t_or = r'\#or'

t_mayor = r'\>'
t_menor = r'\<'

t_pizquierdo = r'\('
t_pderecho = r'\)'

t_lizquierdo = r'\{'
t_lderecho = r'\}'

t_cizquierdo = r'\['
t_cderecho = r'\]'

t_coma = r'\,'
t_igual = r'\='
t_menor_igual = r'\<\='
t_mayor_igual = r'\>\='
t_diferente = r'\!\='

def t_identificador(t):
  r'(?!decimal|si|sino|num|print|string|ciclo|return|func|false|true|main)[a-zA-Z]+[\w]*'
  try:
    t.value = t.value
  except ValueError:
    t.value = 0
  return t



# A regular expression rule with some action code
def t_false(t):
  r'false'
  t.value = False # guardamos el valor del lexema
  return t

def t_true(t):
  r'true'
  t.value = True # guardamos el valor del lexema
  return t

def t_lnum(t):
  r'\d+(?!\.)'
  try:
    t.value = int(t.value) # guardamos el valor del lexema
  except ValueError:
    t.value = 0
  return t

def t_ldecimal(t):
  r'(0|[1-9][0-9]*)\.[0-9]*'
  try:
    t.value = float(t.value)
  except ValueError:
    t.value = 0
  return t

def t_lstring(t):
  r'\"(\W|\w)+\"'
  t.value = t.value # guardamos el valor del lexema
  return t

def t_COMMENT(t):
    r'\-->.*'

# Define a rule so we can track line numbers
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
# Error handling rule
def t_error(t):
  print("Error léxico, caracter no conocido: '%s'" % t.value[0])
  t.lexer.skip(1)
  raise SystemExit
# Build the lexer
lexer = lex.lex()
# Test it out


def get_tokens(file):
    tokens = []

    f = open(file, "r")
    data = f.read()

    lexer.input(data)
    
    # Tokenize
    while True:
        unitok=[]
        tok = lexer.token()
        if not tok: 
            break
        tokens.append( [tok.type, tok.value, tok.lineno] )

    return tokens

file=open('test1.txt','r')
texto=file.readlines()
file.close()
data = texto
tokens=[]
tokens_info=[]
for renglon in texto:
  # Give the lexer some input
  lexer.input(renglon)
  # Tokenize
  while True:
    tok = lexer.token()
    if not tok:
      break # No more input
    tokens.append(tok.type)
    tokens_info.append(tok)
    #print(tok)