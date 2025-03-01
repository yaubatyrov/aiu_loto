import pytest
from src.lotto_card import LottoCard
from src.barrel_bag import BarrelBag
from src.lotto_game import LottoGame


@pytest.fixture
def game():
    """Создаёт новую игру перед каждым тестом."""
    return LottoGame()


def test_game_initialization(game):
    """Проверяет, что игра инициализируется корректно."""
    assert isinstance(game.user_card, LottoCard)
    assert isinstance(game.computer_card, LottoCard)
    assert isinstance(game.bag, BarrelBag)
    assert game.bag.remaining_count() == 90


def test_gameplay_round(game, monkeypatch):
    """Тестирует один раунд игры с разными вариантами действий игрока."""
    game.user_card.card[0, 0] = 10  # Предопределяем число в карточке игрока
    game.computer_card.card[0, 0] = 10  # То же самое для компьютера
    barrel = 10

    def mock_draw_barrel():
        return barrel

    game.bag.draw_barrel = mock_draw_barrel  # Подменяем метод draw_barrel

    # Тест: игрок правильно зачеркивает число
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert game.play_round() is True
    assert bool(game.user_card.marked[0, 0]) is True  # Число зачеркнуто

    # Тест: игрок ошибается, выбирая "зачеркнуть", когда числа нет
    game.user_card.card[0, 0] = 0  # Теперь в карточке нет числа
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert game.play_round() is False  # Игра должна завершиться

    # Тест: игрок ошибается, выбирая "пропустить", когда число есть
    game.user_card.card[0, 0] = 10
    game.user_card.marked[0, 0] = False  # Сбрасываем отметку
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert game.play_round() is False  # Игра должна завершиться


def test_game_end_conditions(game, monkeypatch):
    """Тестирует завершение игры при полном закрытии карточки."""
    game.user_card.marked[:] = True  # Полностью зачеркнутая карточка
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert game.play_round() is False  # Должно завершиться победой игрока

    game.user_card.marked[:] = False  # Сбрасываем
    game.computer_card.marked[:] = True  # Теперь компьютер выиграл
    assert game.play_round() is False  # Должно завершиться победой компьютера
