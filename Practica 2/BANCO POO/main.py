from funciones import clear, pause, registro, login, menu

def main():
    while True:
        clear()
        print("Bienvenido al sistema bancario")
        print("1. Iniciar sesion")
        print("2. Registrarse")
        print("0. Salir")
        option = int(input("Seleccione una opcion: "))

        if option == 1:
            user = login()
            if user:
                menu(user)
        elif option == 2:
            registro()
        elif option == 0:
            break

if __name__ == "__main__":
    main()
