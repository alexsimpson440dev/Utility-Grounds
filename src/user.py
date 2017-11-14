class User(object):
    def __int__(self, user_id, first_name, last_name, email_address, password):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password

    def __repr__(self):
        return '{id}:{fn} {ln}' \
               '{ea}:{pw}' \
                .format(id=self.user_id, fn=self.first_name, ln=self.last_name,
                        ea=self.email_address, pw=self.password)

    def __str__(self):
        return self.__reduce__()