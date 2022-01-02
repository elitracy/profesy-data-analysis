import os
rootdir="."
for root, subdirs, files in os.walk(rootdir):
    for file in files:
        if(file[-4:] == ".csv"):
            file = open(f"registrarReportData_CSV/{file[:2]}/{file}")
            for line in file:
                lineData = line.split(",")
                if "-" in lineData[0] and len(lineData[0]) == 12:
                    print(lineData)
            file.close()