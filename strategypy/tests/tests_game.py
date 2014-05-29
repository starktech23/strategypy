import unittest
from mock import patch, call, Mock

from core.game import Game
from core.players import Player
import settings


@patch('core.game.pygame')
class TestGameDrawGrid(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        Game.__init__ = lambda x: None
        self.game = Game()
        self.game.screen = None

    @patch('core.game.settings.SCREEN_SIZE', (6, 4))
    @patch('core.game.settings.UNIT_SIZE', (2, 2))
    def test_2x3(self, pg):
        self.game.draw_grid()
        calls = [
            call(None, settings.GRID_COLOR, (0, 0), (0, 4), 1),
            call(None, settings.GRID_COLOR, (2, 0), (2, 4), 1),
            call(None, settings.GRID_COLOR, (4, 0), (4, 4), 1),
            call(None, settings.GRID_COLOR, (6, 0), (6, 4), 1),
            call(None, settings.GRID_COLOR, (0, 0), (6, 0), 1),
            call(None, settings.GRID_COLOR, (0, 2), (6, 2), 1),
            call(None, settings.GRID_COLOR, (0, 4), (6, 4), 1),
        ]
        self.assertListEqual(calls, pg.draw.line.call_args_list)


class TestGameDraw(unittest.TestCase):
    def setUp(self):
        Game.__init__ = lambda x: None
        Game.units = []  # We override the property
        self.game = Game()
        self.game.screen = Mock()
        self.game.draw_grid = Mock()

    def test_game_draw_no_units(self):
        self.game.units = []

        self.game.draw()

        self.assertEqual(self.game.draw_grid.call_count, 1)
        self.game.screen.fill.assert_called_once_with(settings.BG_COLOR)

    def test_game_draw_multiple_units(self):
        self.game.units = [Mock(), Mock(), Mock()]

        self.game.draw()

        self.assertEqual(self.game.draw_grid.call_count, 1)
        self.game.screen.fill.assert_called_once_with(settings.BG_COLOR)
        for unit in self.game.units:
            self.assertEqual(unit.render.call_count, 1)


class TestInitPlayers(unittest.TestCase):
    def setUp(self):
        Game.__init__ = lambda x: None
        self.game = Game()

    def test_no_function(self):
        self.game.functions = []
        self.game.init_players()
        self.assertListEqual(self.game.players, [])

    def test_multiple_functions(self):
        first_function = lambda: 1
        second_function = lambda: 2
        self.game.functions = [first_function, second_function]

        self.game.init_players()

        first_player, second_player = self.game.players
        self.assertEqual(first_player.pk, 0)
        self.assertEqual(first_player.action_func, first_function)
        self.assertIsInstance(first_player, Player)
        self.assertEqual(second_player.pk, 1)
        self.assertEqual(second_player.action_func, second_function)
        self.assertIsInstance(second_player, Player)


class TestInitFunctions(unittest.TestCase):
    def setUp(self):
        Game.__init__ = lambda x: None
        self.game = Game()

    def test_no_args(self):
        self.game.args = []
        self.game.init_functions()
        self.assertListEqual(self.game.functions, [])

    def test_multiple_args(self):
        self.game.args = ['test_one', 'test_two']
        self.game.init_functions()
        from bots.test_one import action as action_one
        from bots.test_two import action as action_two
        self.assertListEqual(
            self.game.functions,
            [action_one, action_two]
        )

    @unittest.skip('TODO')
    def test_multiple_args_in_package(self):
        self.game.args = ['tests.test_one', 'tests.test_two']
        self.game.init_functions()
        from bots.tests.test_one import action as action_one
        from bots.tests.test_two import action as action_two
        self.assertListEqual(
            self.game.functions,
            [action_one, action_two]
        )