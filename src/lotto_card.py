import random
import numpy as np


class LottoCard:
    def __init__(self):
        """Создаёт карточку с 15 случайными числами."""
        self.card: np.ndarray = self._generate_card()
        self.marked: np.ndarray = np.zeros((3, 9), dtype=bool)  # Отмеченные числа

    @staticmethod
    def _generate_card() -> np.ndarray:
        """Генерирует карточку 3x9 по классическим правилам лото."""

        # Диапазоны чисел для столбцов
        ranges = [np.arange(start, start + 10) for start in range(1, 91, 10)]

        # Генерация структуры карточки (True - там будет число, False - пустая ячейка)
        while True:
            mask = np.zeros((3, 9), dtype=bool)
            for row in mask:
                row[random.sample(range(9), 5)] = True

            # Проверка, чтобы в каждом столбце было хотя бы одно число
            if np.all(mask.sum(axis=0) > 0):
                break

        # 2) Генерируем все числа 3x9
        card = np.zeros((3, 9), dtype=int)
        for col in range(9):
            card[:, col] = np.random.choice(ranges[col], size=3, replace=False)

        # 3) Применяем маску: оставляем только те числа, что соответствуют маске, остальные делаем None
        card = np.where(mask, card, 0)

        return card

    def mark_number(self, number: int) -> bool:
        """Зачёркивает число, если оно есть. Возвращает True, если число было найдено и зачёркнуто, иначе False."""
        mask = (self.card == number)
        self.marked[mask] = True
        return np.any(mask)

    def is_complete(self) -> bool:
        """Возвращает True, если во всех строках карточки все 5 чисел зачёркнуты"""
        return np.all(self.marked[self.card > 0])

    def __str__(self) -> str:
        """Возвращает строковое представление карточки."""
        return '\n'.join(
            ' '.join(' X' if self.marked[i, j] else f'{num:2}' if num else '  '
                     for j, num in enumerate(row))
            for i, row in enumerate(self.card)
        )


if __name__ == '__main__':
    card_ = LottoCard()
    print(card_)
