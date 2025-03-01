import pytest
import numpy as np
from src.lotto_card import LottoCard  # Импортируем класс


@pytest.fixture
def lotto_card():
    """Создаёт новую карточку перед каждым тестом."""
    return LottoCard()


def test_card_structure(lotto_card):
    """Проверяем, что карточка корректно генерируется."""
    assert lotto_card.card.shape == (3, 9)  # Размерность 3x9
    assert lotto_card.marked.shape == (3, 9)  # Размерность 3x9
    assert np.all((lotto_card.card >= 0) & (lotto_card.card <= 90))  # Числа в пределах 1-90
    assert np.count_nonzero(lotto_card.card) == 15  # Должно быть ровно 15 чисел


def test_mark_number(lotto_card):
    """Проверяем, что числа корректно отмечаются."""
    number_to_mark = lotto_card.card[lotto_card.card > 0][0]  # Берём любое число из карточки
    assert lotto_card.mark_number(number_to_mark)  # Число должно быть найдено
    assert lotto_card.marked[lotto_card.card == number_to_mark].all()  # Число должно быть зачёркнуто

    assert not lotto_card.mark_number(999)  # Несуществующее число не должно быть найдено


def test_is_complete(lotto_card):
    """Проверяем, что метод is_complete() работает корректно."""
    assert not lotto_card.is_complete()  # В начале карточка не может быть заполнена

    # Отмечаем все числа в карточке
    for num in lotto_card.card[lotto_card.card > 0]:
        lotto_card.mark_number(num)

    assert lotto_card.is_complete()  # Теперь карточка должна быть завершена
