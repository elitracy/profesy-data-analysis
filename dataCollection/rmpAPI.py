from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import math
import json
import requests
import time


NO_INFO = "N/A"

class rmp:
    def __init__(self, sid=1003):
        self.profBaseUrl = "https://www.ratemyprofessors.com"
        self.sid = sid
        self.profsDict = {}

        # profsDict format:
        # {profName: {
        #               numOccurrences : number of times we encountered a professor that is same as profName,
        #               occurrence[i] : {
        #                                   reviews : [{course : val, date : val, comments : val}, {}, {}],
        #                                   profUrl : url for each prof reviews page,
        #                                   department : val,
        #                                   overallRating : val / 5
        #                                   numRatings : total number of ratings
        #                                   wouldTakeAgain : % of reviewers who would take the prof again
        #                                   difficulty : average difficulty
        #                               }
        #            }
        # }
    

    # Could clean up this function by splitting tasks into several functions
    def getProfsInfo(self):

        url = "https://www.ratemyprofessors.com/search/teachers?query=*&sid=" + str(self.sid) # url with all profs at given school
        driver = webdriver.Chrome(os.path.abspath("chromedriver.exe"))
        driver.get(url) # request url & open driver
        numPages = math.floor(4475/8) # number of "show more" buttons on base page

        for i in range(numPages):
            try:
                # click the buttons, wait until button is present to avoid race condition
                WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button[class="Buttons__Button-sc-19xdot-1 PaginationButton__StyledPaginationButton-txi1dr-1 gjQZal"]'))).click()
            except TimeoutException:
                print('Page timed out after 20 seconds')
            
            print(i)
        
        # driver.page_source should now have all the professors after clicking all "show more" buttons
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        # get all prof cards elements after all pages are available 
        profCards = soup.findAll('a', {'class' : 'TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx'}) 
        print(len(profCards))

        currNumRequests = 1 # used to sleep the code so that num of requests made to rmp website does not max out (the max is around 100 req per 2 mins)

        for prof in profCards:
            print(currNumRequests)
            if currNumRequests % 100 == 0:
                print("Sleeping for 1 minute...")
                print("This happened", reqUpperBound/100, "times")
                time.sleep(60) # give 1 min for every 100 requests to reset IP address

            rmpProfName = prof.find("div", {"class" : "CardName__StyledCardName-sc-1gyrgim-0 cJdVEK"}).text.strip()
            firstAndLast = rmpProfName.split()

            # errors with name length
            if len(firstAndLast) < 2 or len(firstAndLast) > 3:
                continue

            # track current occurrence in case of encountering prof with same last name and first initial
            currOccurrence = ""
            firstInitial = firstAndLast[0][0].upper()
            lastName = ""

            # setting up first and last name of prof to match tamu registrar report format
            if len(firstAndLast) == 3:
                lastName = firstAndLast[1].upper() + " " + firstAndLast[2].upper()
            elif len(firstAndLast) == 2:
                lastName = firstAndLast[1].upper()

            profName = lastName + " " + firstInitial

            # checking if current prof exists (hence another prof with same first initial and last name)
            if profName in self.profsDict:
                self.profsDict[profName]["numOccurrences"] += 1
            else:
                self.profsDict[profName] = {}
                self.profsDict[profName]["numOccurrences"] = 1
            
            currOccurrence = "occurrence" + str(self.profsDict[profName]["numOccurrences"])
            self.profsDict[profName][currOccurrence] = {"reviews" : []}

            # obtaining current prof's reviews url from very outer html element for current prof
            profUrl = self.profBaseUrl + str(prof['href'])

            # find department element
            department = prof.find('div', {'class' : 'CardSchool__Department-sc-19lmz2k-0 haUIRO'}).text.strip()

            # find total number of ratings element
            numRatings = prof.find('div', {'class' : 'CardNumRating__CardNumRatingCount-sc-17t4b9u-3 jMRwbg'}).text.strip()

            # finding % that would take again and overall difficulty. 
            # both have same element class name, so get both (since findAll returns list) and assign accordingly
            takeAgainAndDifficulty = prof.findAll('div', {'class' : 'CardFeedback__CardFeedbackNumber-lq6nix-2 hroXqf'})
            take_again = takeAgainAndDifficulty[0].text.strip()
            difficulty = takeAgainAndDifficulty[1].text.strip()

            # update all info retrieved so far for current occurrence of a prof
            self.profsDict[profName][currOccurrence]["profUrl"] = profUrl
            self.profsDict[profName][currOccurrence]["department"] = department
            self.profsDict[profName][currOccurrence]["overallRating"] = ""
            self.profsDict[profName][currOccurrence]["numRatings"] = numRatings
            self.profsDict[profName][currOccurrence]["wouldTakeAgain"] = take_again
            self.profsDict[profName][currOccurrence]["difficulty"] = difficulty

            # get personal prof url in order to retrieve the overall rating and list of reviews
            page = requests.get(profUrl)
            profSoup = BeautifulSoup(page.content, "html.parser")

            # get element of overall rating, check for errors, and update it
            overallRating = profSoup.find("div", {"class" : "RatingValue__Numerator-qw8sqy-2 liyUjw"})

            if overallRating is None:
                self.profsDict[profName][currOccurrence]["overallRating"] = NO_INFO
            else:
                if str(overallRating.text.strip()) == NO_INFO:
                    self.profsDict[profName][currOccurrence]["overallRating"] = NO_INFO
                else:
                    self.profsDict[profName][currOccurrence]["overallRating"] = str(overallRating.text.strip()) + "/5"

            # find all reviews for current prof and iterate through each to remove the elements and just obtain the necessary text
            reviews = profSoup.find_all("div", {"class" : "Rating__RatingInfo-sc-1rhvpxz-3 kEVEoU"})

            if len(reviews) == 0:
                self.profsDict[profName][currOccurrence]["reviews"] = [{"course" : NO_INFO, "date" : NO_INFO, "comments" : NO_INFO}]
                reqUpperBound += 1
                continue

            for review in reviews:
                currReviewInfo = {}

                course = review.find("div", {"class" : "RatingHeader__StyledClass-sc-1dlkqw1-2 gxDIt"}).text.strip()
                date = review.find("div", {"class" : "TimeStamp__StyledTimeStamp-sc-9q2r30-0 bXQmMr RatingHeader__RatingTimeStamp-sc-1dlkqw1-3 BlaCV"}).text.strip()
                comments = review.find("div", {"class" : "Comments__StyledComments-dzzyvm-0 gRjWel"}).text.strip()

                currReviewInfo["course"] = course
                currReviewInfo["date"] = date
                currReviewInfo["comments"] = comments

                self.profsDict[profName][currOccurrence]["reviews"].append(currReviewInfo)
            
            # update number of requests 
            currNumRequests += 1



    def updateJson(self):
        self.getProfsInfo() # populate self.profsDict with prof info

        # update json file with new data
        filename = "allRmpInfo.json"
        with open(filename, "r") as file:
            data = json.load(file)

        data = self.profsDict
        print("dict size:", len(self.profsDict))

        with open(filename, "w") as file:
            json.dump(data, file)


profs = rmp(1003)
profs.updateJson()

# check if json size is same as self.profsDict
# filename = "allRmpInfo.json"
# with open(filename, "r") as file:
#     data = json.load(file)

# print("dict size:", len(data))
