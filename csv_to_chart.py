import os
import csv
import pinyin
from matplotlib import pyplot as plt

def readCSV(csv_name):
    spots_dic = {}
    if os.path.exists(csv_name):
        with open(csv_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header_row = next(csv_reader)
            for row in csv_reader:
                spot = {
                    'name': row[0],
                    'grade': row[1],
                    'start_time': row[2].split('~')[0],
                    'end_time': row[2].split('~')[1],
                    'time': row[3],
                    'num': row[4],
                    'max_num': row[5]
                }
                first_py = pinyin.get_initial(spot['name'], '')
                if first_py not in spots_dic.keys():
                    spots_dic[first_py] = []
                same_time = False
                for spot_item in spots_dic[first_py]:
                    if spot_item['time'] == spot['time']:
                        same_time = True
                if not same_time:
                    spots_dic[first_py].append(spot)
            return spots_dic
    else:
        print('文件不存在,请先运行rfsp.py')


def get_spot_by_initial_pinyin(initial_pinyin, data):
    findKeys = []
    for key in data.keys():
        if key.find(initial_pinyin.lower()) != -1:
            findKeys.append(key)
    if len(findKeys) > 0:
        print("已找到如下景点:")
        for f_key in findKeys:
            tip = str(findKeys.index(f_key) + 1) + ' --- ' + data[f_key][0]['name']
            print(tip)
        index = -1
        while index < 0 or index >= len(findKeys):
            index_input = input('请输入序号选择景点:')
            index = int(index_input) - 1
            if index < 0 or index >= len(findKeys):
                print('序号输入错误,请重新输入')
        k = findKeys[index]
        return data[k]
    else:
        print('没有找到景点,请重新输入')
        return []


def get_spot_by_time(time, data):
    spot_time_list = []
    for spot in data:
        if spot['time'].find(time) != -1:
            spot_time_list.append(spot)
    return spot_time_list

# 1-年视图
# 2-月视图
# 3-日视图
def get_chart_data(spot_list, type=3):
    x, y = [], []
    title = ""
    if type == 1:
        for spot in spot_list:
            title = spot['name']
            time = spot['time']
            x.append(time)
            num = spot['num']
            y.append(int(num))
    elif type == 2:
        for spot in spot_list:
            title = spot['name']
            time = spot['time']
            x.append(time)
            num = spot['num']
            y.append(int(num))
    elif type == 3:
        for spot in spot_list:
            title = spot['name']
            time = spot['time']
            x.append(time)
            num = spot['num']
            y.append(int(num))
    print(x)
    print(y)
    print(title)
    fig = plt.figure(dpi=128, figsize=(10, 6))
    plt.plot(x, y)
    # plt.title(title)
    fig.autofmt_xdate()
    plt.show()


def main():
    data = readCSV('spot.csv')
    spot_list = []
    while len(spot_list) == 0:
        initial_pinyin = input("dfmz（景点首字母查询 例：东方明珠）")
        spot_list = get_spot_by_initial_pinyin(initial_pinyin, data)
    print('1-年视图')
    print('2-月视图')
    print('3-日视图')
    type = input('请输入生成图表视图模式序号:')
    get_chart_data(spot_list,3)


main()
