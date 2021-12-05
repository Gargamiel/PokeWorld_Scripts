import requests, json, time, re
from lxml import html

with open("Data/DataMoves.json", "r", encoding = "utf8") as f:
	MoveData = json.load(f)

with open("Data/legal_moves.txt", "r") as f:
	legalMoves = f.read().split("\n")[:-1]

lowerMoveset  = [name for name in MoveData.keys() if MoveData[name]["dexNumber"] < 808]
higherMoveset = [name for name in MoveData.keys() if MoveData[name]["dexNumber"] > 807]

def getMoveData(POKEMON):
	if POKEMON in lowerMoveset:
		a = requests.get(f"https://bulbapedia.bulbagarden.net/wiki/{POKEMON}_(Pokémon)/Generation_VII_learnset").text
	else:
		a = requests.get(f"https://bulbapedia.bulbagarden.net/wiki/{POKEMON}_(Pokémon)").text
	print(POKEMON)
	time.sleep(.1)

	parsed = html.fromstring(a)

	tableList = parsed.xpath('//table[@class="roundy"]')

	for table in tableList:
		if table.xpath("./tbody/tr/td/table/tbody/tr/th[2]/table/tbody/tr/th/small/text()") == ['Other\xa0generations:']:
			levelUpTable = table
			break

	moveList = []

	for move in levelUpTable.xpath("./tbody/tr[2]/td/table/tbody/tr")[1:]:
		try:
			learnLvl = move.xpath("./td[1]/text()")[0].replace("\n", "")
			if learnLvl != '':
				moveName = move.xpath("./td[2]//a/span/text()")[0]
				moveName = moveName.replace(" ", "")
				moveList.append((learnLvl, moveName))
		
		except IndexError:
			learnLvl = move.xpath("./td[2]/text()")[0].replace("\n", "")
			if re.findall("[0-9]", learnLvl) != []:
				moveName = move.xpath("./td[3]//a/span/text()")[0]
				moveName = moveName.replace(" ", "")
				moveList.append((learnLvl, moveName))

	return(moveList)


for pkmn in lowerMoveset + higherMoveset:
	MoveData[pkmn]["moves"] = []
	for learnLvl, moveName in getMoveData(pkmn):
		if moveName in legalMoves:
			moveDict = {
				"moveName" : moveName,
				"learnLvl" : learnLvl
			}
			MoveData[pkmn]["moves"].append(moveDict)

with open("Data/DataMoves.json", 'w+', encoding = "utf8") as f:
	json.dump(MoveData, f)