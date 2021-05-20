import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import datetime

def init():
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

def show_epsfb_e2v(start_time,end_time = 0,city = '厦门'):
    init()
    fileurl = '../data/epsfb_city_daily.xls'
    df = pd.read_excel(fileurl)
    df['日期'] =pd.to_datetime(df['日期'].apply(str))
    #df['日期'] = df['日期'].apply(str)
    if end_time == 0:
        df = df.loc[(df['地市'] == city) & (df['日期'] >= start_time)]
    else:
        df = df.loc[(df['地市'] == city) & df['日期'] >= start_time & df['日期'] <= end_time]
    #df = df.reset_index()
    #print(df)
    df['日期'] = df['日期'].apply(lambda x : x.strftime('%m-%d'))
    plt.plot(df['日期'], df['E2V时延'])
    plt.xticks(rotation=-90, fontsize=7)
    plt.title(city+"E2V接续时延（单位：ms）")
    #plt.show()

def show_plot_epsfb_e2v(start_time,end_time = 0):
    init()
    fileurl = '../data/epsfb_city_daily.xls'
    df = pd.read_excel(fileurl)
    df['日期'] =pd.to_datetime(df['日期'].apply(str))
    #df['日期'] = df['日期'].apply(str)
    citys = set(df['地市'])
    citys.remove('全省')
    for city in citys:
        #print(city)
        if end_time == 0:
            epsfbdata = df.loc[(df['地市'] == city) & (df['日期'] >= start_time)]
        else:
            epsfbdata = df.loc[(df['地市'] == city) & df['日期'] >= start_time & df['日期'] <= end_time]
        #df = df.reset_index()
        #print(df)
        quiretime = epsfbdata['日期'].apply(lambda x : x.strftime('%m-%d'))
        plt.plot(quiretime, epsfbdata['E2V时延'],label=city)
    plt.legend(loc='lower center', ncol=len(citys), fontsize=5)
    plt.xticks(rotation=-90, fontsize=7)
    plt.title("各地市E2V接续时延（单位：ms）")
    plt.show()

def show_bar_epsfb_e2v(start_time):
    init()
    fileurl = '../data/epsfb_city_daily.xls'
    df = pd.read_excel(fileurl)
    df['日期'] = pd.to_datetime(df['日期'].apply(str))
    df = df.loc[(df['日期'] == start_time) & (df['地市'] != '全省')].sort_values(by=["E2V时延"])
    #df = df.loc[(df['日期'] == start_time) ].sort_values(by=["E2V时延"])
    recs = plt.bar(df['地市'], df['E2V时延'])
    for rec in recs:
        h = rec.get_height()
        plt.text(rec.get_x() + rec.get_width() / 2, h, str(h)+'ms', ha='center', va='bottom',fontsize=10)
    plt.title("地市E2V接续时延（日期："+start_time+")")
    plt.show()

def show_xm_5G_user(start_time,city='厦门'):
    init()
    arrowprops = dict(arrowstyle='->',connectionstyle='arc3')
    fileurl = '../data/sa_city_daily.xls'
    df = pd.read_excel(fileurl)
    df['日期'] = pd.to_datetime(df['日期'].apply(str))
    sadata = df.loc[(df['地市'] == city) & (df['日期'] >= start_time)].sort_values(by='日期').reset_index(drop=True)
    quiretime = sadata['日期'].apply(lambda x: x.strftime('%m-%d'))
    dadalen = len(sadata['5G终端用户数'])-1
    distance = sadata['5G终端用户数'][dadalen]*0.08
    plt.plot(quiretime, sadata['5G终端用户数'], '^',ls='-',label='5G终端用户数')
    plt.annotate(str(round(sadata['5G终端用户数'][dadalen]/10000,1))+"万",xy=(dadalen,sadata['5G终端用户数'][dadalen]),
                 xytext=(dadalen-1,sadata['5G终端用户数'][dadalen]-distance),arrowprops=arrowprops)
    plt.plot(quiretime, sadata['NSA活跃用户'], 'o',ls='-',label='NSA活跃用户')
    plt.annotate(str(round(sadata['NSA活跃用户'][dadalen] / 10000, 1)) + "万", xy=(dadalen, sadata['NSA活跃用户'][dadalen]),
                 xytext=(dadalen - 1, sadata['NSA活跃用户'][dadalen]-distance), arrowprops=arrowprops)
    plt.plot(quiretime, sadata['SA活跃用户数'], 'v',ls='-',label='SA活跃用户数')
    plt.annotate(str(round(sadata['SA活跃用户数'][dadalen] / 10000, 1)) + "万", xy=(dadalen, sadata['SA活跃用户数'][dadalen]),
                 xytext=(dadalen - 1, sadata['SA活跃用户数'][dadalen] - distance), arrowprops=arrowprops)
    plt.legend(loc='upper left', ncol=3, fontsize=8)
    plt.xticks(rotation=-90, fontsize=7)
    plt.title(city+"5G用户数")
    plt.show()

