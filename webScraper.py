'''
This program will be used to gather data
Norlan Prudente
Comp261
'''
#imports
import requests
import json
import nltk
from bs4 import BeautifulSoup
import csv

#write data to csv file
def writeToCSV(animeReviews, outFile):
    print('writing to csv')
    headers = ['Name', 'Rating']
    writer = csv.writer(outFile, delimiter=',', lineterminator='\n')

    try:
        writer.writerow(headers)
        for key, value in animeReviews.items():
            try:
                writer.writerow([key, animeReviews[key]['mean']])
            except:
                continue
    except:
        a = input("Can't write, error!!!")
    
#get the mean score
def getMean(animeReviews):
    print('getting the mean value...')
    try:
        for key, value in animeReviews.items():
            if animeReviews[key]['count'] != 0:
                animeReviews[key]['mean'] = animeReviews[key]['score'] / animeReviews[key]['count']
    except Exception as e:
        print("can't get the mean")
        print(e)
        
#store the words as keys and their score as value
def getScoringSystem(afinn_file, scores):
    print('setting the scoring system...')
    try:
        with open(afinn_file) as file:
            #one line at a time
            for line in file:
                #store the word and score
                word, score = line.split('\t')
                scores[word] = int(score)
            #close file
            file.close()
            return True;
    except:
        print("can't open file", afinn_file)
        return False
        
#validate the text to be > 10 different words
def validateReview(tokenizeReview):
    count = 0
    words = []

    #check if there are more than 10 words
    for word in tokenizeReview:
        try:
            #if they are already a copy
            if not word in words:
                words.append(word)

            #early escape if requirment are satisfied
            if len(words) > 20:
                return True
        except:
            continue

    return False

#give score on the review that was acquired
def getScore(tokenizeReview, scores):
    count = 0
    sentiment = 0
    
    for word in tokenizeReview:
        try:
            if word.lower() in scores:
                #since the rating goes to ten in anime list
                #multiply value to 2
                sentiment += scores[word.lower()] * 2
                count += 1
        except:
            continue

    #return the average only
    return sentiment/count

#gather data from a website
def webScraper(scores):
    #to count if page no longer exist
    error = 0
    pageCount = 0
    start = 1500
    stop = 0
    step = -1
    
    #map to store all the comments key=animeName value=comments
    animeReviews = {}

    #gather all the comments from myanimelist.net
    for i in range(start, stop, step):
        if error >= 5:
            break

        pageCount += 1
        
        try:
            #starting url
            url = "https://myanimelist.net/reviews.php?t=anime&p=" + str(i)
            #reset error
            error = 0

            #print the current page
            print ("Gathering page " + str(i) + "\n")

            #used for beautifulsoup
            r = requests.get(url)

            #get the whole html to be used by beautiful soup
            soup = BeautifulSoup(r.content, "html.parser")

            #html part that will be explored. This is what we're interested in
            data = soup.find_all("div", {"class": "borderDark"})

            #loop through all the data that was gathered
            for item in data:
                    try:
                        #anime title
                        animeTitle = item.contents[1].select("div > strong > a")[0].text
                        #store it to our map as key
                        if not animeTitle in animeReviews:
                            animeReviews[animeTitle] = {}
                            #will hold up the scores done with NLP
                            animeReviews[animeTitle]['score'] = 0
                            #count the reviews stored here to be used later
                            #to find the mean
                            animeReviews[animeTitle]['count'] = 0
                            #will be used to store the mean
                            animeReviews[animeTitle]['mean'] = 0
                    except:
                        continue
                    
                    try:
                        #Extract or remove unneeded strings.
                        #Rating
                        firstDiv        = item.contents[3].select("div")[0].extract()
                        rating          = item.contents[3].select("div")[0].extract()

                        #remove helpful
                        try:
                            helpful     = item.contents[3].select("span > div")[0].extract()
                        except:
                            pass
                        #remove readMore
                        try:
                            readMore    = item.contents[3].select("a")[0].extract()
                        except:
                            pass

                        #comment
                        review = item.contents[3].text

                        #tokenize the review
                        tokenizeReview = nltk.word_tokenize(review)
                        #validate if > 10 different words then accept it
                        proceed = validateReview(tokenizeReview)

                        if proceed:
                            #get the score and add it to the total
                            animeReviews[animeTitle]['score'] += getScore(tokenizeReview, scores)
                            #increment the count
                            animeReviews[animeTitle]['count'] += 1
                        
                    except:
                        continue
            if pageCount%100 == 0:
                #get the mean of each each anime
                getMean(animeReviews)

                #write it to a csv file
                outFile = open('animeSentiments.csv', 'w+')
                writeToCSV(animeReviews, outFile)
                outFile.close()
                    
        except:
            error += 1
            continue

    #get the mean of each each anime
    getMean(animeReviews)

    #write it to a csv file
    outFile = open('animeSentiments.csv', 'w+')
    writeToCSV(animeReviews, outFile)
    outFile.close()


def main():
    #for holding the score value
    scores = {}

    #get a scoring system for the words used in the review
    if (getScoringSystem('AFINN-111.txt', scores)):
        print('Starting Web Scraping...')
        webScraper(scores)
    else:
        print('fail to get scoring system')

    input('done')
        
#main
if __name__ == '__main__':
    main()
