from json import JSONDecodeError
from unittest import mock
from unittest import TestCase

from context import Pokemon, InvalidLevelException, InvalidSpeciesException


class UnitTestPokemonClass(TestCase):
    def test_constructor_happy(self):
        """Tests happy path of Pokemon Object Construction"""
        expected_stats = {
            'hp': 3,
            'attack': 0,
            'defense': 0,
            'special-attack': 0,
            'special-defense': 0,
            'speed': 0
        }
        with mock.patch.object(Pokemon, '_retrieve_stats', return_value=expected_stats):
            p = Pokemon('cryogonal', 2)
            self.assertEqual(p.stats, expected_stats)

    @mock.patch.object(Pokemon, '_retrieve_stats', return_value=None)
    def test_invalid_level(self, patched_object):
        """Tests that ValueError is raised when attempting to create a pokemon with an invalid level."""
        for i in range(-5, 121, 3):
            if i < 1 or i > 100:
                with self.assertRaises(InvalidLevelException):
                    p = Pokemon('agumon', i)
            else:
                p = Pokemon('patamon', i)

    @mock.patch.object(
        Pokemon,
        '_retrieve_stats',
        return_value={
            'hp': 24,
            'attack': 48,
            'defense': 48,
            'special-attack': 48,
            'special-defense': 48,
            'speed': 48
        }
    )
    def test_boosts(self, patched):
        # fix boosts instead of generating them randomly
        boosts = {
            'hp': 3,
            'attack': 3,
            'defense': 3,
            'special-attack': 3,
            'special-defense': 3,
            'speed': 3,
        }

        expected_result = {
            'hp': 24 + 3*3,
            'attack': 48 + 3*4,
            'defense': 48 + 3*6,
            'special-attack': 48 + 3*4,
            'special-defense': 48 + 3*6,
            'speed': 48 + 3*3
        }

        p = Pokemon('ditto', 7)

        # test unboosted state
        self.assertEqual(p._boosted, False)

        # apply boost and test for boosted state
        p.apply_boosts(boosts)
        self.assertEqual(p._boosted, True)
        self.assertEqual(p.stats, expected_result)

        # test that attempting to re-boost is not allowed
        with self.assertRaises(UserWarning):
            p.apply_boosts(boosts)

        # test and see that the stats remain the same after failed boost attempt
        self.assertEqual(p.stats, expected_result)

    @mock.patch.object(Pokemon, '_retrieve_stats', return_value=None)
    def test_boost_count(self, patched):
        """Tests that the right number of boosts are generated based on level"""
        levels = [1, 5, 10, 50, 100]

        for lvl in levels:
            p = Pokemon('rayquaza', lvl)
            boosts = p.generate_boosts()
            num_boosts = sum([b for b in boosts.values()])
            self.assertEqual(num_boosts, 3*(lvl-1))

    @mock.patch('requests.get')
    def test_retrieve_stats_happy(self, mocked_get_request):
        """Tests retrieve stats for Ditto"""
        mocked_get_request.return_value.json.return_value = {
            # portion of real API response for Ditto. url tags removed, as they are unused
            'stats': [
                {"base_stat": 48, "effort": 0, "stat": {"name": "speed", "url": ""}},
                {"base_stat": 48, "effort": 0, "stat": {"name": "special-defense", "url": ""}},
                {"base_stat": 48, "effort": 0, "stat": {"name": "special-attack", "url": ""}},
                {"base_stat": 48, "effort": 0, "stat": {"name": "defense", "url": ""}},
                {"base_stat": 48, "effort": 0, "stat": {"name": "attack", "url": ""}},
                {"base_stat": 48, "effort": 1, "stat": {"name": "hp", "url": ""}}
            ]
        }

        # shouldn't need to input ditto because the request is mocked!
        ditto = Pokemon('jeff from the overwatch team', 1)
        expected_ditto_stats = {
            'hp': 24,
            'attack': 48,
            'defense': 48,
            'special-attack': 48,
            'special-defense': 48,
            'speed': 48,
        }
        self.assertEqual(ditto._retrieve_stats(), expected_ditto_stats)

    @mock.patch('requests.get')
    def test_retrieve_stats_angy(self, mocked_request_get):
        """Tests that if an invalid pokemon name is supplied, it raises a ValueError"""
        mocked_request_get.return_value.json.side_effect = JSONDecodeError("", "", 0)

        with self.assertRaises(InvalidSpeciesException):
            p = Pokemon('big chungus', 2)
