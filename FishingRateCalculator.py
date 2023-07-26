# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 13:45:25 2023

@author: Gargamiel
"""

import pandas as pd
from lxml.etree import Element, SubElement, Comment, ElementTree, tostring, indent

def GetCSVData(filePath):
    data = pd.read_csv(filePath,keep_default_na=False)    
    return data

def GetSpawnRate(rarity, factor):     
    spawnRate = rarity**factor
    return 1 / spawnRate

def main():
    
    pokemonData = GetCSVData("Data/DataPokemon.csv")   
    fishRateData = GetCSVData("Data/FishingTable.csv")
    
    biomes = ['BorealForest', 'ColdBog', 'Tundra', 'IceSheet', 'SeaIce', 'TemperateForest', 'TemperateSwamp', 'TropicalRainforest', 'TropicalSwamp', 'AridShrubland', 'Desert', 'ExtremeDesert']
    terrainsList = ["WaterShallow", "WaterDeep", "WaterMovingShallow", "WaterMovingChestDeep", "WaterOceanShallow", "WaterOceanDeep", "Marsh"]
    rodsFactors = {"OldRod": 2, "GoodRod": 1.5, "SuperRod":1.2}
    pokemonNames = fishRateData.DefName
    
    root = Element("Defs")
    def_element = SubElement(root, "PokeWorld.FishingRateDef")
    SubElement(def_element, "defName").text = ("FishingRates")
    biome_title_elem = SubElement(def_element, "biomes")
    
    for biome in biomes:
        flagBiomeElem = True
        for terrain in terrainsList: 
            flagTerrainElem = True
            for rod in rodsFactors.keys():
                flagRodElem = True
                spawnRateDict = {} #Used to normalize the computed values
                for pokemon in pokemonNames:
                    
                    if(fishRateData[fishRateData.DefName == pokemon][biome].values[0] == ''):
                        continue
                    if(fishRateData[fishRateData.DefName == pokemon][terrain].values[0] == ''):
                        continue
                    if(fishRateData[fishRateData.DefName == pokemon][rod].values[0] == ''):
                        continue
                    
                    rarity = pokemonData[pokemonData.DefName == pokemon].Rarity.values[0]
                    factor = rodsFactors[rod]
                    spawnRate = GetSpawnRate(rarity, factor)
                    spawnRateDict[pokemon] = spawnRate
                
                if not spawnRateDict:
                    continue
                if (flagBiomeElem):
                    biome_elem = SubElement(biome_title_elem, biome)
                    flagBiomeElem = False
                if (flagTerrainElem):
                    terrain_elem = SubElement(biome_elem, terrain)
                    flagTerrainElem = False
                if (flagRodElem):
                    rod_elem = SubElement(terrain_elem, "PW_" + rod)
                    flagRodElem = False
                    
                spawnRateSum = sum(spawnRateDict.values())
                for pokemon,spawnRate in spawnRateDict.items():
                    
                    spawnRateNorm = spawnRate/spawnRateSum
                    
                    SubElement(rod_elem, "PW_"+pokemon).text = ("%.4f" %spawnRateNorm)
    
    with open('OutputFiles/FishingRates.xml', 'wb') as f:
        indent(root, space = "  ")
        content = tostring(root, xml_declaration=True, encoding='utf8', method='xml')
        f.write(content)

if __name__ == '__main__':
    main()