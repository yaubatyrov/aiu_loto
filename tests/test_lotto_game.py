import pytest
from src.lotto_card import LottoCard
from src.barrel_bag import BarrelBag, EmptyBagException
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
    for i in range(game.user_card.card.shape[0]):
        for j in range(game.user_card.card.shape[1]):
            if game.user_card.card[i, j] == barrel:
                game.user_card.card[i, j] = 0  # Полностью убираем число из карточки
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


def test_game_start(game, monkeypatch):
    """Тестирует запуск и завершение игры."""
    inputs = iter(["y", "y", "n"])  # Симулируем три ответа
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    game.user_card.marked[:] = True  # Игрок сразу выигрывает
    game.start()


def test_empty_bag(game):
    """Проверяет поведение игры, если мешок пуст."""
    game.bag.barrels = []  # Делаем мешок пустым
    with pytest.raises(EmptyBagException):
        game.play_round()