def show_city_5G_coverrate(start_time):
    init()
    fileurl = '../data/sa_city_daily.xls'
    df = pd.read_excel(fileurl)
    df['5G覆盖率'] = round(100*(df['SA活跃用户数']+df['NSA活跃用户'])/df['5G软开关开启'],1)
    #print(df[['地市','5G覆盖率']])
    df['日期'] = pd.to_datetime(df['日期'].apply(str))
    df = df.loc[(df['日期'] == start_time) & (df['地市'] != '全省')].sort_values(by=["5G覆盖率"],ascending=False)
    recs = plt.bar(df['地市'], df['5G覆盖率'])
    for rec in recs:
        h = rec.get_height()
        plt.text(rec.get_x() + rec.get_width() / 2, h, str(h), ha='center', va='bottom', fontsize=10)
    plt.title("5G用户网络覆盖率(单位：%)\n日期：" + start_time)
    plt.show()

def show_xm_5G_coverrate(start_time):
    init()
    fileurl = '../data/sa_xm_daily.xls'
    df = pd.read_excel(fileurl)
    df['5G覆盖率'] = round(100*(df['SA活跃用户数']+df['NSA活跃用户'])/df['5G软开关开启'],1)
    #print(df[['地市','5G覆盖率']])
    df['日期'] = pd.to_datetime(df['日期'].apply(str))
    df = df.loc[df['日期'] == start_time].sort_values(by=["5G覆盖率"],ascending=False)
    recs = plt.bar(df['区县'], df['5G覆盖率'])
    for rec in recs:
        h = rec.get_height()
        plt.text(rec.get_x() + rec.get_width() / 2, h, str(h), ha='center', va='bottom', fontsize=10)
    plt.title("厦门区县5G用户网络覆盖率(单位：%)\n日期：" + start_time)
    plt.show()

def show_plot_epsfb_e2e(start_time,end_time = 0):
    init()
    fileurl = '../data/epsfb_analysis_city_daily.xls'
    df = pd.read_excel(fileurl)
    df['日期'] =pd.to_datetime(df['日期'].apply(str))
    #df['日期'] = df['日期'].apply(str)
    citys = set(df['地市'])
    citys.remove('全省')
    for city in citys:
        #print(city)
        if end_time == 0:
            epsfbdata = df.loc[(df['地市'] == city) & (df['日期'] >= start_time)]
        else:
            epsfbdata = df.loc[(df['地市'] == city) & df['日期'] >= start_time & df['日期'] <= end_time]
        #df = df.reset_index()
        #print(df)
        quiretime = epsfbdata['日期'].apply(lambda x : x.strftime('%m-%d'))
        plt.plot(quiretime, epsfbdata['E2E接续时延'],label=city)
    plt.legend(loc='lower center', ncol=len(citys), fontsize=7)
    plt.xticks(rotation=-90, fontsize=7)
    plt.title("各地市E2E接续时延（单位：ms）")
    plt.show()

