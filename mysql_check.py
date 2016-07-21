#coding=utf-8
import MySQLdb
import requests
import time

import wymlog
import logging
import mod_config

logger = wymlog.Logger('mysql_log.txt', 'mysql').getlog()

def init():
    fields = {}
    tags = {}
    start = time.time()

    try:
        conn = MySQLdb.connect(host=mod_config.getConfig("database", "dbhost"
        ), user=mod_config.getConfig("database", "dbuser"), passwd=
        mod_config.getConfig("database", "dbpassword"), port=int(
        mod_config.getConfig("database", "dbport")))
        
        cur = conn.cursor()
        cur.execute('create database if not exists cron_test')
        conn.select_db('cron_test')
        cur.execute('create table if not exists test(u varchar(100),v varchar(100))')
        conn.commit()
        cur.close()
        conn.close()
        fields.update({
            "status_code": 200,
            "response_time": time.time() - start,
            "success": 1,
        })
    except MySQLdb.Error, e:
        fields.update({
            "status_code": int(e.args[0]),
            "response_time": time.time - start,
            "success": 0,
        })
        logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    
    logger.debug("The connection is successful!")
    tags.update({
        "from_host": mod_config.getConfig("database", "dbhost"),
        "url": 'mysql_init',
    })

    post_to_mallard(fields, tags)

def execute(command, name):
    start = time.time()
    fields = {}
    tags = {}
    try:
        conn = MySQLdb.connect(host=mod_config.getConfig("database", "dbhost"
        ), user=mod_config.getConfig("database", "dbuser"), passwd=
        mod_config.getConfig("database", "dbpassword"), port=int(
        mod_config.getConfig("database", "dbport")))
        
        cur = conn.cursor()
        conn.select_db('cron_test')
        cur.execute(command)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        
        if len(name) == 8:
            fields.update({"status_code": 204,})
        else:
            fields.update({"status_code": 200,})
        if name == '':
            fields.update(result)
        fields.update({
            "response_time": time.time() - start,
            "success": 1,
        })

    except MySQLdb.Error, e:
        fields.update({
            "status_code": int(e.args[0]),
            "response_time": time.time - start,
            "success": 0,
        })
        logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    if name == '':
        name = 'status'
        for i in result:
            log_info = ''
            for j in i:
                log_info = log_info + ' ' + j
            logger.info(log_info)
    else:
        logger.debug("The %s is successful!" % (name))
    
    tags.update({
        "from_host": mod_config.getConfig("database", "dbhost"),
        "url": 'mysql_' + name,
    })

    post_to_mallard(fields, tags)

def dict2str(dictname):
    #join key value in dict with '=' and seprate elements with ','
    return ','.join('{0}={1}'.format(key, val) for key, val in sorted(
    dictname.items()))

def post_to_mallard(fields, tags):
    data2send.update({
        "tags": dict2str(tags),
        "fields": dict2str(fields),
        "timestamp": int(time.time()),
    })

    print data2send
    url = 'http://127.0.0.1:10699/v1/push'
    try:
        r = requests.post(url, json=[data2send])
        logger.info('post result to mallard: ' + r.text + '.msg:')
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    #var define
    data2send={
        "metric": "check_mysql",
        "tags": "",
        "endpoint": "",
        "value": 0,
        "fields": "",
        "timestamp": 1465963648,
        "counterType": "GAUGE",
        "step": 60,
    }

    #run testing jobs
    init()
    execute('insert into test(u,v) value(\'wym\',\'510\')', 'insertion')
    execute('select * from test', 'selection')
    execute('update test set u=\'510\' where u=\'wym\'', 'modification')
    execute('delete from test where v=\'510\'', 'deletion')
    execute('show status', '')
