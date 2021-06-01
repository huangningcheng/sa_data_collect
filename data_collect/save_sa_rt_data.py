from data_collect.login_emos import *
import pandas as pd
import json
from datetime import datetime,timedelta

def get_sa_city_rt_data(s,rt_time):
    url = "http://10.53.160.65/jksdev_190_171_8050/sa/api/realTime/loadRealTimeData"
    fileurl = '../data/sa_city_rt_daily.xls'
    columns = ["时间", "地市", "初始注册请求次数", "移动性注册请求次数", "初始注册成功", "初始注册成功率(排除用户原因)",
               "移动性注册成功率","鉴权成功率", "业务请求成功率", "PDU会话建立成功率", "寻呼请求次数", "寻呼成功率", "寻呼平均响应时延"]
    if not os.path.exists(fileurl):
        df = pd.DataFrame(columns=columns)
        df.to_excel(fileurl,sheet_name='SA地市实时KPI指标',index=None)
    df = pd.read_excel(fileurl)
    if rt_time not in list(df['时间'].astype('str')):
        payload = {"area": "全省","queryTime": rt_time,"type": "realSignalCity"}
        r = s.post(url, json=payload)
        js = json.loads(r.text)
        citydatas = js['data']['rows']
        #print(rt_time)
        if len(citydatas):
            for citydata in citydatas:
                #print(citydata['city_name'])
                #print(len(citydata))
                if len(citydata) == 40:
                    citydataform = [
                        [rt_time, citydata['city_name'], citydata['i_register_req'], citydata['m_register_req'],
                         citydata['i_register_rate'],
                         citydata['i_register_rate2'], citydata['m_register_rate'], citydata['authentication_rate'],
                         citydata['service_rate'],
                         citydata['pdu_rate'], citydata['paging_req'], citydata['paging_rate'],
                         citydata['paging_delay_av']]]
                    df1 = pd.DataFrame(citydataform, columns=columns)
                    df = df.append(df1)

    df.to_excel(fileurl, index=None)

def get_upf_city_rt_data(s,rt_time):
    url = "http://10.53.160.65/jksdev_190_171_8050/realTime/api/sa/loadRealTimeData"
    fileurl = '../data/upf_city_rt_daily.xls'
    columns = ["时间", "网元", "上行流量(GB)", "下行流量(GB)", "上行RTT时延(ms)", "下行RTT时延(ms)",
               "HTTP成功率(%)","500KB下载速率(kbps)"]
    if not os.path.exists(fileurl):
        df = pd.DataFrame(columns=columns)
        df.to_excel(fileurl,sheet_name='UPF地市实时KPI指标',index=None)
    df = pd.read_excel(fileurl)
    if rt_time not in list(df['时间'].astype('str')):
        payload = {"ne": "","queryTime": rt_time,"type": "realNeZX"}
        r = s.post(url, json=payload)
        js = json.loads(r.text)
        citydatas = js['data']['rows']
        #print(rt_time)
        if len(citydatas):
            for citydata in citydatas:
                #print(citydata['city_name'])
                #print(len(citydata))
                if len(citydata) == 17:
                    citydataform = [[rt_time, citydata['ne_name'], citydata['upflow'], citydata['downflow'], citydata['up_rtt_delay'],
                         citydata['down_rtt_delay'],citydata['http_suc_rate'],citydata['http_dl_rate500']]]
                    df1 = pd.DataFrame(citydataform, columns=columns)
                    df = df.append(df1)

    df.to_excel(fileurl, index=None)

def get_sgw_city_rt_data(s,rt_time):
    url = "http://10.53.160.65/jksdev_190_171_8050/realTime/api/lte/loadLteData"
    fileurl = '../data/sgw_city_rt_daily.xls'
    columns = ["时间", "网元", "上行流量(MB)", "下行流量(MB)", "tcp时延(ms)","HTTP成功率(%)","http下载速率(kbps)"]
    if not os.path.exists(fileurl):
        df = pd.DataFrame(columns=columns)
        df.to_excel(fileurl,sheet_name='SGW地市实时KPI指标',index=None)
    df = pd.read_excel(fileurl)
    if rt_time not in list(df['时间'].astype('str')):
        payload = {"queryTime": rt_time,"type": "lteSgw"}
        r = s.post(url, json=payload)
        js = json.loads(r.text)
        citydatas = js['data']['rows']
        #print(rt_time)
        if len(citydatas):
            for citydata in citydatas:
                #print(citydata['city_name'])
                #print(len(citydata))
                if len(citydata) == 8:
                    citydataform = [[rt_time, citydata['sgw_name'], citydata['ulTraffic'], citydata['dlTraffic'], citydata['tcpAvgTime'],
                         citydata['httpSuccRate'],citydata['httpAvgDlRate']]]
                    df1 = pd.DataFrame(citydataform, columns=columns)
                    df = df.append(df1)

    df.to_excel(fileurl, index=None)

def get_period_data(s,n=30):
    minutes = list(range(1, n))
    minutes.reverse()
    # print(days)
    for n in minutes:
        today = datetime.now()
        delta = timedelta(minutes=n)
        rt_time = (today - delta).strftime('%Y%m%d%H%M')
        get_sa_city_rt_data(s, rt_time)
        #get_upf_city_rt_data(s, rt_time)
        #get_sgw_city_rt_data(s, rt_time)

if __name__ == '__main__':
    s = login_pp('huangningcheng', 'Asdf.202103')
    get_period_data(s,n=1440*5)
