import math
import chevron
import configparser
from PyQt5 import QtCore, QtGui, QtWidgets

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
DETraversalChainTemplate = templates['EternalTraversalChainA']
DETraversalChainMidTemplate = templates['EternalTraversalChainB']

DEpmNormalViewHeight = float(config['Misc.']['Eternalpm_normalViewHeight'])
D16pmNormalViewHeight = float(config['Misc.']['2016pm_normalViewHeight'])

tempAnimList = []

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
with open(r"Animations\Eternal\animationSet2.txt", 'r') as f:
    animationSet2 = [line.rstrip() for line in f]
with open(r"Animations\Eternal\animationSet3.txt", 'r') as f:
    animationSet3 = [line.rstrip() for line in f]
with open(r"Animations\Eternal\animationSet4.txt", 'r') as f:
    animationSet4 = [line.rstrip() for line in f]
with open(r"Animations\Eternal\animationSet5.txt", 'r') as f:
    animationSet5 = [line.rstrip() for line in f]

DEAnimDictionary = {
    1: animationSet1,
    2: animationSet2,
    3: animationSet3,
    4: animationSet4,
    5: animationSet5
}

# DE: get info needed for idInfoTraversal via console input, then pass it on to be generated
def consoleInputDEInfoTraversal(
    ):
        
    entityNum = int(input("\nSet entity numbering start value: ")); # Set number to append at end of entity name

    while True:
        # Get start and end coords
        startCoords = stringToList(input("Starting coords: "), 'float')
        endCoords = stringToList(input("Destination coords: "), 'float')

        monsterIndices = list(map(int, input("Monster types: ").split()))
        animIndex = int(input("Animation type: "))
        reciprocalTraversal = yesNoToBool(input("Generate reciprocal traversal? (Y/N): "))

        generateDEInfoTraversal(entityNum, startCoords, endCoords, monsterIndices, animIndex, reciprocalTraversal)
        
        entityNum += 1; # increment by 1 after every generated entity

        if loopGeneration == False:
            break


