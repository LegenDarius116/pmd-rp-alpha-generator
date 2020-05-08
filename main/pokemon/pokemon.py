import random
import requests

from collections import defaultdict
from json.decoder import JSONDecodeError

from .exceptions import InvalidSpeciesException, InvalidLevelException

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
        if not (1 <= level <= 100):
            raise InvalidLevelException("Level must be in the range 1-100.")

        self.species = species.lower()
        self.level = level
        self._boosted = False

        # get base stats based on Pokémon species
        self.stats, self.moveset, self.image = self._retrieve_stats()

    def generate_boosts(self):
        """Generates stat boosts by picking random stats 3 times for every level after level 1.

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

        For a pokemon of level (3+1+1+2+3+5)/3 + 1 = 6
        """
        boosts = defaultdict(int)
        stats = [k for k in BOOSTS_PER_LEVEL.keys()]
        for _ in range(self.level-1):
            for _ in range(3):
                boosts[random.choice(stats)] += 1

        return boosts

    def apply_boosts(self, boosts):
        """Applies boosts found in dictionary based on each stat's respective power.

        Ex Input:
        {
            'hp': 3,
            'attack': 2,
            'defense': 0,
            'special-attack': 0,
            'special-defense': 1,
            'speed': 0,
        }

        Max HP gained will be 3*3 = 9 HP, as each HP boost gives +3 max HP.
        Attack gained will be 2*4 = 8 Atk, as each Attack Boost gives +4 attack
        SpDef gained will be 1*6 = 6, as each SpDef boost gives +6 SpDef
        """
        if not self._boosted:
            # apply boosts
            for stat, num_boosts in boosts.items():
                self.stats[stat] += BOOSTS_PER_LEVEL[stat] * num_boosts

            # set boosted state. Now the object cannot be boosted again
            self._boosted = True
        else:
            raise UserWarning("Boosts have already been applied")

    def _retrieve_stats(self):
        """Attempts to retrieve base stats based off of species name using API. Also retrieves four moves at random.

        returns (dict, list, str): dict represents stats, list represents the moveset, str represents an image url
        """
        try:
            rjson = requests.get(POKEMON_API_URL + '/pokemon/' + self.species).json()
        except JSONDecodeError:
            raise InvalidSpeciesException("Invalid species! Please enter a valid species name or dex number.")

        base_stats = defaultdict(int)
        moveset = [
            r['move']['name'] for r in
            random.sample(
                rjson['moves'],
                min(4, len(rjson['moves']))
            )
        ]

        for stat in rjson['stats']:
            stat_name = stat['stat']['name']
            base_stats[stat_name] = stat['base_stat'] // 2 if stat_name == 'hp' else stat['base_stat']

        return dict(base_stats), moveset, rjson['sprites']['front_default']
