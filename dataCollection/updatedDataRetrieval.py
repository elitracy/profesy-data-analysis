import os
from pprint import pprint
import pymongo
from pymongo import MongoClient
import json

directory = "/mnt/c/Profesy/dataCollection/gpa_csvs"

# filename = "fall2016_business.csv"
profs_dict = {}
university = 'TAMU'
department = ''
instructor = ''
course_no = ''
name = ''
overallGPA = ''
final_profs_list = []
NO_INFO = "N/A"
final_coursesList = []
coursesDict = {}
newUpdatedProfList = []

# opening and creating access to the rmp info json file
jsonFile = "tamuRmpInfo.json"
with open(jsonFile, "r") as rmpFile:
    rmpInfo = json.load(rmpFile)

#function to add all contents of the dictionary to a list for easier db access
def addToList(dictionary, list):
	for dic in dictionary.keys():
		list.append(dictionary[dic])

# function to update the professors table to the new format
def updateProfsInfo(final_profs_list, newUpdatedProfList):
	for prof in final_profs_list:
		for course in prof["courses"]:
			courseName = course["course"]
			if courseName not in prof["courseAverages"]:
				continue
			profAndCourseDict = {}
			profAndCourseDict["name"] = prof["name"]
			profAndCourseDict["overallGPA"] = prof["overallGPA"]
			profAndCourseDict["course"] = courseName
			profAndCourseDict["courseAverage"] = prof["courseAverages"][courseName]["courseAverage"]
			profAndCourseDict["semester"] = course["semester"]
			profAndCourseDict["semesterGPA"] = course["semGPA"]
			profAndCourseDict["university"] = "TAMU"
			profAndCourseDict["A"] = course["A"]
			profAndCourseDict["B"] = course["B"]
			profAndCourseDict["C"] = course["C"]
			profAndCourseDict["D"] = course["D"]
			profAndCourseDict["F"] = course["F"]
			profAndCourseDict["Q"] = course["Q"]

			newUpdatedProfList.append(profAndCourseDict)


# function to update course averages for each prof
def populateCourseAvgInfo(final_profs_list):

	for prof in final_profs_list:
		prof['courseAverages'] = {}

		for course in prof['courses']:
			currCourse = course['course']
			currGPA = float(course['semGPA'])

			# GPA error checking
			if currGPA < 1 or course['semester'] == '':
				continue

			if currCourse not in prof['courseAverages']:
				prof['courseAverages'][currCourse] = {"numSemesters" : 1, "totalGPA" : currGPA, "courseAverage" : currGPA}
			else:
				prof['courseAverages'][currCourse]["numSemesters"] += 1
				prof['courseAverages'][currCourse]["totalGPA"] += currGPA
				totalGPA = prof['courseAverages'][currCourse]["totalGPA"]
				numSemesters = prof['courseAverages'][currCourse]["numSemesters"]
				prof['courseAverages'][currCourse]["courseAverage"] = round(totalGPA / numSemesters, 3)	

def updateCourseAvgs(final_profs_list):
	# print(len(profsList))
	for profDict in final_profs_list:
		# print(profDict)
		for course in profDict["courseAverages"].keys():
			if course not in coursesDict:
				coursesDict[course] = {}
				coursesDict[course]["course"] = course
				coursesDict[course]["professors"] = [] 
				currCourse = {}
				currCourse["name"] = profDict["name"]
				currCourse["courseAverage"] = profDict["courseAverages"][course]["courseAverage"]
				coursesDict[course]["professors"].append(currCourse)
			else:
				coursesDict[course]["professors"].append({"name": profDict["name"], "courseAverage" : profDict["courseAverages"][course]["courseAverage"]})

	for course in coursesDict:
		final_coursesList.append(coursesDict[course])			
				

