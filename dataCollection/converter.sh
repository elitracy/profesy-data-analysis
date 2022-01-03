#!/bin/bash
find . -maxdepth 3 -type f | while read file; do
    if [[ $file == *".xlsx" ]]; then
        folderName=$(echo "$file" | cut -c28-29)
        fileName=$(echo "$file" | tail -c 15)
        echo "$fileName"
        in2csv "$file" > "registrarReportData_CSV/$folderName/$fileName.csv"
    fi
    
done