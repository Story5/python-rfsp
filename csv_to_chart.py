import os
import calendar
import csv
import pinyin
from matplotlib import pyplot as plt


def print_menu(menu):
    print(menu)


def print_error(error):
    print(error)


def _print_dev(dev):
    print(dev)


def read_csv(csv_name):
    spots_dic = {}
    if os.path.exists(csv_name):
        with open(csv_name, 'r',encoding='gbk') as csv_file:
            csv_reader = csv.reader(csv_file)
            header_row = next(csv_reader)
            for row in csv_reader:
                if len(row) == 0:
                    continue
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
        print_error('文件不存在,请先运行rfsp.py')


def get_spot_data(data):
    find_keys = []
    while len(find_keys) == 0:
        initial_pinyin = input("dfmz（景点首字母查询 例：东方明珠）")
        for key in data.keys():
            if key.find(initial_pinyin.lower()) != -1:
                find_keys.append(key)
        if len(find_keys) == 0:
            print_error("没有找到景点,请重新输入")
    print_menu("已找到如下景点:")
    for f_key in find_keys:
        tip = str(find_keys.index(f_key) + 1) + ' --- ' + data[f_key][0]['name']
        print_menu(tip)
    index = -1
    while index < 0 or index >= len(find_keys):
        index_input = input('请输入序号选择景点:')
        index = int(index_input) - 1
        if index < 0 or index >= len(find_keys):
            print_error('序号输入错误,请重新输入')
    k = find_keys[index]
    return data[k]


def get_spot_by_time(time, data):
    spot_time_list = []
    for spot in data:
        if spot['time'].find(time) != -1:
            spot_time_list.append(spot)
    return spot_time_list


def get_months():
    return range(1, 13)


def get_days(month):
    return range(1, 23)


# "2021/2/22 19:58"
# "2021-02-22 20:22:01"
def get_int_by_index(s, index):
    d_s = s.split()[0]
    if d_s.find('-') != -1:
        return int(d_s.split('-')[index])
    elif d_s.find('/') != -1:
        return int(d_s.split('/')[index])
    else:
        return -1


# 1-年视图
# 2-月视图
# 3-日视图
def get_chart_data(spot_list):
    print_menu('1-年视图')
    print_menu('2-月视图')
    print_menu('3-日视图')
    type_int = -1
    while type_int not in [1, 2, 3]:
        type_input = input('请输入生成图表视图模式序号:')
        type_int = int(type_input)
        if type_int not in [1, 2, 3]:
            print_error('输入错误,请重新输入')
    title, x, y = "", [], []
    year_spot_list = []
    while len(year_spot_list) == 0:
        year_input = input("请输入要查看的年份(格式为yyyy),如2020:")
        for spot in spot_list:
            if spot['time'].startswith(year_input):
                year_spot_list.append(spot)
        if len(year_spot_list) == 0:
            print_error("未找到该年份数据,请重新输入")
        else:
            title = year_input + " year "
    if type_int == 1:
        x = get_months()
        y = [0] * 12
        title
        for spot in year_spot_list:
            month_i = get_int_by_index(spot['time'], 1)
            if month_i != -1:
                y[month_i - 1] += int(spot['num'])
    elif type_int in [2, 3]:
        month_spot_list = []
        while len(month_spot_list) == 0:
            month_input = input("请输入要查看的月份(1-12):")
            month_int = int(month_input)
            if month_int not in get_months():
                print_error("输入月份错误,请输入1-12之间的月份")
                continue
            for spot in year_spot_list:
                m = get_int_by_index(spot['time'], 1)
                if month_int == m:
                    month_spot_list.append(spot)
            if len(month_spot_list) == 0:
                print_error("未找到该月份数据,请重新输入")
            else:
                title = title + month_input + " month "
        month_total_days = calendar.mdays[month_int]
        if type_int == 2:
            x = range(1, month_total_days + 1)
            y = [0] * month_total_days
            for spot in month_spot_list:
                day_i = get_int_by_index(spot['time'], 2)
                if day_i != -1:
                    y[day_i - 1] += int(spot['num'])
        else:
            day_spot_list = []
            while len(day_spot_list) == 0:
                day_input = input("请输入要查看的日期(1-"+str(month_total_days)+"):")
                day_int = int(day_input)
                if day_int < 0 or day_int > month_total_days:
                    print_error("输入日期错误,请重新输入")
                    continue
                for spot in month_spot_list:
                    d = get_int_by_index(spot['time'], 2)
                    if d == day_int:
                        day_spot_list.append(spot)
                if len(day_spot_list) == 0:
                    print_error("没有找到该日期数据,请重新输入");
                else:
                    title = title + day_input + " day"
            for spot in day_spot_list:
                time = spot['time']
                x.append(time)
                num = spot['num']
                y.append(int(num))

    _print_dev(x)
    _print_dev(y)
    _print_dev(title)

    fig = plt.figure(dpi=128, figsize=(10, 6))
    plt.plot(x, y)
    plt.title(title)
    fig.autofmt_xdate()
    plt.show()


def main():
    data = read_csv('spot.csv')
    while True:
        spot_list = get_spot_data(data)
        get_chart_data(spot_list)

main()
