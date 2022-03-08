# -*- coding: utf-8 -*-

import pandas as pd
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
    defNameList = list(PokemonData.DefName)
    
    
    """Opening xml file where we write the Pokemon Defs"""
    #f = codecs.open("OutputFiles/Races_Pokemon.xml", "w", "utf-8")
    root = Element("Defs")
    
    for i, pokemonDefName in enumerate(defNameList):

        isLegendary = PokemonData.Legendary[i]  
        if(not isLegendary or pokemonDefName == "Phione"):
            continue

        pokemonFullName = PokemonData.Name[i]       
        pokemonFullName = FixNameIfNeeded(pokemonFullName, pokemonDefName)   

        QuestScriptDef = SubElement(root, "QuestScriptDef")
        SubElement(QuestScriptDef, "defName").text = "PW_Script_" + pokemonDefName
        SubElement(QuestScriptDef, "autoAccept").text = "true"
        SubElement(QuestScriptDef, "defaultChallengeRating").text = "4"
        SubElement(QuestScriptDef, "isRootSpecial").text = "true"
        SubElement(QuestScriptDef, "affectedByPoints").text = "false"
        
        questNameRules = SubElement(QuestScriptDef, "questNameRules")
        rulesStrings = SubElement(questNameRules, "rulesStrings")
        SubElement(rulesStrings, "li").text = "questName->Legendary Pokémon"
        
        questDescriptionRules = SubElement(QuestScriptDef, "questDescriptionRules")
        rulesStrings_2 = SubElement(questDescriptionRules, "rulesStrings")
        SubElement(rulesStrings_2, "li").text = "questDescription->Legendary Pokémon: " + pokemonFullName
        
        root_2 = SubElement(QuestScriptDef, "root", {"Class":"QuestNode_Sequence"})
        nodes = SubElement(root_2, "nodes")
        
        SubElement(nodes, "li", {"Class":"QuestNode_GetMap"})
        li_1 = SubElement(nodes, "li", {"Class":"QuestNode_Set"})
        SubElement(li_1, "name").text = "siteDistRange"
        SubElement(li_1, "value").text = "15~30"
        
        li_2 = SubElement(nodes, "li", {"Class":"QuestNode_GetSiteTile"})
        SubElement(li_2, "storeAs").text = "siteTile"
        SubElement(li_2, "preferCloserTiles").text = "false"
        
        li_3 = SubElement(nodes, "li", {"Class":"QuestNode_Set"})
        SubElement(li_3, "name").text = "siteThreatChance"
        SubElement(li_3, "value").text = "0"
        
        li_4 = SubElement(nodes, "li", {"Class":"QuestNode_Set"})
        SubElement(li_4, "name").text = "legendaryKind"
        SubElement(li_4, "value").text = "PW_" + pokemonDefName
        
        li_5 = SubElement(nodes, "li", {"Class":"QuestNode_GetSitePartDefsByTagsAndFaction"})
        SubElement(li_5, "storeAs").text = "sitePartDefs"
        sitePartsTags = SubElement(li_5, "sitePartsTags")
        li_6 = SubElement(sitePartsTags, "li")
        SubElement(li_6, "tag").text = "PW_LegendaryPokemon"
        
        li_7 = SubElement(nodes, "li", {"Class":"QuestNode_GetDefaultSitePartsParams"})
        SubElement(li_7, "tile").text = "$siteTile"
        SubElement(li_7, "sitePartDefs").text = "$sitePartDefs"
        SubElement(li_7, "storeSitePartsParamsAs").text = "sitePartsParams"
        
        li_8 = SubElement(nodes, "li", {"Class":"QuestNode_SubScript"})
        SubElement(li_8, "def").text = "Util_GenerateSite"
        parms = SubElement(li_8, "parms")
        SubElement(parms, "hiddenSitePartsPossible").text = "true"
        
        li_9 = SubElement(nodes, "li", {"Class":"QuestNode_SpawnWorldObjects"})
        SubElement(li_9, "worldObjects").text = "$site"
        
        li_10 = SubElement(nodes, "li", {"Class":"QuestNode_AddPawnReward"})
        SubElement(li_10, "pawn").text = "$legendaryPokemon"
        SubElement(li_10, "inSignalChoiceUsed").text = "site.MapGenerated"
        SubElement(li_10, "rewardDetailsHidden").text = "true"
        
        li_11 = SubElement(nodes, "li", {"Class":"QuestNode_NoWorldObject"})
        SubElement(li_11, "worldObject").text = "$site"
        SubElement(li_11, "node", {"Class":"QuestNode_End"})       
        
    with open('OutputFiles/Scripts.xml', 'wb') as f:
        indent(root, space = "  ")
        scripts = tostring(root, xml_declaration=True, encoding='utf8', method='xml')
        f.write(scripts)

if __name__ == "__main__":
    main()
