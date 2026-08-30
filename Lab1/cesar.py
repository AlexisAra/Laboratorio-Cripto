import sys

def cifrado_cesar(texto, corrimiento):
    resultado = ""
    
    for char in texto:
        # Verificar si el carácter es una letra
        if char.isalpha():
            # Definir el valor base ASCII dependiendo si es mayúscula o minúscula
            base = ord('A') if char.isupper() else ord('a')
            
            # Aplicar la fórmula del cifrado César y agregar al resultado
            nuevo_char = chr((ord(char) - base + corrimiento) % 26 + base)
            resultado += nuevo_char
        else:
            # Si no es letra (como los espacios), se mantiene igual
            resultado += char
            
    return resultado

if __name__ == "__main__":
    # Verificar que se hayan entregado los argumentos correctos
    if len(sys.argv) != 3:
        print("Uso correcto: python3 cesar.py \"<texto_a_cifrar>\" <corrimiento>")
        sys.exit(1)

    texto_original = sys.argv[1]
    
    try:
        corrimiento = int(sys.argv[2])
    except ValueError:
        print("Error: El corrimiento debe ser un número entero.")
        sys.exit(1)

    # Llamar a la función e imprimir el resultado
    texto_cifrado = cifrado_cesar(texto_original, corrimiento)
    print(texto_cifrado)