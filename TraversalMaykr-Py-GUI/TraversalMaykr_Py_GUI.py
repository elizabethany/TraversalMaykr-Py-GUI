import math
import chevron
import configparser

# Read config file to get operating mode, output files, templates, and other parameters
config = configparser.ConfigParser()
config.read("config.ini")

settings = config['Settings']
gameMode = int(settings['gameMode'])
clearSetting = int(settings['clearSetting'])
loopGeneration = bool(int(settings['loopGeneration']))
printToConsole = bool(int(settings['printToConsole']))

output1 = config['Output Files']['output1']
output2 = config['Output Files']['output2']

templates = config['Templates']
EternalTraversalTemplate = templates['EternalTraversal']

DEpmNormalViewHeight = float(config['Misc.']['Eternalpm_normalViewHeight'])
D16pmNormalViewHeight = float(config['Misc.']['2016pm_normalViewHeight'])

DEMonsterNameDictionary = {
    1  : "archvile",
    2  : "blood_maykr",
    3  : "carcass",
    4  : "doom_hunter",
    5  : "dread_knight",
    6  : "gargoyle",
    7  : "marauder",
    8  : "prowler",
    9  : "revenant",
    10 : "tyrant",
    11 : "whiplash",
    12 : "maykr_drone",
    13 : "mecha_zombie",
    14 : "arachnatron",
    15 : "wolf",
    16 : "zombie",
    17 : "baron",
    18 : "hell_knight",
    19 : "imp",
    20 : "mancubus",
    21 : "pinky",
    22 : "soldier"
}

DEMonsterTypeDictionary = {
    1  : "TRAVERSALMONSTERTYPE_ARCHVILE",
    2  : "TRAVERSALMONSTERTYPE_BLOOD_ANGEL",
    3  : "TRAVERSALMONSTERTYPE_CARCASS",
    4  : "TRAVERSALMONSTERTYPE_DOOM_HUNTER",
    5  : "TRAVERSALMONSTERTYPE_DREADKNIGHT",
    6  : "TRAVERSALMONSTERTYPE_GARGOYLE",
    7  : "TRAVERSALMONSTERTYPE_MARAUDER",
    8  : "TRAVERSALMONSTERTYPE_PROWLER",
    9  : "TRAVERSALMONSTERTYPE_REVENANT",
    10 : "TRAVERSALMONSTERTYPE_TYRANT",
    11 : "TRAVERSALMONSTERTYPE_WHIPLASH",
    12 : "TRAVERSALMONSTERTYPE_ZOMBIE_MAYKR",
    13 : "TRAVERSALMONSTERTYPE_ZOMBIE_T3",
    14 : "TRAVERSALMONSTERTYPE_ARACHNATRON",
    15 : "TRAVERSALMONSTERTYPE_MARAUDER_WOLF",
    16 : "TRAVERSALMONSTERTYPE_ZOMBIE",
    17 : "TRAVERSALMONSTERTYPE_BARON",
    18 : "TRAVERSALMONSTERTYPE_HELLKNIGHT",
    19 : "TRAVERSALMONSTERTYPE_IMP",
    20 : "TRAVERSALMONSTERTYPE_MANCUBUS",
    21 : "TRAVERSALMONSTERTYPE_PINKY",
    22 : "TRAVERSALMONSTERTYPE_HELLIFIED_SOLDIER"
}

DEMonsterPathDictionary = {
    1  : "archvile/traversal",
    2  : "bloodangel/traversal",
    3  : "carcass/traversal",
    4  : "doomhunter/traversal",
    5  : "dreadknight/traversal",
    6  : "gargoyle/traversal",
    7  : "marauder/traversals",
    8  : "prowler/traversal",
    9  : "revenant/traversals",
    10 : "tyrant/traversal",
    11 : "whiplash/traversal",
    12 : "zombie_maykr/traversal",
    13 : "zombie_tier_3/traversal",
    14 : "arachnotron/traversal",
    15 : "marauder_wolf/traversals",
    16 : "zombie_tier_1/traversal",
    17 : "baron/traversal",
    18 : "hellknight/traversal",
    19 : "imp/traversal",    
    20 : "mancubus_fire/traversal",
    21 : "pinky/traversal",
    22 : "soldier_blaster/traversal"
}

# Read text files to get anim sets
with open(r"Animations\Eternal\animationSet1.txt", 'r') as f:
    animationSet1 = [line.rstrip() for line in f]
    f.close()
with open(r"Animations\Eternal\animationSet2.txt", 'r') as f:
    animationSet2 = [line.rstrip() for line in f]
    f.close()
with open(r"Animations\Eternal\animationSet3.txt", 'r') as f:
    animationSet3 = [line.rstrip() for line in f]
    f.close()
with open(r"Animations\Eternal\animationSet4.txt", 'r') as f:
    animationSet4 = [line.rstrip() for line in f]
    f.close()
