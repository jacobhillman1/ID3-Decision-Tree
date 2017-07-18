import json
import math


# Returns a dict containing each variable as a key, and the number of times it appears in the data set as the its value
def calculateValueFrequencies(dataSet, targetAttr):
    valueFrequencies = {}

    for record in dataSet:
        if record[targetAttr] in valueFrequencies:
            valueFrequencies[record[targetAttr]] += 1.0
        else:
            valueFrequencies[record[targetAttr]] = 1.0

    return valueFrequencies


def calculateEntropy(dataSet, targetAttr):
    valueFrequencies = calculateValueFrequencies(dataSet, targetAttr)

    dataEntropy = 0.0
    for value in valueFrequencies:
        probability = valueFrequencies[value] / len(dataSet)
        dataEntropy += -(probability * math.log(probability, 2))

    return dataEntropy


def calculateInformationGain(dataSet, attr, targetAttr):
    valueFrequencies = calculateValueFrequencies(dataSet, attr)

    subsetEntropy = 0.0
    for value in valueFrequencies.keys():
        dataSubset = [record for record in dataSet if record[attr] == value]
        proportion = valueFrequencies[value] / len(dataSet)
        subsetEntropy += proportion * calculateEntropy(dataSubset, targetAttr)

    return(calculateEntropy(dataSet, targetAttr) - subsetEntropy)


# Return the attribute that results in the highest information gain
def chooseBestAttribute(dataSet, inputAttributes, targetAttr):
    # Delete the target attribute
    newAttributes = inputAttributes
    if targetAttr in newAttributes:
        newAttributes.remove(targetAttr)

    highestInformationGain = 0.0

    for attribute in newAttributes:
        a = calculateInformationGain(dataSet, attribute, targetAttr)
        if a > highestInformationGain:
            highestInformationGain = a
            bestAttribute = attribute

    return bestAttribute


# Return true if the value for the target variable is the same for each data set
def sameTargetAttrValue(data, targetAttr):
    sameValues = True

    for entry in data:
        if entry[targetAttr] != data[0][targetAttr]:
            sameValues = False

    return sameValues


# Return a list of the unique values of a specific attribute in a data set
def getValues(data, targetAttr):
    values = calculateValueFrequencies(data, targetAttr)
    return list(values.keys())


# Return a subset of the data where each row has the value of input attr == input value
def getDataSubset(data, attr, value):
    dataSubSet = []
    for row in range(len(data)):
        if data[row][attr] == value:
            dataSubSet.append(data[row])

    return dataSubSet


# Returns the most common value of the output attribute
def pickDefaultValue(data, targetAttr):
    values = calculateValueFrequencies(data, targetAttr)
    keys = list(values.keys())
    frequencies = list(values.values())

    return keys[frequencies.index(max(frequencies))]




def buildDecisionTree(data, attributes, targetAttr):

    data = data[:]

    targetValues = getValues(data, targetAttr)

    default = pickDefaultValue(data, targetAttr)

    # Base Case 1
    # Check to see if the data is empty, or if there is only one attribute remaining
    # If so, simply return the majority value of the target attribute (not ideal)
    if not data or (len(attributes) - 1) <= 0:
        return default

    # Base Case 2
    # Check to see if the value of the target attribute is the same for all values of the current attribute that
    # is being checked
    # If so, this means the unanimous value should be returned as the decided value
    elif len(targetValues) == 1:
        return targetValues[0]

    else:
        best = chooseBestAttribute(data, attributes, targetAttr)
        values = getValues(data, best)
        tree = {best:{}}

        for value in values:
            # Get all the data that is remaining where the value is true
            dataSubSet = getDataSubset(data, best, value)
            otherAttributes = [attr for attr in attributes if attr != best]
            subtree = buildDecisionTree(dataSubSet, otherAttributes, targetAttr)
            tree[best][value] = subtree

    return tree


with open('weather.json') as data_file:
    data = json.load(data_file)["data"]

attributes = list(data[0].keys())

print(buildDecisionTree(data, attributes, "play"))

