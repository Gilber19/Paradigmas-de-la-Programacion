import os
import platform
from clases import Bank

def clear():
    system = platform.system()
    if system in ["Linux", "Darwin"]:
        os.system("clear")
    elif system == "Windows":
        os.system("cls")

def pause():
    system = platform.system()
    if system in ["Linux", "Darwin"]:
        input("Presione Enter para continuar...")
    elif system == "Windows":
        os.system("pause")

def registro():
    clear()
    print("Bienvenido al sistema de registro\nPor favor ingrese los datos que se piden")

    tName = input("Nombre de Usuario: ")
    tApp = input("Apellido Paterno: ")
    tApm = input("Apellido Materno: ")

    clear()
    print("Fecha de nacimiento")
    tDay = int(input("Dia: "))
    tMonth = int(input("Mes: "))
    tYear = int(input("Año: "))

    clear()
    print("Informacion de contacto")
    tMail = input("Correo: ")
    tPhone = input("Número de celular: ")

    while True:
        tPass = input("Contrasenia: ")
        tPassConfirm = input("Confirmar Contrasenia: ")
        if tPass == tPassConfirm:
            break
        else:
            print("Las contrasenias no coinciden. Intente de nuevo.")

    tCurp = input("CURP: ")

    user = Bank(tName, tApp, tApm, tDay, tMonth, tYear, tMail, tPhone, tPass, tCurp)
    save_user(user)

    print("Usuario registrado correctamente")
    print(f"Su cuenta es {user.no_cuenta}\nSu CLABE es {user.clabe}\nY su saldo actual es {user.saldo:,.2f}")
    pause()

def save_user(user):
    dir_actual = os.path.dirname(os.path.realpath(__file__))
    dir_reg = os.path.join(dir_actual, "reg")

    if not os.path.exists(dir_reg):
        os.makedirs(dir_reg)

    doc_name = os.path.join(dir_reg, "cuentas.txt")

    with open(doc_name, 'a') as doc:
        doc.write("=== Usuario ===\n")
        doc.write(f"Nombre: {user.name}\n")
        doc.write(f"Apellido Paterno: {user.app}\n")
        doc.write(f"Apellido Materno: {user.apm}\n")
        doc.write(f"Fecha de Nacimiento: {user.day}/{user.month}/{user.year}\n")
        doc.write(f"Correo: {user.mail}\n")
        doc.write(f"Telefono: {user.num_phone}\n")
        doc.write(f"Contrasenia: {user.get_password()}\n")
        doc.write(f"CURP: {user.curp}\n")
        doc.write(f"Cuenta: {user.no_cuenta}\n")
        doc.write(f"CLABE: {user.clabe}\n")
        doc.write(f"Saldo: {user.saldo:,.2f}\n")
        doc.write("\n")

def load_user(name, password):
    dir_actual = os.path.dirname(os.path.realpath(__file__))
    dir_reg = os.path.join(dir_actual, "reg", "cuentas.txt")

    if not os.path.exists(dir_reg):
        return None

    with open(dir_reg, 'r') as doc:
        for line in doc:
            if "=== Usuario ===" in line:
                tUser = {}
            if line.startswith("Nombre:"):
                tUser["name"] = line.split(": ")[1].strip()
            elif line.startswith("Apellido Paterno:"):
                tUser["app"] = line.split(": ")[1].strip()
            elif line.startswith("Apellido Materno:"):
                tUser["apm"] = line.split(": ")[1].strip()
            elif line.startswith("Fecha de Nacimiento:"):
                fecha = line.split(": ")[1].strip().split("/")
                tUser["day"], tUser["month"], tUser["year"] = int(fecha[0]), int(fecha[1]), int(fecha[2])
            elif line.startswith("Correo:"):
                tUser["mail"] = line.split(": ")[1].strip()
            elif line.startswith("Telefono:"):
                tUser["num_phone"] = line.split(": ")[1].strip()
            elif line.startswith("Contrasenia:"):
                tUser["password"] = line.split(": ")[1].strip()
            elif line.startswith("CURP:"):
                tUser["curp"] = line.split(": ")[1].strip()
            elif line.startswith("Cuenta:"):
                tUser["no_cuenta"] = line.split(": ")[1].strip()
            elif line.startswith("CLABE:"):
                tUser["clabe"] = line.split(": ")[1].strip()
            elif line.startswith("Saldo:"):
                tUser["saldo"] = float(line.split(": ")[1].replace(",", "").strip())

                if tUser["name"] == name and tUser["password"] == password:
                    return Bank(
                        tUser["name"], tUser["app"], tUser["apm"], tUser["day"], tUser["month"], tUser["year"],
                        tUser["mail"], tUser["num_phone"], tUser["password"], tUser["curp"],
                        tUser["no_cuenta"], tUser["clabe"], tUser["saldo"]
                    )
    return None

