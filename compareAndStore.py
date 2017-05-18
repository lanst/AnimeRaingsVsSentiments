'''------------------------- Documentation -----------------------------
    Name:       Norlan Prudente
    Descripton: This program will read in the anime rating and the anime
                sentiments and will combine them to a csv file.
'''
import csv

'''-------------------------- writeToCSV -------------------------------
    Write the map to a csv
---------------------------------------------------------------------'''
def writeToCSV(combinedRatings, outFile):
    headers = ['Name', 'Rating', 'Sentiment']
    writer = csv.writer(outFile, delimiter=',', lineterminator='\n')

    try:
        writer.writerow(headers)
        for key, value in combinedRatings.items():
            try:
                writer.writerow([key, \
                                 combinedRatings[key]['rating'], \
                                 combinedRatings[key]['sentiment']])
            except:
                continue
    except:
        a = input("Can't write, error!!!")

'''----------------------- compareAndCombine ---------------------------
    Compare two maps and if the have the same key put both values in the
    new map.
---------------------------------------------------------------------'''
def compareAndCombine(animeRatings, animeSentiments, combinedRatings):
    #look through animeRatings
    for key, value in animeRatings.items():
        name = key.decode('utf-8')
        rating = value

        #if name boths exist put it in the map
        if name in animeSentiments:
            sentiment = animeSentiments[name]
            combinedRatings[name] = {}
            combinedRatings[name]['rating'] = rating
            #add 5 to make correction on what the AFINN file scoring
            combinedRatings[name]['sentiment'] = str(float(sentiment)/2 + 5)

        

'''------------------------- readInRatings -----------------------------
    This will read in a csv file and get the rating that the anime has.
    Store all the anime name as key and rating as the value.
---------------------------------------------------------------------'''
def readInRatings(file, animeRatings):
    #for skipping the header of the files
    skip = True

    #read the csv file and turn it into a list
    try:
        rowList = csv.reader(file)
    except Exception as e:
        print("csv reader fail")
        print(e)

    #traverse through all the data
    for row in rowList:
        try:
            if not skip:
                animeRatings[row[1].encode('ascii')] = row[5]
            else:
                skip = False
        except Exception as e:
            print(e)
            continue

'''------------------------ readInSentiments --------------------------
    This will read in a csv file and get the sentiments that the anime
    has. fStore all the anime name as key and rating as the value.
---------------------------------------------------------------------'''
def readInSentiments(file, animeSentiments):
    #for skipping the header of the files
    skip = True

    #read the csv file and turn it into a list
    try:
        rowList = csv.reader(file)
    except Exception as e:
        print("csv reader fail")
        print(e)

    #traverse through all the data
    for row in rowList:
        try:
            if not skip:
                animeSentiments[row[0]] = row[1]
            else:
                skip = False
        except Exception as e:
            print(e)
            continue

'''------------------------------ main ---------------------------------
    The main program to call and run all the function
---------------------------------------------------------------------'''
def main():
    #map to hold all the anime rating
    animeRatings = {}
    #map to hold all the sentiment values
    animeSentiments = {}
    #holds the combined data
    combinedRatings = {}
    
    #read in the anime names as key and ratings as value
    with open('anime.csv', 'rt', encoding='utf-8') as file:
        readInRatings(file, animeRatings)
    file.close()
      
    #read in the anime names as key and sentiments as value
    with open('animeSentiments.csv') as file:
        readInSentiments(file, animeSentiments)
    file.close()

    #compare and combine
    compareAndCombine(animeRatings, animeSentiments, combinedRatings)

    try:
        outFile = open('combinedRating2.csv', 'w+')
        writeToCSV(combinedRatings, outFile)
        outFile.close()
    except Exception as e:
        print("Can't open file")
        print(e)
    
if __name__ == '__main__':
    main()
