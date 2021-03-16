import matplotlib
matplotlib.rcParams['font.family']
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
import pymysql
import matplotlib.pyplot as plt


font_name = fm.FontProperties(fname = 'C:/Windows/Fonts/malgun.ttf').get_name()
matplotlib.rc('font', family = font_name)
matplotlib.rcParams['axes.unicode_minus'] = False


conn = pymysql.connect(host = 'skuser57-instance.ctxvewe48g71.us-west-2.rds.amazonaws.com',port = 3306, user = 'admin', password = 'pax5022kr', db = 'mydb')
curs = conn.cursor()

sql = "SELECT * FROM my_topic_users"
curs.execute(sql)
rows = curs.fetchall()

df  = pd.read_sql(sql, conn)

def change_money(data):
    data = data.replace("$","")
    if data[-1] == 'M':
        data = data.replace("M","")
        data = float(data)*1000000
    elif data[-1] == 'K':
        data = data.replace("K","")
        data = float(data)*1000
    return int(data)

def change_people(data):
    return float(data.replace(",",""))

df['weekend'] = df['weekend'].apply(change_money)
df = df.sort_values(by=['weekend'], axis=0, ascending=False)
fig = plt.figure()
ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
ax.plot(df['title'],df['weekend'])
ax.set_xlabel('title')
ax.set_ylabel('weekend gross')
ax.set_title('movie weekend gross')
plt.xticks(rotation=45)
plt.show()


df['gross'] = df['gross'].apply(change_money)
df = df.sort_values(by=['gross'], axis=0, ascending=False)
fig = plt.figure()
ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
ax.plot(df['title'],df['gross'])
ax.set_xlabel('title')
ax.set_ylabel('total gross')
ax.set_title('movie total gross')
plt.xticks(rotation=45)
plt.show()

print(df)

df = df.sort_values(by=['rating'], axis=0, ascending=False)
fig = plt.figure()
ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
ax.barh(df['title'],df['rating'])
ax.set_xlabel('title')
ax.set_ylabel('rating')
ax.set_title('movie rating')
plt.xticks(rotation=45)
plt.show()
print(df)

df['people'] = df['people'].apply(change_people)
df = df.sort_values(by=['people'], axis=0, ascending=False)
fig = plt.figure()
ax = fig.add_axes([0.1, 0.3, 0.8, 0.6])
ax.plot(df['title'],df['people'])
ax.set_xlabel('title')
ax.set_ylabel('people')
ax.set_title('movie people')
plt.xticks(rotation=45)
plt.show()
print(df)

conn.close()