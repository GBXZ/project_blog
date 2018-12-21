# 发送邮件部分(以后换成异步)
from django.core.mail import send_mail

to_address = '18814124132@139.com'
from_address = 'hupan0818@163.com'


def send_email(subject, message):
    send_mail(subject, message, from_address, recipient_list=[to_address])
