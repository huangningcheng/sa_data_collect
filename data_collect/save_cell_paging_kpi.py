from data_collect.login_emos import *
from datetime import datetime,timedelta
import pandas as pd
import json

def get_cell_paging_kpi(s,date):
    url = "http://10.53.160.65/jksdev_190_171_8050/sa/api/signal/loadUpDayData"
    fileurl = '../data/xm_cell_paging_kpi.xls'
    #countries = ['思明区', '湖里区', '海沧区', '集美区','同安区','翔安区']
    payload = {'cell': 'all', 'city': '厦门', 'handleType': 'pagination',
               'order': '', 'pageNumber': '1', 'pageSize': '10000', 'queryTime': date, 'sort': '', 'type': 'signalCell'}
    #print(payload)
    columns = ["日期", "小区", "ECI", "地市", "区县", "注册成功用户数", "初始注册成功率", "初始注册成功率（排除用户因素）",
               "移动性注册成功率", "寻呼请求数", "寻呼成功数", "寻呼成功率"]
    if not os.path.exists(fileurl):
        df = pd.DataFrame(columns=columns)
        df.to_excel(fileurl,sheet_name='SA小区级KPI指标',index=None)
    df = pd.read_excel(fileurl)
    if date not in list(df['日期'].astype('str')):
        r = s.post(url, json=payload)
        js = json.loads(r.text)
        if 'error' not in js:
            celldatas = js['data']['rows']
            for celldata in celldatas:
                if 'county_name' not in celldata:
                    continue
                if 'i_register_rate' not in celldata:
                    continue
                if 'm_register_rate' not in celldata:
                    continue
                if 'paging_rate' not in celldata:
                    continue
                celldataform = [[date,celldata['cellname'],celldata['eci'],celldata['city_name'],
                                celldata['county_name'],celldata['user_re_succ_cnt'],celldata['i_register_rate'],
                                celldata['i_register_rate2'],celldata['m_register_rate'],celldata['paging_req'],
                                celldata['paging_succ'],celldata['paging_rate']]]
                df1 = pd.DataFrame(celldataform, columns=columns)
                df = df.append(df1)
    df.to_excel(fileurl, index=None)

def get_sa_days_data(s,n):
    days = list(range(1, n+1))
    days.reverse()
    for m in days:
        today = datetime.now()
        delta = timedelta(days=m)
        date = (today - delta).strftime('%Y%m%d')
        get_cell_paging_kpi(s, date)

if __name__ == '__main__':
    s = login_pp('huangningcheng', 'Asdf.202103')
    get_sa_days_data(s,3)





