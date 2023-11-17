from datetime import datetime
import re


class Field:
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return str(self.__value)

class Name(Field):
    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value) -> None:
        self.__value = value

class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        PHONE_LENGTH = 10
        if not all([len(new_value) == PHONE_LENGTH, new_value.isdigit()]):
            raise ValueError
        self.__value = new_value

class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_date: str) -> str:
        today = datetime.now().date()
        date_to_check = datetime.strptime(new_date, '%Y-%m-%d').date()
        if today < date_to_check:
            raise ValueError
        self.__value = date_to_check


    def __str__(self):
        return datetime.strftime(self.__value, '%d %B')
    
class Adress(Field):
    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value) -> None:
        self.__value = value

class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_email: str):
        result = re.findall(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', new_email)
        if not new_email in result:
            raise ValueError
        self.__value = new_email   

    def __str__(self):
        return self.__value