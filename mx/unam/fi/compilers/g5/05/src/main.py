import lector
import parser

def main():
    while True:
        seleccion = input("Select how you will enter your code (archive/terminal): ").strip().lower()
        match seleccion:
            case "archive":
                try:
                    ruta = input("Enter your file path:\n")
                    tokens = lector.analizearchive(ruta)
                    if tokens:
                        print("Tokens generados exitosamente")
                        parser.analizar(tokens)
                except:
                    print("Error, invalid location")
                break
            case "terminal":
                code = input("Enter your code:\n")
                tokens = lector.analizeterminal(code)
                if tokens:
                    print("Tokens generados exitosamente")
                    parser.analizar(tokens)
                break
            case "exit":
                exit()
            case _:
                print("Error: Invalid option. Please try again.\n")

if __name__ == "__main__":
    print("Welcome to Parser & SDT from Team 5")
    main()