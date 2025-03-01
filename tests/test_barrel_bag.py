import pytest
from src.barrel_bag import BarrelBag


def test_barrel_bag_init():
    """Тест инициализации мешка с 90 бочонками."""
    bag = BarrelBag()
    assert len(bag.barrels) == 90
    assert sorted(bag.barrels) == list(range(1, 91))  # Проверка номеров


def test_draw_barrel():
    """Тест вытягивания бочонка – количество уменьшается на 1."""
    bag = BarrelBag()
    initial_count = len(bag.barrels)
    barrel = bag.draw_barrel()
    assert barrel is not None  # Должен вернуть число
    assert barrel in range(1, 91)  # Число в диапазоне 1-90
    assert len(bag.barrels) == initial_count - 1  # Количество уменьшилось


def test_empty_bag():
    """Тест – мешок становится пустым после 90 вытягиваний и выбрасывает ошибку при следующем вытягивании."""
    bag = BarrelBag()
    drawn_numbers = {bag.draw_barrel() for _ in range(90)}
    assert len(drawn_numbers) == 90  # Все 90 бочонков уникальны

    # Проверяем, что при попытке взять 91-й бочонок выбрасывается ValueError
    with pytest.raises(ValueError):
        bag.draw_barrel()


def test_unique_numbers():
    """Тест – вытянутые номера не повторяются."""
    bag = BarrelBag()
    drawn_numbers = {bag.draw_barrel() for _ in range(90)}
    assert len(drawn_numbers) == 90  # Уникальность номеров
