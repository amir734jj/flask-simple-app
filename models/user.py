class User(object):
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def __str__(self):
        return self.firstname + " " + self.lastname