class Bills(object):
    def __init__(self, date_added, electricity, gas, internet, city, total_per_user, total, due_date, bill_id=None):
        self.date_added = date_added
        self.electricity = electricity
        self.gas = gas
        self.internet = internet
        self.city = city
        self.total_per_user = total_per_user
        self.total = total
        self.due_date = due_date
        self.bill_id = bill_id

    def __repr__(self):
        return '{id},' \
               '{da},' \
               '{e},' \
               '{g},' \
               '{i},' \
               '{c},' \
               '{tpu}' \
               '{t},' \
               '{dd}' \
                .format(id=self.bill_id, da=self.date_added,
                        e=self.electricity,
                        g=self.gas,
                        i=self.internet,
                        c=self.city,
                        tpu=self.total_per_user,
                        t=self.total, dd=self.due_date)

    def __str__(self):
        return self.__repr__()