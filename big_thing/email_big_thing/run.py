#!/bin/python

from big_thing_py.big_thing import *


from email.mime.text import MIMEText
import datetime
import argparse
import smtplib
import ssl
from secret import *


def send(address: str = None, text: str = None) -> bool:
    SMTP_SSL_PORT = 465  # SSL connection

    SENDER_EMAIL = address

    RECEIVER_EMAIL = SENDER_EMAIL

    if 'gmail' in address:
        SMTP_SERVER = "smtp.gmail.com"
        SENDER_PASSWORD = EMAIL_PASSWORD_GMAIL
    elif 'naver' in address:
        SMTP_SERVER = "smtp.naver.com"
        SENDER_PASSWORD = EMAIL_PASSWORD_NAVER
    elif 'live' in address:
        SMTP_SERVER = "smtp.live.com"
        SENDER_PASSWORD = EMAIL_PASSWORD_LIVE

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SSL_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        msg = MIMEText(
            f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \n{text}')
        msg['From'] = SENDER_EMAIL
        msg['Subject'] = 'TEST'
        msg['To'] = RECEIVER_EMAIL
        result = server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

    if result is not {}:
        return True
    else:
        return False


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='basic_thing', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='127.0.0.1', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=1883, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=60, help="alive cycle")
    parser.add_argument("--auto_scan", '-as', action='store_true',
                        required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true',
                        required=False, help="log enable")
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    tag_list = [SoPTag(name='email')]
    function_list = [SoPFunction(func=send,
                                 return_type=SoPType.BOOL,
                                 tag_list=tag_list,
                                 arg_list=[SoPArgument(name='address',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000)),
                                           SoPArgument(name='text',
                                                       type=SoPType.STRING,
                                                       bound=(0, 10000))])]
    value_list = []

    thing = SoPBigThing(name=args.name, ip=args.host, port=args.port, alive_cycle=args.alive_cycle,
                        service_list=function_list + value_list)
    return thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()