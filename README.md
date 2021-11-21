# PokeWorld_Scripts
A set of scripts and data to generate Pokémon Defs for PokéWorld, a RimWorld mod.

If you are looking for the mod itself, it is located at https://github.com/Gargamiel/PokeWorld

The main script used to create all 498 Pokémon defs from the first four generation is Races_Pokemon_Script.py. It uses data from the three csv files and automatically generate all Defs in a click. To change something in the def, just edit the data in the csv file, save it and run the script. To generate more Pokémon defs, just add a row in the DataPokemon.csv file with all the data needed and run the script. The DataEvolutions.csv file contain all info on Pokémon evolution, and the DataMoves.csv file contain data on which move is learned by which Pokémon.

Note: most data are in the csv files, but the script computes other values used in the defs based on those data.
