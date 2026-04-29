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

    def limpiar(self):
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
    
    def mostrar(self):
        for nombre, datos in self.simbolos.items():
            print(f"{nombre} -> type: {datos['tipo']}, value: {datos['valor']}")

tabla_simbolos = TablaSimbolos()

def evaluarexpresion(nodo):
    if nodo is None:
        raise Exception("Semantic error: invalid expression")
    
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
    
    else:
        raise Exception(f"Unknown operator: {nodo.tipo}")

def accion_semantica(num_prod, elementos):
    #D -> TYPE ID = E
    if num_prod == 2:
        tipo_dato = elementos[0]
        nombre_var = elementos[1]
        expr_nodo = elementos[3]

        valor = evaluarexpresion(expr_nodo)

        if tipo_dato == "int" and isinstance(valor, float):
            raise Exception(
                f"Semantic error: cannot assign float value {valor} to int variable '{nombre_var}'"
            )
        
        tabla_simbolos.declarar(nombre_var, tipo_dato)
        tabla_simbolos.asignar(nombre_var, valor)

        return Nodo('DECL', nombre_var, [Nodo('TYPE', tipo_dato), expr_nodo])
    
    #E -> E + T
    elif num_prod == 3:
        return Nodo('+', None, [elementos[0], elementos[2]])
    
    # E -> T
    elif num_prod == 4:
        return elementos[0]

    #T -> T * F
    elif num_prod == 5:
        return Nodo('*', None, [elementos[0], elementos[2]])
    
    # T -> F 
    elif num_prod == 6:
        return elementos[0]
    
    # F -> ( E )
    elif num_prod == 7:
        return elementos[1]
    
    # F -> ID
    elif num_prod == 8:
        return Nodo('ID', elementos[0])
    
    # F -> CONST
    elif num_prod == 9:
        val = elementos[0]

        if isinstance(val, (int, float)):
            return Nodo('CONST', val)

        if isinstance(val, str):
            try:
                val = float(val) if '.' in val else int(val)
            except ValueError:
                raise Exception(f"Semantic error: invalid constant '{val}'")

            return Nodo('CONST', val)

        raise Exception(f"Semantic error: invalid constant '{val}'")
    
    # S -> D
    elif num_prod == 1:
        return elementos[0]
    
    return None

def imprimir_arbol(nodo, nivel=0):
    if nodo is None:
        return

    sangria = "  " * nivel
    print(f"{sangria}{nodo.tipo}: {nodo.valor}")

    for hijo in nodo.hijos:
        imprimir_arbol(hijo, nivel + 1)

def exportar_arbol_graphviz(nodo, nombre_archivo="ast"):
    if nodo is None:
        print("No AST available.")
        return

    dot_path = f"{nombre_archivo}.dot"
    png_path = f"{nombre_archivo}.png"

    contador = [0]
    lineas = [
        "digraph AST {",
        '    node [shape=box, style="rounded"];'
    ]

    def recorrer(n):
        node_id = f"n{contador[0]}"
        contador[0] += 1

        etiqueta = n.tipo
        if n.valor is not None:
            etiqueta += f"\\n{n.valor}"

        lineas.append(f'    {node_id} [label="{etiqueta}"];')

        for hijo in n.hijos:
            hijo_id = recorrer(hijo)
            lineas.append(f"    {node_id} -> {hijo_id};")

        return node_id

    recorrer(nodo)
    lineas.append("}")

    with open(dot_path, "w") as archivo:
        archivo.write("\n".join(lineas))

    print(f"AST DOT generated: {dot_path}")

    try:
        import subprocess
        subprocess.run(
            ["dot", "-Tpng", dot_path, "-o", png_path],
            check=True
        )
        print(f"AST image generated: {png_path}")
    except Exception:
        print("Graphviz image could not be generated.")
        print("You can still open the .dot file with a Graphviz viewer.")