import requests

departments = [
"AG",
"AR",
"GB",
"BA",
"DN",
"ED",
"EN",
"EX",
"GV",
"GS",
"GE",
"LA",
"NU",
"PH",
"QT",
"SC",
"VM",
"UT"
]

for i in range(2016,2022):
    for j in range(1,4):
        for d in departments:
            requestString=f'https://web-as.tamu.edu/GradeReports/PDFReports/{i}{j}/grd{i}{j}{d}.pdf'
            r = requests.get(requestString,allow_redirects=True)
            open(f'./registrarReportData/{d}/{d}_{i}_{j}.pdf',"wb").write(r.content)
