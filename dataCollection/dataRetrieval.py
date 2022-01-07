import os
import pprint
import pymongo
from pymongo import MongoClient

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

#function to add all contents of the dictionary to a list for easier db access
def addToList(dictionary, list):
	for dic in dictionary.keys():
		list.append(dictionary[dic])

# function to manipulate and read all csv data
def retrieve_data(filename):
	#print(filename)
	file = open(filename, "r+")
	semester = ''
	for line in file:
		lineList = line.split(",")

		if lineList[4][0:5] == 'GRADE':
			semesterStringList = lineList[4].split(" ")
			semester = semesterStringList[-2] + " " + semesterStringList[-1]
		if line[4] == '-' and line[0] != '-': # means it's a line with course info (e.g. CSCE-121)
			instructor = lineList[-1][0:-1]
			name = instructor
			department = lineList[0][0:4]
			course_no = lineList[0][5:8]
			course = department + course_no

			if instructor not in profs_dict:
				profs_dict[instructor] = {}
				profs_dict[instructor]['name'] = name
				profs_dict[instructor]['university'] = university
				profs_dict[instructor]['overallGPA'] = overallGPA
				courseList = []
				courseInfo = {'course' : course, 'semester' : semester, 'semGPA' : '0', 'totalGPA' : lineList[7], 'numSections' : '1', 'A' : lineList[1], 'B' : lineList[2], 'C' : lineList[3], 'D' : lineList[4], 'F' : lineList[5], 'Q' : lineList[11], 'CourseTotal' : lineList[-2]}
				courseList.append(courseInfo)
				profs_dict[instructor]['courses'] = courseList
			else:
				courseFound = False
				for dic in profs_dict[instructor]['courses']:
					if dic['course'] == course and dic['semester'] == semester:
						courseFound = True
						newTotalGPA = float(lineList[7]) + float(dic['totalGPA'])
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
					courseInfo = {'course' : course, 'semester' : semester, 'semGPA' : '0', 'totalGPA' : lineList[7], 'numSections' : '1', 'A' : lineList[1], 'B' : lineList[2], 'C' : lineList[3], 'D' : lineList[4], 'F' : lineList[5], 'Q' : lineList[11], 'CourseTotal' : lineList[-2]}
					profs_dict[instructor]['courses'].append(courseInfo)
				
 

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
	for dic in profs_dict[instructor]['courses']:
		semGPA = round(float(dic['totalGPA']) / float(dic['numSections']), 3)
		dic['semGPA'] = str(semGPA)
		newOverallGPA += float(dic['totalGPA'])
		overallNumSections += float(dic['numSections'])
	overallGPA = round(newOverallGPA / overallNumSections, 3)
	profs_dict[instructor]['overallGPA'] = str(overallGPA)

#appending to list 
addToList(profs_dict, final_profs_list)


# setup initial connection to cluster 
cluster = MongoClient("mongodb+srv://<username>:<password>@cluster0.8bwmh.mongodb.net/profesy?retryWrites=true&w=majority")
db = cluster["profesy"]
collection = db["professors"]

# insert list of dicts to db
collection.insert_many(final_profs_list)
	
# profs_dict.clear()
# print(profs_dict)
pp = pprint.PrettyPrinter(width=41, compact=True)
# pp.pprint(final_profs_list)
# for i in final_profs_list:
# 	if i['name'] == 'AHMED S':
# 		pp.pprint(i)
