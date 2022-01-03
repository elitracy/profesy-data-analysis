#!/bin/bash

find . -maxdepth 3 -type f | while read file; do
    if [[ $file == *".xlsx.csv" ]]; then
        mv "$file" "$(echo "$file" | cut -c1-38).csv"
    fi
done