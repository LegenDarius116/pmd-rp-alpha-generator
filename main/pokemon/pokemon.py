import random
import requests

from collections import defaultdict
from json.decoder import JSONDecodeError

from alpha_enemy_generator.settings import POKEMON_API_URL



BOOSTS_PER_LEVEL = {
    'hp': 3,
    'attack': 4,
    'defense': 6,
    'special-attack': 4,
    'special-defense': 6,
    'speed': 3,
}


class Pokemon:
    """Randomly generates a Pokemon with stats for a D&D-style roleplay.
    This is done by retrieving the Pokemon's base stats using an API.

    We then randomly boost a stat for every level past lv.1. The strength
    of the point boost for each stat is defined by BOOSTS_PER_LEVEL.

    """
    def __init__(self, species: str, level: int):
        self.species = species.lower()
        self.level = level
        self._boosted = False

        # get base stats based on Pokémon species
        # if species is invalid, stats remain zero
        self.stats = {
            'hp': 0,
            'attack': 0,
            'defense': 0,
            'special-attack': 0,
            'special-defense': 0,
            'speed': 0,
        }

        base_stats = self._retrieve_stats()
        if base_stats is not None:
            self.stats = base_stats

    def generate_boosts(self):
        """Generates stat boosts by picking random stats level-1 times

        :return:    Dictionary of strings mapped to integers. String is the stat to be boosted,
                    integer is number of boosts for that stat.

        Ex:
        {
            'hp': 3,
            'attack': 1,
            'defense': 1,
            'special-attack': 2,
            'special-defense': 3,
            'speed': 5,
        }

        For a pokemon of level (3+1+1+2+3+5)+1 = 16
        """
        boosts = defaultdict(int)
        stats = [k for k in BOOSTS_PER_LEVEL.keys()]
        for _ in range(self.level-1):
            boosts[random.choice(stats)] += 1

        return boosts

    def apply_boosts(self, boosts):
        """Applies boosts found in list"""
        if not self._boosted:
            for boost_stat in boosts:
                self.stats[boost_stat] += BOOSTS_PER_LEVEL[boost_stat]
        else:
            print("Warning! Pokemon already boosted.")

    def _retrieve_stats(self):
        """Attempts to retrieve base stats based off of species name using API"""
        try:
            rjson = requests.get(POKEMON_API_URL + '/pokemon/' + self.species).json()
        except JSONDecodeError:
            print("Invalid species")
            return

        base_stats = {}

        for stat in rjson['stats']:
            stat_name = stat['stat']['name']
            base_stats[stat_name] = stat['base_stat'] // 2 if stat_name == 'hp' else stat['base_stat']

        return base_stats
