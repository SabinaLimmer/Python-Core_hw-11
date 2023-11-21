from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value=None):
        self.__value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self.__value = new_value
    
    def validate(self, value):
        pass
    
    def __str__(self):
        return str(self.value)

class FirstName(Field):
    pass

class LastName(Field):
    pass

class Email(Field):
    pass

class Phone(Field):
    def validate(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits.")

class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD.")

class Record:
    def __init__(self, first_name, last_name, email=None, phones=None, birthday=None):
        self.first_name = FirstName(first_name)
        self.last_name = LastName(last_name)
        self.email = Email(email)
        self.phones = []
        self.birthday = Birthday(birthday)
        
        if phones is not None:
            for phone in phones:
                self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = Phone(new_phone)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            birthday_current_year = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > birthday_current_year:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            else:
                next_birthday = birthday_current_year
            difference_days = (next_birthday - today).days
            return difference_days

class AddressBook(UserDict):
    def add_record(self, record: Record):
        key = record.first_name.value
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(record)

    def __iter__(self, n=1):
        self.current_index = 0
        self.page_size = n
        return self
    
    def __next__(self):
        keys = list(self.data.keys())
        if self.current_index < len(keys):
            view = {key: self.data[key] for key in keys[self.current_index:self.current_index + self.page_size]}
            self.current_index += self.page_size
            return view
        else:
            raise StopIteration