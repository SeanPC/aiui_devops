#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb,re,xlwt,sys,time

def mysql(cursor,sql):
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
    #import pdb;pdb.set_trace()
    #mysql basic info
    dbhost = ''
    dbuser = 'ooofans'
    dbpassword = '3aG92f20S2owf8M2'
    db = 'ticketdb'    
    
    #excel info and title
    date = time.strftime("%Y%m%d", time.localtime())
    excel_name = 'order_data_%s.xls' % date
    excel = xlwt.Workbook()
    sheet = excel.add_sheet(u'藕粉网订单信息导出')
    #title = [u'订单号',u'收件人姓名',u'收件人联系电话',u'省',u'市',u'区',u'详细地址',u'托寄物内容',u'快递产品',u'付款方式',u'身份证号码',u'演出信息',u'付款时间',u'单价',u'数量',u'运费',u'总价',u'支付渠道',u'订单状态']
    title = [u'订单号',u'收件人姓名',u'收件人联系电话',u'地址',u'托寄物内容',u'快递产品',u'付款方式',u'身份证号码',u'演出信息',u'付款时间',u'单价',u'数量',u'运费',u'总价',u'支付渠道',u'订单状态']
    status = [u'待付款',u'待出票',u'已出票',u'已发货',u'交易完成',u'已申请退款',u'交易取消',u'已退款',u'交易关闭',u'付款完成（未收到异步通知结果）']
    pay = [u'支付宝',u'微信',u'银联']
    deliver = [u'快递',u'上门自取']
    col = range(len(title))
    for i in col:
        sheet.write(0,i,title[i])
    j = 1
    
    #build mysql connection
    try:    
        sqlconnect = MySQLdb.connect(dbhost,dbuser,dbpassword,db,charset='utf8')
        cursor = sqlconnect.cursor()
    except:
        print "Failed to connect database"
        sys.exit(1)
    for serial in sys.argv[1].split(','):
        try:
            sql = "select serial,raddressid,deliverytype,checkprice,status,title,createtime,deliveryfee,paytype,userid from user_order_list where serial='%s';" % serial
            info0 = mysql(cursor,sql)
            #print info0[1],info0[0]
            if info0[2] == 1:
                sql = "select province,city,district,address,uname,tel,idcard from user_recv_address where id='%s';" % info0[1]
                print 'send by diliver'
            else:
                sql = "select province,city,district,address,uname,tel,idcard,id from user_recv_address where userid='%s' order by id desc limit 1;" % info0[9]
            info1 = mysql(cursor,sql)
            #print info0[0],info1[7]
            sql = "select singleprice,sum(pcount) from ticket_order_product_list where serial='%s';" % serial
            info2 = mysql(cursor,sql)
            sql = " select updatetime from pay_record_status_notify where ordercode='%s' order by id desc limit 1;" % serial
            paytime = str(mysql(cursor,sql)[0])
        except Exception as e:
            print 'data error when execute sql: %s for serial %s' % (sql,serial)
            continue
        #move id card to the specified column
        address = info1[3]
        idcard = info1[6]
        # match = re.findall(ur'[\u4E00-\u9FA5]{2,4}[ +]*[0-9a-zA-Z]{18}',address)
        # if match:
            # address = address.replace(match[0],'')
            # idcard += ",%s" % match[0] 
        address = info1[0]+info1[1]+info1[2]+address
        #row = [info0[0],info1[4],info1[5],info1[0],info1[1],info1[2],address,u'门票','',deliver[info0[2]-1],idcard,info0[5],paytime,info2[0],info2[1],info0[7],info0[3],pay[info0[8]-1],status[info0[4]-1]]
        row = [info0[0],info1[4],info1[5],address,u'门票','',deliver[info0[2]-1],idcard,info0[5],paytime,info2[0],info2[1],info0[7],info0[3],pay[info0[8]-1],status[info0[4]-1]]
        for i in col:
            sheet.write(j,i,row[i])
        j = j+1
    sqlconnect.close()
    excel.save(excel_name)

if __name__ == '__main__':
    gen_excel()

