import random
import pandas as pd
from functools import reduce

class BoosterFactory:
    def __init__(self, slots):
        self.slots = slots

    def generateBooster(self):
        booster = Booster([])
        for slot in self.slots:
            choice = slot.rollSlot()
            booster.addChoice(choice)
        return booster
    def getPandasColumns(self):
        returnList = []
        for slot in self.slots:
            returnList.append(slot.name)
            returnList.append(slot.name + "_score")
        returnList.append("Summation_Score")
        returnList.append("Product_Score")
        return returnList


class Booster:
    def __init__(self, choices):
        self.chosenSlots = choices
    def addChoice(self, choice):
        self.chosenSlots.append(choice)
    def getScoreMultiplicative(self):
        return reduce((lambda x, y: x * y), [z[1] for z in self.chosenSlots])
    def getScoreAdditive(self):
        return sum(choice[1] for choice in self.chosenSlots)
    def getRow(self):
        returnList = []
        for choice in self.chosenSlots:
            returnList.extend(list(choice))
        returnList.append(self.getScoreAdditive())
        returnList.append(self.getScoreMultiplicative())
        return returnList
    def __str__(self):
        return str(self.chosenSlots)
    def __repr__(self):
        return str(self)

class Slot:
    
    def __init__(self, name,probabilities,choiceNames):
        self.name = name
        self.choices = []
        totalProb = 0
        for prob,choiceName in zip(probabilities[::-1], choiceNames[::-1]): #Note, go in reverse order to handle "most preferable" first
            choice = Choice(choiceName, totalProb, prob)
            self.choices.append(choice)
            totalProb = round(totalProb + prob,4)
    
    def rollSlot(self):
        randFloat = random.random()
        for choice in self.choices:
            if randFloat <= choice.prob:
                return (choice.name, choice.score)
    def __str__(self):
        return "{}: {}".format(self.name, self.choices)
    def __repr__(self):
        return str(self)

class Choice:
    name = ""
    prob = 0.0
    score = 0
    def __init__(self, name, prevProb, prob):
        self.name = name
        totalProb = prevProb + prob
        self.prob = round(totalProb,4)
        self.score = round(1 / totalProb,4)
    def getCellOutput(self):
        return [self.name, self.score]
    def __str__(self):
        return "{}: Score {}".format(self.name,self.score)
    def __repr__(self):
        return str(self)

# Slot 0 art slot: 0.05 to get gold signature 0.95 ow
# Slot 1 land slot: 0.15 to get foil, 0.85 ow
# Slot 2 commons and uncommons: 6un 0.02, 5un 0.035, 4un 0.07, 3un 0.125, 2un 0.4, 1un 0.35
# Slot 3 wildcards: 0.0003 mm, 0.0037 mr, 0.012 rr,0.0058 mu, 0.0236 mc, 0.0372 ru, 0.1514 rc,0.031 uu,0.245 uc,0.49 cc
# Slot 4 rare slot: 0.135 m, 0.865 r
# Slot 5 ad/list card: 0.25 the list, 0.75 ad
slot0 = Slot("Art slot",[0.95,0.05],['Normal Art Card','Gold Signed Art Card'])
slot1 = Slot("Land slot",[0.85,0.15],['Normal land','Foil land'])
slot2 = Slot("Theme slot",[0.35,0.4,0.125,0.07,0.035,0.02],['1 uncommon 5 commons','2 uncommons 4 commons','3 uncommons 3 commons','4 uncommons 2 commons','5 uncommons 1 commons','6 uncommons'])
slot3 = Slot("Wildcard slot",[0.49,0.245,0.031,0.1514,0.0372,0.0236,0.0058,0.012,0.0037,0.0003],['common common','uncommon common','uncommon uncommon','rare common','rare uncommon','mythic common','mythic uncommon','rare rare', 'mythic rare', 'mythic mythic'])
slot4 = Slot("Rare slot",[0.865,0.135],['rare','mythic'])
slot5 = Slot("Ad slot",[0.75,0.25],['Ad card','The List card'])

print(slot0)
print(slot1)
print(slot2)
print(slot3)
print(slot4)
print(slot5)

generator = BoosterFactory([slot0,slot1,slot2,slot3,slot4,slot5])
dataFrame = pd.DataFrame(columns=generator.getPandasColumns())

for i in range(100000):
    if i % 100 == 0:
        print("iteration {}".format(i))
    booster = generator.generateBooster()
    dataFrame.loc[i] = booster.getRow()
    # print(booster.getRow())
print(dataFrame['Summation_Score'].describe())
print(dataFrame['Product_Score'].describe())
dataFrame.to_csv("output.csv")