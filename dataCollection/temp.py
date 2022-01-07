import os
import pymongo
from pymongo import MongoClient

directory = "/mnt/c/Profesy/dataCollection/gpa_csvs"

# filename = "fall2016_business.csv"
profs_dict = {}
university = 'TAMU'
department = ''
instructor = ''
course_no = ''
semester = ''

def retrieve_data(filename):
	#print(filename)
	file = open(filename, "r+")
	for line in file:
		lineList = line.split(",")
		# if lineList[5] == 'TEXAS A&M UNIVERSITY':
		# 	#print("REACHED HERE")
		# 	university = 'TAMU'
		# if lineList[0] == 'DEPARTMENT:':
		#     #print("REACHED HERE")
		#     department = lineList[1]
		if lineList[4][0:5] == 'GRADE':
			semester = lineList[4][-11:]
		if line[4] == '-' and line[0] != '-': # means it's a line with course info (e.g. CSCE-121)
			instructor = lineList[-1][0:-1]
			department = lineList[0][0:4]
			course_no = lineList[0][5:8]
			course = department + course_no
			if instructor in profs_dict and university in profs_dict[instructor] and department in profs_dict[instructor][university] and course_no in profs_dict[instructor][university][department]:
				# if the same course taught by the same prof is encountered, then update all totals
				newTotalGPA = float(profs_dict[instructor][university][department][course_no]['totalGPA']) + float(lineList[7])
				profs_dict[instructor][university][department][course_no]['totalGPA'] = str(newTotalGPA)
				newTotalSections = int(profs_dict[instructor][university][department][course_no]['numSections']) + 1
				profs_dict[instructor][university][department][course_no]['numSections'] = str(newTotalSections)
				newNumAs = int(profs_dict[instructor][university][department][course_no]['A']) + int(lineList[1])
				profs_dict[instructor][university][department][course_no]['A'] = str(newNumAs)
				newNumBs = int(profs_dict[instructor][university][department][course_no]['B']) + int(lineList[2])
				profs_dict[instructor][university][department][course_no]['B'] = str(newNumBs)
				newNumCs = int(profs_dict[instructor][university][department][course_no]['C']) + int(lineList[3])
				profs_dict[instructor][university][department][course_no]['C'] = str(newNumCs)
				newNumDs = int(profs_dict[instructor][university][department][course_no]['D']) + int(lineList[4])
				profs_dict[instructor][university][department][course_no]['D'] = str(newNumDs)
				newNumFs = int( profs_dict[instructor][university][department][course_no]['F']) + int(lineList[5])
				profs_dict[instructor][university][department][course_no]['F'] = str(newNumFs)
				newNumQs = int(profs_dict[instructor][university][department][course_no]['Q']) + int(lineList[11])
				profs_dict[instructor][university][department][course_no]['Q'] = str(newNumQs)
				newTotal = int(profs_dict[instructor][university][department][course_no]['Course Total']) + int(lineList[-2])
				profs_dict[instructor][university][department][course_no]['Course Total'] = str(newTotal)
				#print(profs_dict[instructor][university][department][course_no]['Course Total'])
			if instructor not in profs_dict:
				profs_dict[instructor] = {}
			if university not in profs_dict[instructor]:
				profs_dict[instructor][university] = {}
			if department not in profs_dict[instructor][university]:
				profs_dict[instructor][university][department] = {}
			if course_no not in profs_dict[instructor][university][department]:
				profs_dict[instructor][university][department][course_no] = {}
				profs_dict[instructor][university][department][course_no]['avgGPA'] = '0'
				profs_dict[instructor][university][department][course_no]['totalGPA'] = lineList[7]
				profs_dict[instructor][university][department][course_no]['numSections'] = '1'
				profs_dict[instructor][university][department][course_no]['A'] = lineList[1]
				profs_dict[instructor][university][department][course_no]['B'] = lineList[2]
				profs_dict[instructor][university][department][course_no]['C'] = lineList[3]
				profs_dict[instructor][university][department][course_no]['D'] = lineList[4]
				profs_dict[instructor][university][department][course_no]['F'] = lineList[5]
				profs_dict[instructor][university][department][course_no]['Q'] = lineList[11]
				profs_dict[instructor][university][department][course_no]['Course Total'] = lineList[-2]

		print(line.split(","))

# iterating through all subdirectories and files, and retrieving + storing the data from each file into the global dict
# for subdir, dirs, files in os.walk(directory):
#     for filename in files:
#         filepath = subdir + os.sep + filename
#         retrieve_data(filepath)

filename = "fall2021_acasuccess.csv"
retrieve_data(filename)


#updating average GPAs
# for instructor in profs_dict.keys():
#     for university in profs_dict[instructor].keys():
#         for department in profs_dict[instructor][university].keys():
#             for course_no in profs_dict[instructor][university][department].keys():
#                 totalGPA = float(profs_dict[instructor][university][department][course_no]['totalGPA'])
#                 numSections = float(profs_dict[instructor][university][department][course_no]['numSections'])
#                 avgGPA = round(totalGPA / numSections, 3)
#                 profs_dict[instructor][university][department][course_no]['avgGPA'] = str(avgGPA)

# setup initial connection to cluster 
# cluster = MongoClient("mongodb+srv://dylann39:<password>@cluster0.8bwmh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = cluster["profesy"]
# collection = db["professors"]

# collection.insert_one(profs_dict)

# print("TESTING WITH AHMED----------------------------------")
#print(profs_dict)
	
# profs_dict.clear()
#print(profs_dict)