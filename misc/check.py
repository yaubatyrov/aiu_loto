

class Person:
    def __init__(self, name):
        self._name = name
        self.age = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise Exception(f'Нельзя дать человеку новое имя')


if __name__ == '__main__':
    person = Person('Петя')
    print(person.name)
    person.name = 'Вася'


