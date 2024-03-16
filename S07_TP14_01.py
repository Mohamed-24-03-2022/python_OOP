import random


class Element:
    def __init__(self, char_repr):
        self.__char_repr = char_repr

    def __repr__(self):
        return self.__char_repr

    def __eq__(self, other):
        return other.__repr__() == self.__repr__() and isinstance(other, self.__class__)
        # if isinstance(other, self.__class__):
        #     return other.__repr__() == self.__repr__()
        # else:
        #     return False


class Ground(Element):
    def __init__(self):
        Element.__init__(self, '\u2B1C')


class Resource(Element):
    def __init__(self, char_repr, value):
        Element.__init__(self, char_repr)
        self.__value = value

    def get_value(self):
        return self.__value


class Water(Resource):
    def __init__(self):
        Resource.__init__(self, '\U0001F41F', 1)


class Herb(Resource):
    def __init__(self):
        Resource.__init__(self, '\U0001F33F', 2)


class Animal(Element):
    def __init__(self, char_repr, life_max):
        Element.__init__(self, char_repr)
        self.__life_max = life_max
        self.__age = 0
        self.__gender = random.choice([0, 1])  # 0 for Female, 1 for Masculine
        self.__bar_life = [0, life_max]

        d1, d2 = random.choices([-1, 0, 1], k=2)
        while (d1 == 0 and d2 == 0):
            d1, d2 = random.choices([-1, 0, 1], k=2)

        self.__current_direction = [d1, d2]

    def get_age(self):
        return self.__age

    def ageing(self):
        self.__age += 1

    def get_gender(self):
        return self.__gender

    def get_life_max(self):
        return self.__life_max

    def get_life(self):
        return self.__bar_life[0]

    def is_alive(self):
        return self.__bar_life[0] > 0

    def is_dead(self):
        return not self.__is_alive()

    def recovering_life(self, value):
        self.__bar_life[0] = min(self.__bar_life[0] + value, self.__life_max)

    def losing_life(self, value):
        self.__bar_life[0] = max(0, self.__bar_life[0] - value)

    def get_current_direction(self):
        return self.__current_direction

    def set_current_direction(self, line_direction, column_direction):
        self.__current_direction = [line_direction, column_direction]


class Cow(Animal):
    def __init__(self):
        Animal.__init__(self, '\U0001F42E', 5)


class Dragon(Animal):
    def __init__(self):
        Animal.__init__(self, '\U0001F432', 20)


class Lion(Animal):
    def __init__(self):
        Animal.__init__(self, '\U0001F981', 10)


class Mouse(Animal):
    def __init__(self):
        Animal.__init__(self, '\U0001F42D', 3)


class Snake(Element):
    def __init__(self):
        Element.__init__(self, '\U0001F40D')


class Human(Element):
    def __init__(self):
        Element.__init__(self, '\U0001F464')


class Turmite(Element):
    def __init__(self):
        Element.__init__(self, '\U0001F7E5')


if (__name__ == "__main__"):
    print(Ground(), str(Ground()))
    print(Ground() == str(Ground()))
    print(Ground() == Ground())
    print(Ground() is Ground())

    TYPES_COUNT = {Herb: 2, Water: 3,  Cow: 2, Dragon: 1, Lion: 5, Mouse: 10}
    ELEMENTS_BY_TYPE = {element_type: [element_type() for _ in range(element_count)]
                        for element_type, element_count in TYPES_COUNT.items()}

    for element_type, elements in ELEMENTS_BY_TYPE.items():
        print(f"{element_type.__name__}: {elements}")
