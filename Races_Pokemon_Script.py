# -*- coding: utf-8 -*-
import math
import pandas as pd
import numpy as np
import codecs
import string
import json
from lxml.etree import Element, SubElement, Comment, ElementTree, tostring, indent

def LagrangeInterpol(x, y, xp):
    yp = 0
    for i in range(5):
        p = 1
        for j in range(5):
            if i != j:
                p = p * (xp - x[j])/(x[i] - x[j])
        
        yp = yp + p * y[i] 
    return yp

def LagrangeInterpolSpeed(xp):
    return LagrangeInterpol([5, 30, 50, 135, 160], [1, 3, 4, 6, 8], xp)

def LagrangeInterpolSize(xp):
    return LagrangeInterpol([0.2, 1, 5, 10, 14], [1.5, 2, 3.5, 5, 6], xp)

def GetMinimumComfortableTemperature(pokemonType1, pokemonType2):
    MinimumTempType1 = GetMinTemp(pokemonType1)
    MinimumTempType2 = GetMinTemp(pokemonType2)          
    if(MinimumTempType2 == None):
        return MinimumTempType1
    elif(MinimumTempType1 <= MinimumTempType2):
        return MinimumTempType1
    else:
        return MinimumTempType2
        
def GetMaximumComfortableTemperature(pokemonType1, pokemonType2):
    MaximumTempType1 = GetMaxTemp(pokemonType1)
    MaximumTempType2 = GetMaxTemp(pokemonType2)         
    if(MaximumTempType2 == None):
        return MaximumTempType1
    elif(MaximumTempType1 >= MaximumTempType2):
        return MaximumTempType1
    else:
        return MaximumTempType2
    
def GetMinTemp(pokemonType):
    if(pokemonType == "Ice"):
        return -100
    elif(pokemonType == "Dragon"):
        return -60
    elif(pokemonType in ["Ground", "Rock", "Steel"]):
        return -50
    elif(pokemonType == "Ghost"):
        return -40
    elif(pokemonType in ["Normal", "Fighting", "Poison", "Electric", "Psychic", "Dark", "Fairy"]):
        return -30
    elif(pokemonType in ["Flying", "Bug", "Water", "Grass"]):
        return -25
    elif(pokemonType == "Fire"):
        return -15
    else:
        return None

def GetMaxTemp(pokemonType):
    if(pokemonType == "Ice"):
        return 20
    elif(pokemonType in ["Bug", "Water", "Grass"]):
        return 40
    elif(pokemonType in ["Normal", "Fighting", "Flying", "Poison", "Ghost", "Electric", "Psychic", "Dark", "Fairy"]):
        return 45
    elif(pokemonType in ["Ground", "Rock"]):
        return 55
    elif(pokemonType == "Steel"):
        return 60
    elif(pokemonType == "Dragon"):
        return 70
    elif(pokemonType == "Fire"):
        return 100
    else:
        return None
    
def GetLeatherType(bodySize, eggGroup1, eggGroup2, isLegendary):
    if(isLegendary):
        return "PW_Leather_Legendary"    
    elif(eggGroup1 == "Flying" or eggGroup2 == "Flying"):
        return "Leather_Bird"
    elif (bodySize < 0.6):    
        return "Leather_Light"
    elif (bodySize < 2):
        return "Leather_Plain"
    else:
        return "Leather_Heavy"
    
def GetToxicSensitivity(type1, type2):  
    toxicSensitivity = 0.5
    toxicSensitivity *= GetToxicMult(type1)
    toxicSensitivity *= GetToxicMult(type2)
    return toxicSensitivity
        
def GetToxicMult(pokemonType):
    if(pokemonType in ["Poison", "Steel"]):
        return 0
    elif(pokemonType in ["Ground", "Rock", "Ghost"]):
        return 0.5
    elif(pokemonType in ["Grass", "Fairy"]): 
        return 2
    else:
        return 1

def GetDescription(descriptionFile):
    desc1 = descriptionFile.readline()
    desc2 = descriptionFile.readline()    
    if desc1 != desc2:
        description = desc1.strip() + "\\n" + desc2.strip()
    else:
        description = desc1.strip()
    return description

def GetGeneration(i):
    if(i < 151):
        generation = 1
    elif(i < 251):
        generation = 2
    elif (i < 386):
        generation = 3
    elif (i < 493):
        generation = 4
    elif (i < 649):
        generation = 5
    elif (i < 721):
        generation = 6
    elif (i < 809):
        generation = 7
    else:
        generation = 8
    return generation

