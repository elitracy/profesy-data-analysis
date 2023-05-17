import os
import requests
import csv
import tabula
import pandas as pd
import tempfile
import shutil
import os.path

collegeAbbreviations = [
    "AG", "AE", "AR", "AG", "AC", "AP", "AT", "GB", "BA", "DN", "DN_PROF",
    "ED", "EH", "EN", "GV", "SL", "SL_PROF", "LA", "MN", "MN_PROF", "MS", "NS",
    "PM_PROF", "PH", "QT", "VF", "VT_PROF", "GE", "LA", "MD", "MD_PROF", "CP_PROF",
    "VM", "VM_PROF"
]

seasons = ["spring", "summer", "fall"]

for year in range(2018, 2023):
    for season in seasons:
        season_param = 0
        if season == "spring":
            season_param = 1
        elif season == "summer":
            season_param = 2
        elif season == "fall":
            season_param = 3
        
        # if year == 2022 and season_param == 3:
        #     break

        for college in collegeAbbreviations:
            
            # url = "https://web-as.tamu.edu/GradeReports/PDFReports/20223/grd20223AR.pdf"

            yearAndSeason = str(year) + str(season_param)

            extension = "/grd" + yearAndSeason + college + ".pdf"

            url = "https://web-as.tamu.edu/GradeReports/PDFReports/" + yearAndSeason + extension

            response = requests.get(url)

            if response.status_code >= 200 and response.status_code < 300:

                folder_path = "./gpa_csvs/" + str(season) + str(year)

                if not os.path.isdir(folder_path):
                    os.mkdir(folder_path)

                file_name = os.path.basename(url)
                pdf_file_path = os.path.join(folder_path, file_name)

                with open(pdf_file_path, "wb") as f:
                    f.write(response.content)

                csv_file_path = os.path.splitext(pdf_file_path)[0] + ".csv"
                tabula.convert_into(pdf_file_path, csv_file_path, output_format="csv", pages="all")

                # Delete the PDF file
                os.remove(pdf_file_path)

                # Custom column headers
                custom_headers = ["Section", "A", "B", "C", "D", "F", "Total A-F", "GPA", "I", "S", "U", "Q", "X", "Total", "Instructor"]

                # Create a temporary file to store the modified CSV content
                temp_csv_file_path = os.path.join(folder_path, "temp.csv")

                # Open the temporary file in write mode
                with open(temp_csv_file_path, "w", newline="") as temp_file:
                    # Write the custom headers
                    writer = csv.writer(temp_file)
                    writer.writerow(custom_headers)

                    # Open the original CSV file in read mode
                    with open(csv_file_path, "r") as original_file:
                        csv_reader = csv.reader(original_file)
                        # Copy rows from the original file to the temporary file,
                        # excluding rows with an empty first value or starting with "COURSE TOTAL:"
                        for row in csv_reader:
                            if row and row[0] != "" and not row[0].startswith("COURSE TOTAL:"):
                                writer.writerow(row)

                # Replace the original CSV file with the modified file
                shutil.move(temp_csv_file_path, csv_file_path)

        print("Year:", year, ", Season:", season)
