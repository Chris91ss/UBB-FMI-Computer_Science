import unittest
from src.services.game_service import GameService


class Tests(unittest.TestCase):
    def setUp(self):
        self.game_service = GameService(10)

    def test_game_service(self):
        self.game_service.start_game()
        self.game_service.make_move(0, 0)
        self.assertEqual(self.game_service.board.grid[0][0], 'X')

        self.game_service.make_computer_move()
        self.assertEqual(self.game_service.board.grid[5][5], 'O')

        self.game_service.make_move(1, 1)
        self.assertEqual(self.game_service.board.grid[1][1], 'X')
        self.game_service.make_move(2, 2)
        self.assertEqual(self.game_service.board.grid[2][2], 'X')
        self.game_service.make_move(3, 3)
        self.assertEqual(self.game_service.board.grid[3][3], 'X')
        self.game_service.make_move(4, 4)
        self.assertEqual(self.game_service.board.grid[4][4], 'X')

        self.assertEqual(self.game_service.check_winner(), True)
        self.assertEqual(self.game_service.is_game_over(), True)


if __name__ == '__main__':
    unittest.main()