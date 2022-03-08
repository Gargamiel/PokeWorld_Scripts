# -*- coding: utf-8 -*-

import pandas as pd
import json
from lxml.etree import Element, SubElement, Comment, ElementTree, tostring, indent

def FixNameIfNeeded(fullName, defName):
    if(defName == "NidoranM"):
        return "Nidoran♂"
    if(defName == "NidoranF"):
        return "Nidoran♀"
    if(defName == "Flabebe"):
        return "Flabébé"
    return fullName

def GetCSVData(filePath):
    data = pd.read_csv(filePath, keep_default_na=False, encoding = "latin1")    
    return data

def main():  
    PokemonData = GetCSVData("Data/DataPokemon.csv")  
    with open("Data/LegendaryConditions.json", "r", encoding = "utf8") as f:
        Conditions = json.load(f)
    
    defNameList = list(PokemonData.DefName)
       
    root = Element("Defs")
      
    for i, pokemonDefName in enumerate(defNameList):

        isLegendary = PokemonData.Legendary[i]  
        if(not isLegendary or not pokemonDefName in Conditions):
            continue

        QuestConditionDef = SubElement(root, "PokeWorld.QuestConditionDef")
        SubElement(QuestConditionDef, "defName").text = "QuestCondition_" + pokemonDefName
        SubElement(QuestConditionDef, "questScriptDef").text = "PW_Script_" + pokemonDefName
        
        if("generationsRequirements" in Conditions[pokemonDefName]):
            generationsRequirements = SubElement(QuestConditionDef, "generationsRequirements")
            for requirement in Conditions[pokemonDefName]["generationsRequirements"]:
                li_1 = SubElement(generationsRequirements, "li")
                SubElement(li_1, "generation").text = requirement["generation"]
                if("minNoLegSeen" in requirement):
                    SubElement(li_1, "minNoLegSeen").text = requirement["minNoLegSeen"]
                if("minNoLegCaught" in requirement):
                    SubElement(li_1, "minNoLegCaught").text = requirement["minNoLegCaught"]
                if("minSeen" in requirement):
                    SubElement(li_1, "minSeen").text = requirement["minSeen"]
                if("minCaught" in requirement):
                    SubElement(li_1, "minCaught").text = requirement["minCaught"]
     
        if("requiredKindSeen" in Conditions[pokemonDefName]):
            requiredKindSeen = SubElement(QuestConditionDef, "requiredKindSeen")
            for req_1 in Conditions[pokemonDefName]["requiredKindSeen"]:
                SubElement(requiredKindSeen, "li").text = "PW_" + req_1
        
        if("requiredSeenMinCount" in Conditions[pokemonDefName]):
            SubElement(QuestConditionDef, "requiredSeenMinCount").text = Conditions[pokemonDefName]["requiredSeenMinCount"]
            
        if("requiredKindCaught" in Conditions[pokemonDefName]):
            requiredKindCaught = SubElement(QuestConditionDef, "requiredKindCaught")
            for req_2 in Conditions[pokemonDefName]["requiredKindCaught"]:
                SubElement(requiredKindCaught, "li").text = "PW_" + req_2
        
        if("requiredCaughtMinCount" in Conditions[pokemonDefName]):
            SubElement(QuestConditionDef, "requiredCaughtMinCount").text = Conditions[pokemonDefName]["requiredCaughtMinCount"]
        

        
    with open('OutputFiles/QuestConditionDef.xml', 'wb') as f:
        indent(root, space = "  ")
        conditions = tostring(root, xml_declaration=True, encoding='utf8', method='xml')
        f.write(conditions)

if __name__ == "__main__":
    main()
