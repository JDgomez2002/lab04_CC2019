# Ejercicio 1
# Jose Daniel Gomez 21429
# Gonzalo Santizo 21504

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
            nodo.derecha = pila.pop()
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

#Infix to postfix example
expression = '(a|b)*c+d'
postfix = infix_to_postfix(expression)
print(postfix)  # Salida: ab|c*d+

# Ejemplo de uso
expresion_postfix = "ABCDE+-*|"
arbol = construir_arbol(expresion_postfix)
imprimir_arbol(arbol)