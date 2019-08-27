import json
import os
import time
import pymysql

liveon = '正在直播'
liveoff = '直播停止'

path = os.path.dirname(os.path.abspath(__file__))

config_file = open(path + '/roomid.json', encoding = "utf-8")
room = json.loads(config_file.read())['user']

check = 'sudo python3 ' + path + '/check.py'

while True:

	conn = pymysql.connect(
		host = 'localhost',
		port = 3306,
		user = 'root',           #MySQL用户名
		password = '123456',     #MySQL密码
		db = 'Monitor',    #数据库名称
		charset = 'utf8'
	)

	cursor = conn.cursor()

	for uid in room :
		SQL = 'select uid from monitor where uid=' + uid['uid']
		cursor.execute(SQL)
		res_select = cursor.fetchall()
		if res_select == () :
			SQL = 'insert into monitor(nickname, uid) values("' + uid['nickname'] + '", ' + uid['uid'] + ');'
			cursor.execute(SQL)
			conn.commit()
		
		out = os.popen(check + " " + uid['uid']).read().strip()
		if liveon == out :
			SQL = 'select live,nickname from monitor where uid=' + uid['uid'] + ';'
			cursor.execute(SQL)
			live_check = cursor.fetchone()
			if live_check[0] != 'NO' :
				os.system('sudo ' + path + '/send.sh ' + live_check[1])
			SQL = 'update monitor set live="ON" where uid=' + uid['uid'] + ';'
			cursor.execute(SQL)
			conn.commit()	
		elif liveoff == out:
			SQL = 'update monitor set live="OFF" where uid=' + uid['uid'] + ';'
			cursor.execute(SQL)
			conn.commit()	
	time.sleep(300)