# function to manipulate and read all csv data
def retrieve_data(filename):
	#print(filename)
	file = open(filename, "r+")
	semester = ''
	i = 0
	for line in file:
		lineList = line.split(",")
		# print(lineList)
		# print(lineList)
		# if i == 2:
		# 	break
		if 'GRADE' in line:
			lineList.remove('\n')
			resultList = [val for val in lineList if val != '']
			semesterStringList = resultList[0].split(" ")
			season = ""
			year = ""
			idx = 0
			for val in semesterStringList:
				if val == "SPRING" or val == "FALL" or val == "SUMMER":
					season = val
					year = semesterStringList[idx+1]
					break
				idx += 1
			semester = season + " " + year
		if line[4] == '-' and line[0] != '-': # means it's a line with course info (e.g. CSCE-121)
			instructor = lineList[-1][0:-1]
			name = instructor
			department = lineList[0][0:4]
			course_no = lineList[0][5:8]
			course = department + course_no
			totalGPA = ''

			if instructor not in profs_dict:
				profs_dict[instructor] = {}
				profs_dict[instructor]['name'] = name
				profs_dict[instructor]['university'] = university
				profs_dict[instructor]['overallGPA'] = overallGPA
				courseList = []
				if semester == 'SPRING 2016' or semester == 'SUMMER 2016':
					splitUp = lineList[6].split(' ')
					totalGPA = splitUp[1]
				else:
					totalGPA = lineList[7]
				
				courseInfo = {'course' : course, 'semester' : semester, 'semGPA' : '0', 'totalGPA' : totalGPA, 'numSections' : '1', 'A' : lineList[1], 'B' : lineList[2], 'C' : lineList[3], 'D' : lineList[4], 'F' : lineList[5], 'Q' : lineList[11], 'CourseTotal' : lineList[-2]}
				courseList.append(courseInfo)
				profs_dict[instructor]['courses'] = courseList
				
				
			else:
				courseFound = False
				for dic in profs_dict[instructor]['courses']:
					if dic['course'] == course and dic['semester'] == semester:
						courseFound = True
						if semester == 'SPRING 2016' or semester == 'SUMMER 2016':
							splitUp = lineList[6].split(' ')
							totalGPA = splitUp[1]
						else:
							totalGPA = lineList[7]
						newTotalGPA = float(totalGPA) + float(dic['totalGPA'])
						dic['totalGPA'] = str(newTotalGPA)
						newNumSections = int(dic['numSections']) + 1
						dic['numSections'] = str(newNumSections)
						newCourseTotal = int(dic['CourseTotal']) + int(lineList[-2])
						dic['CourseTotal'] = str(newCourseTotal)
						newA = int(dic['A']) + int(lineList[1])
						dic['A'] = str(newA)
						newB = int(dic['B']) + int(lineList[2])
						dic['B'] = str(newB)
						newC = int(dic['C']) + int(lineList[3])
						dic['C'] = str(newC)
						newD = int(dic['D']) + int(lineList[4])
						dic['D'] = str(newD)
						newF = int(dic['F']) + int(lineList[5])
						dic['F'] = str(newF)
						newQ = int(dic['Q']) + int(lineList[11])
						dic['Q'] = str(newQ)
				if not courseFound:
					if semester == 'SPRING 2016' or semester == 'SUMMER 2016':
						splitUp = lineList[6].split(' ')
						totalGPA = splitUp[1]
					else:
						totalGPA = lineList[7]
					courseInfo = {'course' : course, 'semester' : semester, 'semGPA' : '0', 'totalGPA' : totalGPA, 'numSections' : '1', 'A' : lineList[1], 'B' : lineList[2], 'C' : lineList[3], 'D' : lineList[4], 'F' : lineList[5], 'Q' : lineList[11], 'CourseTotal' : lineList[-2]}
					profs_dict[instructor]['courses'].append(courseInfo)
				
		i += 1

		# print(line.split(","))

# iterating through all subdirectories and files, and retrieving + storing the data from each file into the global dict
for subdir, dirs, files in os.walk(directory):
    for filename in files:
        filepath = subdir + os.sep + filename
        retrieve_data(filepath)


#updating average GPAs
for instructor in profs_dict.keys():
	newOverallGPA = 0
	overallNumSections = 0
	i = 0
	for dic in profs_dict[instructor]['courses']:
		semGPA = round(float(dic['totalGPA']) / float(dic['numSections']), 3)
		# if semGPA == 0:
		# 	del profs_dict[instructor]['courses'][i]
		# 	# print("here")
		# 	# print(dic['semester'])
		# 	continue 
		dic['semGPA'] = str(semGPA)
		newOverallGPA += float(dic['totalGPA'])
		overallNumSections += float(dic['numSections'])
		i += 1
	overallGPA = round(newOverallGPA / overallNumSections, 3)
	profs_dict[instructor]['overallGPA'] = str(overallGPA)

#appending to list 
addToList(profs_dict, final_profs_list)

# adding course average info into each dict in final_profs_list
populateCourseAvgInfo(final_profs_list)

# updating course averages
updateCourseAvgs(final_profs_list)

# reformatting db to have each prof and semester on a line
updateProfsInfo(final_profs_list, newUpdatedProfList)

# pprint(final_coursesList)
# setup initial connection to cluster 
print("Enter mongodb username:", end=" ")
username = input()
print("Enter mongodb password:", end=" ")
password = input()
# cluster = MongoClient("mongodb+srv://" + str(username) + ":" + str(password) + "@cluster0.8bwmh.mongodb.net/profesyV2?retryWrites=true&w=majority")
cluster = MongoClient("mongodb+srv://profesyv2:" + password + "@profesydbv2.ucfy4ol.mongodb.net/?retryWrites=true&w=majority")
db = cluster["profesyV2"]

# -----------------------------------
# TO IMPORT INTO PROFESSORS COLLECTION
# -----------------------------------

collection = db["professors"]
collection.insert_many(newUpdatedProfList)

# -----------------------------------
# TO IMPORT INTO COURSES COLLECTION
# -----------------------------------

# collection = db["Courses"]
# collection.insert_many(final_coursesList)


# # Use below to pretty print and redirect output to a text file
# pp = pprint.PrettyPrinter(width=41, compact=True)
# pp.pprint(final_profs_list)
# for i in final_profs_list:
# 	if i['name'] == 'LEYK T':
# 		pprint(i)
# pprint(final_profs_list)
