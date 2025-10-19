def uniqueSetFromFile(filePath):
    uniqueItems = set()
    try:
        with open(filePath, "r", encoding = "UTF-8") as fr:
            next(fr) #skip first (header) line of csv
            for line in fr:
                uniqueItems.add(tuple(line.strip().split(",")[:3]))
    except FileNotFoundError:
        with open(filePath, 'w', encoding = "UTF-8") as file:
            file.write("date,bank,currency,buy,sale")
    return uniqueItems

def saveToCSV(itemsToAdd, filePath = "./Exchanges_CSV/Exchanges3.csv" ):
    uniqueCSVItems = uniqueSetFromFile(filePath)

    itemsToAdd = [item for item in itemsToAdd if tuple(item[:3]) not in uniqueCSVItems]

    uniqueListItems = set()
    itemsToFile = list()

    for item in itemsToAdd:
        key = tuple(item[:3])
        if key not in uniqueListItems:
            uniqueListItems.add(key)
            itemsToFile.append(item)

    with open(filePath, "a", encoding = "UTF-8") as fa:
        for line in itemsToFile:
            fa.write(f"\n{line[0]},{line[1]},{line[2]},{line[3]},{line[4]}")

def readFromCSV(filePath = "./Exchanges_CSV/Exchanges3.csv"):
    recordsList = list()
    with open(filePath, "r", encoding="UTF-8") as fr:
        next(fr)  # skip first (header) line of csv
        for line in fr:
            recordsList.extend([line.strip().split(",")])
    return recordsList

if __name__ == "__main__":
    print("It's util file, that handle work with files")
    print("Contains of such methods:")
    print("uniqueSetFromFile(filePath) -> return set of unique items from CSV file")
    print("saveToCSV(itemsToAdd, filePath) -> save unique items from given list to CSV")
    print("readFromCSV(filePath) -> return a list of records as lists of strings from CSV")