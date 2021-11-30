# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import codecs
import string

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

def GetDescription(i, descriptionFile):
    descriptionFile = codecs.open(descriptionFile,"r", "utf-8")   
    for fileLine in range(0,i):
        descriptionFile.readline()
        descriptionFile.readline()
    desc1 = descriptionFile.readline()
    desc2 = descriptionFile.readline()   
    descriptionFile.close()   
    if desc1 != desc2:
        description = desc1.strip() + '\\n' + desc2.strip()
    else:
        description = desc1.strip()
    return description
    
def GetGenerationFolderTexPath(i):
    if(i < 151):
        texPath = "Things/Pawn/Pokemon/Gen_1/"
    elif(i < 251):
        texPath = "Things/Pawn/Pokemon/Gen_2/"
    elif (i < 386):
        texPath = "Things/Pawn/Pokemon/Gen_3/"
    else:
        texPath = "Things/Pawn/Pokemon/Gen_4/"
    return texPath

def GetGeneration(i):
    if(i < 151):
        generation = 1
    elif(i < 251):
        generation = 2
    elif (i < 386):
        generation = 3
    else:
        generation = 4
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

def GetBody(bodyShape):
    return "PW_" + bodyShape

def GetAgeExpectancy(wildLevelMax, isLegendary, isBaby):
    if(isLegendary):
        ageExpectancy = 100 * wildLevelMax
    elif(isBaby):
        ageExpectancy = 12
    else:
        ageExpectancy = wildLevelMax
    return ageExpectancy

def GetWildness(rarity, isBaby):
    if(isBaby):
        wildness = 0
    else:
        wildness = rarity/10
    return wildness

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

def GetPackAnimal(baseBodySize):   
    if (baseBodySize >= 0.6):
        packAnimal = "true"
    else:
        packAnimal = "false"
    return packAnimal

def GetStarter(evolutionTier, isEvolutionMax, rarity, isFossil, isLegendary, isParticular, isBaby):
    if(evolutionTier==1 and isEvolutionMax == 0 and rarity <= 3 and isFossil==0 and isLegendary == 0 and isParticular == 0 and isBaby == 0):
        starter = "true"
    else:
        starter = "false"
    return starter  

def GetManhunterOnDamageChance(rarity):
    return rarity / 10

def GetManhunterOnTameFailChance(rarity):      
    return rarity / 10

def GetEcoSystemWeight(size):
    ecoSystemWeight = size*0.8
    if (ecoSystemWeight > 2):
        ecoSystemWeight = 2
    return ecoSystemWeight

def GetCanEvolve(isEvolutionMax):
    if isEvolutionMax:
        canEvolve = "false"
    else:
        canEvolve = "true"
    return canEvolve

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
    data = pd.read_csv(filePath, keep_default_na=False, encoding = 'latin1')    
    return data

