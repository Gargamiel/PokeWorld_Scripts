# -*- coding: utf-8 -*-
import pandas as pd
import codecs

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
    
    PokemonData = GetCSVData("Data/DataPokemon.csv")   
    
    f = codecs.open("OutputFiles/PokemonEggs.xml", "w", "utf-8")
    
    f.write('<?xml version="1.0" encoding="utf-8" ?>\n')
    f.write("<Defs>\n\n")
    
    for i in range(0,493):      
        
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
            f.write('  <ThingDef ParentName="PokemonEggBase">\n')
            f.write("    <defName>PW_Egg%s</defName>\n"% (defName))
            """Not writing label to keep content secret"""
            #f.write("    <label>%s Egg</label>\n"% (name))
            f.write("    <tradeability>%s</tradeability>\n"% (tradability))
            f.write("    <comps>\n")
            f.write('      <li Class="PokeWorld.CompProperties_PokemonEggHatcher">\n')
            f.write("        <hatcherDaystoHatch>%d</hatcherDaystoHatch>\n"% (eggHatchDays))
            f.write("        <hatcherPawn>PW_%s</hatcherPawn>\n"% (defName))
            f.write("      </li>\n")           
            f.write('      <li Class="CompProperties_TemperatureRuinable">\n')
            f.write("        <minSafeTemperature>%d</minSafeTemperature>\n"%(minSafeTemperature))
            f.write("        <maxSafeTemperature>%d</maxSafeTemperature>\n"%(maxSafeTemperature))
            f.write("        <progressPerDegreePerTick>0.00001</progressPerDegreePerTick>\n")
            f.write("      </li>\n")           
            f.write("    </comps>\n")
            f.write("  </ThingDef>\n\n")
        
    f.write("</Defs>")
    f.close()

if __name__ == '__main__':
    main()