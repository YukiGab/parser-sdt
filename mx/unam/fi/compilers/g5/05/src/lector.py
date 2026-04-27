import re
from lexertable import token              

def analizearchive(ruta):
    lista_tokens =[] #creamos lista vacia
    try:
        with open(ruta,'r') as archivo:
            lineas = archivo.read().splitlines()#leemos las lineas y las asignamos a una lista     


        for linea in lineas: 
            position = 0 #nos aseguramos empezar desde el inicio



            while position < len(linea): #aseguramos agarrar tordos los caracteres la linea actual
                if linea[position].isspace(): #quitamos los espacios
                    position += 1
                    continue

                palabra = linea[position:] #podriamos decir que sirve para apuntar al siguiente token
                palabraval = False

                for palabras, tipo in token: #revisa mi tabla completa
                    validar = re.compile(palabras) #arma una expresion regular para buscar patrones
                    comparar = validar.match(palabra) #intenta buscar patrones al inicio de la cadena

                    if comparar: #si la linea coincide con la tabla es verdadero
                        valor = comparar.group(0) #guarda el token exacto que coincidio con la tabla
                        if tipo: #si existe el tipo en nuestra tabla
                            lista_tokens.append((tipo, valor)) # Guardamos tipo y lexema en una tupla
                    
                        position += len(valor) #nos movemos al siguiente token
                        palabraval = True
                        break
        
            if not palabraval: #si no coincidio con ningun patron (en este caso, con algun elemento de nuestra tabla)
                print(f"Error: Invalid symbol at '{linea[position]}'") 
                return

        return lista_tokens #retornamos la lista de nuestros tokens totales
    except FileNotFoundError:
        print(f"Error, file not found in {ruta}")

def analizeterminal(code):
    lista_tokens =[] #creamos lista vacia
    lineas = code.splitlines() #leemos las lineas y las asignamos a una lista
    for linea in lineas: 
            position = 0 #nos aseguramos empezar desde el inicio



            while position < len(linea): #aseguramos agarrar tordos los caracteres la linea actual
                if linea[position].isspace(): #quitamos los espacios
                    position += 1
                    continue

                palabra = linea[position:] #podriamos decir que sirve para apuntar al siguiente token
                palabraval = False

                for palabras, tipo in token: #revisa mi tabla completa
                    validar = re.compile(palabras) #arma una expresion regular para buscar patrones
                    comparar = validar.match(palabra) #intenta buscar patrones al inicio de la cadena

                    if comparar: #si la linea coincide con la tabla es verdadero
                        valor = comparar.group(0) #guarda el token exacto que coincidio con la tabla
                        if tipo: #si existe el tipo en nuestra tabla
                            lista_tokens.append((tipo, valor)) # Guardamos tipo y lexema en una tupla
                    
                        position += len(valor) #nos movemos al siguiente token
                        palabraval = True
                        break
        
            if not palabraval: #si no coincidio con ningun patron (en este caso, con algun elemento de nuestra tabla)
                print(f"Error: Invalid symbol at '{linea[position]}'") 
                return

    return lista_tokens #retornamos la lista de nuestros tokens totales