def show_plot_initregister_req(start_time,end_time = 0):
    init()
    fileurl = '../data/sa_city_rt_daily.xls'
    df = pd.read_excel(fileurl)
    df['时间'] =pd.to_datetime(df['时间'].apply(str))
    #df['日期'] = df['日期'].apply(str)
    citys = set(df['地市'])
    citys.remove('全省')
    for city in citys:
        #print(city)
        if end_time == 0:
            initregreq = df.loc[(df['地市'] == city) & (df['时间'] >= start_time)]
        else:
            initregreq = df.loc[(df['地市'] == city) & df['时间'] >= start_time & df['时间'] <= end_time]
        #df = df.reset_index()
        #print(df)
        quiretime = initregreq['时间'].apply(lambda x : x.strftime('%H:%M'))
        plt.plot(quiretime, initregreq['初始注册请求次数'],label=city)
    plt.legend(loc='lower center', ncol=len(citys), fontsize=7)
    plt.xticks(rotation=-90, fontsize=7)
    plt.title("各地市初始注册请求次数")
    plt.show()

def show_plot_mobileregister_req(start_time,end_time = 0):
    init()
    fileurl = '../data/sa_city_rt_daily.xls'
    df = pd.read_excel(fileurl)
    df['时间'] =pd.to_datetime(df['时间'].apply(str))
    #df['日期'] = df['日期'].apply(str)
    citys = set(df['地市'])
    citys.remove('全省')
    for city in citys:
        #print(city)
        if end_time == 0:
            initregreq = df.loc[(df['地市'] == city) & (df['时间'] >= start_time)]
        else:
            initregreq = df.loc[(df['地市'] == city) & df['时间'] >= start_time & df['时间'] <= end_time]
        #df = df.reset_index()
        #print(df)
        quiretime = initregreq['时间'].apply(lambda x : x.strftime('%H:%M'))
        plt.plot(quiretime, initregreq['移动性注册请求次数'],label=city)
    plt.legend(loc='lower center', ncol=len(citys), fontsize=7)
    plt.xticks(rotation=-90, fontsize=7)
    plt.title("各地市移动性注册请求次数")
    plt.show()

def show_plot_initregister_ratio(start_time,end_time = 0):
    init()
    fileurl = '../data/sa_city_rt_daily.xls'
    df = pd.read_excel(fileurl)
    df['时间'] =pd.to_datetime(df['时间'].apply(str))
    #df['日期'] = df['日期'].apply(str)
    citys = set(df['地市'])
    citys.remove('全省')
    citys.remove('三明')
    citys.remove('龙岩')
    citys.remove('莆田')
    citys.remove('宁德')
    citys.remove('漳州')
    citys.remove('南平')
    for city in citys:
        #print(city)
        if end_time == 0:
            initregreq = df.loc[(df['地市'] == city) & (df['时间'] >= start_time)]
        else:
            initregreq = df.loc[(df['地市'] == city) & df['时间'] >= start_time & df['时间'] <= end_time]
        #df = df.reset_index()
        #print(df)
        quiretime = initregreq['时间'].apply(lambda x : x.strftime('%H:%M'))
        plt.plot(quiretime, initregreq['初始注册成功率(排除用户原因)'],label=city)
    plt.legend(loc='lower center', ncol=len(citys), fontsize=7)
    plt.xticks(rotation=-90, fontsize=7)
    plt.title("各地市初始注册成功率(排除用户原因)")
    plt.show()

def show_plot_pdu_ratio(start_time,end_time = 0):
    init()
    fileurl = '../data/sa_city_rt_daily.xls'
    df = pd.read_excel(fileurl)
    df['时间'] =pd.to_datetime(df['时间'].apply(str))
    #df['日期'] = df['日期'].apply(str)
    citys = set(df['地市'])
    citys.remove('全省')
    #citys.remove('三明')
    #citys.remove('龙岩')
    #citys.remove('莆田')
    #citys.remove('宁德')
    #citys.remove('漳州')
    #citys.remove('南平')
    for city in citys:
        #print(city)
        if end_time == 0:
            initregreq = df.loc[(df['地市'] == city) & (df['时间'] >= start_time)]
        else:
            initregreq = df.loc[(df['地市'] == city) & df['时间'] >= start_time & df['时间'] <= end_time]
        #df = df.reset_index()
        #print(df)
        quiretime = initregreq['时间'].apply(lambda x : x.strftime('%H:%M'))
        plt.plot(quiretime, initregreq['PDU会话建立成功率'],label=city)
    plt.legend(loc='lower center', ncol=len(citys), fontsize=7)
    plt.xticks(rotation=-90, fontsize=7)
    plt.title("各地市PDU会话建立成功率")
    plt.show()