def update_user(user):
    dir_actual = os.path.dirname(os.path.realpath(__file__))
    dir_reg = os.path.join(dir_actual, "reg", "cuentas.txt")

    if not os.path.exists(dir_reg):
        return

    lines = []
    with open(dir_reg, 'r') as doc:
        lines = doc.readlines()

    with open(dir_reg, 'w') as doc:
        skip = False
        for line in lines:
            if line.startswith("=== Usuario ==="):
                if skip:
                    skip = False
                if not skip:
                    doc.write(line)
            elif line.startswith("Nombre:") and line.split(": ")[1].strip() == user.name:
                skip = True
                doc.write("=== Usuario ===\n")
                doc.write(f"Nombre: {user.name}\n")
                doc.write(f"Apellido Paterno: {user.app}\n")
                doc.write(f"Apellido Materno: {user.apm}\n")
                doc.write(f"Fecha de Nacimiento: {user.day}/{user.month}/{user.year}\n")
                doc.write(f"Correo: {user.mail}\n")
                doc.write(f"Telefono: {user.num_phone}\n")
                doc.write(f"Contrasenia: {user.get_password()}\n")
                doc.write(f"CURP: {user.curp}\n")
                doc.write(f"Cuenta: {user.no_cuenta}\n")
                doc.write(f"CLABE: {user.clabe}\n")
                doc.write(f"Saldo: {user.saldo:,.2f}\n")
                doc.write("\n")
            elif not skip:
                doc.write(line)

def find_user(account_number):
    dir_actual = os.path.dirname(os.path.realpath(__file__))
    dir_reg = os.path.join(dir_actual, "reg", "cuentas.txt")

    if not os.path.exists(dir_reg):
        return None

    with open(dir_reg, 'r') as doc:
        for line in doc:
            if "=== Usuario ===" in line:
                tUser = {}
            if line.startswith("Nombre:"):
                tUser["name"] = line.split(": ")[1].strip()
            elif line.startswith("Apellido Paterno:"):
                tUser["app"] = line.split(": ")[1].strip()
            elif line.startswith("Apellido Materno:"):
                tUser["apm"] = line.split(": ")[1].strip()
            elif line.startswith("Fecha de Nacimiento:"):
                fecha = line.split(": ")[1].strip().split("/")
                tUser["day"], tUser["month"], tUser["year"] = int(fecha[0]), int(fecha[1]), int(fecha[2])
            elif line.startswith("Correo:"):
                tUser["mail"] = line.split(": ")[1].strip()
            elif line.startswith("Telefono:"):
                tUser["num_phone"] = line.split(": ")[1].strip()
            elif line.startswith("Contrasenia:"):
                tUser["password"] = line.split(": ")[1].strip()
            elif line.startswith("CURP:"):
                tUser["curp"] = line.split(": ")[1].strip()
            elif line.startswith("Cuenta:"):
                tUser["no_cuenta"] = line.split(": ")[1].strip()
            elif line.startswith("CLABE:"):
                tUser["clabe"] = line.split(": ")[1].strip()
            elif line.startswith("Saldo:"):
                tUser["saldo"] = float(line.split(": ")[1].replace(",", "").strip())

                if tUser["no_cuenta"] == account_number:
                    return Bank(
                        tUser["name"], tUser["app"], tUser["apm"], tUser["day"], tUser["month"], tUser["year"],
                        tUser["mail"], tUser["num_phone"], tUser["password"], tUser["curp"],
                        tUser["no_cuenta"], tUser["clabe"], tUser["saldo"]
                    )
    return None

def login():
    clear()
    print("Iniciar sesion")
    name = input("Nombre de Usuario: ")
    password = input("Contrasenia: ")

    user = load_user(name, password)
    if user:
        print("Inicio de sesion exitoso")
        pause()
        return user
    else:
        print("Usuario o contrasenia incorrectos")
        pause()
        return None

def menu(user):
    while True:
        clear()
        print(f"Bienvenido, {user.name}")
        print("1. Ver saldo")
        print("2. Depositar")
        print("3. Retirar")
        print("4. Transferir")
        print("0. Salir")
        option = int(input("Seleccione una opcion: "))

        if option == 1:
            user.view_saldo()
            pause()
        elif option == 2:
            amount = float(input("Cantidad a depositar: "))
            user.depositar(amount)
            update_user(user)
            pause()
        elif option == 3:
            amount = float(input("Cantidad a retirar: "))
            user.retirar(amount)
            update_user(user)
            pause()
        elif option == 4:
            target_account = input("Cuenta destino: ")
            amount = float(input("Cantidad a transferir: "))
            target_user = find_user(target_account)
            if target_user:
                user.transferir(target_user,  amount)
                update_user(user)
                update_user(target_user)
            else:
                print("Cuenta destino no encontrada")
            pause()
        elif option == 0:
            break
