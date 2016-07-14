#coding=utf-8
import MySQLdb
import re
import os
import sys,urllib

def init(password):
	try:
		conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd=password,port=3306)
		cur = conn.cursor()
		cur.execute('create database if not exists cron_test')
		conn.select_db('cron_test')
		cur.execute('create table if not exists test(u varchar(100),v varchar(100))')
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		return "Mysql Error %d: %s" % (e.args[0], e.args[1])
	return "The connection is successful!"

def execute(password,command,name):
	try:
		conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd=password,port=3306)
		cur = conn.cursor()
		conn.select_db('cron_test')
		cur.execute(command)
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		return "Mysql Error %d: %s" % (e.args[0], e.args[1])
	return "The %s is successful!" %(name)

password='cxq940215'
print init(password)
print execute(password,'insert into test(u,v) value(\'wym\',\'510\')','insertion')
print execute(password,'select * from test','selection')
print execute(password,'update test set u=\'510\' where u=\'wym\'','modification')
print execute(password,'delete from test where v=\'510\'','deletion')