def main():  
    PokemonData = GetCSVData("Data/DataPokemon.csv")   
    EvolutionData = GetCSVData("Data/DataEvolutions.csv")
    MoveData = GetCSVData("Data/DataMoves.csv")
    
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
    texPathDessicated = "Things/Pawn/PokemonDessicated/PokemonDessicated"
    
    """Opening xml file where we write the Pokemon Defs"""
    f = codecs.open("OutputFiles/Races_Pokemon.xml", "w", "utf-8")

    """writing header"""
    f.write('<?xml version="1.0" encoding="utf-8" ?>\n')
    f.write("<Defs>\n\n")
    
    for i in range(0,len(defNameList)):
        """Getting all data from csv file"""
        pokedexNumber = PokemonData.DexNumber[i]
        pokemonDefName = PokemonData.DefName[i]
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
        texPath = GetGenerationFolderTexPath(i)       
        generation = GetGeneration(i)      
        ComfyTemperatureMin = GetMinimumComfortableTemperature(type1, type2)
        ComfyTemperatureMax = GetMaximumComfortableTemperature(type1, type2)      
        toxicSensitivity = GetToxicSensitivity(type1, type2)       
        descriptionFull = GetDescription(i, descriptionFile)        
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
        body = GetBody(bodyShape)        
        ageExpectancy = GetAgeExpectancy(wildLevelMax, isLegendary, isBaby)
        wildness = GetWildness(rarity, isBaby)
        spawnRate = GetSpawnRate(rarity, isBaby, isLegendary, isFossil, isParticular)
        herdAnimal = GetHerdAnimal(spawnRate, evolutionTier)
        packAnimal = GetPackAnimal(baseBodySize)    
        starter = GetStarter(evolutionTier, isEvolutionMax, rarity, isFossil, isLegendary, isParticular, isBaby)
        manhunterOnDamageChance = GetManhunterOnDamageChance(rarity)
        manhunterOnTameFailChance = GetManhunterOnTameFailChance(rarity)    
        ecoSystemWeight = GetEcoSystemWeight(size)
        canEvolve = GetCanEvolve(isEvolutionMax)
        ShadowVolume1 = shadowVolumeMult_1*drawSize
        ShadowVolume2 = shadowVolumeMult_2*drawSize
        ShadowVolume3 = shadowVolumeMult_3*drawSize     
          
        
        """We write everything for 1 Pokemon in the def file"""
    
        f.write('  <ThingDef ParentName="AnimalThingBase">\n')
        f.write("    <defName>PW_%s</defName>\n"% (pokemonDefName))  
        f.write("    <label>%s</label>\n"% (pokemonFullName))   
        f.write("    <description>%s</description>\n"% (descriptionFull)) 
        
        f.write("    <comps>\n")
        f.write('      <li Class="PokeWorld.CompProperties_Pokemon">\n')
        f.write("        <pokedexNumber>%d</pokedexNumber>\n"% (pokedexNumber))
        f.write("        <generation>%d</generation>\n"% (generation))
        
        f.write("        <types>\n")
        f.write("          <li>%s</li>\n"% (type1))
        if(type2 != ""):
            f.write("          <li>%s</li>\n"% (type2))
        f.write("        </types>\n")   
            
        f.write("        <starter>%s</starter>\n"% (starter))
        f.write("        <rarity>%d</rarity>\n"% (rarity))
        f.write("        <canEvolve>%s</canEvolve>\n"% (canEvolve))
        f.write("        <evolutionLine>%d</evolutionLine>\n"% (evolutionLine))
        """Adding all available evolutions"""
        if (canEvolve == "true"):
            f.write("        <evolutions>\n")
            evolutionCounter=0
            for pokIndice in evolvingFrom:
                if pokIndice == pokemonDefName:
                    f.write("          <li>\n")
                    f.write("            <pawnKind>PW_%s</pawnKind>\n"% (evolvingTo[evolvingFrom.index(pokIndice)+evolutionCounter]))
                    f.write("            <requirement>%s</requirement>\n"% (evolRequirement[evolvingFrom.index(pokIndice)+evolutionCounter]))
                    if evolRequirement[evolvingFrom.index(pokIndice)+evolutionCounter] == "level":
                        if evolvingTo[evolvingFrom.index(pokIndice)+evolutionCounter] == "Hitmonlee":
                            f.write("            <otherRequirement>%s</otherRequirement>\n"% ("attack"))
                        elif evolvingTo[evolvingFrom.index(pokIndice)+evolutionCounter] == "Hitmonchan":
                            f.write("            <otherRequirement>%s</otherRequirement>\n"% ("defense"))
                        elif evolvingTo[evolvingFrom.index(pokIndice)+evolutionCounter] == "Hitmontop":
                            f.write("            <otherRequirement>%s</otherRequirement>\n"% ("balanced"))
                        else:    
                            f.write("            <otherRequirement>%s</otherRequirement>\n"% ("none"))
                        f.write("            <level>%d</level>\n"% (evolLevelMin[evolvingFrom.index(pokIndice)+evolutionCounter]))
                        f.write("            <friendship>%d</friendship>\n"% (evolFriendshipMin[evolvingFrom.index(pokIndice)+evolutionCounter]))
                        f.write("            <timeOfDay>%s</timeOfDay>\n"% (evolRequiredTime[evolvingFrom.index(pokIndice)+evolutionCounter]))
                        f.write("            <gender>%s</gender>\n"% (evolRequiredGender[evolvingFrom.index(pokIndice)+evolutionCounter]))
                    else  :
                        f.write("            <item>PW_%s</item>\n"% (evolRequiredItem[evolvingFrom.index(pokIndice)+evolutionCounter]))
                    f.write("          </li>\n")
                    evolutionCounter+=1
            f.write("        </evolutions>\n")
            
        #Moves will go here
        f.write("        <moves>\n")
        f.write("          <li>\n")
        f.write("            <moveDef>Struggle</moveDef>\n")
        f.write("            <unlockLevel>1</unlockLevel>\n")
        f.write("          </li>\n")
        alreadyAddedMoves = []

        for index in range(0, len(movesPokemonId)):
            if(movesPokemonId[index] == pokedexNumber):
                moveName = movesName[index]
                if(alreadyAddedMoves.count(moveName) > 0):
                    continue
                alreadyAddedMoves.append(moveName)
                if(moveName == "Explosion"):
                    continue
                moveUnlockLevel = movesUnlockLevel[index]
                f.write("          <li>\n")
                f.write("            <moveDef>%s</moveDef>\n" %(moveName))
                f.write("            <unlockLevel>%d</unlockLevel>\n" %(moveUnlockLevel))
                f.write("          </li>\n")
        f.write("        </moves>\n")       
    
        if (isBaby or isLegendary or isFossil or isParticular):
            f.write("        <attributes>\n")
            if (isBaby):
                f.write("          <li>Baby</li>\n")
            if (isLegendary):
                f.write("          <li>Legendary</li>\n")
            if (isFossil):
                f.write("          <li>Fossil</li>\n")
            if (isParticular):
                f.write("          <li>Particular</li>\n")
            f.write("        </attributes>\n")    
        f.write("        <baseFriendship>%d</baseFriendship>\n"% (baseFriendship))
        if(femaleRatio != -1):
            f.write("        <femaleRatio>%g</femaleRatio>\n"% (femaleRatio))
        f.write("        <expCategory>%s</expCategory>\n"% (expCategory))
        f.write("        <wildLevelMin>%d</wildLevelMin>\n"% (wildLevelMin))
        f.write("        <wildLevelMax>%d</wildLevelMax>\n"% (wildLevelMax))
        
        f.write("        <eggGroups>\n")
        f.write("          <li>%s</li>\n"% eggGroup1)
        if(eggGroup2 != ""):
            f.write("          <li>%s</li>\n"% eggGroup2)
        f.write("        </eggGroups>\n")    
        
        f.write("        <baseHP>%d</baseHP>\n"% (statHealth))
        f.write("        <baseAttack>%d</baseAttack>\n"% (statAtk))
        f.write("        <baseDefense>%d</baseDefense>\n"% (statDef))
        f.write("        <baseSpAttack>%d</baseSpAttack>\n"% (statAtkSpe))
        f.write("        <baseSpDefense>%d</baseSpDefense>\n"% (statDefSpe))
        f.write("        <baseSpeed>%d</baseSpeed>\n"% (statSpeed)) 
        
        f.write("        <EVYields>\n") 
        if(hpEV > 0):
            f.write("          <PW_HP>%d</PW_HP>\n"% (hpEV))
        if(attackEV > 0):
            f.write("          <PW_Attack>%d</PW_Attack>\n"% (attackEV))
        if(defenseEV > 0):
            f.write("          <PW_Defense>%d</PW_Defense>\n"% (defenseEV))
        if(spAttackEV > 0):
            f.write("          <PW_SpecialAttack>%d</PW_SpecialAttack>\n"% (spAttackEV))
        if(spDefenseEV > 0):
            f.write("          <PW_SpecialDefense>%d</PW_SpecialDefense>\n"% (spDefenseEV))
        if(speedEV > 0):
            f.write("          <PW_Speed>%d</PW_Speed>\n"% (speedEV))
        f.write("        </EVYields>\n")
        f.write("        <catchRate>%d</catchRate>\n" % (catchRate))
        f.write("        <shinyChance>%g</shinyChance>\n"% (shinyChance)) 
        
        if pokemonDefName == "Pichu":
            f.write("        <formChangerCondition>Fixed</formChangerCondition>\n")
            f.write("        <showFormLabel>false</showFormLabel>\n")
            f.write("        <forms>\n")       
            f.write("          <li>\n")
            f.write("            <label>%s</label>\n"% ("Normal"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Normal"))
            f.write("          </li>\n") 
            f.write("          <li>\n")
            f.write("            <label>%s</label>\n"% ("Spiky"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Spiky"))
            f.write("            <weight>0.01</weight>\n")
            f.write("          </li>\n") 
            f.write("        </forms>\n")
        
        if pokemonDefName == "Unown":
            f.write("        <formChangerCondition>Fixed</formChangerCondition>\n")
            f.write("        <showFormLabel>true</showFormLabel>\n")
            f.write("        <forms>\n")
            
            for letter in list(string.ascii_uppercase):
                f.write("          <li>\n")
                f.write(f"            <label>{letter}</label>\n")
                f.write(f"            <texPathKey>{letter}</texPathKey>\n")
                f.write("          </li>\n")  
            f.write("          <li>\n")
            f.write("            <label>%s</label>\n"% ("!"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Exclamation"))
            f.write("            <weight>0.2</weight>\n")
            f.write("          </li>\n")        
            f.write("          <li>\n")
            f.write("            <label>%s</label>\n"% ("?"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Question"))
            f.write("            <weight>0.2</weight>\n")
            f.write("          </li>\n") 
            f.write("        </forms>\n")
        
        if pokemonDefName == "Castform":
            f.write("        <formChangerCondition>Environnement</formChangerCondition>\n")
            f.write("        <showFormLabel>false</showFormLabel>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Normal"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Normal"))
            f.write("            <isDefault>true</isDefault>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n")  
            f.write("            <timeOfDay>Day</timeOfDay>\n")
            f.write("            <includeWeathers>\n")
            f.write("              <li>Clear</li>\n")
            f.write("            </includeWeathers>\n")
            f.write("            <label>%s</label>\n"% ("Sunny"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Sunny"))
            f.write("            <type1>Fire</type1>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <includeWeathers>\n")
            f.write("              <li>Rain</li>\n")
            f.write("              <li>RainyThunderstorm</li>\n")
            f.write("              <li>FoggyRain</li>\n")
            f.write("            </includeWeathers>\n")
            f.write("            <label>%s</label>\n"% ("Rainy"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Rainy"))
            f.write("            <type1>Water</type1>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <includeWeathers>\n")
            f.write("              <li>SnowHard</li>\n")
            f.write("              <li>SnowGentle</li>\n")
            f.write("            </includeWeathers>\n")
            f.write("            <label>%s</label>\n"% ("Snowy"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Snowy"))
            f.write("            <type1>Ice</type1>\n")
            f.write("          </li>\n")       
            f.write("        </forms>\n")
        
        if pokemonDefName == "Deoxys":
            f.write("        <formChangerCondition>Selectable</formChangerCondition>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n")  
            f.write("            <label>%s</label>\n"% ("Normal"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Normal"))
            f.write("            <isDefault>true</isDefault>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Attack"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Attack"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Defense"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Defense"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Speed"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Speed"))
            f.write("          </li>\n") 
            f.write("        </forms>\n")
        
        if pokemonDefName == "Burmy":
            f.write("        <formChangerCondition>Environnement</formChangerCondition>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n")  
            f.write("            <label>%s</label>\n"% ("Plant"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Plant"))
            f.write("            <isDefault>true</isDefault>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Sandy"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Sandy"))
            f.write("            <includeBiomes>\n")
            f.write("              <li>AridShrubland</li>\n")
            f.write("              <li>Desert</li>\n")
            f.write("              <li>ExtremeDesert</li>\n")
            f.write("            </includeBiomes>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Trash"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Trash"))
            f.write("            <includeBiomes>\n")
            f.write("              <li>Tundra</li>\n")
            f.write("              <li>IceSheet</li>\n")
            f.write("              <li>SeaIce</li>\n")
            f.write("            </includeBiomes>\n")
            f.write("          </li>\n") 
            f.write("        </forms>\n")
            
        if pokemonDefName == "Wormadam":
            f.write("        <formChangerCondition>Fixed</formChangerCondition>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n")
            f.write("            <label>%s</label>\n"% ("Plant"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Plant"))
            f.write("          </li>\n")
            f.write("          <li>\n")      
            f.write("            <label>%s</label>\n"% ("Sandy"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Sandy"))
            f.write("          </li>\n")
            f.write("          <li>\n")
            f.write("            <label>%s</label>\n"% ("Trash"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Trash"))
            f.write("          </li>\n")
            f.write("        </forms>\n")
    
        if pokemonDefName == "Cherrim":
            f.write("        <formChangerCondition>Environnement</formChangerCondition>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Overcast"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Overcast"))
            f.write("            <isDefault>true</isDefault>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n")  
            f.write("            <timeOfDay>Day</timeOfDay>\n")
            f.write("            <includeWeathers>\n")
            f.write("              <li>Clear</li>\n")
            f.write("            </includeWeathers>\n")
            f.write("            <label>%s</label>\n"% ("Sunshine"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Sunshine"))
            f.write("          </li>\n")
            f.write("        </forms>\n")
        
        if pokemonDefName == "Shellos":
            f.write("        <formChangerCondition>Fixed</formChangerCondition>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n")
            f.write("            <label>%s</label>\n"% ("East"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("East"))
            f.write("          </li>\n")
            f.write("          <li>\n")
            f.write("            <label>%s</label>\n"% ("West"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("West"))
            f.write("          </li>\n")
            f.write("        </forms>\n")
            
        if pokemonDefName == "Gastrodon":
            f.write("        <formChangerCondition>Fixed</formChangerCondition>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n")
            f.write("            <label>%s</label>\n"% ("East"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("East"))
            f.write("          </li>\n")
            f.write("          <li>\n")
            f.write("            <label>%s</label>\n"% ("West"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("West"))
            f.write("          </li>\n")
            f.write("        </forms>\n")
            
        if pokemonDefName == "Rotom":
            f.write("        <formChangerCondition>Selectable</formChangerCondition>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n")  
            f.write("            <label>%s</label>\n"% ("Normal"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Normal"))
            f.write("            <isDefault>true</isDefault>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Heat"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Heat"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Wash"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Wash"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Frost"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Frost"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Fan"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Fan"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Mow"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Mow"))
            f.write("          </li>\n") 
            f.write("        </forms>\n")
            
        if pokemonDefName == "Giratina":
            f.write("        <formChangerCondition>Selectable</formChangerCondition>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n")  
            f.write("            <label>%s</label>\n"% ("Altered"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Altered"))
            f.write("            <isDefault>true</isDefault>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Origin"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Origin"))
            f.write("          </li>\n") 
            f.write("        </forms>\n")
            
        if pokemonDefName == "Shaymin":
            f.write("        <formChangerCondition>Selectable</formChangerCondition>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n")  
            f.write("            <label>%s</label>\n"% ("Land"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Land"))
            f.write("            <isDefault>true</isDefault>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Sky"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Sky"))
            f.write("          </li>\n") 
            f.write("        </forms>\n")
            
        if pokemonDefName == "Arceus":
            f.write("        <formChangerCondition>Selectable</formChangerCondition>\n")
            f.write("        <forms>\n")
            f.write("          <li>\n")  
            f.write("            <label>%s</label>\n"% ("Normal"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Normal"))
            f.write("            <isDefault>true</isDefault>\n")
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Fire"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Fire"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Water"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Water"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Electric"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Electric"))
            f.write("          </li>\n") 
            f.write("          <li>\n")  
            f.write("            <label>%s</label>\n"% ("Grass"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Grass"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Ice"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Ice"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Fighting"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Fighting"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Poison"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Poison"))
            f.write("          </li>\n") 
            f.write("          <li>\n")  
            f.write("            <label>%s</label>\n"% ("Ground"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Ground"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Flying"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Flying"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Psychic"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Psychic"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Bug"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Bug"))
            f.write("          </li>\n") 
            f.write("          <li>\n")  
            f.write("            <label>%s</label>\n"% ("Rock"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Rock"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Ghost"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Ghost"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Dragon"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Dragon"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Dark"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Dark"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Steel"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Steel"))
            f.write("          </li>\n") 
            f.write("          <li>\n") 
            f.write("            <label>%s</label>\n"% ("Fairy"))
            f.write("            <texPathKey>%s</texPathKey>\n"% ("Fairy"))
            f.write("          </li>\n") 
            f.write("        </forms>\n")
        
        f.write("      </li>\n")
        
        if eggGroup1 != "Undiscovered":
            if pokemonDefName != "Ditto":
                f.write('      <li Class="CompProperties_EggLayer">\n')
                if pokemonDefName == "Manaphy":                
                    f.write("        <eggFertilizedDef>PW_EggPhione</eggFertilizedDef>\n")
                else :
                    for indexOeuf, DexName in enumerate(defNameList):
                        ######################
                        if pokemonEvolutionLine[indexOeuf] == evolutionLine and pokemonEvolutionTier[indexOeuf] == 1:
                            f.write("        <eggFertilizedDef>PW_Egg%s</eggFertilizedDef>\n"% (DexName))
                            break
                f.write("        <eggFertilizationCountMax>1</eggFertilizationCountMax>\n")
                f.write("        <eggLayIntervalDays>%d</eggLayIntervalDays>\n"% (eggLayDays))
                f.write("        <eggProgressUnfertilizedMax>0</eggProgressUnfertilizedMax>\n")
                f.write("        <eggCountRange>1</eggCountRange>\n")
                if genderLess == 1:
                    f.write("        <eggLayFemaleOnly>false</eggLayFemaleOnly>\n")
                f.write("      </li>\n")   
            else :
                f.write('      <li Class="PokeWorld.CompProperties_DittoEggLayer">\n')
                f.write("        <eggFertilizationCountMax>1</eggFertilizationCountMax>\n")
                f.write("        <eggLayIntervalDays>%d</eggLayIntervalDays>\n"% (eggLayDays))
                f.write("        <eggProgressUnfertilizedMax>0</eggProgressUnfertilizedMax>\n")
                f.write("        <eggCountRange>1</eggCountRange>\n")
                f.write("      </li>\n") 
                
        if((type1 == "Fire" or type2 == "Fire") and not(type1 == "Ice" or type2 == "Ice")):
            f.write('      <li Class="CompProperties_HeatPusher">\n') 
            f.write("        <compClass>PokeWorld.CompPokemonHeatPusher</compClass>\n")
            f.write("        <heatPerSecond>%.2f</heatPerSecond>\n"%(totalStat / 200))
            f.write("        <heatPushMaxTemperature>32</heatPushMaxTemperature>\n")
            f.write("      </li>\n") 
            
        if((type1 == "Ice" or type2 == "Ice") and not(type1 == "Fire" or type2 == "Fire")):
            f.write('      <li Class="CompProperties_HeatPusher">\n') 
            f.write("        <compClass>PokeWorld.CompPokemonHeatPusher</compClass>\n")
            f.write("        <heatPerSecond>%.2f</heatPerSecond>\n"%(-totalStat / 200))
            f.write("        <heatPushMinTemperature>-8</heatPushMinTemperature>\n")
            f.write("      </li>\n")
        """
        if(type1 == "Electric" or type2 == "Electric"):
            f.write('      <li Class="CompProperties_Power">\n') 
            f.write("        <compClass>PokeWorld.CompPokemonPower</compClass>\n")
            f.write("        <basePowerConsumption>%.2f</basePowerConsumption>\n"%(-totalStat / 10))
            f.write("        <transmitsPower>true</transmitsPower>\n")
            f.write("      </li>\n")
        """      
        f.write("    </comps>\n")
    
    
        f.write("    <statBases>\n")
        f.write("      <MoveSpeed>%0.1f</MoveSpeed>\n"% (rimworldSpeed))
        f.write("      <MarketValue>%d</MarketValue>\n"% (marketValue))
        f.write("      <ComfyTemperatureMin>%d</ComfyTemperatureMin>\n"% (ComfyTemperatureMin))
        f.write("      <ComfyTemperatureMax>%d</ComfyTemperatureMax>\n"% (ComfyTemperatureMax))
        f.write("      <LeatherAmount>%d</LeatherAmount>\n"%(leatherAmount))
        f.write("      <PW_BaseXPYield>%d</PW_BaseXPYield>\n"% (expYield * expYieldMultiplier))
        f.write("      <ToxicSensitivity>%g</ToxicSensitivity>\n"% (toxicSensitivity))
        f.write("    </statBases>\n")
        f.write("    <inspectorTabs>\n")
        f.write("      <li>PokeWorld.ITab_Pawn_Moves</li>\n")
        f.write("    </inspectorTabs>\n")
    
        f.write("    <race>\n")
        f.write("      <body>%s</body>\n"% (body))
        if genderLess == 1:
            f.write("      <hasGenders>false</hasGenders>\n")
                
        if (isBaby or isLegendary or isFossil or isParticular):
            f.write("      <herdMigrationAllowed>false</herdMigrationAllowed>\n")
        f.write("      <petness>%.1f</petness>\n"% (petness))
        f.write("      <packAnimal>%s</packAnimal>\n"% (packAnimal))
        f.write("      <herdAnimal>%s</herdAnimal>\n"% (herdAnimal))
        f.write("      <baseBodySize>%.2f</baseBodySize>\n"% (baseBodySize))
        f.write("      <baseHungerRate>0.30</baseHungerRate>\n")
        f.write("      <baseHealthScale>%.2f</baseHealthScale>\n"% (baseHealthScale))
        f.write("      <foodType>OmnivoreAnimal, VegetarianRoughAnimal</foodType>\n")
        if i == 0:
            f.write("      <meatLabel>Pokémon meat</meatLabel>\n")
        elif i == 2:
            f.write("      <meatLabel>Pokémon meat</meatLabel>\n")
        elif baseBodySize < 0.7:
            f.write("      <useMeatFrom>PW_Bulbasaur</useMeatFrom>\n")
        else:
            f.write("      <useMeatFrom>PW_Venusaur</useMeatFrom>\n")
        f.write("      <leatherDef>%s</leatherDef>\n"%(leather))
        f.write("      <nameOnTameChance>1</nameOnTameChance>\n")
        f.write("      <trainability>Advanced</trainability>\n")
        f.write("      <trainableTags>\n")
        f.write("        <li>PW_Pokemon</li>\n")
        f.write("      </trainableTags>\n")
        f.write("      <wildness>%.1f</wildness>\n"%(wildness))
        f.write("      <manhunterOnDamageChance>%.2f</manhunterOnDamageChance>\n" %(manhunterOnDamageChance))
        f.write("      <manhunterOnTameFailChance>%.2f</manhunterOnTameFailChance>\n" %(manhunterOnTameFailChance))
        f.write("      <nuzzleMtbHours>12</nuzzleMtbHours>\n")
        f.write("      <lifeExpectancy>%d</lifeExpectancy>\n"%(ageExpectancy))
        f.write("      <lifeStageAges>\n")
        f.write("        <li>\n")
        f.write("          <def>AnimalAdult</def>\n")
        f.write("          <minAge>0</minAge>\n")
        f.write("          <soundWounded>Pawn_%s_Call</soundWounded>\n"% (pokemonDefName)) 
        f.write("          <soundDeath>Pawn_%s_Call</soundDeath>\n"% (pokemonDefName))
        f.write("          <soundCall>Pawn_%s_Call</soundCall>\n"% (pokemonDefName))
        f.write("          <soundAngry>Pawn_%s_Call</soundAngry>\n"% (pokemonDefName))
        f.write("        </li>\n")
        f.write("      </lifeStageAges>\n")
        f.write("      <soundMeleeHitPawn>Pawn_Melee_SmallScratch_HitPawn</soundMeleeHitPawn>\n")
        f.write("      <soundMeleeHitBuilding>Pawn_Melee_SmallScratch_HitBuilding</soundMeleeHitBuilding>\n")
        f.write("      <soundMeleeMiss>Pawn_Melee_SmallScratch_Miss</soundMeleeMiss>\n")
        f.write("    </race>\n")
        f.write("    <recipes>\n")   
        f.write("      <li>PW_AdministerPotion</li>\n")
        f.write("      <li>PW_AdministerHyperPotion</li>\n")
        f.write("      <li>PW_AdministerMaxPotion</li>\n")
        f.write("      <li>PW_AdministerHealPowder</li>\n")
        f.write("      <li>PW_GiveOneRareCandy</li>\n")
        f.write("      <li>PW_GiveFiveRareCandy</li>\n")
        """Adding recipe for item based evolutions if needed"""
        if (canEvolve == "true"):        
            evolutionCounter2=0
            for pokemonEvolvingFrom in evolvingFrom:
                if pokemonEvolvingFrom == pokemonDefName:
                    if evolRequirement[evolvingFrom.index(pokemonEvolvingFrom)+evolutionCounter2] == "item":
                        f.write("      <li>PW_Expose%s</li>\n"% (evolRequiredItem[evolvingFrom.index(pokemonEvolvingFrom)+evolutionCounter2]))
                    evolutionCounter2+=1
        f.write("    </recipes>\n")
        
        f.write("    <tradeTags>\n")
        for tag in tradeTags:
            f.write("      <li>%s</li>\n"% (tag))
        f.write("    </tradeTags>\n")
        f.write("  </ThingDef>\n")
        
        f.write('  <PawnKindDef ParentName="AnimalKindBase">\n')
        f.write("    <defName>PW_%s</defName>\n"% (pokemonDefName))
        f.write("    <label>%s</label>\n"% (pokemonFullName))
        f.write("    <labelPlural>%s</labelPlural>\n"% (pokemonFullName))
        f.write("    <race>PW_%s</race>\n"% (pokemonDefName))
        f.write("    <combatPower>%.0f</combatPower>\n"% (combatPower))
        
        if (isBaby or isLegendary or isFossil or isParticular):
            f.write("    <canArriveManhunter>false</canArriveManhunter>\n")
        
        f.write("    <ecoSystemWeight>%.2f</ecoSystemWeight>\n"% (ecoSystemWeight))
        if herdAnimal == "true":
            f.write("    <wildGroupSize>%d~%d</wildGroupSize>\n"% (wildGroupMin, wildGroupMax)) 
            
        f.write("    <lifeStages>\n")
        f.write("      <li>\n")
        
        f.write("        <bodyGraphicData>\n")
        if (femaleDifference == 1):
            f.write("          <texPath>%s</texPath>\n"% (texturePathMale))
        else:
            f.write("          <texPath>%s</texPath>\n"% (texturePath))
        f.write("          <drawSize>%.1f</drawSize>\n"% (drawSize))
        f.write("          <shadowData>\n")
        f.write("            <volume>(%.2f, %.2f, %.2f)</volume>\n"% (ShadowVolume1,ShadowVolume2,ShadowVolume3))
        f.write("            <offset>(%.2f, %.2f, %.2f)</offset>\n"% (shadowOffset_1,shadowOffset_2,shadowOffset_3))
        f.write("          </shadowData>\n")
        f.write("        </bodyGraphicData>\n")
        
        f.write("        <dessicatedBodyGraphicData>\n")
        f.write("          <texPath>%s</texPath>\n"% (texPathDessicated))
        f.write("          <drawSize>%.1f</drawSize>\n"% (dessicatedDrawSize))
        f.write("        </dessicatedBodyGraphicData>\n")
        
        if (femaleDifference == 1):
            
            f.write("        <femaleGraphicData>\n")
            f.write("          <texPath>%s</texPath>\n"% (texturePathFemale))
            f.write("          <drawSize>%.1f</drawSize>\n"% (drawSize))
            f.write("          <shadowData>\n")
            f.write("            <volume>(%.2f, %.2f, %.2f)</volume>\n"% (ShadowVolume1,ShadowVolume2,ShadowVolume3))
            f.write("            <offset>(%.2f, %.2f, %.2f)</offset>\n"% (shadowOffset_1,shadowOffset_2,shadowOffset_3))
            f.write("          </shadowData>\n")
            f.write("        </femaleGraphicData>\n")
    
        f.write("      </li>\n")
        f.write("    </lifeStages>\n")
        f.write("  </PawnKindDef>\n\n")
        
    f.write("</Defs>")           
    f.close()

if __name__ == '__main__':
    main()
