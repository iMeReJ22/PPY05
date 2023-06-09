from Person import Person


class LoginHandler:
    def __init__(self):
        self.__people = self.__getPeople()

    def getPersonAndPrintMenuPrompt(self):
        while True:
            try:
                n = int(input("1. Login.\n2. Register.\n3. Exit\n"))
                if n == 1:
                    return self.__login()
                if n == 2:
                    self.__register()
                if n == 3:
                    exit(1)
            except ValueError:
                print("Invalid input, try again.")

    @staticmethod
    def __getPeople():
        people = list()
        file = open("Data/loginData.txt", "r")
        for line in file:
            line = line.replace("\n", "")
            parts = line.split(";")
            person = Person(parts[0], parts[1], parts[2])
            person.decipherObject()
            people.append(person)
        file.close()
        return people

    def __register(self):
        while True:
            try:
                nick = input("Input nick: ")
                email = self.__getEmailAndPrintPrompts()
                password = self.__getPasswordAndPrintPrompts()
                person = Person(nick, email, password)
                for p in self.__people:
                    if p.nick == person.nick:
                        raise ValueError("nick")
                    if p.email == person.email:
                        raise ValueError("email")
                self.__people.append(person)
                person.cypherObject()
                file = open("Data/loginData.txt", "a")
                file.write(person.__str__()+"\n")
                file.close()
                person.decipherObject()
                print("You have been registered.")
                break
            except ValueError as e:
                yn = input(f"There is already a person with that {e} in the database.\nTry again? (y/n)")
                if yn == "n":
                    break

    @staticmethod
    def __getEmailAndPrintPrompts():
        email = input("Input your email:\t")
        while email != input("Repeat your email:\t"):
            print("Email is not the same.")
            email = input("Input your email:\t")
        return email

    @staticmethod
    def __getPasswordAndPrintPrompts():
        password = input("Input your password:\t")
        while password != input("Repeat your password:\t"):
            print("Password is not the same.")
            password = input("Input your password:\t")
        return password

    def __login(self):
        while True:
            try:
                email = input("Input email:\t")
                person = self.__getPersonByEmail(email)

                for i in range(3):
                    password = input("Input password:\t")
                    if person.password == password:
                        print(f"\n******************************\n"
                              f"{person.nick} logged in.\n"
                              f"******************************\n")
                        person.loggedIn = True
                        return person
                    else:
                        print("Wrong password, try again.")
                print("You run out of tries.")
                return None

            except ValueError as ve:
                print(ve.__str__() + "Try again.")
            except Exception as e:
                print(e)
                if input("Do you want to register? (y/n): ") == "y":
                    self.__register()
                else:
                    if input("Do you want to try again? (y/n): ") == "n":
                        exit(1)

    def __getPersonByEmail(self, email):
        person = None
        for p in self.__people:
            if p.email == email:
                person = p
        if person is None:
            raise Exception("No account with that email.")
        if person.loggedIn:
            raise Exception("That account is already logged in.")
        return person