# DE: Generate generateDEInfoTraversal
def generateDEInfoTraversal(
    entityNum,
    startCoords,
    endCoords,
    monsterIndices,
    animIndex,
    reciprocalTraversal
    ):

    entityNumStr = str(entityNum).zfill(5) # Leading zeros padding

    for i in range (0 , len(monsterIndices)):
        monsterIndex = monsterIndices[i]
    
        # Determine which animation set to use, based on the monster type
        if monsterIndex >= 1 and monsterIndex <= 13: # everything else
            animSetIndex = 1
        elif monsterIndex >= 17 and monsterIndex <= 22: # baron, hell knight, imp, mancubus, pinky, soldier
            animSetIndex = 2
        elif monsterIndex == 14: # arachnotron
            animSetIndex = 3
        elif monsterIndex == 15: # wolf
            animSetIndex = 4
        elif monsterIndex == 16: # zombie
            animSetIndex = 5
        
        startZ = startCoords[2] - DEpmNormalViewHeight
        endZ = endCoords[2] - DEpmNormalViewHeight
        animation = DEAnimDictionary[animSetIndex][animIndex - 1]
        monsterName = DEMonsterNameDictionary[monsterIndex]
        monsterPath = DEMonsterPathDictionary[monsterIndex]
        monsterType = DEMonsterTypeDictionary[monsterIndex]
            
        # args to pass into the template
        args = {
            'entityNum': entityNumStr,
            'startX': startCoords[0],
            'startY': startCoords[1],
            'startZ': startZ,
            'endX': endCoords[0] - startCoords[0],
            'endY': endCoords[1] - startCoords[1],
            'endZ': endZ - startZ,
            'monsterName' : monsterName,
            'monsterPath' : monsterPath,
            'animation' : animation,
            'monsterType' : monsterType
        }
        reciprocalArgs = {
            'entityNum': entityNumStr + "_r",
            'startX': endCoords[0],
            'startY': endCoords[1],
            'startZ': endZ,
            'endX': startCoords[0] - endCoords[0],
            'endY': startCoords[1] - endCoords[1],
            'endZ': startZ - endZ,
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
        if reciprocalTraversal:
            with open(EternalTraversalTemplate, 'r') as entityTemplate:
                generatedEntity2 = chevron.render(entityTemplate, reciprocalArgs)
                entityTemplate.close()
            printEntityToConsole(generatedEntity2) # print generated entity
            writeStuffToFile(generatedEntity2, output1)

# Get info needed for Traversal Chain via console
def consoleInputDETraversalChain(
    ):

    isOnCeiling = input("\nIs the midpoint on the ceiling? (Y/N): ")
    entityNum = int(input("Set entity numbering start value: ")); # Set number to append at end of entity name

    while True:
        midCoords = []
        traversalAnims = []

        startCoords = stringToList(input("Start coords: "), 'float')
        traversalAnims.append(int(input("Animation to next point: ")))

        midPoints = int((input ("Number of mid points: ")))
        for i in range (0, midPoints):
            midCoords.append(stringToList(input(f"Mid point {int(i + 1)} coords: "), 'float'))
            traversalAnims.append(int(input("Animation to next point: ")))
        
        endCoords = stringToList(input("End coords: "), 'float')

        monsterIndices = stringToList(input("Monster types: "), 'int')
        reciprocalTraversal = yesNoToBool(input("Generate reciprocal traversal? (Y/N): "))

        print(traversalAnims)

        generateDETraversalChain(entityNum, startCoords, midCoords, endCoords, isOnCeiling, midPoints, monsterIndices, traversalAnims, reciprocalTraversal)
        
        entityNum += 1

        if loopGeneration == False:
            break

# DE: Generate traversal chains
def generateDETraversalChain(
    entityNum,
    startCoords,
    midCoords,
    endCoords,
    isOnCeiling,
    midPoints,
    monsterIndices,
    traversalAnims,
    reciprocalTraversal
    ):
 
    entityNumStr = str(entityNum).zfill(3)
    
    if yesNoToBool(isOnCeiling):
        ceilingCompensation = 0.5;
    else:
        ceilingCompensation = 0 - DEpmNormalViewHeight
    
    for i in range (0 , len(monsterIndices)):
        monsterIndex = monsterIndices[i]
    
        # Determine which animation set to use, based on the monster type
        if monsterIndex >= 1 and monsterIndex <= 13: # everything else
            animSetIndex = 1
        elif monsterIndex >= 17 and monsterIndex <= 22: # baron, hell knight, imp, mancubus, pinky, soldier
            animSetIndex = 2
        elif monsterIndex == 14: # arachnotron
            animSetIndex = 3
        elif monsterIndex == 15: # wolf
            animSetIndex = 4
        elif monsterIndex == 16: # zombie
            animSetIndex = 5
        
        monsterName = DEMonsterNameDictionary[monsterIndex]
        monsterPath = DEMonsterPathDictionary[monsterIndex]
        monsterType = DEMonsterTypeDictionary[monsterIndex]

        # args to pass into the template for the start and end points
        startEndArgs = {
            'entityNum': entityNumStr,
            'startX': startCoords[0],
            'startY': startCoords[1],
            'startZ': startCoords[2] - DEpmNormalViewHeight,
            'endX': endCoords[0],
            'endY': endCoords[1],
            'endZ': endCoords[2] - DEpmNormalViewHeight,
            'monsterName' : monsterName,
            'monsterType' : monsterType,
            'animWeb' : monsterPathTruncater(monsterPath),
            'monsterPathStart' : monsterPath,
            'animation' : DEAnimDictionary[animSetIndex][traversalAnims[0] - 1] # traversalAnims[0] is the start anim; the contents of DEAnimDictionary start from 0
        }
        
        # Open templates and pass through args for star and end points, then write to file
        with open(DETraversalChainTemplate, 'r') as entityTemplate:
            entityTemplateOutput = chevron.render(entityTemplate, startEndArgs)
            printEntityToConsole(entityTemplateOutput) # print generated entity
        writeStuffToFile(entityTemplateOutput, output2)

        for i in range (0, midPoints):
            if i == midPoints - 1:
                nextPoint = f"mod_traversal_point_{monsterName}_end_{entityNumStr}"
            else:
                nextPoint = f"mod_traversal_chain_{monsterName}_mid_{intToChar(i+ 2)}_{entityNumStr}"

            # args to pass into the template for the current mid point
            midArgs = {
                'entityNum': entityNumStr,
                'midCoordX': midCoords[i][0],
                'midCoordY': midCoords[i][1],
                'midCoordZ': midCoords[i][2] + ceilingCompensation,
                'midLetter' : intToChar(i + 1),
                'monsterName' : monsterName,
                'monsterType' : monsterType,
                'animWeb' : monsterPathTruncater(monsterPath),
                'nextPoint' : nextPoint,
                'monsterPathMid' : monsterPath,
                'midAnimation' : DEAnimDictionary[animSetIndex][traversalAnims[i + 1] - 1] # add 1 as traversalAnims[0] is the start anim
            }

            with open(DETraversalChainMidTemplate, 'r') as entityTemplate:
                entityTemplateOutput = chevron.render(entityTemplate, midArgs)
                printEntityToConsole(entityTemplateOutput) # print generated entity
            writeStuffToFile(entityTemplateOutput, output2)

        # create reciprocal traversal chain if option was selected
        if reciprocalTraversal:
            startEndArgsReverse = {
                'entityNum': entityNumStr + "_r",
                'startX': endCoords[0],
                'startY': endCoords[1],
                'startZ': endCoords[2] - DEpmNormalViewHeight,
                'endX': startCoords[0],
                'endY': startCoords[1],
                'endZ': startCoords[2] - DEpmNormalViewHeight,
                'monsterName' : monsterName,
                'monsterType' : monsterType,
                'animWeb' : monsterPathTruncater(monsterPath),
                'monsterPathStart' : monsterPath,
                'animation' : animReverser(DEAnimDictionary[animSetIndex][traversalAnims[midPoints] - 1])
            }
            
            with open(DETraversalChainTemplate, 'r') as entityTemplate:
                entityTemplateOutput = chevron.render(entityTemplate, startEndArgsReverse)
                printEntityToConsole(entityTemplateOutput) # print generated entity
            writeStuffToFile(entityTemplateOutput, output2)

            midLetterReverse = int(1)

            for i in range (midPoints, 0, -1):
                if i == 1:
                    nextPointReverse = f"mod_traversal_point_{monsterName}_end_{entityNumStr}_r"
                else:
                    nextPointReverse = f"mod_traversal_chain_{monsterName}_mid_{intToChar(midLetterReverse+1)}_{entityNumStr}_r"

                midArgsReverse = {
                    'entityNum': entityNumStr + "_r",
                    'midCoordX': midCoords[i-1][0],
                    'midCoordY': midCoords[i-1][1],
                    'midCoordZ': midCoords[i-1][2] + ceilingCompensation,
                    'midLetter' : intToChar(midLetterReverse),
                    'monsterName' : monsterName,
                    'monsterType' : monsterType,
                    'animWeb' : monsterPathTruncater(monsterPath),
                    'nextPoint' : nextPointReverse,
                    'monsterPathMid' : monsterPath,
                    'midAnimation' : animReverser(DEAnimDictionary[animSetIndex][traversalAnims[i-1] - 1])
                }

                with open(DETraversalChainMidTemplate, 'r') as entityTemplate:
                    entityTemplateOutput = chevron.render(entityTemplate, midArgsReverse)
                    printEntityToConsole(entityTemplateOutput) # print generated entity
                writeStuffToFile(entityTemplateOutput, output2)

                midLetterReverse += 1


# Removes /traversal or /traversals from the given string
def monsterPathTruncater(
    monsterPath
    ):

    if "/traversal" in monsterPath:
        return monsterPath.replace("/traversal", "")
    elif "/traversals" in monsterPath:
        return monsterPath.replace("/traversals", "")

def intToChar(
    intInput
    ):

    return chr(ord('`')+intInput)

# pitch yaw roll to spawnOrientation matrix from Zandy
def sin_cos(deg):
    rad = math.radians(float(deg))
    return math.sin(rad), math.cos(rad)

def angle_to_mat3(
    x,
    y,
    z
    ): # yaw, pitch, roll

    sy, cy = sin_cos(x)
    sp, cp = sin_cos(y)
    sr, cr = sin_cos(z)

    return [
        cp * cy,
        cp * sy,
        -sp,
        sr * sp * cy + cr * -sy,
        sr * sp * sy + cr * cy,
        sr * cp,
        cr * sp * cy + -sr * sy,
        cr * sp * sy + -sr * cy,
        cr * cp,
    ]

# Function to round the given value to the nearest specified interval
def roundToInterval(
    inputValue,
    interval
    ):
    
    return round (inputValue / interval) * interval

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

# Clears the specified output file
def clearOutput(
    ):

    with open(output1, 'w') as outFile:
        outFile.write("")
    with open(output2, 'w') as outFile:
        outFile.write("")

def clearOutputDEInfo(
    ):

    with open(output1, 'w') as outFile:
        outFile.write("")

def clearOutputDEChain(
    ):

    with open(output2, 'w') as outFile:
        outFile.write("")

# Dedicated function for printing generated entities to console
def printEntityToConsole(
    printThisItem
    ):

    if printToConsole == True:
        print(printThisItem)

# Convert 'y' or 'n' input to a bool
def yesNoToBool(
    inputString
    ):

    if inputString == 'Y' or inputString == 'y':
        return True
    elif inputString == 'N' or inputString == 'n':
        return False

def stringToList(
    stringInput,
    listType
    ):

    types = {
        "float" : float,
        "int" : int
    }

    return list(map(types[listType], stringInput.split()))

# Main function for console input
def mainConsole(
    ):

    if clearSetting == 0:
        # Ask user if they want to clear the output file, then clear it if the option was selected
        manualClear = input("\nClear the output files from previous sessions? (Y/N): ");
        if manualClear == 'y' or manualClear == 'Y':
            clearOutput()
    elif clearSetting == 2:
        clearOutput()

    consoleInputDETraversalChain()

# Main Window
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(741, 712)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("praetor_dexterity_on_btP_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidgetTraversalEntityTypes = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidgetTraversalEntityTypes.setGeometry(QtCore.QRect(0, 0, 741, 711))
        self.tabWidgetTraversalEntityTypes.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidgetTraversalEntityTypes.setObjectName("tabWidgetTraversalEntityTypes")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.inputEndCoords = QtWidgets.QLineEdit(self.tab)
        self.inputEndCoords.setGeometry(QtCore.QRect(30, 130, 321, 31))
        self.inputEndCoords.setObjectName("inputEndCoords")
        self.buttonClearCoords = QtWidgets.QPushButton(self.tab)
        self.buttonClearCoords.setGeometry(QtCore.QRect(30, 520, 321, 61))
        self.buttonClearCoords.setObjectName("buttonClearCoords")
        self.labelAnimTypeHeader = QtWidgets.QLabel(self.tab)
        self.labelAnimTypeHeader.setGeometry(QtCore.QRect(50, 50, 161, 31))
        self.labelAnimTypeHeader.setLineWidth(0)
        self.labelAnimTypeHeader.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelAnimTypeHeader.setObjectName("labelAnimTypeHeader")
        self.selectReciprocalTraversal = QtWidgets.QCheckBox(self.tab)
        self.selectReciprocalTraversal.setGeometry(QtCore.QRect(480, 630, 151, 31))
        self.selectReciprocalTraversal.setObjectName("selectReciprocalTraversal")
        self.buttonGenerateTraversal = QtWidgets.QPushButton(self.tab)
        self.buttonGenerateTraversal.setGeometry(QtCore.QRect(490, 540, 131, 81))
        self.buttonGenerateTraversal.setObjectName("buttonGenerateTraversal")
        self.groupBoxMonsterSelect = QtWidgets.QGroupBox(self.tab)
        self.groupBoxMonsterSelect.setGeometry(QtCore.QRect(390, 80, 311, 441))
        self.groupBoxMonsterSelect.setTitle("")
        self.groupBoxMonsterSelect.setObjectName("groupBoxMonsterSelect")
        self.demonSelect_15 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_15.setGeometry(QtCore.QRect(220, 130, 81, 31))
        self.demonSelect_15.setObjectName("demonSelect_15")
        self.labelMonsterType_Heavy = QtWidgets.QLabel(self.groupBoxMonsterSelect)
        self.labelMonsterType_Heavy.setGeometry(QtCore.QRect(120, 10, 41, 31))
        self.labelMonsterType_Heavy.setLineWidth(0)
        self.labelMonsterType_Heavy.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterType_Heavy.setObjectName("labelMonsterType_Heavy")
        self.demonSelect_18 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_18.setGeometry(QtCore.QRect(120, 110, 81, 31))
        self.demonSelect_18.setObjectName("demonSelect_18")
        self.demonSelect_14 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_14.setGeometry(QtCore.QRect(120, 30, 81, 31))
        self.demonSelect_14.setObjectName("demonSelect_14")
        self.demonSelect_17 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_17.setGeometry(QtCore.QRect(220, 50, 81, 31))
        self.demonSelect_17.setObjectName("demonSelect_17")
        self.demonSelect_12 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_12.setGeometry(QtCore.QRect(10, 70, 81, 31))
        self.demonSelect_12.setObjectName("demonSelect_12")
        self.demonSelect_7 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_7.setGeometry(QtCore.QRect(220, 90, 81, 31))
        self.demonSelect_7.setObjectName("demonSelect_7")
        self.demonSelect_19 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_19.setGeometry(QtCore.QRect(10, 50, 81, 31))
        self.demonSelect_19.setObjectName("demonSelect_19")
        self.demonSelect_9 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_9.setGeometry(QtCore.QRect(120, 190, 81, 31))
        self.demonSelect_9.setObjectName("demonSelect_9")
        self.demonSelect_3 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_3.setGeometry(QtCore.QRect(120, 70, 81, 31))
        self.demonSelect_3.setObjectName("demonSelect_3")
        self.labelMonsterType_SHeavy = QtWidgets.QLabel(self.groupBoxMonsterSelect)
        self.labelMonsterType_SHeavy.setGeometry(QtCore.QRect(220, 10, 71, 31))
        self.labelMonsterType_SHeavy.setLineWidth(0)
        self.labelMonsterType_SHeavy.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterType_SHeavy.setObjectName("labelMonsterType_SHeavy")
        self.demonSelect_10 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_10.setGeometry(QtCore.QRect(220, 110, 81, 31))
        self.demonSelect_10.setObjectName("demonSelect_10")
        self.demonSelect_5 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_5.setGeometry(QtCore.QRect(120, 90, 81, 31))
        self.demonSelect_5.setObjectName("demonSelect_5")
        self.demonSelect_21 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_21.setGeometry(QtCore.QRect(120, 150, 81, 31))
        self.demonSelect_21.setObjectName("demonSelect_21")
        self.demonSelect_16 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_16.setGeometry(QtCore.QRect(10, 130, 81, 31))
        self.demonSelect_16.setObjectName("demonSelect_16")
        self.demonSelect_13 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_13.setGeometry(QtCore.QRect(10, 90, 91, 31))
        self.demonSelect_13.setObjectName("demonSelect_13")
        self.demonSelect_8 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_8.setGeometry(QtCore.QRect(120, 170, 81, 31))
        self.demonSelect_8.setObjectName("demonSelect_8")
        self.demonSelect_22 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_22.setGeometry(QtCore.QRect(10, 110, 81, 31))
        self.demonSelect_22.setObjectName("demonSelect_22")
        self.demonSelect_2 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_2.setGeometry(QtCore.QRect(120, 50, 81, 31))
        self.demonSelect_2.setObjectName("demonSelect_2")
        self.demonSelect_1 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_1.setGeometry(QtCore.QRect(220, 30, 81, 31))
        self.demonSelect_1.setObjectName("demonSelect_1")
        self.labelMonsterType_Fodder = QtWidgets.QLabel(self.groupBoxMonsterSelect)
        self.labelMonsterType_Fodder.setGeometry(QtCore.QRect(10, 10, 41, 31))
        self.labelMonsterType_Fodder.setLineWidth(0)
        self.labelMonsterType_Fodder.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterType_Fodder.setObjectName("labelMonsterType_Fodder")
        self.demonSelect_20 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_20.setGeometry(QtCore.QRect(120, 130, 81, 31))
        self.demonSelect_20.setObjectName("demonSelect_20")
        self.demonSelect_6 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_6.setGeometry(QtCore.QRect(10, 30, 81, 31))
        self.demonSelect_6.setObjectName("demonSelect_6")
        self.demonSelect_4 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_4.setGeometry(QtCore.QRect(220, 70, 81, 31))
        self.demonSelect_4.setObjectName("demonSelect_4")
        self.demonSelect_11 = QtWidgets.QCheckBox(self.groupBoxMonsterSelect)
        self.demonSelect_11.setGeometry(QtCore.QRect(120, 210, 81, 31))
        self.demonSelect_11.setObjectName("demonSelect_11")
        self.labelMonsterTypeHeader = QtWidgets.QLabel(self.groupBoxMonsterSelect)
        self.labelMonsterTypeHeader.setGeometry(QtCore.QRect(10, -10, 151, 31))
        self.labelMonsterTypeHeader.setLineWidth(0)
        self.labelMonsterTypeHeader.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterTypeHeader.setObjectName("labelMonsterTypeHeader")
        self.labelMonsterTypePresetInfo = QtWidgets.QLabel(self.groupBoxMonsterSelect)
        self.labelMonsterTypePresetInfo.setGeometry(QtCore.QRect(10, 250, 171, 31))
        self.labelMonsterTypePresetInfo.setLineWidth(0)
        self.labelMonsterTypePresetInfo.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterTypePresetInfo.setObjectName("labelMonsterTypePresetInfo")
        self.radioButtonPresetAInfo = QtWidgets.QRadioButton(self.groupBoxMonsterSelect)
        self.radioButtonPresetAInfo.setGeometry(QtCore.QRect(20, 360, 261, 17))
        self.radioButtonPresetAInfo.setObjectName("radioButtonPresetAInfo")
        self.radioButtonPresetSuperHeavyInfo = QtWidgets.QRadioButton(self.groupBoxMonsterSelect)
        self.radioButtonPresetSuperHeavyInfo.setGeometry(QtCore.QRect(20, 340, 82, 17))
        self.radioButtonPresetSuperHeavyInfo.setObjectName("radioButtonPresetSuperHeavyInfo")
        self.radioButtonPresetFodderInfo = QtWidgets.QRadioButton(self.groupBoxMonsterSelect)
        self.radioButtonPresetFodderInfo.setGeometry(QtCore.QRect(20, 300, 82, 17))
        self.radioButtonPresetFodderInfo.setObjectName("radioButtonPresetFodderInfo")
        self.radioButtonPresetCInfo = QtWidgets.QRadioButton(self.groupBoxMonsterSelect)
        self.radioButtonPresetCInfo.setGeometry(QtCore.QRect(20, 420, 261, 17))
        self.radioButtonPresetCInfo.setObjectName("radioButtonPresetCInfo")
        self.radioButtonPresetHeavyInfo = QtWidgets.QRadioButton(self.groupBoxMonsterSelect)
        self.radioButtonPresetHeavyInfo.setGeometry(QtCore.QRect(20, 320, 82, 17))
        self.radioButtonPresetHeavyInfo.setObjectName("radioButtonPresetHeavyInfo")
        self.radioButtonPresetNoneInfo = QtWidgets.QRadioButton(self.groupBoxMonsterSelect)
        self.radioButtonPresetNoneInfo.setGeometry(QtCore.QRect(20, 280, 82, 17))
        self.radioButtonPresetNoneInfo.setObjectName("radioButtonPresetNoneInfo")
        self.radioButtonPresetBInfo = QtWidgets.QRadioButton(self.groupBoxMonsterSelect)
        self.radioButtonPresetBInfo.setGeometry(QtCore.QRect(20, 400, 261, 17))
        self.radioButtonPresetBInfo.setObjectName("radioButtonPresetBInfo")
        self.radioButtonPresetDInfo = QtWidgets.QRadioButton(self.groupBoxMonsterSelect)
        self.radioButtonPresetDInfo.setGeometry(QtCore.QRect(20, 380, 261, 17))
        self.radioButtonPresetDInfo.setObjectName("radioButtonPresetDInfo")
        self.comboBoxAnimSelect = QtWidgets.QComboBox(self.tab)
        self.comboBoxAnimSelect.setGeometry(QtCore.QRect(50, 80, 191, 22))
        self.comboBoxAnimSelect.setMaxVisibleItems(45)
        self.comboBoxAnimSelect.setObjectName("comboBoxAnimSelect")
        self.inputStartCoords = QtWidgets.QLineEdit(self.tab)
        self.inputStartCoords.setGeometry(QtCore.QRect(30, 20, 321, 31))
        self.inputStartCoords.setObjectName("inputStartCoords")
        self.inputEntityNum = QtWidgets.QLineEdit(self.tab)
        self.inputEntityNum.setGeometry(QtCore.QRect(390, 20, 121, 31))
        self.inputEntityNum.setObjectName("inputEntityNum")
        self.buttonClearOutput = QtWidgets.QPushButton(self.tab)
        self.buttonClearOutput.setGeometry(QtCore.QRect(30, 600, 321, 61))
        self.buttonClearOutput.setObjectName("buttonClearOutput")
        self.groupBoxTraversalDelta = QtWidgets.QGroupBox(self.tab)
        self.groupBoxTraversalDelta.setGeometry(QtCore.QRect(50, 180, 131, 111))
        self.groupBoxTraversalDelta.setObjectName("groupBoxTraversalDelta")
        self.labelHorDelta = QtWidgets.QLabel(self.groupBoxTraversalDelta)
        self.labelHorDelta.setGeometry(QtCore.QRect(10, 70, 61, 16))
        self.labelHorDelta.setObjectName("labelHorDelta")
        self.labelVerDelta = QtWidgets.QLabel(self.groupBoxTraversalDelta)
        self.labelVerDelta.setGeometry(QtCore.QRect(10, 90, 41, 16))
        self.labelVerDelta.setObjectName("labelVerDelta")
        self.labelXDelta = QtWidgets.QLabel(self.groupBoxTraversalDelta)
        self.labelXDelta.setGeometry(QtCore.QRect(10, 20, 31, 16))
        self.labelXDelta.setObjectName("labelXDelta")
        self.labelYDelta = QtWidgets.QLabel(self.groupBoxTraversalDelta)
        self.labelYDelta.setGeometry(QtCore.QRect(10, 40, 31, 16))
        self.labelYDelta.setObjectName("labelYDelta")
        self.labelValXDelta = QtWidgets.QLabel(self.groupBoxTraversalDelta)
        self.labelValXDelta.setGeometry(QtCore.QRect(80, 20, 41, 16))
        self.labelValXDelta.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.labelValXDelta.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelValXDelta.setObjectName("labelValXDelta")
        self.labelValYDelta = QtWidgets.QLabel(self.groupBoxTraversalDelta)
        self.labelValYDelta.setGeometry(QtCore.QRect(80, 40, 41, 16))
        self.labelValYDelta.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelValYDelta.setObjectName("labelValYDelta")
        self.labelValHorDelta = QtWidgets.QLabel(self.groupBoxTraversalDelta)
        self.labelValHorDelta.setGeometry(QtCore.QRect(80, 70, 41, 16))
        self.labelValHorDelta.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelValHorDelta.setObjectName("labelValHorDelta")
        self.labelValVerDelta = QtWidgets.QLabel(self.groupBoxTraversalDelta)
        self.labelValVerDelta.setGeometry(QtCore.QRect(80, 90, 41, 16))
        self.labelValVerDelta.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelValVerDelta.setObjectName("labelValVerDelta")
        self.tabWidgetTraversalEntityTypes.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.buttonClearCoordsAndAnims = QtWidgets.QPushButton(self.tab_2)
        self.buttonClearCoordsAndAnims.setGeometry(QtCore.QRect(30, 520, 321, 61))
        self.buttonClearCoordsAndAnims.setObjectName("buttonClearCoordsAndAnims")
        self.inputEndCoordsChain = QtWidgets.QLineEdit(self.tab_2)
        self.inputEndCoordsChain.setGeometry(QtCore.QRect(30, 460, 321, 31))
        self.inputEndCoordsChain.setObjectName("inputEndCoordsChain")
        self.buttonClearOutputChain = QtWidgets.QPushButton(self.tab_2)
        self.buttonClearOutputChain.setGeometry(QtCore.QRect(30, 600, 321, 61))
        self.buttonClearOutputChain.setObjectName("buttonClearOutputChain")
        self.groupBoxMonsterSelect_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBoxMonsterSelect_3.setGeometry(QtCore.QRect(390, 80, 311, 441))
        self.groupBoxMonsterSelect_3.setTitle("")
        self.groupBoxMonsterSelect_3.setObjectName("groupBoxMonsterSelect_3")
        self.demonSelect_15_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_15_Chain.setGeometry(QtCore.QRect(220, 130, 81, 31))
        self.demonSelect_15_Chain.setObjectName("demonSelect_15_Chain")
        self.labelMonsterType_Heavy_4 = QtWidgets.QLabel(self.groupBoxMonsterSelect_3)
        self.labelMonsterType_Heavy_4.setGeometry(QtCore.QRect(120, 10, 41, 31))
        self.labelMonsterType_Heavy_4.setLineWidth(0)
        self.labelMonsterType_Heavy_4.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterType_Heavy_4.setObjectName("labelMonsterType_Heavy_4")
        self.demonSelect_18_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_18_Chain.setGeometry(QtCore.QRect(120, 110, 81, 31))
        self.demonSelect_18_Chain.setObjectName("demonSelect_18_Chain")
        self.demonSelect_14_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_14_Chain.setGeometry(QtCore.QRect(120, 30, 81, 31))
        self.demonSelect_14_Chain.setObjectName("demonSelect_14_Chain")
        self.demonSelect_17_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_17_Chain.setGeometry(QtCore.QRect(220, 50, 81, 31))
        self.demonSelect_17_Chain.setObjectName("demonSelect_17_Chain")
        self.demonSelect_12_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_12_Chain.setGeometry(QtCore.QRect(10, 70, 81, 31))
        self.demonSelect_12_Chain.setObjectName("demonSelect_12_Chain")
        self.demonSelect_7_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_7_Chain.setGeometry(QtCore.QRect(220, 90, 81, 31))
        self.demonSelect_7_Chain.setObjectName("demonSelect_7_Chain")
        self.demonSelect_19_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_19_Chain.setGeometry(QtCore.QRect(10, 50, 81, 31))
        self.demonSelect_19_Chain.setObjectName("demonSelect_19_Chain")
        self.demonSelect_9_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_9_Chain.setGeometry(QtCore.QRect(120, 190, 81, 31))
        self.demonSelect_9_Chain.setObjectName("demonSelect_9_Chain")
        self.demonSelect_3_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_3_Chain.setGeometry(QtCore.QRect(120, 70, 81, 31))
        self.demonSelect_3_Chain.setObjectName("demonSelect_3_Chain")
        self.labelMonsterType_SHeavy_4 = QtWidgets.QLabel(self.groupBoxMonsterSelect_3)
        self.labelMonsterType_SHeavy_4.setGeometry(QtCore.QRect(220, 10, 71, 31))
        self.labelMonsterType_SHeavy_4.setLineWidth(0)
        self.labelMonsterType_SHeavy_4.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterType_SHeavy_4.setObjectName("labelMonsterType_SHeavy_4")
        self.demonSelect_10_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_10_Chain.setGeometry(QtCore.QRect(220, 110, 81, 31))
        self.demonSelect_10_Chain.setObjectName("demonSelect_10_Chain")
        self.demonSelect_5_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_5_Chain.setGeometry(QtCore.QRect(120, 90, 81, 31))
        self.demonSelect_5_Chain.setObjectName("demonSelect_5_Chain")
        self.demonSelect_21_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_21_Chain.setGeometry(QtCore.QRect(120, 150, 81, 31))
        self.demonSelect_21_Chain.setObjectName("demonSelect_21_Chain")
        self.demonSelect_16_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_16_Chain.setGeometry(QtCore.QRect(10, 130, 81, 31))
        self.demonSelect_16_Chain.setObjectName("demonSelect_16_Chain")
        self.demonSelect_13_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_13_Chain.setGeometry(QtCore.QRect(10, 90, 91, 31))
        self.demonSelect_13_Chain.setObjectName("demonSelect_13_Chain")
        self.demonSelect_8_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_8_Chain.setGeometry(QtCore.QRect(120, 170, 81, 31))
        self.demonSelect_8_Chain.setObjectName("demonSelect_8_Chain")
        self.demonSelect_22_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_22_Chain.setGeometry(QtCore.QRect(10, 110, 81, 31))
        self.demonSelect_22_Chain.setObjectName("demonSelect_22_Chain")
        self.demonSelect_2_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_2_Chain.setGeometry(QtCore.QRect(120, 50, 81, 31))
        self.demonSelect_2_Chain.setObjectName("demonSelect_2_Chain")
        self.demonSelect_1_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_1_Chain.setGeometry(QtCore.QRect(220, 30, 81, 31))
        self.demonSelect_1_Chain.setObjectName("demonSelect_1_Chain")
        self.labelMonsterType_Fodder_4 = QtWidgets.QLabel(self.groupBoxMonsterSelect_3)
        self.labelMonsterType_Fodder_4.setGeometry(QtCore.QRect(10, 10, 41, 31))
        self.labelMonsterType_Fodder_4.setLineWidth(0)
        self.labelMonsterType_Fodder_4.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterType_Fodder_4.setObjectName("labelMonsterType_Fodder_4")
        self.demonSelect_20_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_20_Chain.setGeometry(QtCore.QRect(120, 130, 81, 31))
        self.demonSelect_20_Chain.setObjectName("demonSelect_20_Chain")
        self.demonSelect_6_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_6_Chain.setGeometry(QtCore.QRect(10, 30, 81, 31))
        self.demonSelect_6_Chain.setObjectName("demonSelect_6_Chain")
        self.demonSelect_4_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_4_Chain.setGeometry(QtCore.QRect(220, 70, 81, 31))
        self.demonSelect_4_Chain.setObjectName("demonSelect_4_Chain")
        self.demonSelect_11_Chain = QtWidgets.QCheckBox(self.groupBoxMonsterSelect_3)
        self.demonSelect_11_Chain.setGeometry(QtCore.QRect(120, 210, 81, 31))
        self.demonSelect_11_Chain.setObjectName("demonSelect_11_Chain")
        self.labelMonsterTypeHeader_3 = QtWidgets.QLabel(self.groupBoxMonsterSelect_3)
        self.labelMonsterTypeHeader_3.setGeometry(QtCore.QRect(10, -10, 151, 31))
        self.labelMonsterTypeHeader_3.setLineWidth(0)
        self.labelMonsterTypeHeader_3.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterTypeHeader_3.setObjectName("labelMonsterTypeHeader_3")
        self.labelMonsterTypePresetChain = QtWidgets.QLabel(self.groupBoxMonsterSelect_3)
        self.labelMonsterTypePresetChain.setGeometry(QtCore.QRect(10, 250, 171, 31))
        self.labelMonsterTypePresetChain.setLineWidth(0)
        self.labelMonsterTypePresetChain.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterTypePresetChain.setObjectName("labelMonsterTypePresetChain")
        self.radioButtonPresetFodderChain = QtWidgets.QRadioButton(self.groupBoxMonsterSelect_3)
        self.radioButtonPresetFodderChain.setGeometry(QtCore.QRect(20, 300, 82, 17))
        self.radioButtonPresetFodderChain.setObjectName("radioButtonPresetFodderChain")
        self.radioButtonPresetHeavyChain = QtWidgets.QRadioButton(self.groupBoxMonsterSelect_3)
        self.radioButtonPresetHeavyChain.setGeometry(QtCore.QRect(20, 320, 82, 17))
        self.radioButtonPresetHeavyChain.setObjectName("radioButtonPresetHeavyChain")
        self.radioButtonPresetSuperHeavyChain = QtWidgets.QRadioButton(self.groupBoxMonsterSelect_3)
        self.radioButtonPresetSuperHeavyChain.setGeometry(QtCore.QRect(20, 340, 82, 17))
        self.radioButtonPresetSuperHeavyChain.setObjectName("radioButtonPresetSuperHeavyChain")
        self.radioButtonPresetNoneChain = QtWidgets.QRadioButton(self.groupBoxMonsterSelect_3)
        self.radioButtonPresetNoneChain.setGeometry(QtCore.QRect(20, 280, 82, 17))
        self.radioButtonPresetNoneChain.setObjectName("radioButtonPresetNoneChain")
        self.radioButtonPresetAChain = QtWidgets.QRadioButton(self.groupBoxMonsterSelect_3)
        self.radioButtonPresetAChain.setGeometry(QtCore.QRect(20, 360, 261, 17))
        self.radioButtonPresetAChain.setObjectName("radioButtonPresetAChain")
        self.radioButtonPresetBChain = QtWidgets.QRadioButton(self.groupBoxMonsterSelect_3)
        self.radioButtonPresetBChain.setGeometry(QtCore.QRect(20, 400, 261, 17))
        self.radioButtonPresetBChain.setObjectName("radioButtonPresetBChain")
        self.radioButtonPresetCChain = QtWidgets.QRadioButton(self.groupBoxMonsterSelect_3)
        self.radioButtonPresetCChain.setGeometry(QtCore.QRect(20, 420, 261, 17))
        self.radioButtonPresetCChain.setObjectName("radioButtonPresetCChain")
        self.radioButtonPresetDChain = QtWidgets.QRadioButton(self.groupBoxMonsterSelect_3)
        self.radioButtonPresetDChain.setGeometry(QtCore.QRect(20, 380, 261, 17))
        self.radioButtonPresetDChain.setObjectName("radioButtonPresetDChain")
        self.inputStartCoordsChain = QtWidgets.QLineEdit(self.tab_2)
        self.inputStartCoordsChain.setGeometry(QtCore.QRect(30, 20, 321, 31))
        self.inputStartCoordsChain.setObjectName("inputStartCoordsChain")
        self.buttonGenerateTraversalChain = QtWidgets.QPushButton(self.tab_2)
        self.buttonGenerateTraversalChain.setGeometry(QtCore.QRect(490, 540, 131, 81))
        self.buttonGenerateTraversalChain.setObjectName("buttonGenerateTraversalChain")
        self.comboBoxAnimSelectStartChain = QtWidgets.QComboBox(self.tab_2)
        self.comboBoxAnimSelectStartChain.setGeometry(QtCore.QRect(50, 80, 191, 22))
        self.comboBoxAnimSelectStartChain.setMaxVisibleItems(45)
        self.comboBoxAnimSelectStartChain.setPlaceholderText("")
        self.comboBoxAnimSelectStartChain.setObjectName("comboBoxAnimSelectStartChain")
        self.selectReciprocalTraversalChain = QtWidgets.QCheckBox(self.tab_2)
        self.selectReciprocalTraversalChain.setGeometry(QtCore.QRect(470, 630, 181, 31))
        self.selectReciprocalTraversalChain.setObjectName("selectReciprocalTraversalChain")
        self.inputEntityNumChain = QtWidgets.QLineEdit(self.tab_2)
        self.inputEntityNumChain.setGeometry(QtCore.QRect(390, 20, 121, 31))
        self.inputEntityNumChain.setObjectName("inputEntityNumChain")
        self.inputMidCoordsChain = QtWidgets.QLineEdit(self.tab_2)
        self.inputMidCoordsChain.setGeometry(QtCore.QRect(30, 130, 321, 31))
        self.inputMidCoordsChain.setText("")
        self.inputMidCoordsChain.setObjectName("inputMidCoordsChain")
        self.labelStartAnimSelect = QtWidgets.QLabel(self.tab_2)
        self.labelStartAnimSelect.setGeometry(QtCore.QRect(50, 50, 161, 31))
        self.labelStartAnimSelect.setObjectName("labelStartAnimSelect")
        self.labelMidAnimSelect = QtWidgets.QLabel(self.tab_2)
        self.labelMidAnimSelect.setGeometry(QtCore.QRect(50, 160, 221, 31))
        self.labelMidAnimSelect.setObjectName("labelMidAnimSelect")
        self.comboBoxAnimSelectStartChain_2 = QtWidgets.QComboBox(self.tab_2)
        self.comboBoxAnimSelectStartChain_2.setGeometry(QtCore.QRect(50, 190, 191, 22))
        self.comboBoxAnimSelectStartChain_2.setMaxVisibleItems(45)
        self.comboBoxAnimSelectStartChain_2.setPlaceholderText("")
        self.comboBoxAnimSelectStartChain_2.setObjectName("comboBoxAnimSelectStartChain_2")
        self.pushButtonAddMidpoint = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonAddMidpoint.setGeometry(QtCore.QRect(280, 170, 71, 61))
        self.pushButtonAddMidpoint.setObjectName("pushButtonAddMidpoint")
        self.labelCurrentMidPoints = QtWidgets.QLabel(self.tab_2)
        self.labelCurrentMidPoints.setGeometry(QtCore.QRect(50, 210, 91, 31))
        self.labelCurrentMidPoints.setObjectName("labelCurrentMidPoints")
        self.listWidgetMidpoints = QtWidgets.QListWidget(self.tab_2)
        self.listWidgetMidpoints.setGeometry(QtCore.QRect(50, 240, 161, 192))
        self.listWidgetMidpoints.setObjectName("listWidgetMidpoints")
        self.listWidgetMidAnims = QtWidgets.QListWidget(self.tab_2)
        self.listWidgetMidAnims.setGeometry(QtCore.QRect(220, 240, 131, 192))
        self.listWidgetMidAnims.setObjectName("listWidgetMidAnims")
        self.tabWidgetTraversalEntityTypes.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # For DE Info Traversal
        self.radioButtonPresetNoneInfo.setChecked(True)
        self.comboBoxAnimSelect.addItems(DEAnimDictionary[1])
        self.buttonClearOutput.clicked.connect(clearOutputDEInfo)
        self.buttonClearCoords.clicked.connect(self.clearCoordsDEInfo)
        self.buttonGenerateTraversal.clicked.connect(self.getGUIInputsDEInfoTraversal)

        self.inputStartCoords.textChanged.connect(self.displayDeltaValues)
        self.inputEndCoords.textChanged.connect(self.displayDeltaValues)

        # For DE Traversal Chain
        self.radioButtonPresetNoneChain.setChecked(True)
        self.comboBoxAnimSelectStartChain.addItems(DEAnimDictionary[1])
        self.comboBoxAnimSelectStartChain_2.addItems(DEAnimDictionary[1])
        self.buttonClearOutputChain.clicked.connect(clearOutputDEChain)
        self.buttonClearCoordsAndAnims.clicked.connect(self.clearCoordsDEChain)
        self.pushButtonAddMidpoint.clicked.connect(self.addMidPointToList)
        self.buttonGenerateTraversalChain.clicked.connect(self.getGUIInputsDETraversalChain)

        self.retranslateUi(MainWindow)
        self.tabWidgetTraversalEntityTypes.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TraversalMaykr-Py-GUI v0.1"))
        self.inputEndCoords.setPlaceholderText(_translate("MainWindow", "Destination Coordiantes"))
        self.buttonClearCoords.setText(_translate("MainWindow", "Clear Coordinates"))
        self.labelAnimTypeHeader.setText(_translate("MainWindow", "Select animation to Destination"))
        self.selectReciprocalTraversal.setText(_translate("MainWindow", "Create reciprocal traversal"))
        self.buttonGenerateTraversal.setText(_translate("MainWindow", "Generate Traversals"))
        self.demonSelect_15.setText(_translate("MainWindow", "Wolf"))
        self.labelMonsterType_Heavy.setText(_translate("MainWindow", "Heavy"))
        self.demonSelect_18.setText(_translate("MainWindow", "Hell Knight"))
        self.demonSelect_14.setText(_translate("MainWindow", "Arachnotron"))
        self.demonSelect_17.setText(_translate("MainWindow", "Baron of Hell"))
        self.demonSelect_12.setText(_translate("MainWindow", "Maykr Drone"))
        self.demonSelect_7.setText(_translate("MainWindow", "Marauder"))
        self.demonSelect_19.setText(_translate("MainWindow", "Imp"))
        self.demonSelect_9.setText(_translate("MainWindow", "Revenant"))
        self.demonSelect_3.setText(_translate("MainWindow", "Carcass"))
        self.labelMonsterType_SHeavy.setText(_translate("MainWindow", "Super Heavy"))
        self.demonSelect_10.setText(_translate("MainWindow", "Tyrant"))
        self.demonSelect_5.setText(_translate("MainWindow", "Dread Knight"))
        self.demonSelect_21.setText(_translate("MainWindow", "Pinky"))
        self.demonSelect_16.setText(_translate("MainWindow", "Zombie"))
        self.demonSelect_13.setText(_translate("MainWindow", "Mecha Zombie"))
        self.demonSelect_8.setText(_translate("MainWindow", "Prowler"))
        self.demonSelect_22.setText(_translate("MainWindow", "Soldier"))
        self.demonSelect_2.setText(_translate("MainWindow", "Blood Maykr"))
        self.demonSelect_1.setText(_translate("MainWindow", "Archvile"))
        self.labelMonsterType_Fodder.setText(_translate("MainWindow", "Fodder"))
        self.demonSelect_20.setText(_translate("MainWindow", "Mancubus"))
        self.demonSelect_6.setText(_translate("MainWindow", "Gargoyle"))
        self.demonSelect_4.setText(_translate("MainWindow", "Doom Hunter"))
        self.demonSelect_11.setText(_translate("MainWindow", "Whiplash"))
        self.labelMonsterTypeHeader.setText(_translate("MainWindow", "__**Monster Type Selection**__"))
        self.labelMonsterTypePresetInfo.setText(_translate("MainWindow", "Presets (Ignores Above Selections)"))
        self.radioButtonPresetAInfo.setText(_translate("MainWindow", "Fodder + Carcass, Prowler, Whiplash, Marauder"))
        self.radioButtonPresetSuperHeavyInfo.setText(_translate("MainWindow", "Super Heavy"))
        self.radioButtonPresetFodderInfo.setText(_translate("MainWindow", "Fodder"))
        self.radioButtonPresetCInfo.setText(_translate("MainWindow", "All"))
        self.radioButtonPresetHeavyInfo.setText(_translate("MainWindow", "Heavy"))
        self.radioButtonPresetNoneInfo.setText(_translate("MainWindow", "None"))
        self.radioButtonPresetBInfo.setText(_translate("MainWindow", "All sans Tyrant"))
        self.radioButtonPresetDInfo.setText(_translate("MainWindow", "Thruster Assisted and Teleporting Demons"))
        self.inputStartCoords.setPlaceholderText(_translate("MainWindow", "Start Coordinates"))
        self.inputEntityNum.setPlaceholderText(_translate("MainWindow", "Starting Entity Number"))
        self.buttonClearOutput.setText(_translate("MainWindow", "Clear Output File"))
        self.groupBoxTraversalDelta.setTitle(_translate("MainWindow", "Delta Values"))
        self.labelHorDelta.setText(_translate("MainWindow", "Horizontal :"))
        self.labelVerDelta.setText(_translate("MainWindow", "Vertical :"))
        self.labelXDelta.setText(_translate("MainWindow", "X :"))
        self.labelYDelta.setText(_translate("MainWindow", "Y : "))
        self.labelValXDelta.setText(_translate("MainWindow", "0.0000"))
        self.labelValYDelta.setText(_translate("MainWindow", "0.0000"))
        self.labelValHorDelta.setText(_translate("MainWindow", "0.0000"))
        self.labelValVerDelta.setText(_translate("MainWindow", "0.0000"))
        self.tabWidgetTraversalEntityTypes.setTabText(self.tabWidgetTraversalEntityTypes.indexOf(self.tab), _translate("MainWindow", "Traversal Info"))
        self.buttonClearCoordsAndAnims.setText(_translate("MainWindow", "Clear Coordinates and Midpoints"))
        self.inputEndCoordsChain.setPlaceholderText(_translate("MainWindow", "Destination Coordiantes"))
        self.buttonClearOutputChain.setText(_translate("MainWindow", "Clear Output File"))
        self.demonSelect_15_Chain.setText(_translate("MainWindow", "Wolf"))
        self.labelMonsterType_Heavy_4.setText(_translate("MainWindow", "Heavy"))
        self.demonSelect_18_Chain.setText(_translate("MainWindow", "Hell Knight"))
        self.demonSelect_14_Chain.setText(_translate("MainWindow", "Arachnotron"))
        self.demonSelect_17_Chain.setText(_translate("MainWindow", "Baron of Hell"))
        self.demonSelect_12_Chain.setText(_translate("MainWindow", "Maykr Drone"))
        self.demonSelect_7_Chain.setText(_translate("MainWindow", "Marauder"))
        self.demonSelect_19_Chain.setText(_translate("MainWindow", "Imp"))
        self.demonSelect_9_Chain.setText(_translate("MainWindow", "Revenant"))
        self.demonSelect_3_Chain.setText(_translate("MainWindow", "Carcass"))
        self.labelMonsterType_SHeavy_4.setText(_translate("MainWindow", "Super Heavy"))
        self.demonSelect_10_Chain.setText(_translate("MainWindow", "Tyrant"))
        self.demonSelect_5_Chain.setText(_translate("MainWindow", "Dread Knight"))
        self.demonSelect_21_Chain.setText(_translate("MainWindow", "Pinky"))
        self.demonSelect_16_Chain.setText(_translate("MainWindow", "Zombie"))
        self.demonSelect_13_Chain.setText(_translate("MainWindow", "Mecha Zombie"))
        self.demonSelect_8_Chain.setText(_translate("MainWindow", "Prowler"))
        self.demonSelect_22_Chain.setText(_translate("MainWindow", "Soldier"))
        self.demonSelect_2_Chain.setText(_translate("MainWindow", "Blood Maykr"))
        self.demonSelect_1_Chain.setText(_translate("MainWindow", "Archvile"))
        self.labelMonsterType_Fodder_4.setText(_translate("MainWindow", "Fodder"))
        self.demonSelect_20_Chain.setText(_translate("MainWindow", "Mancubus"))
        self.demonSelect_6_Chain.setText(_translate("MainWindow", "Gargoyle"))
        self.demonSelect_4_Chain.setText(_translate("MainWindow", "Doom Hunter"))
        self.demonSelect_11_Chain.setText(_translate("MainWindow", "Whiplash"))
        self.labelMonsterTypeHeader_3.setText(_translate("MainWindow", "__**Monster Type Selection**__"))
        self.labelMonsterTypePresetChain.setText(_translate("MainWindow", "Presets (Ignores Above Selections)"))
        self.radioButtonPresetFodderChain.setText(_translate("MainWindow", "Fodder"))
        self.radioButtonPresetHeavyChain.setText(_translate("MainWindow", "Heavy"))
        self.radioButtonPresetSuperHeavyChain.setText(_translate("MainWindow", "Super Heavy"))
        self.radioButtonPresetNoneChain.setText(_translate("MainWindow", "None"))
        self.radioButtonPresetAChain.setText(_translate("MainWindow", "Fodder + Carcass, Prowler, Whiplash, Marauder"))
        self.radioButtonPresetBChain.setText(_translate("MainWindow", "All sans Tyrant"))
        self.radioButtonPresetCChain.setText(_translate("MainWindow", "All"))
        self.radioButtonPresetDChain.setText(_translate("MainWindow", "Thruster Assisted and Teleporting Demons"))
        self.inputStartCoordsChain.setPlaceholderText(_translate("MainWindow", "Start Coordinates"))
        self.buttonGenerateTraversalChain.setText(_translate("MainWindow", "Generate Traversal Chain"))
        self.selectReciprocalTraversalChain.setText(_translate("MainWindow", "Create reciprocal traversal chain"))
        self.inputEntityNumChain.setPlaceholderText(_translate("MainWindow", "Starting Entity Number"))
        self.inputMidCoordsChain.setPlaceholderText(_translate("MainWindow", "Midpoint Coordinates"))
        self.labelStartAnimSelect.setText(_translate("MainWindow", "Select animation to first midpoint"))
        self.labelMidAnimSelect.setText(_translate("MainWindow", "Select animation to next midpoint/destination"))
        self.pushButtonAddMidpoint.setText(_translate("MainWindow", "Add Midpoint"))
        self.labelCurrentMidPoints.setText(_translate("MainWindow", "Current Midpoints"))
        self.tabWidgetTraversalEntityTypes.setTabText(self.tabWidgetTraversalEntityTypes.indexOf(self.tab_2), _translate("MainWindow", "Traversal Chain"))

    def clearCoordsDEInfo(
        self
        ):
        
        self.inputStartCoords.clear()
        self.inputEndCoords.clear()

    def clearCoordsDEChain(
        self
        ):
        
        self.inputStartCoordsChain.clear()
        self.inputMidCoordsChain.clear()
        self.inputEndCoordsChain.clear()
        self.listWidgetMidpoints.clear()
        self.listWidgetMidAnims.clear()
        tempAnimList.clear()

    def getMonsterTypesDEInfoTraversal(
        self
        ):

        # Incredibly ugly, but it works. PLEASE replace this if possible!!!
        if self.radioButtonPresetNoneInfo.isChecked():
            tempList = []
            if self.demonSelect_1.isChecked():
            	tempList.append(1)
            if self.demonSelect_2.isChecked():
            	tempList.append(2)
            if self.demonSelect_3.isChecked():
            	tempList.append(3)
            if self.demonSelect_4.isChecked():
            	tempList.append(4)
            if self.demonSelect_5.isChecked():
            	tempList.append(5)
            if self.demonSelect_6.isChecked():
            	tempList.append(6)
            if self.demonSelect_7.isChecked():
            	tempList.append(7)
            if self.demonSelect_8.isChecked():
            	tempList.append(8)
            if self.demonSelect_9.isChecked():
            	tempList.append(9)
            if self.demonSelect_10.isChecked():
            	tempList.append(10)
            if self.demonSelect_11.isChecked():
            	tempList.append(11)
            if self.demonSelect_12.isChecked():
            	tempList.append(12)
            if self.demonSelect_13.isChecked():
            	tempList.append(13)
            if self.demonSelect_14.isChecked():
            	tempList.append(14)
            if self.demonSelect_15.isChecked():
            	tempList.append(15)
            if self.demonSelect_16.isChecked():
            	tempList.append(16)
            if self.demonSelect_17.isChecked():
            	tempList.append(17)
            if self.demonSelect_18.isChecked():
            	tempList.append(18)
            if self.demonSelect_19.isChecked():
            	tempList.append(19)
            if self.demonSelect_20.isChecked():
            	tempList.append(20)
            if self.demonSelect_21.isChecked():
            	tempList.append(21)
            if self.demonSelect_22.isChecked():
            	tempList.append(22)
            return tempList
        elif self.radioButtonPresetFodderInfo.isChecked(): # Fodder
                return list([6, 19, 12, 13, 22, 16])
        elif self.radioButtonPresetHeavyInfo.isChecked(): # Heavy
                return list([14, 2, 3, 5, 18, 20, 21, 8, 9, 11])
        elif self.radioButtonPresetSuperHeavyInfo.isChecked(): # Super Heavy
                return list([1, 17, 4, 7, 10, 15])
        elif self.radioButtonPresetAInfo.isChecked(): # Fodder + Carcass, Prowler, Whiplash, Marauder
                return list([6, 19, 12, 13, 22, 16, 3, 8, 11, 7])
        elif self.radioButtonPresetDInfo.isChecked(): # Maykr Drone, Soldier, Prowler, Revenant, Archvile, Doom Hunter
                return list([12, 22, 8, 9, 1, 4])
        elif self.radioButtonPresetBInfo.isChecked(): # All sans Tyrant
                return list([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
        elif self.radioButtonPresetCInfo.isChecked(): # All
                return list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])

    def getMonsterTypesDETraversalChain(
        self
        ):
        
        if self.radioButtonPresetNoneChain.isChecked():
            tempList = []
            if self.demonSelect_1_Chain.isChecked():
            	tempList.append(1)
            if self.demonSelect_2_Chain.isChecked():
            	tempList.append(2)
            if self.demonSelect_3_Chain.isChecked():
            	tempList.append(3)
            if self.demonSelect_4_Chain.isChecked():
            	tempList.append(4)
            if self.demonSelect_5_Chain.isChecked():
            	tempList.append(5)
            if self.demonSelect_6_Chain.isChecked():
            	tempList.append(6)
            if self.demonSelect_7_Chain.isChecked():
            	tempList.append(7)
            if self.demonSelect_8_Chain.isChecked():
            	tempList.append(8)
            if self.demonSelect_9_Chain.isChecked():
            	tempList.append(9)
            if self.demonSelect_10_Chain.isChecked():
            	tempList.append(10)
            if self.demonSelect_11_Chain.isChecked():
            	tempList.append(11)
            if self.demonSelect_12_Chain.isChecked():
            	tempList.append(12)
            if self.demonSelect_13_Chain.isChecked():
            	tempList.append(13)
            if self.demonSelect_14_Chain.isChecked():
            	tempList.append(14)
            if self.demonSelect_15_Chain.isChecked():
            	tempList.append(15)
            if self.demonSelect_16_Chain.isChecked():
            	tempList.append(16)
            if self.demonSelect_17_Chain.isChecked():
            	tempList.append(17)
            if self.demonSelect_18_Chain.isChecked():
            	tempList.append(18)
            if self.demonSelect_19_Chain.isChecked():
            	tempList.append(19)
            if self.demonSelect_20_Chain.isChecked():
            	tempList.append(20)
            if self.demonSelect_21_Chain.isChecked():
            	tempList.append(21)
            if self.demonSelect_22_Chain.isChecked():
            	tempList.append(22)
            return tempList
        elif self.radioButtonPresetFodderChain.isChecked(): # Fodder
                return list([6, 19, 12, 13, 22, 16])
        elif self.radioButtonPresetHeavyChain.isChecked(): # Heavy
                return list([14, 2, 3, 5, 18, 20, 21, 8, 9, 11])
        elif self.radioButtonPresetSuperHeavyChain.isChecked(): # Super Heavy
                return list([1, 17, 4, 7, 10, 15])
        elif self.radioButtonPresetAChain.isChecked(): # Fodder + Carcass, Prowler, Whiplash, Marauder
                return list([6, 19, 12, 13, 22, 16, 3, 8, 11, 7])
        elif self.radioButtonPresetDChain.isChecked(): # Maykr Drone, Soldier, Prowler, Revenant, Archvile, Doom Hunter
                return list([12, 22, 8, 9, 1, 4])
        elif self.radioButtonPresetBChain.isChecked(): # All sans Tyrant
                return list([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
        elif self.radioButtonPresetCChain.isChecked(): # All
                return list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])

    def displayDeltaValues(
        self
        ):

        startCoordsStr = self.inputStartCoords.text()
        endCoordsStr = self.inputEndCoords.text()
        startCoordsFloat = stringToList(startCoordsStr, 'float')
        endCoordsFloat = stringToList(endCoordsStr, 'float')

        if startCoordsStr == '' or endCoordsStr == '' or len(startCoordsFloat) < 3 or len(endCoordsFloat) < 3:
            self.labelValXDelta.setText("0.0000")
            self.labelValYDelta.setText("0.0000")
            self.labelValHorDelta.setText("0.0000")
            self.labelValVerDelta.setText("0.0000")
        else:
            deltaX = endCoordsFloat[0] - startCoordsFloat[0]
            deltaY = endCoordsFloat[1] - startCoordsFloat[1]
            deltaZ = endCoordsFloat[2] - startCoordsFloat[2]
            deltaHor = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
            self.labelValXDelta.setText(format(deltaX, '.4f'))
            self.labelValYDelta.setText(format(deltaY, '.4f'))
            self.labelValHorDelta.setText(format(deltaHor, '.4f'))
            self.labelValVerDelta.setText(format(deltaZ, '.4f'))

    def getGUIInputsDEInfoTraversal(
        self
        ):

        entityNum = int(self.inputEntityNum.text())
        startCoords = stringToList(self.inputStartCoords.text(), 'float')
        endCoords = stringToList(self.inputEndCoords.text(), 'float')
        monsterIndices = self.getMonsterTypesDEInfoTraversal()
        reciprocalTraversal = bool(self.selectReciprocalTraversal.isChecked())
        animIndex = int(self.comboBoxAnimSelect.currentIndex()) + 1

        # entityNum,startCoords,endCoords,monsterIndices,animIndex,reciprocalTraversal
        generateDEInfoTraversal(entityNum, startCoords, endCoords, monsterIndices, animIndex, reciprocalTraversal)
        self.inputEntityNum.setText(str(entityNum + 1))

    def addMidPointToList(
        self
        ):

        self.listWidgetMidpoints.addItem(self.inputMidCoordsChain.text())
        tempAnimList.append(self.comboBoxAnimSelectStartChain_2.currentIndex())
        self.listWidgetMidAnims.addItem(DEAnimDictionary[1][self.comboBoxAnimSelectStartChain_2.currentIndex()])
        self.inputMidCoordsChain.clear()

    def getGUIInputsDETraversalChain(
        self
        ):

        entityNum = int(self.inputEntityNumChain.text())
        startCoords = stringToList(self.inputStartCoordsChain.text(), 'float')

        midCoords = []
        for i in range (self.listWidgetMidpoints.count()):
            placeHolder = str(self.listWidgetMidpoints.item(i).text())
            midCoords.append(stringToList(placeHolder, 'float'))
        
        endCoords = stringToList(self.inputEndCoordsChain.text(), 'float')

        midPoints = len(tempAnimList)
        monsterIndices = self.getMonsterTypesDETraversalChain()
        tempAnimList.insert(0, int(self.comboBoxAnimSelectStartChain.currentIndex()) + 1)
        reciprocalTraversal = bool(self.selectReciprocalTraversalChain.isChecked())

        generateDETraversalChain(entityNum, startCoords, midCoords, endCoords, False, midPoints, monsterIndices, tempAnimList, reciprocalTraversal)
        #generateDETraversalChain(entityNum, startCoords, midCoords, endCoords, isOnCeiling, midPoints, monsterIndices, traversalAnims, reciprocalTraversal)

        self.clearCoordsDEChain()
        self.inputEntityNumChain.setText(str(entityNum + 1))

# if name main
if __name__ == "__main__":
    #mainConsole()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())