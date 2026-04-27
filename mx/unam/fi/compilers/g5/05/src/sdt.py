class Nodo:
    def __init__(self, tipo, valor=None, hijos=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = hijos if hijos else []

    def __repr__(self):
        return f"Nodo({self.tipo}, {self.valor}, {self.hijos})"

class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}

    def declarar(self, nombre, tipo):
        if nombre in self.simbolos:
            raise Exception(f"Semantic error: variable '{nombre}' already declared")
        self.simbolos[nombre] = {'tipo': tipo, 'valor': None}

    def asignar(self, nombre, valor):
        if nombre not in self.simbolos:
            raise Exception(f"Semantic error: variable '{nombre}' not declared")
        self.simbolos[nombre]['valor'] = valor

    def obtener(self, nombre):
        if nombre not in self.simbolos:
            raise Exception(f"Semantic error: variable '{nombre}' not declared")
        return self.simbolos[nombre]

tabla_simbolos = TablaSimbolos()

def evaluarexpresion(nodo):
    if nodo.tipo == 'CONST':
        return nodo.valor
    elif nodo.tipo == 'ID':
        var = tabla_simbolos.obtener(nodo.valor)
        if var['valor'] is None:
            raise Exception(f"Semantic error: variable '{nodo.valor}' used before initialization")
        return var['valor']
    elif nodo.tipo == '+':
        return evaluarexpresion(nodo.hijos[0]) + evaluarexpresion(nodo.hijos[1])
    elif nodo.tipo == '*':
        return evaluarexpresion(nodo.hijos[0]) * evaluarexpresion(nodo.hijos[1])
    elif nodo.tipo == '=':
        return evaluarexpresion(nodo.hijos[1])
    else:
        raise Exception(f"Unknown operator: {nodo.tipo}")

def accion_semantica(num_prod, elementos):
    if num_prod == 2:
        tipo_dato = elementos[0]
        nombre_var = elementos[1]
        expr_nodo = elementos[3]
        valor = evaluarexpresion(expr_nodo)
        tabla_simbolos.declarar(nombre_var, 'int')
        tabla_simbolos.asignar(nombre_var, valor)
        return Nodo('DECL', nombre_var, [Nodo('TYPE', tipo_dato), expr_nodo])
    elif num_prod == 3:
        return Nodo('+', None, [elementos[0], elementos[2]])
    elif num_prod == 5:
        return Nodo('*', None, [elementos[0], elementos[2]])
    elif num_prod in (4, 6):
        return elementos[0]
    elif num_prod == 7:
        return elementos[1]
    elif num_prod == 8:
        return Nodo('ID', elementos[0])
    elif num_prod == 9:
        val = elementos[0]
        try:
            val = float(val) if '.' in val else int(val)
        except:
            pass
        return Nodo('CONST', val)
    elif num_prod == 1:
        return elementos[0]
    else:
        return None