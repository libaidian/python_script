#-*- coding: utf-8 -*-
#!/usr/bin/python
import paramiko
import threading
import time
import csv
import os


def ssh2(ip, username, passwd, path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd,  timeout=5)
        date = time.strftime('%Y%m%d', time.localtime(time.time()))
        date1 = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        new_path = os.path.join(path, date)
        if not os.path.isdir(new_path):
             os.makedirs(new_path)

        filename = ip +"_san_check.csv"
        filepath = new_path + "/"+filename
        f = open(filepath, 'a+')
        writer = csv.writer(f)

        writer.writerow([" command : uptime "])
        stdin, stdout, stderr = ssh.exec_command('uptime')
        out = stdout.read()
        uptime = out.split(' ')[3]
        if (int(uptime) > 100):
            uptimemsg = "uptime check is ok,"+ uptime + " days"
        else:
            uptimemsg = "the machine  has been restart ! please check out"

        writer.writerow([uptimemsg])

        writer.writerow([" command : fanshow "])
        stdin, stdout, stderr = ssh.exec_command('fanshow')
        out = stdout.readlines()
        i = 0
        for line in out:
             status = line.split(',')[0].split(' ')[3]
             if status != 'Ok':
                 writer.writerow([line])
                 i = i +1
        if i == 0:
             writer.writerow(["fan check pass"])

        writer.writerow([" command : psshow "])
        stdin, stdout, stderr = ssh.exec_command('psshow')
        out = stdout.readlines()
        for line in out:
             writer.writerow([line])
        writer.writerow([" command : hashow "])
        stdin, stdout, stderr = ssh.exec_command('hashow')
        out = stdout.readlines()
        for line in out:
             writer.writerow([line])
        writer.writerow([" command : tempshow "])
        stdin, stdout, stderr = ssh.exec_command('tempshow')
        out = stdout.readlines()
        for line in out:
             writer.writerow([line])
        writer.writerow([" command : errdump "])
        stdin, stdout, stderr = ssh.exec_command('errdump')
        out = stdout.readlines()
        for line in out :
            logdate = line.split(',')[0].split('-')[0]
            if logdate == date1 :

                writer.writerow([line])

        writer.writerow([" command : porterrshow "])
        stdin, stdout, stderr = ssh.exec_command('porterrshow')
        out = stdout.readlines()
        for line in out:
             writer.writerow([line])
        f.close()
        ssh.close()
    except Exception as e:
        print '%s\tException,": "\n'%(ip)+e


if __name__=='__main__':
    path = "/Users/libd/PycharmProjects/untitled/mypython/"
    threads = []   #多线程
    print "Begin......"
    iplist = ['ip1', 'ip2']
    username = "moni"
    passwdlist = ['pwd1', 'pwd2']
    for i in range(0, len(iplist)):
        ip = iplist[i]
        password = passwdlist[i]
        a=threading.Thread(target=ssh2, args=(ip, username, password, path))
        a.start()