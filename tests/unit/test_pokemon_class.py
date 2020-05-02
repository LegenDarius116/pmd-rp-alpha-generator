from unittest import mock
from unittest import TestCase

from context import Pokemon


class TestPokemonClass(TestCase):
    @mock.patch.object(
        Pokemon,
        '_retrieve_stats',
        return_value={
            'hp': 3,
            'attack': 0,
            'defense': 0,
            'special-attack': 0,
            'special-defense': 0,
            'speed': 0
        }
    )
    def test_constructor_happy(self, patched_object):
        """Tests happy path of Pokemon Object Construction"""
        expected_stats = {
            'hp': 3,
            'attack': 0,
            'defense': 0,
            'special-attack': 0,
            'special-defense': 0,
            'speed': 0
        }
        # disable request calls
        p = Pokemon('cryogonal', 2)
        self.assertEqual(p.stats, expected_stats)

    @mock.patch.object(Pokemon, '_retrieve_stats', return_value=None)
    def test_constructor_sad(self, patched_object):
        """Tests sad path of object construction (i.e when API Call fails)"""
        expected_stats = {
            'hp': 0,
            'attack': 0,
            'defense': 0,
            'special-attack': 0,
            'special-defense': 0,
            'speed': 0
        }
        p = Pokemon('agumon', 3)
        self.assertEqual(p.stats, expected_stats)

    @mock.patch.object(Pokemon, '_retrieve_stats', return_value=None)
    def test_boost_count(self, patched):
        """Tests that the right number of boosts are generated based on level"""
        levels = [1, 5, 10, 50, 100]

        for lvl in levels:
            p = Pokemon('rayquaza', lvl)
            boosts = p.generate_boosts()
            self.assertEqual(len(boosts), lvl-1)
