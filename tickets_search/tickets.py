"""
火车票查询器

Usage:
    ticket [-dgktz] <from> <to> <data>

Options:
    -h --help       Show this screen
    -d              动车
    -g              高铁
    -k              快速
    -t              特快
    -z              直达

"""

from docopt import docopt
import stations
import requests
from prettytable import PrettyTable
from colorama import Fore


def cli():
    arguments = docopt(__doc__, version='Tickets1.0')
    from_station = stations.get_telecode(arguments.get('<from>'))
    to_station = stations.get_telecode(arguments.get('<to>'))
    data = arguments.get('<data>')

    options = ''.join([key for key, values in arguments.items() if values is True])

    url = 'https://kyfw.12306.cn/otn/leftTicket/query?' \
          'leftTicketDTO.train_date={}&' \
          'leftTicketDTO.from_station={}&' \
          'leftTicketDTO.to_station={}&' \
          'purpose_codes=ADULT'.format(data, from_station, to_station)

    header = '车次 车站 时间 历时 商务座 一等 二等 软卧 硬卧 硬座 无座'.split()
    pt = PrettyTable()
    pt._set_field_names(header)

    # 获取接口
    res = requests.get(url, verify=False)
    raw_data = res.json()['data']['result']
    for data in raw_data:
        data_list = data.split('|')
        train_no = data_list[3]
        train_sort = train_no[0].lower()

        if not options or train_sort in options:
            from_station_name = data_list[6]
            to_station_name = data_list[7]
            start_time = data_list[8]
            arrive_time = data_list[9]
            cost_time = data_list[10]
            business_seat = data_list[32] or '--'
            first_class_seat = data_list[31] or '--'
            second_class_seat = data_list[30] or '--'
            soft_sleep = data_list[23] or '--'
            hard_sleep = data_list[28] or '--'
            hard_seat = data_list[29] or '--'
            no_seat = data_list[26] or '--'

            pt.add_row([
                train_no,
                '\n'.join([Fore.GREEN + stations.get_name(from_station_name) + Fore.RESET, Fore.RED + stations.get_name(to_station_name) + Fore.RESET]),
                '\n'.join([Fore.GREEN + start_time + Fore.RESET, Fore.RED + arrive_time + Fore.RESET]),
                cost_time,
                business_seat,
                first_class_seat,
                second_class_seat,
                soft_sleep,
                hard_sleep,
                hard_seat,
                no_seat
            ])
    print(pt)

cli()



