from src.lotto_card import LottoCard
from src.barrel_bag import BarrelBag


class LottoGame:
    def __init__(self):
        """Инициализирует игру с двумя игроками: пользователем и компьютером."""
        self.user_card = LottoCard()
        self.computer_card = LottoCard()
        self.bag = BarrelBag()

    def play_round(self) -> bool:
        """Проводит один раунд игры. Возвращает False, если игра окончена."""
        try:
            barrel = self.bag.draw_barrel()
        except ValueError:
            print("Мешок пуст. Игра окончена!")
            return False

        print(f"\nНовый бочонок: {barrel} (осталось {self.bag.remaining_count()})")
        print("Карточка игрока:")
        print(self.user_card)
        print("\nКарточка компьютера:")
        print(self.computer_card)

        # Действие пользователя
        action = input("Зачеркнуть число? (y/n): ").strip().lower()
        user_has_number = self.user_card.mark_number(barrel)

        if action == "y" and not user_has_number:
            print("Вы ошиблись! Вы проиграли.")
            return False
        elif action == "n" and user_has_number:
            print("Число было в карточке! Вы проиграли.")
            return False

        # Действие компьютера (он автоматически зачеркивает)
        self.computer_card.mark_number(barrel)

        # Проверка победителя
        if self.user_card.is_complete():
            print("Поздравляем! Вы выиграли!")
            return False
        elif self.computer_card.is_complete():
            print("Компьютер выиграл! Вы проиграли.")
            return False

        return True

    def start(self):
        """Запускает игровой цикл."""
        print("Добро пожаловать в Лото!")
        while self.play_round():
            pass
        print("Игра окончена.")


if __name__ == "__main__":
    game = LottoGame()
    game.start()
