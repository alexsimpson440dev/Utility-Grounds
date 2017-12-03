class User(object):
    def __init__(self, first_name, last_name, email_address, password, user_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password
        self.user_id = user_id

    def __repr__(self):
        return '{id}: {fn} {ln}\n' \
                '{ea}:{pw}' \
                .format(id=self.user_id, fn=self.first_name, ln=self.last_name,
                        ea=self.email_address, pw=self.password)
    def __str__(self):
        return self.__repr__()