def show_plot_upf_flow(start_time,end_time = 0):
    init()
    fileurl = '../data/upf_city_rt_daily.xls'
    df = pd.read_excel(fileurl)
    df['时间'] =pd.to_datetime(df['时间'].apply(str))
    #df['日期'] = df['日期'].apply(str)
    upfs = ['XIMUPF201BZX','XIMUPF202BZX','XIMUPF203BZX','XIMUPF204BZX']

    for upf in upfs:
        #print(city)
        if end_time == 0:
            upf_flow = df.loc[(df['网元'] == upf) & (df['时间'] >= start_time)].sort_values(by='时间').reset_index(drop=True)
        else:
            upf_flow = df.loc[(df['网元'] == upf) & df['时间'] >= start_time & df['时间'] <= end_time].sort_values(by='时间').reset_index(drop=True)
        #df = df.reset_index()
        #print(df)
        quiretime = upf_flow['时间'].apply(lambda x : x.strftime('%H:%M'))
        plt.plot(quiretime, upf_flow['下行流量(GB)'],label=upf)
    plt.legend(loc='lower center', ncol=len(upfs), fontsize=7)
    plt.xticks(rotation=-90, fontsize=7)
    plt.title("各UPF下行流量(GB)")
    plt.show()

def show_plot_sgw_flow(start_time,end_time = 0):
    init()
    fileurl = '../data/sgw_city_rt_daily.xls'
    df = pd.read_excel(fileurl)
    df['时间'] =pd.to_datetime(df['时间'].apply(str))
    #df['日期'] = df['日期'].apply(str)
    upfs = ['XIMSAEGW2ABNK','XIMSAEGW2BBNK','XIMSAEGW2CBNK','XIMSAEGW2DBNK','XIMSAEGW2EBNK','XIMSAEGW2FBNK']

    for upf in upfs:
        #print(city)
        if end_time == 0:
            upf_flow = df.loc[(df['网元'] == upf) & (df['时间'] >= start_time)].sort_values(by='时间').reset_index(drop=True)
        else:
            upf_flow = df.loc[(df['网元'] == upf) & df['时间'] >= start_time & df['时间'] <= end_time].sort_values(by='时间').reset_index(drop=True)
        #df = df.reset_index()
        #print(df)
        quiretime = upf_flow['时间'].apply(lambda x : x.strftime('%H:%M'))
        plt.plot(quiretime, upf_flow['下行流量(MB)'],label=upf)
    plt.legend(loc='lower center', ncol=len(upfs), fontsize=7)
    plt.xticks(rotation=-90, fontsize=7)
    plt.title("各SAEGW下行流量(MB)")
    plt.show()

if __name__ == '__main__':
    '''
    plt.figure("sa kpi")
    plt.subplot(121)
    show_plot_epsfb_e2v('20210101')
    plt.subplot(122)
    show_bar_epsfb_e2v('20210303')
    plt.show()
    '''
    #show_plot_initregister_req('202105180800')
    #how_plot_initregister_ratio('202105170800')
    show_plot_mobileregister_req('202105200800')
    #show_plot_pdu_ratio('202105180800')
    #show_plot_sgw_flow('202105190000')
    show_plot_upf_flow('202105201200')
    #show_plot_epsfb_e2e('20210303')
    #show_plot_epsfb_e2v('20210320')
    #show_xm_5G_user('20210201',city='福州')
    #show_city_5G_coverrate('20210413')
    #show_xm_5G_coverrate('20210317')