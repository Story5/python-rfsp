import requests
import os
import csv
import time


def get_spots_data():
    url = 'https://shanghaicity.openservice.kankanews.com/public/tour/filterinfo2'
    response = requests.get(url, headers={'user-agent': 'rfsp/0.0.1'})
    spots = response.json()
    return spots


def getCSVHeader():
    return ['景点', '级别', '开放时间', '数据更新时间', '当前客流', '瞬时最大承载量']


def getCSVRow(fieldnames, spot):
    dic = {
        fieldnames[0]: spot['NAME'],
        fieldnames[1]: spot['GRADE'],
        fieldnames[2]: spot['START_TIME'] + '~' + spot['END_TIME'],
        fieldnames[3]: spot['TIME'],
        fieldnames[4]: spot['NUM'],
        fieldnames[5]: spot['MAX_NUM']
    }
    return dic


def writeCSV(csv_name, spot_list):
    exist = os.path.exists(csv_name)
    with open(csv_name, 'a') as csvfile:
        fieldnames = getCSVHeader()
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not exist:
            csv_writer.writeheader()
        for spot in spot_list:
            dic = getCSVRow(fieldnames, spot)
            csv_writer.writerow(dic)


def requestAndCSV():
    spotList = get_spots_data()
    print(spotList)
    writeCSV('spot.csv', spotList)


def main():
    sleep_input = input("输入多少秒获取一次数据(s),如一分钟输入60:")
    sleep_time = int(sleep_input)
    while True:
        requestAndCSV()
        time.sleep(sleep_time)


main()
