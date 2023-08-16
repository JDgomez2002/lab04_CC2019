# Ejercicio 1
# Jose Daniel Gomez 21429
# Gonzalo Santizo 21504

def infix_to_postfix(expression):
  # Diccionario para asignar precedencia a los operadores
  precedence = {'*': 3, '+': 2, '|': 1}
  
  output = []  # Lista para almacenar la salida
  stack = []   # Pila para almacenar los operadores
  
  for char in expression:
    if char.isalpha():
      # Si el carácter es una letra, se agrega directamente a la salida
      output.append(char)
    elif char == '(':
      # Si el carácter es un paréntesis de apertura, se agrega a la pila
      stack.append(char)
    elif char == ')':
      # Si el carácter es un paréntesis de cierre, se desapilan los operadores
      # hasta encontrar el paréntesis de apertura correspondiente
      while stack and stack[-1] != '(':
        output.append(stack.pop())
      stack.pop()  # Se elimina el paréntesis de apertura de la pila
    elif char in precedence:
      # Si el carácter es un operador, se desapilan los operadores de mayor
      # o igual precedencia y se agregan a la salida
      while stack and stack[-1] != '(' and precedence[char] <= precedence.get(stack[-1], 0):
        output.append(stack.pop())
      stack.append(char)  # Se agrega el operador a la pila
  
  # Se desapilan los operadores restantes y se agregan a la salida
  while stack:
    output.append(stack.pop())
  
  # Se devuelve la expresión en notación postfija como un string
  return ''.join(output)

expression = '(a|b)*c+d'
postfix = infix_to_postfix(expression)
print(postfix)  # Salida: ab|c*d+