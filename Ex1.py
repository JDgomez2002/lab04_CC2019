# Ejercicio 1
# Jose Daniel Gomez 21429
# Gonzalo Santizo 21504

from graphviz import Digraph

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

def infix_to_postfix(expression):
    precedence = {'*': 3, '+': 2, '|': 1}
    
    def is_operator(char):
        return char in precedence or char in '()'

    output = []
    stack = []
    
    for char in expression:
        if char.isalpha():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif char in precedence:
            while stack and stack[-1] != '(' and precedence[char] <= precedence.get(stack[-1], 0):
                output.append(stack.pop())
            stack.append(char)
    
    while stack:
        output.append(stack.pop())

    result = []

    for item in output:
        if item.isalpha():
            result.insert(0, item)
        else:
            result.append(item)
    
    return ''.join(result)

def construir_arbol(expresion_postfix):
    pila = []

    for caracter in expresion_postfix:
        if caracter.isalpha():
            nodo = Nodo(caracter)
            pila.append(nodo)
        else:
            nodo = Nodo(caracter)
            if len(pila)>0:
                nodo.derecha = pila.pop()
                if len(pila)>0:
                    nodo.izquierda = pila.pop()
            pila.append(nodo)

    return pila[-1]

def imprimir_arbol(nodo, espaciado=0):
    if nodo is None:
        return
    espaciado += 4
    imprimir_arbol(nodo.derecha, espaciado)
    if nodo.derecha is not None:
        print(" " * (espaciado - 4) + "│", " │")
    print(" " * (espaciado - 4) + "──", nodo.valor)
    if nodo.izquierda is not None:
        print(" " * (espaciado-1) + "│")
    imprimir_arbol(nodo.izquierda, espaciado)

#--------------------------------------------------------------------------------

class Estado:
    contador = 0
    
    def __init__(self, aceptacion=False, simbolo=None):
        self.id = Estado.contador
        Estado.contador += 1
        self.aceptacion = aceptacion
        self.simbolo = simbolo
        self.transiciones = {}
    
    def agregar_transicion(self, simbolo, estado):
        if simbolo in self.transiciones:
            self.transiciones[simbolo].add(estado)
        else:
            self.transiciones[simbolo] = {estado}
    

def crear_afn(nodo):
    if nodo is None:
        return []
    
    if nodo.valor.isalpha():
        estado_inicial = Estado()
        estado_final = Estado(aceptacion=True, simbolo=nodo.valor)
        estado_inicial.agregar_transicion(nodo.valor, estado_final)
        return [estado_inicial, estado_final]
    
    if nodo.valor == "*":
        nodo_izq = nodo.izquierda
        
        afn_izq = crear_afn(nodo_izq)
        
        estado_inicial = Estado()
        estado_final = Estado(aceptacion=True)
        if len(afn_izq)>0:
            estado_inicial.agregar_transicion('ε', afn_izq[0])
            estado_inicial.agregar_transicion('ε', estado_final)
            afn_izq[-1].agregar_transicion('ε', afn_izq[0])
            afn_izq[-1].agregar_transicion('ε', estado_final)
            return [estado_inicial, estado_final]

    if nodo.valor == "+":
        nodo_izq = nodo.izquierda
        
        afn_izq = crear_afn(nodo_izq)
        
        if len(afn_izq)>0:
            estado_inicial = afn_izq[0]
            estado_final = Estado(aceptacion=True)
            estado_final.agregar_transicion('ε', estado_inicial)
            afn_izq[-1].agregar_transicion('ε', estado_final)
            return [estado_inicial, estado_final]

    if nodo.valor in "|":
        nodo_izq, nodo_der = nodo.izquierda, nodo.derecha
        
        afn_izq = crear_afn(nodo_izq)
        afn_der = crear_afn(nodo_der)
        
        estado_inicial = Estado()
        estado_final = Estado(aceptacion=True)
        estado_inicial.agregar_transicion('ε', afn_izq[0])
        estado_inicial.agregar_transicion('ε', afn_der[0])
        afn_izq[-1].agregar_transicion('ε', estado_final)
        afn_der[-1].agregar_transicion('ε', estado_final)
        return [estado_inicial, estado_final]

# Función para obtener los estados alcanzables desde un estado dado
def estados_alcanzables(estado, visitados=None):
    if visitados is None:
        visitados = set()
    visitados.add(estado)
    if 'ε' in estado.transiciones:
        for siguiente_estado in estado.transiciones['ε']:
            if siguiente_estado not in visitados:
                estados_alcanzables(siguiente_estado, visitados)
    return visitados

