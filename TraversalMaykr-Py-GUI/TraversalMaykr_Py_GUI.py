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
        startCoords = formatCoords(input("Starting coords: "))
        endCoords = formatCoords(input("Destination coords: "))

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

    consoleInputDEInfoTraversal()

#if __name__ == '__main__':
#    mainConsole()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(622, 587)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.selectReciprocalTraversal = QtWidgets.QCheckBox(self.centralwidget)
        self.selectReciprocalTraversal.setGeometry(QtCore.QRect(340, 500, 151, 31))
        self.selectReciprocalTraversal.setObjectName("selectReciprocalTraversal")
        self.buttonGenerateTraversal = QtWidgets.QPushButton(self.centralwidget)
        self.buttonGenerateTraversal.setGeometry(QtCore.QRect(190, 470, 131, 81))
        self.buttonGenerateTraversal.setObjectName("buttonGenerateTraversal")
        self.buttonClearOutput = QtWidgets.QPushButton(self.centralwidget)
        self.buttonClearOutput.setGeometry(QtCore.QRect(470, 40, 101, 61))
        self.buttonClearOutput.setObjectName("buttonClearOutput")
        self.inputStartCoords = QtWidgets.QLineEdit(self.centralwidget)
        self.inputStartCoords.setGeometry(QtCore.QRect(50, 40, 291, 31))
        self.inputStartCoords.setObjectName("inputStartCoords")
        self.inputEndCoords = QtWidgets.QLineEdit(self.centralwidget)
        self.inputEndCoords.setGeometry(QtCore.QRect(50, 80, 291, 31))
        self.inputEndCoords.setObjectName("inputEndCoords")
        self.inputEntityNum = QtWidgets.QLineEdit(self.centralwidget)
        self.inputEntityNum.setGeometry(QtCore.QRect(360, 40, 81, 31))
        self.inputEntityNum.setObjectName("inputEntityNum")
        self.buttonClearCoords = QtWidgets.QPushButton(self.centralwidget)
        self.buttonClearCoords.setGeometry(QtCore.QRect(50, 120, 111, 31))
        self.buttonClearCoords.setObjectName("buttonClearCoords")
        self.comboBoxAnimSelect = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxAnimSelect.setGeometry(QtCore.QRect(400, 200, 191, 22))
        self.comboBoxAnimSelect.setMaxVisibleItems(45)
        self.comboBoxAnimSelect.setObjectName("comboBoxAnimSelect")
        self.comboBoxAnimSelect.addItems(DEAnimDictionary[1])
        self.labelAnimTypeHeader = QtWidgets.QLabel(self.centralwidget)
        self.labelAnimTypeHeader.setGeometry(QtCore.QRect(400, 170, 151, 31))
        self.labelAnimTypeHeader.setLineWidth(0)
        self.labelAnimTypeHeader.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelAnimTypeHeader.setObjectName("labelAnimTypeHeader")
        self.groupBoxMonsterSelect = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxMonsterSelect.setGeometry(QtCore.QRect(40, 180, 311, 261))
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
        self.labelMonsterTypeHeader = QtWidgets.QLabel(self.centralwidget)
        self.labelMonsterTypeHeader.setGeometry(QtCore.QRect(50, 170, 151, 31))
        self.labelMonsterTypeHeader.setLineWidth(0)
        self.labelMonsterTypeHeader.setTextFormat(QtCore.Qt.MarkdownText)
        self.labelMonsterTypeHeader.setObjectName("labelMonsterTypeHeader")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.buttonClearOutput.clicked.connect(clearOutput)
        self.buttonClearCoords.clicked.connect(self.clearCoords)
        self.buttonGenerateTraversal.clicked.connect(self.getGUIInputs)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TraversalMaykr-Py-GUI v0.1"))
        self.selectReciprocalTraversal.setText(_translate("MainWindow", "Create reciprocal traversal"))
        self.buttonGenerateTraversal.setText(_translate("MainWindow", "Generate Traversals"))
        self.buttonClearOutput.setText(_translate("MainWindow", "Clear output files"))
        self.inputStartCoords.setPlaceholderText(_translate("MainWindow", "Start Coordinates"))
        self.inputEndCoords.setPlaceholderText(_translate("MainWindow", "Destination Coordiantes"))
        self.inputEntityNum.setPlaceholderText(_translate("MainWindow", "Entity Number"))
        self.buttonClearCoords.setText(_translate("MainWindow", "Clear coordinates"))
        self.labelAnimTypeHeader.setText(_translate("MainWindow", "__**Animation Type Selection**__"))
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

    def clearCoords(
        self
        ):
        
        self.inputStartCoords.clear()
        self.inputEndCoords.clear()

    def getMonsterTypes(
        self
        ):

        # Incredibly ugly, but it works. PLEASE replace this if possible!!!
        tempStr = ""
        if self.demonSelect_1.isChecked():
	        tempStr += " 1"
        if self.demonSelect_2.isChecked():
        	tempStr += " 2"
        if self.demonSelect_3.isChecked():
        	tempStr += " 3"
        if self.demonSelect_4.isChecked():
        	tempStr += " 4"
        if self.demonSelect_5.isChecked():
        	tempStr += " 5"
        if self.demonSelect_6.isChecked():
        	tempStr += " 6"
        if self.demonSelect_7.isChecked():
        	tempStr += " 7"
        if self.demonSelect_8.isChecked():
        	tempStr += " 8"
        if self.demonSelect_9.isChecked():
        	tempStr += " 9"
        if self.demonSelect_10.isChecked():
        	tempStr += " 10"
        if self.demonSelect_11.isChecked():
        	tempStr += " 11"
        if self.demonSelect_12.isChecked():
        	tempStr += " 12"
        if self.demonSelect_13.isChecked():
        	tempStr += " 13"
        if self.demonSelect_14.isChecked():
        	tempStr += " 14"
        if self.demonSelect_15.isChecked():
        	tempStr += " 15"
        if self.demonSelect_16.isChecked():
        	tempStr += " 16"
        if self.demonSelect_17.isChecked():
        	tempStr += " 17"
        if self.demonSelect_18.isChecked():
        	tempStr += " 18"
        if self.demonSelect_19.isChecked():
        	tempStr += " 19"
        if self.demonSelect_20.isChecked():
        	tempStr += " 20"
        if self.demonSelect_21.isChecked():
        	tempStr += " 21"
        if self.demonSelect_22.isChecked():
        	tempStr += " 22"

        return stringToList(tempStr, 'int')

    def getGUIInputs(
        self
        ):

        entityNum = int(self.inputEntityNum.text())
        startCoords = stringToList(self.inputStartCoords.text(), 'float')
        endCoords = stringToList(self.inputEndCoords.text(), 'float')
        monsterIndices = self.getMonsterTypes()
        reciprocalTraversal = bool(self.selectReciprocalTraversal.isChecked())
        animIndex = int(self.comboBoxAnimSelect.currentIndex()) + 1

        # entityNum,startCoords,endCoords,monsterIndices,animIndex,reciprocalTraversal
        generateDEInfoTraversal(entityNum, startCoords, endCoords, monsterIndices, animIndex, reciprocalTraversal)
        self.inputEntityNum.setText(str(entityNum + 1))


if __name__ == "__main__":
    #mainConsole()
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())