def GetDrawSize(size, sizeMult):
    return LagrangeInterpolSize(size) * sizeMult

def GetDessicatedDrawSize(size, sizeMult, dessicatedDrawSize_Mult):
    return GetDrawSize(size, sizeMult) * dessicatedDrawSize_Mult

def GetTexturePath(texPath, i, pokemonDefName):
    return "%s%03d_%s/%s"% (texPath, i,pokemonDefName,pokemonDefName)

def GetTexturePathMale(texPath, i, pokemonDefName):
    return "%s%03d_%s/%sMale"% (texPath, i,pokemonDefName,pokemonDefName)
    
def GetTexturePathFemale(texPath, i, pokemonDefName):
    return "%s%03d_%s/%sFemale"% (texPath, i,pokemonDefName,pokemonDefName)

def GetAgeExpectancy(wildLevelMax, isLegendary, isBaby):
    if(isLegendary):
        ageExpectancy = 100 * wildLevelMax
    elif(isBaby):
        ageExpectancy = 12
    else:
        ageExpectancy = wildLevelMax
    return ageExpectancy

def GetSpawnRate(rarity, isBaby, isLegendary, isFossil, isParticular):     
    if(isBaby or isLegendary or isFossil or isParticular):
        spawnRate = 0
    else:
        spawnRate = rarity
    return spawnRate

def GetHerdAnimal(spawnRate, evolutionTier):   
    if (spawnRate<3 and spawnRate!=0 and evolutionTier == 1):
        herdAnimal = "true"
    else:
        herdAnimal = "false"
    return herdAnimal

def GetStarter(evolutionTier, isEvolutionMax, rarity, isFossil, isLegendary, isParticular, isBaby):
    if(evolutionTier==1 and isEvolutionMax == 0 and rarity <= 3 and isFossil==0 and isLegendary == 0 and isParticular == 0 and isBaby == 0):
        starter = "true"
    else:
        starter = "false"
    return starter  

def GetEcoSystemWeight(size):
    ecoSystemWeight = size*0.8
    if (ecoSystemWeight > 2):
        ecoSystemWeight = 2
    return ecoSystemWeight

def GetTradeTags(rarity, evolutionTier, isBaby, isLegendary, isFossil, isParticular):
    tradeTags = []
    rarity = int(rarity)
    if (isBaby or isLegendary or isFossil or isParticular or rarity >= 8):
        tradeTags=["PW_PokemonExotic"]    
    elif (rarity >= 6):
        tradeTags=["PW_PokemonRare"]
    elif (rarity >= 4):
        tradeTags=["PW_PokemonUncommon"]
    elif (rarity == 3 and evolutionTier == 1):
        tradeTags=["PW_PokemonStarter"]
    else:
        tradeTags=["PW_PokemonCommon"]
    return tradeTags

def FixNameIfNidoran(fullName, defName):
    if(defName == "NidoranM"):
        return "Nidoran♂"
    elif(defName == "NidoranF"):
        return "Nidoran♀"
    else:
        return fullName

def GetCSVData(filePath):
    data = pd.read_csv(filePath, keep_default_na=False, encoding = "latin1")    
    return data

def GetGlowBothTypes(type1, type2):
    value = GetGlow(type1)
    if (value[0] == False):
        value = GetGlow(type2)     
    return value

def GetGlow(type1):
    flag = True
    if(type1 == "Ghost"):
        colors = (112,88,152)
    elif(type1 == "Fire"):
        colors = (240,128,48)
    elif(type1 == "Electric"):
        colors = (248,208,48)
    elif(type1 == "Ice"):
        colors = (152,216,216)
    elif(type1 == "Dragon"):
        colors = (112,56,248)
    elif(type1 == "Dark"):
        colors = (112,88,72)
    elif(type1 == "Fairy"):
        colors = (238,153,172)
    else:
        flag = False
        colors = ()
        
    return [flag, colors]