# Crear una lista de nodos y una lista de estados para mostrarlos en pantalla
nodos = []
estados = []

# if type(afn)!='NoneType':
#     for estado in afn:
#         estados_alcanzables_desde_estado = estados_alcanzables(estado)
#         nodos.append(estado)
#         estados.append(estados_alcanzables_desde_estado)

# Imprimir nodos y estados
for i, estado in enumerate(nodos):
    print(f"Nodo {i}: {estado.simbolo if estado.aceptacion else 'No aceptación'}")

# for i, estados_alcanzables_desde_estado in enumerate(estados):
#     print(f"Estados alcanzables desde Nodo {i}: {[estado.id for estado in estados_alcanzables_desde_estado]}")

# def crear_grafico_afn(afn):
#     dot = Digraph(comment='AFN')
    
#     for estado in afn:
#         dot.node(str(estado.id), label=f"{estado.id}\n{estado.simbolo if estado.simbolo else ''}", shape='doublecircle' if estado.aceptacion else 'circle')
        
#         if estado.transiciones:
#             for simbolo, destinos in estado.transiciones.items():
#                 for destino in destinos:
#                     dot.edge(str(estado.id), str(destino.id), label=simbolo)
    
#     return dot

def crear_grafico_afn(afn):
    if afn is None:
        return None

    dot = Digraph(comment='AFN')

    for estado in afn:
        dot.node(str(estado.id), label=f"{estado.id}\n{estado.simbolo if estado.simbolo else ''}", shape='doublecircle' if estado.aceptacion else 'circle')

        if estado.transiciones:
            for simbolo, destinos in estado.transiciones.items():
                for destino in destinos:
                    dot.edge(str(estado.id), str(destino.id), label=simbolo)

    return dot


#Infix to postfix
expression = "(a*|b*)+"
postfix = infix_to_postfix(expression)
print("1)",postfix)  # Salida: ab|c*d+

# arbol desde postfix
arbol = construir_arbol(postfix)
imprimir_arbol(arbol)

# Ejemplo de uso con el árbol generado anteriormente
# arbol = construir_arbol("(a*|b*)+")
afn = crear_afn(arbol)

# Crear el gráfico del AFN
afn_grafico = crear_grafico_afn(afn)
if afn_grafico is not None:
    afn_grafico.format = 'jpg'
    afn_grafico.render('afn1', view=True)

print("\n\n")

#Infix to postfix
expression = "((e|a)|b*)*"
postfix = infix_to_postfix(expression)
print("2)",postfix)  # Salida: ab|c*d+

# arbol desde postfix
arbol = construir_arbol(postfix)
imprimir_arbol(arbol)

# Ejemplo de uso con el árbol generado anteriormente
# arbol = construir_arbol("(a*|b*)+")
afn = crear_afn(arbol)

# Crear el gráfico del AFN
afn_grafico = crear_grafico_afn(afn)
if afn_grafico is not None:
    afn_grafico.format = 'jpg'
    afn_grafico.render('afn2', view=True)

print("\n\n")

#Infix to postfix
expression = "(a|b)*abb(a|b)*"
postfix = infix_to_postfix(expression)
print("3)",postfix)  # Salida: ab|c*d+

# arbol desde postfix
arbol = construir_arbol(postfix)
imprimir_arbol(arbol)

# Ejemplo de uso con el árbol generado anteriormente
# arbol = construir_arbol("(a*|b*)+")
afn = crear_afn(arbol)

# Crear el gráfico del AFN
afn_grafico = crear_grafico_afn(afn)
if afn_grafico is not None:
    afn_grafico.format = 'jpg'
    afn_grafico.render('afn3', view=True)

print("\n\n")

#Infix to postfix
expression = "0?(1?)?0*"
postfix = infix_to_postfix(expression)
print("4)",postfix)  # Salida: ab|c*d+

# arbol desde postfix
arbol = construir_arbol(postfix)
imprimir_arbol(arbol)

# Ejemplo de uso con el árbol generado anteriormente
# arbol = construir_arbol("(a*|b*)+")
afn = crear_afn(arbol)

# Crear el gráfico del AFN
afn_grafico = crear_grafico_afn(afn)
if afn_grafico is not None:
    afn_grafico.format = 'jpg'
    afn_grafico.render('afn4', view=True)
