
# Отредактировано

> Изменены:<br>
> Функция get_age, set_name, set_address, is_homeless

## class Person
    def __init__(self, name, year_of_birth, address=''):
        self.name = name
        self.yob = year_of_birth
        self.address = address
    
    def get_age(self):
        # now = datetime.datetime.now()
        # return self.yob - now.year
        import datetime 
        now = datetime.datetime.now()
        return now.year - self.yob

    def set_name(self, name):
        # self.name = self.name
        self.name = name

    def set_address(self, address):
        # self.address == address
        self.address = address    

    def get_address(self):
        return self.address
    
    def is_homeless(self):
        '''
        returns True if address is not set, false in other case
        '''
        # return address is None
        return self.address is None