def main():  
    PokemonData = GetCSVData("Data/DataPokemon.csv")   
    EvolutionData = GetCSVData("Data/DataEvolutions.csv")
    useOldMove = True
    if(useOldMove == True):
        MoveData = GetCSVData("Data/DataMovesOld.csv")
    else:
        with open("Data/DataMoves.json", "r", encoding = "utf8") as f:
            MoveData = json.load(f)

    """Defining some lists containing data we iterate on, for evolutions and moves"""
    pokemonEvolutionLine = list(PokemonData.EvolLine)
    pokemonEvolutionTier = list(PokemonData.EvolTier)
    defNameList = list(PokemonData.DefName)
    
    evolvingTo = list(EvolutionData.EvolvingTo)
    evolvingFrom = list(EvolutionData.EvolvingFrom)
    evolRequirement = list(EvolutionData.EvolutionRequirement)
    evolLevelMin = list(EvolutionData.Level)
    evolFriendshipMin = list(EvolutionData.Happinness)
    evolRequiredTime = list(EvolutionData.Time)
    evolRequiredGender = list(EvolutionData.Gender)
    evolRequiredItem = list(EvolutionData.Item)

    evolutions = list(zip(evolvingTo, evolvingFrom, evolRequirement, evolLevelMin, 
        evolFriendshipMin, evolRequiredTime, evolRequiredGender, evolRequiredItem))

    otherEvoRequirements = {
        "Hitmonlee" : "attack",
        "Hitmonchan": "defense",
        "Hitmontop" : "balanced"
    }

    with open("Data/forms.json", "r") as f:
        formsData = json.load(f)

    hasForm = list(formsData.keys())
    
    for name in [name for name in defNameList if name not in otherEvoRequirements.keys()]:
        otherEvoRequirements[name] = "none"
    
    if(useOldMove == True):
        movesPokemonId = list(MoveData.DexNumber)
        movesName = list(MoveData.Moves)
        movesUnlockLevel = list(MoveData.Level)
 
    """defining some global variables"""
    dessicatedDrawSize_Mult = 0.5
    shadowVolumeMult_1 = 0.35
    shadowVolumeMult_2 = 0.25
    shadowVolumeMult_3 = 0.25
    shadowOffset_1 = 0
    shadowOffset_2 = 0
    shadowOffset_3 = -0.3    
    averageHumanSize = 1.6
    baseHealthScale = 1
    shinyChance = 0.00125
    leatherAmount = 30    
    wildGroupMin = 2
    wildGroupMax = 4    
    petness = 1   
    expYieldMultiplier = 2
    descriptionFile = "pokemonDescription.txt"
    descriptionFile = open(descriptionFile, "r", encoding = "utf-8")
    texPathDessicated = "Things/Pawn/PokemonDessicated/PokemonDessicated"
    
    """Opening xml file where we write the Pokemon Defs"""
    #f = codecs.open("OutputFiles/Races_Pokemon.xml", "w", "utf-8")
    root = Element("Defs")
    
    for i, pokemonDefName in enumerate(defNameList):
        #print(pokemonDefName)
        """Getting all data from csv file"""
        pokedexNumber = PokemonData.DexNumber[i]
        pokemonFullName = PokemonData.Name[i]        
        hpEV = PokemonData.HPEv[i]
        attackEV = PokemonData.AttackEv[i]
        defenseEV = PokemonData.DefenseEv[i]
        spAttackEV = PokemonData.SpAttackEv[i]
        spDefenseEV = PokemonData.SpDefenseEv[i]
        speedEV = PokemonData.SpeedEv[i]        
        type1 = PokemonData.Type1[i]
        type2 = PokemonData.Type2[i]       
        eggGroup1 = PokemonData.EggGroup1[i]
        eggGroup2 = PokemonData.EggGroup2[i]       
        size = PokemonData.Size[i]     
        sizeMult = PokemonData.SizeMulti[i] #2x Multiplicator for oversized sprites like Wailord/Rayquaza        
        wildLevelMin = PokemonData.MinWildLvl[i]
        wildLevelMax = PokemonData.MaxWildLvl[i]        
        statHealth = PokemonData.HP[i]
        statAtk = PokemonData.Attack[i]
        statDef = PokemonData.Defense[i]
        statAtkSpe = PokemonData.SpAttack[i]
        statDefSpe = PokemonData.SpDefense[i]
        statSpeed = PokemonData.Speed[i]  
        genderLess = PokemonData.GenderLess[i]   
        femaleDifference = PokemonData.GenderDifference[i]   
        isBaby = PokemonData.Baby[i]      
        isLegendary = PokemonData.Legendary[i]
        isFossil = PokemonData.Fossil[i]
        isParticular = PokemonData.ParticularSpawn[i]       
        evolutionLine = PokemonData.EvolLine[i]
        rarity = PokemonData.Rarity[i]
        evolutionTier = PokemonData.EvolTier[i]
        isEvolutionMax = PokemonData.EvolMax[i]
        baseFriendship = PokemonData.BaseFriendship[i]  
        bodyShape = PokemonData.RimworldShape[i]
        femaleRatio = PokemonData.FemaleRatio[i]       
        expCategory = PokemonData.XpCategory[i]
        eggLayDays = PokemonData.EggLayTime[i]
        catchRate = PokemonData.CatchRate[i]
        expYield = PokemonData.ExpYield[i]
               
        """Computing other values based on the data"""
        pokemonFullName = FixNameIfNidoran(pokemonFullName, pokemonDefName)      
        tradeTags = GetTradeTags(rarity, evolutionTier, isBaby, isLegendary, isFossil, isParticular) 
        generation = GetGeneration(i)              
        texPath = f"Things/Pawn/Pokemon/Gen_{generation}/"
        ComfyTemperatureMin = GetMinimumComfortableTemperature(type1, type2)
        ComfyTemperatureMax = GetMaximumComfortableTemperature(type1, type2)      
        toxicSensitivity = GetToxicSensitivity(type1, type2)       
        descriptionFull = GetDescription(descriptionFile)        
        drawSize = GetDrawSize(size, sizeMult)
        dessicatedDrawSize = GetDessicatedDrawSize(size, sizeMult, dessicatedDrawSize_Mult)     
        texturePath = GetTexturePath(texPath,i+1,pokemonDefName)
        texturePathMale = GetTexturePathMale(texPath,i+1,pokemonDefName)
        texturePathFemale = GetTexturePathFemale(texPath,i+1,pokemonDefName)           
        totalStat = statHealth + statAtk + statDef + statAtkSpe + statDefSpe + statSpeed 
        avrgStat = totalStat // 6
        avrgLevel = wildLevelMin + ((wildLevelMax - wildLevelMin) // 2)
        combatPower = (totalStat * avrgLevel) // 55
        marketValue = round(avrgStat * 7 / 50) * 50 #round to nearest 50-step       
        baseBodySize = size/averageHumanSize   
        rimworldSpeed = LagrangeInterpolSpeed(statSpeed)
        leather = GetLeatherType(baseBodySize, eggGroup1, eggGroup2, isLegendary)
        body = "PW_" + bodyShape
        ageExpectancy = GetAgeExpectancy(wildLevelMax, isLegendary, isBaby)
        wildness = 0 if isBaby else rarity/10
        spawnRate = GetSpawnRate(rarity, isBaby, isLegendary, isFossil, isParticular)
        herdAnimal = GetHerdAnimal(spawnRate, evolutionTier)
        packAnimal = "true" if baseBodySize >= 0.6 else "false"
        starter = GetStarter(evolutionTier, isEvolutionMax, rarity, isFossil, isLegendary, isParticular, isBaby)
        manhunterOnDamageChance = rarity / 10
        manhunterOnTameFailChance = rarity / 10  
        ecoSystemWeight = GetEcoSystemWeight(size)
        canEvolve = "false" if isEvolutionMax else "true"
        ShadowVolume1 = shadowVolumeMult_1*drawSize
        ShadowVolume2 = shadowVolumeMult_2*drawSize
        ShadowVolume3 = shadowVolumeMult_3*drawSize  
        shouldGlow, colors = GetGlowBothTypes(type1, type2)
        
        """We write everything for 1 Pokemon in the def file"""
    
        ThingDef = SubElement(root, "ThingDef", {"ParentName": "AnimalThingBase"})
        SubElement(ThingDef, "defName").text = "PW_" + pokemonDefName
        SubElement(ThingDef, "label").text = pokemonFullName
        SubElement(ThingDef, "description").text = descriptionFull
        
        comps = SubElement(ThingDef, "comps")
        li    = SubElement(comps, "li", {"Class":"PokeWorld.CompProperties_Pokemon"})
        SubElement(li, "pokedexNumber").text = str(pokedexNumber)
        SubElement(li, "generation").text = str(generation)

        types  = SubElement(li, "types")
        SubElement(types, "li").text = type1
        
        if type2:
            SubElement(types, "li").text = type2 
            
        SubElement(li, "starter").text = starter
        SubElement(li, "rarity").text = str(rarity)
        SubElement(li, "canEvolve").text = canEvolve
        SubElement(li, "evolutionLine").text = str(evolutionLine)

        """Adding all available evolutions"""
        currentPokemonEvos = [evo for evo in evolutions if evo[1] == pokemonDefName]
        #print(pokemonDefName, evolutions[0][1])

        if currentPokemonEvos:
            evolutions_EL = SubElement(li, "evolutions")
            for evolution in currentPokemonEvos:
                evoTo, evoFrom, evoReq, evoLevelMin, evoFriendship, evoTime, evoGender, evoItem = evolution

                sub1Li = SubElement(evolutions_EL, "li")
                SubElement(sub1Li, "pawnKind").text = "PW_" + evoTo
                SubElement(sub1Li, "requirement").text = evoReq
                if evoReq == "level":
                    SubElement(sub1Li, "otherRequirement").text = otherEvoRequirements[evoTo]
                    SubElement(sub1Li, "level").text = str(evoLevelMin)
                    SubElement(sub1Li, "friendship").text = str(evoFriendship)
                    SubElement(sub1Li, "timeOfDay").text = evoTime
                    SubElement(sub1Li, "gender").text = evoGender
                else:
                    SubElement(sub1Li, "item").text = "PW_" + evoItem
            
        #Moves will go here
        moves = SubElement(li, "moves")
        sub2Li = SubElement(moves, "li")
        SubElement(sub2Li, "moveDef").text = "Struggle"
        SubElement(sub2Li, "unlockLevel").text = "1"
        alreadyAddedMoves = []

        if(useOldMove == True):

            for index, moveID in enumerate(movesPokemonId):
                if(moveID == pokedexNumber):
                    moveName = movesName[index]
                    
                    if(alreadyAddedMoves.count(moveName) > 0):
                        continue
                    alreadyAddedMoves.append(moveName)
                    
                    if(moveName == "Explosion"):
                        continue
                    
                    sub3Li = SubElement(moves, "li")
                    SubElement(sub3Li, "moveDef").text = moveName
                    SubElement(sub3Li, "unlockLevel").text = str(movesUnlockLevel[index]) 
        else:
           
            for move in MoveData[pokemonFullName]["moves"]:
                #print(moveID, pokedexNumber)
                if move["moveName"] in alreadyAddedMoves:
                    continue
                
                alreadyAddedMoves.append(move["moveName"])
                
                if(move["moveName"] == "Explosion"):
                    continue
                
                sub3Li = SubElement(moves, "li")
                SubElement(sub3Li, "moveDef").text = move["moveName"]
                SubElement(sub3Li, "unlockLevel").text = str(move["learnLvl"]) 
           
        if (isBaby or isLegendary or isFossil or isParticular):
            attributes = SubElement(li, "attributes")
            if (isBaby):
                SubElement(attributes, "li").text = "Baby"
            if (isLegendary):
                SubElement(attributes, "li").text = "Legendary"
            if (isFossil):
                SubElement(attributes, "li").text = "Fossil"
            if (isParticular):
                SubElement(attributes, "li").text = "Particular"

        SubElement(li, "baseFriendship").text = str(baseFriendship)
        
        if(femaleRatio != -1):
            SubElement(li, "femaleRatio").text = f"{femaleRatio:g}"
        
        SubElement(li, "expCategory").text = expCategory
        SubElement(li, "wildLevelMin").text = str(wildLevelMin)
        SubElement(li, "wildLevelMax").text = str(wildLevelMax)
        
        eggGroups = SubElement(li, "eggGroups")
        SubElement(eggGroups, "li").text = eggGroup1
        
        if eggGroup2:
            SubElement(eggGroups, "li").text = eggGroup2
        
        SubElement(li, "baseHP").text        = str(statHealth)
        SubElement(li, "baseAttack").text    = str(statAtk)
        SubElement(li, "baseDefense").text   = str(statDef)
        SubElement(li, "baseSpAttack").text  = str(statAtkSpe)
        SubElement(li, "baseSpDefense").text = str(statDefSpe)
        SubElement(li, "baseSpeed").text     = str(statSpeed)

        EVYields = SubElement(li, "EVYields")
        
        if(hpEV > 0):
            SubElement(EVYields, "PW_HP").text = str(hpEV)
        if(attackEV > 0):
            SubElement(EVYields, "PW_Attack").text = str(attackEV)
        if(defenseEV > 0):
            SubElement(EVYields, "PW_Defense").text = str(defenseEV)
        if(spAttackEV > 0):
            SubElement(EVYields, "PW_SpecialAttack").text = str(spAttackEV)
        if(spDefenseEV > 0):
            SubElement(EVYields, "PW_SpecialDefense").text = str(spDefenseEV)
        if(speedEV > 0):
            SubElement(EVYields, "PW_Speed").text = str(speedEV)
        
        SubElement(li, "catchRate").text = str(catchRate)
        SubElement(li, "shinyChance").text = str(shinyChance)
        
        if pokemonDefName in hasForm:
            currData = formsData[pokemonDefName]
            SubElement(li, "formChangerCondition").text = currData["formChangerCondition"]
            if "showFormLabel" in currData.keys():
                SubElement(li, "showFormLabel").text = currData["showFormLabel"]

            formElement = SubElement(li, "forms")
            for form in currData["forms"]:
                sub4Li = SubElement(formElement, "li")

                for key, value in form.items():
                    if isinstance(value, list): #if the value is a list of stuff like biomes
                        below = SubElement(sub4Li, key) #we need to add two lower tags
                        for criteria in value:
                            SubElement(below, "li").text = criteria
                    else:
                        SubElement(sub4Li, key).text = value

                if "texPathKey" not in form.keys():
                    SubElement(sub4Li, "texPathKey").text = form["label"]

        if eggGroup1 != "Undiscovered":
            if pokemonDefName != "Ditto":
                li = SubElement(comps, "li", {"Class":"CompProperties_EggLayer"})
                
                if pokemonDefName == "Manaphy":  
                    SubElement(li, "eggFertilizedDef").text = "PW_EggPhione"
                
                else:
                    for indexOeuf, DexName in enumerate(defNameList):
                        if pokemonEvolutionLine[indexOeuf] == evolutionLine and pokemonEvolutionTier[indexOeuf] == 1:
                            SubElement(li, "eggFertilizedDef").text = "PW_Egg" + DexName
                            break
                
                SubElement(li, "eggFertilizationCountMax").text = "1"
                SubElement(li, "eggLayIntervalDays").text = str(int(eggLayDays))
                SubElement(li, "eggProgressUnfertilizedMax").text = "0"
                SubElement(li, "eggCountRange").text = "1"
    
                if genderLess == 1:
                    SubElement(li, "eggLayFemaleOnly").text = "false"

            else:
                li = SubElement(comps, "li", {"Class":"PokeWorld.CompProperties_DittoEggLayer"})
                SubElement(li, "eggFertilizationCountMax").text = "1"
                SubElement(li, "eggLayIntervalDays").text = str(int(eggLayDays))
                SubElement(li, "eggProgressUnfertilizedMax").text = "0"
                SubElement(li, "eggCountRange").text = "1"
                
        if((type1 == "Fire" or type2 == "Fire") and not(type1 == "Ice" or type2 == "Ice")):
            li = SubElement(comps, "li", {"Class":"CompProperties_HeatPusher"})
            
            SubElement(li, "compClass").text = "PokeWorld.CompPokemonHeatPusher"
            SubElement(li, "heatPerSecond").text = f"{totalStat / 220:.2f}"
            SubElement(li, "heatPushMaxTemperature").text = "28"
            
        if((type1 == "Ice" or type2 == "Ice") and not(type1 == "Fire" or type2 == "Fire")):
            li = SubElement(comps, "li", {"Class":"CompProperties_HeatPusher"})
            
            SubElement(li, "compClass").text = "PokeWorld.CompPokemonHeatPusher"
            SubElement(li, "heatPerSecond").text = f"{-totalStat / 220:.2f}"
            SubElement(li, "heatPushMinTemperature").text = "-8"

        if(type1 == "Electric" or type2 == "Electric"):
            basePowerConsumption = -totalStat / 8
            if(isLegendary):
                basePowerConsumption *= 3
            li = SubElement(comps, "li", {"Class":"CompProperties_Power"})
            
            SubElement(li, "compClass").text = "PokeWorld.CompPokemonPower"
            SubElement(li, "basePowerConsumption").text = f"{basePowerConsumption:.2f}"

        """
        if(shouldGlow):
            f.write("      <li Class=\"CompProperties_Glower\">\n") 
            f.write("        <glowRadius>%d</glowRadius>\n"% (math.ceil(totalStat / 200)))
            f.write("        <glowColor>(%d,%d,%d,0)</glowColor>\n"% (colors[0], colors[1], colors[2]))
            f.write("      </li>\n")
        """
    
        statBases = SubElement(ThingDef, "statBases")
        SubElement(statBases, "MoveSpeed").text = f"{rimworldSpeed:.1f}"
        SubElement(statBases, "MarketValue").text = str(marketValue)
        SubElement(statBases, "ComfyTemperatureMin").text = str(ComfyTemperatureMin)
        SubElement(statBases, "ComfyTemperatureMax").text = str(ComfyTemperatureMax)
        SubElement(statBases, "LeatherAmount").text = str(leatherAmount)
        SubElement(statBases, "PW_BaseXPYield").text = str(expYield * expYieldMultiplier)
        SubElement(statBases, "ToxicSensitivity").text = f"{toxicSensitivity:g}"
        
        inspectorTabs = SubElement(ThingDef, "inspectorTabs")
        SubElement(inspectorTabs, "li").text = "PokeWorld.ITab_Pawn_Moves"
        
        if(type1 == "Steel" or type2 == "Steel"):
            SubElement(ThingDef, "soundDrop").text = "ChunkSlag_Drop"
        elif(type1 == "Rock" or type2 == "Rock"):
            SubElement(ThingDef, "soundDrop").text = "ChunkRock_Drop"

        race = SubElement(ThingDef, "race")
    
        SubElement(race, "body").text = body

        if genderLess == 1:
            SubElement(race, "hasGenders").text = "false"
                
        if (isBaby or isLegendary or isFossil or isParticular):
            SubElement(race, "herdMigrationAllowed").text = "false"
        
        SubElement(race, "petness").text = f"{petness:.1f}"
        SubElement(race, "packAnimal").text = packAnimal
        SubElement(race, "herdAnimal").text = herdAnimal
        SubElement(race, "baseBodySize").text = f"{baseBodySize:.2f}"
        SubElement(race, "baseHungerRate").text = "0.30"
        SubElement(race, "baseHealthScale").text = f"{baseHealthScale:.2f}"
        SubElement(race, "foodType").text = "OmnivoreAnimal, VegetarianRoughAnimal"

        if i in [0, 2]:
            SubElement(race, "meatLabel").text = "Pokémon meat"
        elif baseBodySize < 0.7:
            SubElement(race, "useMeatFrom").text = "PW_Bulbasaur"
        else:
            SubElement(race, "useMeatFrom").text = "PW_Venusaur"
        
        SubElement(race, "leatherDef").text = leather
        SubElement(race, "nameOnTameChance").text = "1"
        SubElement(race, "trainability").text = "Advanced"
        trainableTags = SubElement(race, "trainableTags")
        SubElement(trainableTags, "li").text = "PW_Pokemon"

        SubElement(race, "wildness").text = f"{wildness:.1f}"
        SubElement(race, "manhunterOnDamageChance").text   = f"{manhunterOnDamageChance:.2f}"
        SubElement(race, "manhunterOnTameFailChance").text = f"{manhunterOnTameFailChance:.2f}"
        SubElement(race, "nuzzleMtbHours").text = "12"
        SubElement(race, "lifeExpectancy").text = str(ageExpectancy)

        lifeStageAges = SubElement(race, "lifeStageAges")
        sub5Li = SubElement(lifeStageAges, "li")

        SubElement(sub5Li, "def").text = "AnimalAdult"
        SubElement(sub5Li, "minAge").text = "0"
        SubElement(sub5Li, "soundWounded").text = f"Pawn_{pokemonDefName}_Call"
        SubElement(sub5Li, "soundDeath").text = f"Pawn_{pokemonDefName}_Call"
        SubElement(sub5Li, "soundCall").text = f"Pawn_{pokemonDefName}_Call"
        SubElement(sub5Li, "soundAngry").text = f"Pawn_{pokemonDefName}_Call"

        SubElement(race, "soundMeleeHitPawn").text = "Pawn_Melee_SmallScratch_HitPawn"
        SubElement(race, "soundMeleeHitBuilding").text = "Pawn_Melee_SmallScratch_HitBuilding"
        SubElement(race, "soundMeleeMiss").text = "Pawn_Melee_SmallScratch_Miss"
        SubElement(race, "soundCallIntervalRange").text = "3000~6000"

        recipes = SubElement(ThingDef, "recipes")

        SubElement(recipes, "li").text = "PW_AdministerPotion"
        SubElement(recipes, "li").text = "PW_AdministerHyperPotion"
        SubElement(recipes, "li").text = "PW_AdministerMaxPotion"
        SubElement(recipes, "li").text = "PW_AdministerHealPowder"
        SubElement(recipes, "li").text = "PW_GiveOneRareCandy"
        SubElement(recipes, "li").text = "PW_GiveFiveRareCandy"
        
        """Adding recipe for item based evolutions if needed"""
        if currentPokemonEvos:        
            for evolution in currentPokemonEvos:
                evoReq  = evolution[2]
            
                if evoReq == "item":
                    evoItem = evolution[7]
                    SubElement(recipes, "li").text = "PW_Expose" + evoItem

        tradeTags_EL = SubElement(ThingDef, "tradeTags")
        
        for tag in tradeTags:
            SubElement(tradeTags_EL, "li").text = tag

        PawnKindDef = SubElement(root, "PawnKindDef", {"ParentName": "AnimalKindBase"})

        SubElement(PawnKindDef, "defName").text = "PW_" + pokemonDefName
        SubElement(PawnKindDef, "label").text = pokemonFullName
        SubElement(PawnKindDef, "labelPlural").text = pokemonFullName
        SubElement(PawnKindDef, "race").text = "PW_" + pokemonDefName
        SubElement(PawnKindDef, "combatPower").text = str(combatPower)
        
        if (isBaby or isLegendary or isFossil or isParticular):
            SubElement(PawnKindDef, "canArriveManhunter").text = "false"

        SubElement(PawnKindDef, "ecoSystemWeight").text = f"{ecoSystemWeight:.2f}"
        
        if herdAnimal == "true":
            SubElement(PawnKindDef, "wildGroupSize").text = f"{wildGroupMin}~{wildGroupMax}"
            
        lifeStages      = SubElement(PawnKindDef, "lifeStages")
        li              = SubElement(lifeStages, "li")
        bodyGraphicData = SubElement(li, "bodyGraphicData")

        if (femaleDifference == 1):
            SubElement(bodyGraphicData, "texPath").text = texturePathMale
        else:
            SubElement(bodyGraphicData, "texPath").text = texturePath

        SubElement(bodyGraphicData, "drawSize").text = f"{drawSize:.1f}"

        shadowData = SubElement(bodyGraphicData, "shadowData")
        
        SubElement(shadowData, "volume").text = f"({ShadowVolume1:.2f}, {ShadowVolume2:.2f}, {ShadowVolume3:.2f})"
        SubElement(shadowData, "offset").text = f"({shadowOffset_1:.2f}, {shadowOffset_2:.2f}, {shadowOffset_3:.2f})"
        
        dessicatedBodyGraphicData = SubElement(li, "dessicatedBodyGraphicData")
        
        SubElement(dessicatedBodyGraphicData, "texPath").text = texPathDessicated
        SubElement(dessicatedBodyGraphicData, "drawSize").text = f"{dessicatedDrawSize:.1f}"
        
        if (femaleDifference == 1):
            femaleGraphicData = SubElement(li, "femaleGraphicData")

            SubElement(femaleGraphicData, "texPath").text = texturePathFemale
            SubElement(femaleGraphicData, "drawSize").text = f"{drawSize:.1f}"
            
            shadowData = SubElement(femaleGraphicData, "shadowData")

            SubElement(shadowData, "volume").text = f"({ShadowVolume1:.2f}, {ShadowVolume2:.2f}, {ShadowVolume3:.2f})"
            SubElement(shadowData, "offset").text = f"({shadowOffset_1:.2f}, {shadowOffset_2:.2f}, {shadowOffset_3:.2f})"
        
    with open('OutputFiles/Races_Pokemon.xml', 'wb') as f:
        indent(root, space = "  ")
        test = tostring(root, xml_declaration=True, encoding='utf8', method='xml')
        f.write(test)


if __name__ == "__main__":
    main()
