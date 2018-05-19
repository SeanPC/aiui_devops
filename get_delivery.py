#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb,re,xlwt,sys,time

def init_mysql():
    global sqlconnect,cursor
    dbhost = 'rm-2ze2679z58k5p87ze.mysql.rds.aliyuncs.com'
    dbuser = 'ooofans'
    dbpassword = '3aG92f20S2owf8M2'
    db = 'ticketdb'  
    try:    
        sqlconnect = MySQLdb.connect(dbhost,dbuser,dbpassword,db,charset='utf8')
        cursor = sqlconnect.cursor()
    except:
        print "Failed to connect database"
        sys.exit(1)

def mysql(sql):
    try:
        cursor.execute(sql)
        res = cursor.fetchall()[0]
        if not res:
            print 'result empty sql:%s' % sql
            raise
        return res
    except Exception as e:
        print 'sql errors when execute %s' % sql
        raise   
        
def gen_excel():
#user_order_list;user_bind_info;user_recv_address;ticket_order_product_list
    #excel info and title
    date = time.strftime("%Y%m%d", time.localtime())
    excel_name = 'deliver_data_%s.xls' % date
    excel = xlwt.Workbook()
    sheet = excel.add_sheet(u'藕粉网快递信息导出')
    title = [u'订单号',u'收件人姓名*',u'收件人联系电话*',u'省*',u'市*',u'详细地址*',u'托寄物内容*',u'快递产品*',u'付款方式*',u'身份证号码']
    col = range(len(title))
    for i in col:
        sheet.write(0,i,title[i])
    j = 1   
    for serial in sys.argv[1].split(','):
        sql = "select raddressid from user_order_list where serial='%s';" % serial
        raddressid = mysql(sql)[0]
        if raddressid == 0:
            print 'The ticket %s will be got by door' % serial
            continue
        sql = "select uname,tel,province,city,address,idcard from user_recv_address where id='%s';" % raddressid
        info = mysql(sql)
        info = [serial,info[0],info[1],info[2],info[3],info[4],'','','',info[5]]
        for i in col:
            sheet.write(j,i,info[i])
        j = j+1
    sqlconnect.close()
    excel.save(excel_name)

if __name__ == '__main__':
    init_mysql()
    gen_excel()

