import random

class Person:
    def __init__(self, name, app, apm, day, month, year, mail, num_phone, password, curp):
        self.name = name
        self.app = app
        self.apm = apm
        self.day = day
        self.month = month
        self.year = year
        self.mail = mail
        self.num_phone = num_phone
        self.__password = password
        self.curp = curp

    def get_password(self):
        return self.__password

class Bank(Person):
    def __init__(self, name, app, apm, day, month, year, mail, num_phone, password, curp, no_cuenta=None, clabe=None, saldo=0.0):
        super().__init__(name, app, apm, day, month, year, mail, num_phone, password, curp)
        self.no_cuenta = no_cuenta if no_cuenta else self.gen_cuenta()
        self.clabe = clabe if clabe else self.gen_clabe()
        self.saldo = saldo

    def gen_cuenta(self):
        return str(random.randint(1000000000, 9999999999))

    def gen_clabe(self):
        return str(random.randint(100000000000000000, 999999999999999999))

    def depositar(self, amount):
        self.saldo += amount
        print(f"Depositado: {amount:,.2f}")
        print(f"Nuevo saldo: {self.saldo:,.2f}")

    def retirar(self, amount):
        if self.saldo >= amount:
            self.saldo -= amount
            print(f"Retirado: {amount:,.2f}")
            print(f"Nuevo saldo: {self.saldo:,.2f}")
        else:
            print("Saldo insuficiente")

    def transferir(self, other, amount):
        if self.saldo >= amount:
            self.saldo -= amount
            other.saldo += amount
            print(f"Transferido: {amount:,.2f}")
            print(f"Nuevo saldo de {self.name}: {self.saldo:,.2f}")
            print(f"Nuevo saldo de {other.name}: {other.saldo:,.2f}")
        else:
            print("Saldo insuficiente")

    def view_saldo(self):
        print(f"Saldo actual: {self.saldo:,.2f}")
