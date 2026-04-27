from parsertable import tabla_action, tabla_goto, productions, prod_num
from sdt import tabla_simbolos, accion_semantica
from sdt import Nodo

def mapear_tokens(tokens):
    simbolos = []
    lexemas = []
    for tipo, valor in tokens:
        if tipo == 'keyword' and valor in {'int', 'float', 'double', 'char', 'void', 'bool', 'long', 'short', 'unsigned'}:
            simbolos.append('TYPE')
            lexemas.append(valor)
        elif tipo == 'identifier':
            simbolos.append('ID')
            lexemas.append(valor)
        elif tipo == 'constant':
            simbolos.append('CONST')
            lexemas.append(valor)
        elif tipo == 'operator' and valor == '=':
            simbolos.append('=')
            lexemas.append(valor)
        elif tipo == 'operator' and valor == '+':
            simbolos.append('+')
            lexemas.append(valor)
        elif tipo == 'operator' and valor == '*':
            simbolos.append('*')
            lexemas.append(valor)
        elif tipo == 'punctuation' and valor == ';':
            simbolos.append(';')
            lexemas.append(valor)
        elif tipo == 'punctuation' and valor == '(':
            simbolos.append('(')
            lexemas.append(valor)
        elif tipo == 'punctuation' and valor == ')':
            simbolos.append(')')
            lexemas.append(valor)
        else:
            raise Exception(f"Unexpected token: {tipo} {valor}")
    simbolos.append('$')
    lexemas.append('$')
    return simbolos, lexemas

def analizar(tokens):
    try:
        entrada, lexemas = mapear_tokens(tokens)
    except Exception as e:
        print(f"Token mapping error: {e}")
        return False

    pila = [0]
    pila_sem = []
    pos = 0
    pos_lex = 0

    while True:
        estado = pila[-1]
        token = entrada[pos]
        accion = tabla_action.get(estado, {}).get(token)
        if accion is None:
            print("Parsing error...")
            return False

        if accion.startswith('S'):
            siguiente = int(accion[1:])
            pila.append(token)
            pila.append(siguiente)
            if token in ('ID', 'CONST', 'TYPE'):
                pila_sem.append(lexemas[pos_lex])
                pos_lex += 1
            else:
                pila_sem.append(token)
                pos_lex += 1
            pos += 1
        elif accion.startswith('R'):
            num_prod = int(accion[1:])
            lhs, rhs = productions[num_prod]
            cantidad = len(rhs)
            elementos = []
            for _ in range(cantidad):
                pila.pop()
                simbolo = pila.pop()
                elementos.insert(0, pila_sem.pop())
            resultado = accion_semantica(num_prod, elementos)
            pila_sem.append(resultado)
            estado_expuesto = pila[-1]
            siguiente = tabla_goto[estado_expuesto][lhs]
            pila.append(lhs)
            pila.append(siguiente)
        elif accion == 'acc':
            print("Parsing Success!")
            if len(tabla_simbolos.simbolos) > 0:
                print("SDT Verified!")
            else:
                print("SDT error: no declarations")
            return True
        else:
            print("Parsing error...")
            return False