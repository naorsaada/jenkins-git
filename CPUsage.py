from time import sleep
import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def mailToUser(parameter, value):
    mail_content = str(datetime.datetime.now())+'\nYour '+parameter+' usage is higher then expected\n'+parameter+' usage was around '+str(value)+'% in the last minute!'
    
    sender_address = 'Naor.mor.netflix@Gmail.com'
    sender_pass = 'MHMSN123'
    receiver_address = 'Naor1512@Gmail.com'
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = parameter+' Usage Alert!!!'
    
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    
    #Create SMTP session for sending the mail
    #use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)
    #enable security
    session.starttls() 
    #login with mail_UN and password
    session.login(sender_address, sender_pass)

    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

def avg_limit_test(CPU_avg,memory_avg):
    #we will send email about high usage if we go over the 'load limit' parameter.
    load_limit = 80 
    print ('average CPU usage in the last minute is: '+str(CPU_avg))
    print ('average memory usage in the last minute is: '+str(memory_avg))

    if CPU_avg > load_limit and memory_avg > load_limit:
        mailToUser('CPU', CPU_avg)
        mailToUser('Memory', memory_avg)
        
    elif CPU_avg > load_limit:
        mailToUser('CPU', CPU_avg)
        
    elif memory_avg > load_limit:
        mailToUser('Memory', memory_avg)

secondsCounter = 1
interval_time = 60 #seconds
CPU_counter = 0
memory_counter = 0
CPU_avg = 0
memory_avg = 0

while secondsCounter < interval_time:
    #get CPU utilization, Return a float representing the current system-wide CPU utilization as a percentage.
    CPU_usage = psutil.cpu_percent()
    print ('CPU usage: '+str(CPU_usage)+'%')
    
    #get memory usage, usage calculated as (total - available) / total * 100
    memory_usage = dict(psutil.virtual_memory()._asdict())
    print ('Memory usage: '+str(memory_usage['percent'])+'%\n')

    CPU_counter += CPU_usage
    CPU_avg = CPU_counter / secondsCounter
    
    memory_counter += float(memory_usage['percent'])
    memory_avg = memory_counter / secondsCounter
	
    secondsCounter += 1

    if secondsCounter == interval_time - 1:
        avg_limit_test(CPU_avg, memory_avg)
        secondsCounter = 1
        CPU_counter = 0
        memory_counter = 0
        CPU_avg = 0
        memory_avg = 0

    sleep(1.0)
