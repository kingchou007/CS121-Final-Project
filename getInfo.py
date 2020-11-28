from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt


def main():
    baseurl = "https://weather.com/weather/tenday/l/0863aac4979c8782a8b6b0a01ef3efd00b49d2132fe8320b1df30e559a772459"
    COVIDurl = "https://weather.com/coronavirus/l/d58593b7542d43e658f6d167c8aa96a2c833cc678aa90aa4f2b711789b72cb1f"
    datalist = getData(baseurl,COVIDurl)
    savePathExcel = "Weather&COVID-19 Status.xls"
    saveDataExcel(datalist,savePathExcel)


findDate=re.compile(r'<span class="day-detail clearfix">(.*?)<')
findDesc=re.compile(r'<td class="description".*?<span>(.*?)<',re.S)
findHTemp=re.compile(r'<td class="temp".*?class="">(.*?)<')
findLTemp=re.compile(r'<span class="slash".*?class="">(.*?)<')
findPrecip=re.compile(r'<td class="precip".*?<span>(.*?)<')
findWind=re.compile(r'<td class="wind".*?<span class="">(.*?)<')
findHumidity=re.compile(r'<td class="humidity".*?<span>(.*?)<')
findCity=re.compile(r'<span class=".*?type="button">(.*?)<svg',re.S)
findTown = re.compile(r'>(.*?)<')
findTime = re.compile(r'>(.*?)<')
findCases = re.compile(r'>(.*?)<')
findCCGR = re.compile(r'>(.*?)<')
findDeaths = re.compile(r'>(.*?)<')
findDGR = re.compile(r'>(.*?)<')
findState = re.compile(r'>(.*?)<')


def getData(baseurl,COVIDurl):
    datalist = []
    html1, html2 = askURL(baseurl, COVIDurl)
    soup1 = BeautifulSoup(html1, "html.parser")
    for eachDay in soup1.find_all("tr",class_="clickable closed"):
        data = []
        eachDay = str(eachDay)
        date = re.findall(findDate, eachDay)[0]
        data.append(date)
        description = re.findall(findDesc, eachDay)[0]
        data.append(description)
        if(re.findall(findHTemp, eachDay)[0]==""):
            high_temp = ""
        else:
            high_temp = re.findall(findHTemp, eachDay)[0]
        data.append(high_temp)
        if (re.findall(findLTemp, eachDay)[0] == ""):
            low_temp = ""
        else:
            low_temp = re.findall(findLTemp, eachDay)[0]
        data.append(low_temp)
        precip = re.findall(findPrecip, eachDay)[0]
        data.append(precip)
        wind = re.findall(findWind, eachDay)[0]
        data.append(wind)
        humidity = re.findall(findHumidity, eachDay)[0]
        data.append(humidity)
        datalist.append(data)

    dataCOVID = []
    soup2 = BeautifulSoup(html2, "html.parser")
    city = re.findall(findCity, str(soup2.find_all("span", class_="_-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--primaryLocation--3FwcU _-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--location--go4kA")))[0]
    location = re.findall(findTown, str(soup2.find_all("h2", class_="_-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--countyName--22yuQ")))[0]+", "+str(city)
    dataCOVID.append(location)
    timeOfRecord = re.findall(findTime, str(soup2.find_all("span", class_="_-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--asOfDate--1ytig")))[0]
    dataCOVID.append(timeOfRecord)
    ConfCases = re.findall(findCases, str(soup2.find_all("span", class_="_-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--primaryCount--1LVTn _-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--count--3L86P _-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--confirmed--2KnoH")))[0]
    dataCOVID.append(ConfCases)
    CCGrowthRate=re.findall(findCCGR, str(soup2.find_all("span",class_="_-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--delta--5uh-r _-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--positiveDelta--3wURb")))[0]
    dataCOVID.append(CCGrowthRate)
    Deaths=re.findall(findDeaths, str(soup2.find_all("span", class_="_-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--primaryCount--1LVTn _-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--count--3L86P _-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--deaths--1iTju")))[0]
    dataCOVID.append(Deaths)
    DGrowthRate=re.findall(findDGR, str(soup2.find_all("span", class_="_-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--delta--5uh-r _-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--positiveDelta--3wURb")))[2]
    dataCOVID.append(DGrowthRate)
    state=re.findall(findState,str(soup2.find_all("h3", class_="_-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--location--go4kA")))[0]
    dataCOVID.append(state)
    SConfCases = re.findall(findCases, str(soup2.find_all("span", class_="_-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--count--3L86P _-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--confirmed--2KnoH")))[0]
    dataCOVID.append(SConfCases)
    SDeaths=re.findall(findDeaths, str(soup2.find_all("span", class_="_-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--count--3L86P _-_-components-src-organism-CovidCasesOverview-CovidCasesOverview--deaths--1iTju")))[0]
    dataCOVID.append(SDeaths)
    datalist.append(dataCOVID)
    return datalist


def askURL(url1, url2):
    head = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    request1 = urllib.request.Request(url1, headers=head)
    html1 = ""
    try:
        response1 = urllib.request.urlopen(request1)
        html1 = response1.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    request2 = urllib.request.Request(url2, headers=head)
    html2 = ""
    try:
        response2 = urllib.request.urlopen(request2)
        html2 = response2.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html1, html2


def saveDataExcel(datalist,savePath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("weather", cell_overwrite_ok=True)
    col = ("Date", "Description", "High/Low Temp(°F)", "Precipitation", "Wind", "Humidity","Location","Record Time","Confirmed Cases","Growth rate of confirmed cases","Deaths","Growth rate of deaths","State","State's total confirmed cases","State's total deaths")
    for i in range(0,15):
        sheet.write(0, i, col[i])
        sheet.col(i).width=256*20
        if(i==6 or i==7):
            sheet.col(i).width=256*35
    for i in range(len(datalist)-1):
        data = datalist[i]
        for j in range(len(data)):
            if(j<4):
                if (j == 2):
                    sheet.write(i+1, j, data[j]+"°/"+data[j+1]+"°")
                    j+=1
                else:
                    sheet.write(i+1, j, data[j])
            else:
                if(j==4 or j==6):
                    sheet.write(i+1, j - 1, data[j]+"%")
                else:
                    sheet.write(i+1, j-1, data[j])
    for i in range(len(datalist[len(datalist)-1])):
        sheet.write(1,6+i,datalist[len(datalist)-1][i])
    book.save(savePath)


if __name__ == "__main__":
    main()
    
