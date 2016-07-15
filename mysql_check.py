#coding=utf-8
import MySQLdb
import re
import os
import sys,urllib

import wymlog
import logging
import mod_config

logger = wymlog.Logger('mysql_log.txt','mysql').getlog()

def init():
	try:
		conn = MySQLdb.connect(host=mod_config.getConfig("database","dbhost"),user=mod_config.getConfig("database","dbuser"),passwd=mod_config.getConfig("database","dbpassword"),port=int(mod_config.getConfig("database","dbport")))
		cur = conn.cursor()
		cur.execute('create database if not exists cron_test')
		conn.select_db('cron_test')
		cur.execute('create table if not exists test(u varchar(100),v varchar(100))')
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))
	logger.debug("The connection is successful!")

def execute(command,name):
	try:
		#conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd=password,port=3306)
		conn = MySQLdb.connect(host=mod_config.getConfig("database","dbhost"),user=mod_config.getConfig("database","dbuser"),passwd=mod_config.getConfig("database","dbpassword"),port=int(mod_config.getConfig("database","dbport")))
		cur = conn.cursor()
		conn.select_db('cron_test')
		cur.execute(command)
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))
	logger.debug("The %s is successful!" %(name))

init()
execute('insert into test(u,v) value(\'wym\',\'510\')','insertion')
execute('select * from test','selection')
execute('update test set u=\'510\' where u=\'wym\'','modification')
execute('delete from test where v=\'510\'','deletion')
