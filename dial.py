#!/usr/bin/python3
import sys
import configparser
import urllib.request
import os
import tkinter


def filter_num(number):
    valid_nums = ['0', '1', '2', '3', '4', '5', '6', '7', 
                  '8', '9', '*', '#']
    if number.upper() == 'VM':
            return ['VM']
    clean_num = []
    for l in list(number):
        if l not in valid_nums:
            print('Invalid digit')
            sys.exit(1)
        else:
            if l == '#':
                clean_num.append('HASH')
            elif l == '*':
                clean_num.append('STAR')
            else:
                clean_num.append(l)
    return clean_num


def parse_phone(number, send):
    clean_num = filter_num(number)
    if send:
        clean_num.append('SEND')
    return ':'.join(clean_num)


def get_config():
    config = configparser.ConfigParser()
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'dial_config.ini')
    conf_file = config.read(conf_path)

    if not conf_file:
        print('Configuration file not found, please ensure file is located in {}'.format(os.getcwd()))
        print('Ensure file is named dial_config.ini')
        sys.exit(1)

    dial = config['dial']
    if not dial:
        print('Improperly prepared config file dial section is not found, \
               please check spelling')
        sys.exit(1)
    else:
        return dial


def send_keys(keys):
    dial = get_config()
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
    num = parse_phone(keys, add_send)
    req = urllib.request.Request('http://{}/cgi-bin/api-send_key?passcode={}&keys={}'.format(host, passcode, num),
                                 headers=req_header)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print('Request returned a {}:{} please check your \
                       configuration and try again.'.format(response.status,
                                                            response.reason))
    except urllib.error.URLError:
        print('There was an error with the url that accessed.  Attempted to access {}'.format(req))


def main():
    """
    This takes care of sending digits to your grandstream
    phone and optionally dialing.
    """
    if len(sys.argv) < 2:
        def get_text():
            send_keys(e1.get())
        master = tkinter.Tk()
        master.title("GS Dial")
        tkinter.Label(master, text="Enter Phone Number").grid(row=0)
        e1 = tkinter.Entry(master)
        e1.grid(row=0, column=1)
        tkinter.Button(master,
                       text='Quit',
                       command=master.quit).grid(row=3,
                                                 column=0,
                                                 sticky=tkinter.W,
                                                 pady=4)
        tkinter.Button(master,
                       text='Dial',
                       command=get_text).grid(row=3,
                                              column=1,
                                              sticky=tkinter.W,
                                              pady=4)
        e1.bind('<Return>', lambda _: get_text())
        e1.bind('<KP_Enter>', lambda _: get_text())
        tkinter.mainloop()
    else:
        send_keys(sys.argv[1])

if __name__ == "__main__":
    main()
