#!/usr/bin/python3
import sys
import configparser
import urllib.request
import os


def parse_phone(number, send):
    if len(number) > 12:
        print('Phone number has to many digits please double check number.')
        sys.exit(1)
    else:
        prep_number = list(number)
        print(prep_number)
        if send:
            prep_number.append('SEND')
        print(':'.join(prep_number))
        return ':'.join(prep_number)

def main():
    """
    This takes care of sending digits to your grandstream phone and optionally dialing.
    """
    if len(sys.argv) < 2:
        print('Please enter the digits dialed as a command line argument')
        sys.exit(1)

    config = configparser.ConfigParser()
    conf_file = config.read('dial_config.ini')

    if not conf_file:
        print('Configuration file not found, please ensure file is located in {}'.format(os.getcwd()))
        print('Ensure file is named dial_config.ini')
        sys.exit(1)

    dial = config['dial']
    if not dial:
        print('Improperly prepared config file dial section is not found, please check spelling')
        sys.exit(1)

    host = dial.get('host') or 'localhost'
    passcode = dial.get('passcode') or 'admin'
    send = dial.get('send') or 'true'
    add_send = send.lower() == 'true'
    req_header = {'Host': host,
                  'User-Agent': 'Python dial script',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Language': 'en-US,en;q=0.5',
                  'Accept-Encoding': 'gzip, deflate',
                  'Connection': 'keep-alive',
                  'Cookie': 'session-role=admin; session-identity=12345; TRACKID=789',
                  'Upgrade-Insecure-Requests': 1,
                  'Pragma': 'no-cache',
                  'Cache-Control': 'no-cache', }

    if sys.argv[1].isdigit():
        num = parse_phone(sys.argv[1], add_send)
    else:
        print('Please ensure phone number entered contains only numbers')
        sys.exit()

    req = urllib.request.Request('http://{}/cgi-bin/api-send_key?passcode={}&keys={}'.format(host, passcode, num),
                                 headers=req_header)

    with urllib.request.urlopen(req) as response:
        if response.status != 200:
            print('Request returned a {}:{} please check your configuration and try again.'.format(response.status, response.reason))

if __name__ == "__main__":
    main()