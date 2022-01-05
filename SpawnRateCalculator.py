# -*- coding: utf-8 -*-
import pandas as pd
from lxml.etree import Element, SubElement, Comment, ElementTree, tostring, indent

def GetCSVData(filePath):
    data = pd.read_csv(filePath,keep_default_na=False)    
    return data

def GetSpawnRate(rarity, isBaby, isLegendary, isFossil, isParticular):     
    if(isBaby or isLegendary or isFossil or isParticular):
        spawnRate = 0
    else:
        spawnRate = rarity
    return spawnRate

def main():
    DictTypeIndex = {"Grass" : 1, "Fire" : 2, "Water" : 3, "Bug" : 4,
                     "Normal" : 5, "Poison" : 6, "Electric" : 7, "Ground" : 8,
                     "Fairy" : 9, "Fighting" : 10, "Psychic" : 11, "Rock" : 12,
                     "Ghost" : 13, "Ice" : 14, "Dragon" : 15, "Dark" : 16, 
                     "Steel" : 17, "Flying" : 18}

    PokemonData = GetCSVData("Data/DataPokemon_gen8.csv")   
    SpawnRateData = GetCSVData("Data/SpawnRateByType.csv")
    biomes = list(SpawnRateData.columns)
    biomes.remove("Type")
    root = Element("Patch")
    
    for biome in biomes:      
        operation = SubElement(root, "Operation", {"Class": "PatchOperationAdd"})
        SubElement(operation, "xpath").text = '/Defs/BiomeDef[defName="{0}"]/wildAnimals'.format(biome)
        value = SubElement(operation, "value")
        for i in range(0, len(PokemonData.DefName)):
            defName = PokemonData.DefName[i]
            type1 = PokemonData.Type1[i]
            type2 = PokemonData.Type2[i] 
            rarity = PokemonData.Rarity[i]
            isBaby = PokemonData.Baby[i]      
            isLegendary = PokemonData.Legendary[i]
            isFossil = PokemonData.Fossil[i]
            isParticular = PokemonData.ParticularSpawn[i]             
            spawnRateFactor = GetSpawnRate(rarity, isBaby, isLegendary, isFossil, isParticular)
            if (spawnRateFactor == 0):
                continue
            index = DictTypeIndex[type1]-1
            typeMultiplier1 = SpawnRateData[biome][index]
            if(type2 != ""): 
                index = DictTypeIndex[type2]-1
                typeMultiplier2 = SpawnRateData[biome][index]
            else:
                typeMultiplier2 = 0
            if(typeMultiplier1 >= typeMultiplier2):
                typeMultiplier = typeMultiplier1
            else:
                typeMultiplier = typeMultiplier2
            spawnRate = (0.5**spawnRateFactor) * typeMultiplier  
            if (spawnRate != 0):             
                SubElement(value, "PW_"+defName).text = ("%.4f" %spawnRate)

    with open('OutputFiles/Patch_BiomeWildAnimals.xml', 'wb') as f:
        indent(root, space = "  ")
        test = tostring(root, xml_declaration=True, encoding='utf8', method='xml')
        f.write(test)

if __name__ == '__main__':
    main()