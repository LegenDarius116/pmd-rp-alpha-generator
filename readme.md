# Pokémon Mystery Dungeon: Alpha Roleplay Enemy Generator

This project was developed for a friend DM'ing a homebrewed, D&D-esque roleplay. This appplication takes a Pokémon species and level and generates an enemy with randomized stats. The stat distribution is based on the following design.

Every time a Pokémon levels up, he/she receives 3 stat boosts, which they can assign to any stat. However, each boost gives different points depending on the stat. Below is a table showing the points per boost for each stat.

Stat | Points per Boost
:---:|:---:
HP | 3
Attack | 4
Defense | 6
Special Attack | 4
Special Defense | 6
Speed | 3

Given a species, their starting stats (as a Level 1 Pokémon) are given below.

Stat | Starting Value at Lv. 1
:---:|:---:
HP | Base HP / 2
Attack | Base Attack
Defense | Base Defense
Special Attack | Base Special Attack
Special Defense | Base Special Defense
Speed | Base Speed

Given a valid level (1-100), the application will generate 3*(level-1) boosts, each of them randomly selected from the six available stats. After they are selected, each stat boost is applied according to its respective points per boost to the Pokémon's starting stats.

For example, take a Lv. 2 Pichu. After that first level up, the Pichu decides to invest 1 stat boost in HP, 1 in Attack, and 1 in Special Defense. The table below shows the Pichu's stats before and after the boost.

Stat | Before | After
:---:|:---:|:---:
HP | 10 | 10 + 3 = 13
Attack | 40 | 40 + 4 = 44
Defense | 15 | 15 + 0 = 15
Special Attack | 35 | 35 + 0 = 35
Special Defense | 35 | 35 + 6 = 41
Speed | 60 | 60 + 0 = 60

## Usage
1. Navigate to the [web application](https://pmd-alpha-generator.herokuapp.com/).
2. Enter the name of a Pokémon's species. If it is invalid, the application will show an error after clicking Submit.
3. Enter the level. If it is not within the range 1-100, the application will show an error after clicking Submit.
4. Click submit, and it should show you your generated enemy with randomized stats!

## Alternate Forms
To generate a Pokémon in its Alolan form (if applicable), type "-Alola" after the species name, e.g. "sandshrew-alola".

To see a full list of forms, see the [Pokeapi Documentation](https://pokeapi.co/docs/v2.html#pokemon).