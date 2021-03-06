
import json
import smtplib
import socks, socket

from datetime import date, timedelta, datetime
from pathlib import Path
from email.mime.text import MIMEText
from sshtunnel import SSHTunnelForwarder

oper_list = ['LTN','AppleDaily', 'DogNews', 'BusinessTimes','ChinaElectronicsNews','Chinatimes']
#oper_list = ['AppleDaily']
PATH   = '../00_corpus2/'          # testing (small) corpus
#PATH = '/data2/Dslab_News/'        # full corpus
report = ''

#print(yesterday.strftime('%Y%m%d'))

# check whether dataleak
def check_a_day(target_day,report):
    for oper_name in oper_list:

        p0 = Path(PATH+oper_name+'/'+target_day.strftime('%Y%m%d'))
        p1 = Path(PATH+oper_name+'/'+target_day.strftime('%Y%m%d') + '/' + target_day.strftime('%Y%m%d') + '.json')
        # check folder exist
        if not p0.exists():
            print('can NOT find folder=> \t' + str(p0))
            continue

        # check summary-json exist
        if not p1.exists():
            print('can NOT find json file=>\t' + str(p1) + ' missing')
            continue

        # check each file in json is exactly exist
        fn        = open(str(p1))
        json_data = fn.read()                                             # for extrieve news number from a json, loading it first
        data      = json.loads(json_data)
        day_art   = len(data)
        miss_count= 0

        for j_item in data:
            BigCategory = data[j_item]['BigCategory']
            Category    = data[j_item]['Category']
            Title       = data[j_item]['Title']
            p2_root     = PATH+oper_name+'/'+target_day.strftime('%Y%m%d')       # ./LTN/20181211
            p2_middle   = '/' + BigCategory + '/' + Category + '/' if Category != '' else  BigCategory # ./LTN/20181211/BigCategory/Category
            p2_end      = target_day.strftime('%Y%m%d')+'_'+ Title + '.json'     # ./LTN/20181211/BigCategory/Category/20181211_Tilte.json
            p2          = Path(p2_root + p2_middle + p2_end)

            if not p2.exists():
                if not Path(p2_root+p2_middle).exists():
                    #print(str(p2_root)+str(p2_middle) + ' is missing')
                    report += str(p2_root) + str(p2_middle) + ' is missing [middle level]\n'
                else:
                    #print(str(p2) + ' is missing')
                    report += str(p2) + ' is missing\n'
                miss_count += 1
        fn.close()
        if miss_count != 0:
            #print('{:s} {:20s} completed, json number {:03d}, error number {:03d}'.format(target_day.strftime('%Y%m%d'),oper_name,day_art,miss_count))
            report += '{:s} {:20s} completed, json number {:03d}, error number {:03d}\n'.format(target_day.strftime('%Y%m%d'),oper_name,day_art,miss_count)
        return report

#================================================================
# send mail
#================================================================
def send_mail(email_report):
    # ================================================================
    # port forwarding
    # ================================================================
    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, 'localhost', 6666)
    socket.socket = socks.socksocket

    # https://amoshyc.github.io/blog/2018/sending-gmail-in-python.html
    gmail_user = 'ailabnews@gmail.com'
    gmail_password = 'icrd0000' # your gmail password

    msg = MIMEText(email_report)
    msg['Subject'] = 'AI lab News Spider Report: ' + str(target_day.strftime('%Y%m%d'))
    msg['From'] = gmail_user
    #msg['To'] = 'chen.yongcheng@gmail.com;elic7772425@gmail.com'
    msg['To'] = 'chen.yongcheng@gmail.com'

    # SSL method
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()

    # NO SSL
    #server = smtplib.SMTP('smtp.gmail.com', 587)
    #server.starttls()


    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()

    print('Email sent!')

def Lab2LongYuan_port_forward():
    service =  SSHTunnelForwarder((22,6666),ssh_password='icrd00',ssh_username='alvin')
    


#================================================================
# check for a range
#================================================================
'''
for i in range(1,30):
    target_day = datetime(2018, 11, i, 18, 00)
    check_a_oper_name(target_day)
'''

#================================================================
# check yesterday and send report by email
#================================================================
#target_day = date.today() - timedelta(1)
target_day = datetime(2018, 11, 8, 18, 00)
email_report = check_a_day(target_day,report)

service = SSHTunnelForwarder(('localhost',22),ssh_password='icrd00',ssh_username='alvin',remote_bind_address=('60.250.226.78',6666))
print(service)
print('---------------------------n')
send_mail(email_report)




