# -*- coding: utf-8 -*-
import pandas as pd
import codecs
from lxml.etree import Element, SubElement, Comment, ElementTree, tostring, indent

def GetCSVData(filePath):
    data = pd.read_csv(filePath,keep_default_na=False)    
    return data

def GetMinSafeTemperature(type1, type2):        
        if(type1 == "Ice" or type2 == "Ice"):
            minSafeTemperature = -20
        else:
            minSafeTemperature = 0
        return minSafeTemperature
    
def GetMaxSafeTemperature(type1, type2):        
        if(type1 == "Fire" or type2 == "Fire"):
            maxSafeTemperature = 70   
        else:
            maxSafeTemperature = 50
        return maxSafeTemperature
   
def GetTradability(isLegendary, isFossil, isParticular):
        if(not isLegendary and not isFossil and not isParticular):
            tradability = "Buyable"        
        else:
            tradability = "None"
        return tradability
    
def main():
    
    PokemonData = GetCSVData("Data/DataPokemon_gen8.csv")   
    
    #f = codecs.open("OutputFiles/PokemonEggs.xml", "w", "utf-8")

    root = Element("Defs")

    defNameList = list(PokemonData.DefName)

    for i, pokemonDefName in enumerate(defNameList):    
        
        defName = PokemonData.DefName[i]
        name = PokemonData.Name[i]   
        evolutionTier = PokemonData.EvolTier[i] 
        eggHatchDays = PokemonData.EggHatchTime[i]   
        type1 = PokemonData.Type1[i]
        type2 = PokemonData.Type2[i]       
        eggGroup1 = PokemonData.EggGroup1[i]
        eggGroup2 = PokemonData.EggGroup2[i]       
        isBaby = PokemonData.Baby[i]      
        isLegendary = PokemonData.Legendary[i]
        isFossil = PokemonData.Fossil[i]
        isParticular = PokemonData.ParticularSpawn[i]     
   
        minSafeTemperature = GetMinSafeTemperature(type1, type2)
        maxSafeTemperature = GetMaxSafeTemperature(type1, type2)
        tradability = GetTradability(isLegendary, isFossil, isParticular)
        
        if (evolutionTier == 1 and ((eggGroup1 != "Undiscovered" and eggGroup2 != "Undiscovered") or isBaby == 1 or defName == "Phione") and defName != "Ditto" and defName != "Manaphy"):
            ThingDef = SubElement(root, "ThingDef", {"ParentName": "PokemonEggBase"})

            SubElement(ThingDef, "defName").text = "PW_Egg" + pokemonDefName

            """Not writing label to keep content secret"""
            #SubElement(ThingDef, "label").text = pokemonDefName + " Egg" 

            SubElement(ThingDef, "tradeability").text = tradability

            comps = SubElement(ThingDef, "comps")
            
            li = SubElement(comps, "li", {"Class": "PokeWorld.CompProperties_PokemonEggHatcher"})
            SubElement(li, "hatcherDaystoHatch").text = str(int(eggHatchDays))
            SubElement(li, "hatcherPawn").text = "PW_" + pokemonDefName
            
            li = SubElement(comps, "li", {"Class": "CompProperties_TemperatureRuinable"})         
            SubElement(li, "minSafeTemperature").text = str(minSafeTemperature)
            SubElement(li, "maxSafeTemperature").text = str(maxSafeTemperature)
            SubElement(li, "progressPerDegreePerTick").text = "0.00001"
        
    with open('OutputFiles/PokemonEggs.xml', 'wb') as f:
        indent(root, space = "  ")
        test = tostring(root, xml_declaration=True, encoding='utf8', method='xml')
        f.write(test)

if __name__ == '__main__':
    main()
