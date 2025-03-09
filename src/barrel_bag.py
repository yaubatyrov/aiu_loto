import random


class EmptyBagException(Exception):
    def __str__(self):
        return 'Мешок с бочонками пуст'


class BarrelBag:
    def __init__(self):
        """Создает мешок с бочонками от 1 до 90"""
        self.barrels = list(range(1, 91))
        random.shuffle(self.barrels)

    def draw_barrel(self) -> int:
        """Достает один случайный бочонок из мешка"""
        if self.barrels:
            return self.barrels.pop()
        else:
            raise EmptyBagException

    def remaining_count(self) -> int:
        """Возвращает количество оставшихся бочонков"""
        return len(self.barrels)


if __name__ == '__main__':
    barrel_bag = BarrelBag()
    barrel = barrel_bag.draw_barrel()
    print(barrel)
    print(barrel_bag.remaining_count())