with open(r"Animations\Eternal\animationSet5.txt", 'r') as f:
    animationSet5 = [line.rstrip() for line in f]
    f.close()

DEAnimDictionary = {
    1: animationSet1,
    2: animationSet2,
    3: animationSet3,
    4: animationSet4,
    5: animationSet5
}

# DE idInfoTraversal
def generateDEInfoTraversal(
    ):
        
    entityNum = int(input("\nSet entity numbering start value: ")); # Set number to append at end of entity name

    while True:
        entityNumStr = str(entityNum).zfill(5) # Leading zeros padding
        
        # Get start and end coords
        startCoords = list(map(float, input("Starting coords: ").split()));
        endCoords = list(map(float, input("Destination coords: ").split()));

        monsterIndices = list(map(int, input("Monster types: ").split()));
        animIndex = int(input("Animation type: "))
        reciprocalTraversal = input("Generate reciprocal traversal? (Y/N): ")

        for i in range (0 , len(monsterIndices)):
            monsterIndex = monsterIndices[i]

            # Determine which animation set to use, based on the monster type
            if monsterIndex == 14: # arachnotron
                animSetIndex = 3
            elif monsterIndex == 15: # wolf
                animSetIndex = 4
            elif monsterIndex == 16: # zombie
                animSetIndex = 5
            elif monsterIndex >= 17 and monsterIndex <= 22: # baron, hell knight, imp, mancubus, pinky, soldier
                animSetIndex = 2
            else: # everything else
                animSetIndex = 1

            startCoords[2] -= DEpmNormalViewHeight
            endCoords[2] -= DEpmNormalViewHeight
            animation = DEAnimDictionary[animSetIndex][animIndex - 1]
            monsterName = DEMonsterNameDictionary[monsterIndex]
            monsterPath = DEMonsterPathDictionary[monsterIndex]
            monsterType = DEMonsterTypeDictionary[monsterIndex]
                
            # args to pass into the template
            args = {
                'entityNum': entityNumStr,
                'startX': startCoords[0],
                'startY': startCoords[1],
                'startZ': startCoords[2],
                'endX': endCoords[0] - startCoords[0],
                'endY': endCoords[1] - startCoords[1],
                'endZ': endCoords[2] - startCoords[2],
                'monsterName' : monsterName,
                'monsterPath' : monsterPath,
                'animation' : animation,
                'monsterType' : monsterType
            }
            reciprocalArgs = {
                'entityNum': entityNumStr + "_r",
                'startX': endCoords[0],
                'startY': endCoords[1],
                'startZ': endCoords[2],
                'endX': startCoords[0] - endCoords[0],
                'endY': startCoords[1] - endCoords[1],
                'endZ': startCoords[2] - endCoords[2],
                'monsterName' : monsterName,
                'monsterPath' : monsterPath,
                'animation' : animReverser(animation),
                'monsterType' : monsterType
            }
            
            # Open templates and pass through args, then write generated entity to file
            with open(EternalTraversalTemplate, 'r') as entityTemplate:
                generatedEntity1 = chevron.render(entityTemplate, args)
                printEntityToConsole(generatedEntity1) # print generated entity
                entityTemplate.close()
            writeStuffToFile(generatedEntity1, output1)
                       
            # Do the same for reciprocal traversal, if option was chosen
            if reciprocalTraversal == "Y" or reciprocalTraversal == "y":
                with open(EternalTraversalTemplate, 'r') as entityTemplate:
                    generatedEntity2 = chevron.render(entityTemplate, reciprocalArgs)
                    entityTemplate.close()
                printEntityToConsole(generatedEntity2) # print generated entity
                writeStuffToFile(generatedEntity2, output1)
        
        entityNum += 1; # increment by 1 after every generated entity

        if loopGeneration == False:
            break

# Check if the given animation is up or down, then return the reverse if applicable
def animReverser(
    animString
    ):

    if "up" in animString:
        return animString.replace("up", "down")
    elif "down" in animString:
        return animString.replace("down", "up")
    else:
        return animString

# Write generated entities to file
def writeStuffToFile(
    inputItem,
    outputFile
    ):

    # Open output txt and write spawn targets to file
    with open(outputFile, 'a') as output_File:
        output_File.write("\n" + inputItem)

# Clears the output files
def clearOutput(
    ):

    with open(output1, 'w') as outFile:
        outFile.write("")
        outFile.close()
    with open(output2, 'w') as outFile:
        outFile.write("")
        outFile.close()

# Dedicated function for printing generated entities to console
def printEntityToConsole(
    printThisItem
    ):

    if printToConsole == True:
        print(printThisItem)

def mainBody(
    ):

    if clearSetting == 0:
        # Ask user if they want to clear the output file, then clear it if the option was selected
        manualClear = input("\nClear the output files from previous sessions? (Y/N): ");
        if manualClear == 'y' or manualClear == 'Y':
            clearOutput()
    elif clearSetting == 2:
        clearOutput()

    generateDEInfoTraversal()

mainBody()