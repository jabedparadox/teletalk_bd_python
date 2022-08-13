import requests
import re
from bs4 import BeautifulSoup
import time
import datetime
import random
from prettytable import PrettyTable
from termcolor import colored, cprint
from tabulate import tabulate
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pickle
import os   

text = '\033[97m' + """
################# A Simple Python Module of Teletalk Bangladesh Ltd. ################# 
############# Developed by : Md Jabed Ali (jabed). jabed.akcc@gmail.com ##############
""" + '\033[00m'

table = [[text]]
output = tabulate(table, tablefmt='fancy_grid')
print('\n'+output)

def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)

def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def balance_transfer(recipient, amount):
    while not os.path.exists('teletalk'):
          print (color.RED + "\n    No session file exists. Login first." + color.END)
          teletalk_login()
          
    dashboard_headers = {
	    'Host': 'teletalk.com.bd',
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Referer': 'https://teletalk.com.bd/en/login-with-otp',
	    'Upgrade-Insecure-Requests': '1',
	    'Sec-Fetch-Dest': 'document',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-Site': 'same-origin',
	    'Sec-Fetch-User': '?1',
	}
    a = requests.get('https://teletalk.com.bd/en/e-selfcare', cookies=load_cookies('teletalk'), headers=dashboard_headers, verify=False)
    is_session_expired = bool(re.findall('id="user-balance">', str(a.text)))
    while not is_session_expired:
         from termcolor import colored, cprint
         cprint('\n    Session expired. Login in again.', 'red', attrs=['blink'])
         teletalk_login()
         a = requests.get('https://teletalk.com.bd/en/e-selfcare', cookies=load_cookies('teletalk'), headers=dashboard_headers, verify=False)
         #is_session_expired = bool(re.findall('id="user-balance">', str(a.text)))
         if 'id="user-balance">' in str(a.text):
            break
         
          
          
    soup = BeautifulSoup(a.text, 'html.parser')
    _session_key = str(re.findall('"_session_key" type="hidden" value="(.*?)"', str(soup), re.DOTALL)[0])
    _token = str(re.findall('"_token" type="hidden" value="(.*?)"', str(soup), re.DOTALL)[0])
    detail = soup.find_all("div", {"class": "col-lg-7 col-xlg-7 col-sm-6 col-xs-10"})
    detail_balance = soup.find_all(id="balance-main")
    name = str(re.findall('<h3 class="m-b-0">(.*?)<', str(detail[0]), re.DOTALL)[0])
    balance = str(re.findall('id="user-balance">(.*?)<', str(soup), re.DOTALL)[0]).replace('\n', '').replace('                            ', ' ')
    validity = str(re.findall('<h3 class="m-b-0 font-light">(.*?)<', str(detail_balance), re.DOTALL)[0]).replace('\n', '')

    data = {
	  '_handler': 'onTransfer',
	  '_session_key': _session_key,
	  '_token': _token,
	  'recipient': recipient,
	  'amount': amount
	}
    balnce_transfer_requests = requests.post('https://teletalk.com.bd/en/e-selfcare', headers=dashboard_headers, cookies=load_cookies('teletalk'), data=data,  allow_redirects=True, verify=False)
    print (color.BLUE + "\n    Balance transfer otp has been sent to your mobile."+color.END)
    otp = input(color.BLUE + "    Enter balance transfer otp : "+color.END)
    print (color.BLUE + "    Amount {} tk will be transfer to this number {}.".format(amount, recipient)+color.END)
    transfer_amount = input('\n    To confirm enter "Y" or "N." : ')

    while transfer_amount != 'N' and transfer_amount != 'Y' :
         from termcolor import colored, cprint
         print ('    Enter ' ,colored('Y', 'green'), 'or', colored('N.', 'red'))
         transfer_amount = input('\n    To confirm enter "Y" or "N." : ')

    
    soup = BeautifulSoup(balnce_transfer_requests.text, 'html.parser')
    _session_key = str(re.findall('"_session_key" type="hidden" value="(.*?)"', str(soup), re.DOTALL)[0])
    _token = str(re.findall('"_token" type="hidden" value="(.*?)"', str(soup), re.DOTALL)[0])
    data = {
	  '_handler': 'onSubmitOtp',
	  '_session_key': _session_key,
	  '_token': _token,
	  'otp': otp
	}
    balnce_transfer_requests_submit = requests.post('https://teletalk.com.bd/en/submit-otp-balance-transfer', headers=dashboard_headers, cookies=load_cookies('teletalk'), data=data, verify=False,  allow_redirects=True)
    verification_transfer = bool(re.findall('Verification failed', str(balnce_transfer_requests_submit.text)))

    if verification_transfer:
       print (color.RED+ color.BLINK +"    Otp Verification failed. Start over.\n" + color.END)

       
    if not verification_transfer:
       transfer = '\n    Balance transferred successfully. Amount {}. Number {}.'.format(amount, recipient)
       soup = BeautifulSoup(balnce_transfer_requests_submit.text, 'html.parser')
       detail = soup.find_all("div", {"class": "col-lg-7 col-xlg-7 col-sm-6 col-xs-10"})
       detail_balance = soup.find_all(id="balance-main")
       name = str(re.findall('<h3 class="m-b-0">(.*?)<', str(detail[0]), re.DOTALL)[0])
       balance = str(re.findall('id="user-balance">(.*?)<', str(soup), re.DOTALL)[0]).replace('\n', '').replace('                            ', ' ')
       validity = str(re.findall('<h3 class="m-b-0 font-light">(.*?)<', str(detail_balance), re.DOTALL)[0]).replace('\n', '')
       print (transfer+color.END+ "\n")
    return [name, balance.replace(' ', ''), validity.replace('                        ', '').replace('                            ', ''),]

class color():
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    
def teletalk_login():
    headers = {
	    'Host': 'teletalk.com.bd',
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Upgrade-Insecure-Requests': '1',
	    'Sec-Fetch-Dest': 'document',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-Site': 'none',
	    'Sec-Fetch-User': '?1',
	} 

    response = requests.get('https://teletalk.com.bd/en/login-with-otp', headers=headers, verify=False)
    for cookie in response.cookies:
        a = cookie.value
    
    _session_key = str(re.findall('"_session_key" type="hidden" value="(.*?)"', str(response.text), re.DOTALL)[0])
    _token = str(re.findall('"_token" type="hidden" value="(.*?)"', str(response.text), re.DOTALL)[0])
    print ('\n')
    mobile = input(color.BLUE+ "    Enter Teletalk Mobile Number : " + color.END)
    is_teletalk_mobile = bool(re.match('^(?:\+?015)?015\d{8}$', mobile))
    #mobile = str(mobile).replace('88', '', 1).replace('+88', '', 1).replace('088', '', 1).replace('+', '', 1)#01533884503
    while not is_teletalk_mobile:
         mobile = input(color.BLUE+ "    Enter a valid Teletalk Mobile Number : " + color.END)
         is_teletalk_mobile = bool(re.match('^(?:\+?015)?015\d{8}$', mobile))
         if is_teletalk_mobile:
            break

    data = {"_session_key":  _session_key, "_token": _token, "mobile": mobile, "contact_submit": ""}
    response_get_otp_cookies = {
	    'october_session': a,
	    'PHPSESSID': '',
	}

    response_get_otp_headers = {
	    'Host': 'teletalk.com.bd',
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
	    'Accept': '*/*',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'X-OCTOBER-REQUEST-HANDLER': 'onHandleLogin',
	    'X-OCTOBER-REQUEST-PARTIALS': '',
	    'X-Requested-With': 'XMLHttpRequest',
	    'Origin': 'https://teletalk.com.bd',
	    'Referer': 'https://teletalk.com.bd/en/login-with-otp',
	    'Sec-Fetch-Dest': 'empty',
	    'Sec-Fetch-Mode': 'cors',
	    'Sec-Fetch-Site': 'same-origin',
	}

    response_get_otp = requests.post('https://teletalk.com.bd/en/login-with-otp', headers=response_get_otp_headers, cookies=response_get_otp_cookies, data=data,verify=False)
    for cookie in response_get_otp.cookies:
        b = cookie.value
    print (color.BLUE + "    Otp has been sent to your mobile." + color.END)
    otp = input(color.BLUE + "    Enter Otp : " + color.END)
    data_otp = {"mobile":  mobile, "password": otp}

    response_submit_otp_cookies = {
	    '_ga_KL862SDS3T': 'GS1.1.1660067717.1.1.1660069946.0',
	    'october_session': b,
	    'PHPSESSID': 'ruv910grno9vq7ha7jc5lnt2v3',
	}

    response_submit_otp_headers = headers = {
	    'Host': 'teletalk.com.bd',
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
	    'Accept': '*/*',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'X-OCTOBER-REQUEST-HANDLER': 'onHandleAuth',
	    'X-OCTOBER-REQUEST-PARTIALS': '',
	    'X-Requested-With': 'XMLHttpRequest',
	    'Origin': 'https://teletalk.com.bd',
	    'Referer': 'https://teletalk.com.bd/en/login-with-otp',
	    'Sec-Fetch-Dest': 'empty',
	    'Sec-Fetch-Mode': 'cors',
	    'Sec-Fetch-Site': 'same-origin',
	}

    response_submit_otp = requests.post('https://teletalk.com.bd/en/login-with-otp',    headers=response_submit_otp_headers, data=data_otp, cookies=response_submit_otp_cookies, verify=False, allow_redirects=True)
    
    opt_response__ = response_submit_otp.text
    a___ = 'enter a valid OTP' in str(opt_response__)
    while a___:
         from termcolor import colored, cprint
         #print ('Otp is not valid. Enter valid otp.')
         cprint('    Otp is not valid. Enter valid otp. Otp Has been sent to your mobile.', 'red', attrs=['blink'])
         otp = input(color.BLUE+ "    Enter valid otp: "+ color.END)
         data_otp = {"mobile":  mobile, "password": otp}
         response_submit_otp = requests.post('https://teletalk.com.bd/en/login-with-otp',    headers=response_submit_otp_headers, data=data_otp, cookies=response_submit_otp_cookies, verify=False, allow_redirects=True)
         opt_response__ = response_submit_otp.text
         if 'user_auth' in str(response_submit_otp.headers):
             break
            
    dashboard_cookies_user_auth = str(re.findall('user_auth=(.*?);', str(response_submit_otp.headers), re.DOTALL)[0])

    dashboard_cookies = {
	    '_ga_KL862SDS3T': 'GS1.1.1660067717.1.1.1660069946.0',
	    'october_session': b,
	    'PHPSESSID': 'ruv910grno9vq7ha7jc5lnt2v3',
	    'user_auth': dashboard_cookies_user_auth,
	}

    dashboard_headers = {
	    'Host': 'teletalk.com.bd',
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Referer': 'https://teletalk.com.bd/en/login-with-otp',
	    'Upgrade-Insecure-Requests': '1',
	    'Sec-Fetch-Dest': 'document',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-Site': 'same-origin',
	    'Sec-Fetch-User': '?1',
	}

    response_dashboard = requests.get('https://teletalk.com.bd/en/e-selfcare', headers=dashboard_headers,     cookies=dashboard_cookies, verify=False)
    print (color.BLUE+ '    To transfer balance it will save session to a temp file.'+ color.END)
    save_cookies(response_dashboard.cookies, 'teletalk')
    national_idnumber = requests.get('https://teletalk.com.bd/en/e-selfcare/registered-numbers', headers=dashboard_headers, cookies=dashboard_cookies, verify=False)

    soup = BeautifulSoup(response_dashboard.text, 'html.parser')
    soup_ = BeautifulSoup(national_idnumber.text, 'html.parser')
    detail = soup.find_all("div", {"class": "col-lg-7 col-xlg-7 col-sm-6 col-xs-10"})
    detail_balance = soup.find_all(id="balance-main")
    parsed = soup_.select("tbody")
    national_id = str(re.findall('<td rowspan="2">(.*?)<', str(parsed), re.DOTALL)[0])
    registered_numbers = re.findall('<td>(.*?)</td>', str(parsed), re.DOTALL)


    name = str(re.findall('<h3 class="m-b-0">(.*?)<', str(detail[0]), re.DOTALL)[0])
    balance = str(re.findall('id="user-balance">(.*?)<', str(soup), re.DOTALL)[0]).replace('\n', '').replace('                            ', ' ')
    validity = str(re.findall('<h3 class="m-b-0 font-light">(.*?)<', str(detail_balance), re.DOTALL)[0]).replace('\n', '')
    
    print ('\n')
    print (color.GREEN+"      Details of your Teletalk number. ")
    print ('\n')
    print (color.BLUE+'    Name                 :'+color.END, name)
    print (color.BLUE+'    Balance              :'+color.END, balance.replace(' ', ''))
    print (color.BLUE+'    Validity             :'+color.END, validity.replace('                            ', ''))
    print (color.BLUE+'    National Id Number   :'+color.END, national_id)
    print (color.BLUE+'    Registered Number    :'+color.END, ', '.join(registered_numbers))
    print ('\n')    
    return [name, balance.replace(' ', ''), validity.replace('                        ', '').replace('                            ', ''), ', '.join(registered_numbers)]
       

def login_with_session():
    dashboard_headers = {
	    'Host': 'teletalk.com.bd',
	    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	    'Accept-Language': 'en-US,en;q=0.5',
	    'Referer': 'https://teletalk.com.bd/en/login-with-otp',
	    'Upgrade-Insecure-Requests': '1',
	    'Sec-Fetch-Dest': 'document',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-Site': 'same-origin',
	    'Sec-Fetch-User': '?1',
	}

    response_dashboard = requests.get('https://teletalk.com.bd/en/e-selfcare', headers=dashboard_headers,     cookies=load_cookies('teletalk'), verify=False)
    is_session_expired = bool(re.findall('id="user-balance">', str(response_dashboard.text)))
    while not is_session_expired:
         from termcolor import colored, cprint
         cprint('    Session expired. Login in again.', 'red', attrs=['blink'])
         teletalk_login()
         break
   
    save_cookies(response_dashboard.cookies, 'teletalk')
    national_idnumber = requests.get('https://teletalk.com.bd/en/e-selfcare/registered-numbers', headers=dashboard_headers, cookies=load_cookies('teletalk'), verify=False)

    soup = BeautifulSoup(response_dashboard.text, 'html.parser')
    soup_ = BeautifulSoup(national_idnumber.text, 'html.parser')
    detail = soup.find_all("div", {"class": "col-lg-7 col-xlg-7 col-sm-6 col-xs-10"})
    detail_balance = soup.find_all(id="balance-main")
    parsed = soup_.select("tbody")
    national_id = str(re.findall('<td rowspan="2">(.*?)<', str(parsed), re.DOTALL)[0])
    registered_numbers = re.findall('<td>(.*?)</td>', str(parsed), re.DOTALL)


    name = str(re.findall('<h3 class="m-b-0">(.*?)<', str(detail[0]), re.DOTALL)[0])
    balance = str(re.findall('id="user-balance">(.*?)<', str(soup), re.DOTALL)[0]).replace('\n', '').replace('                            ', ' ')
    validity = str(re.findall('<h3 class="m-b-0 font-light">(.*?)<', str(detail_balance), re.DOTALL)[0]).replace('\n', '')
    print ('\n')
    print (color.GREEN+"      Details of your Teletalk number. ")
    print ('\n')
    print (color.BLUE+'    Name                 :'+color.END, name)
    print (color.BLUE+'    Balance              :'+color.END, balance.replace(' ', ''))
    print (color.BLUE+'    Validity             :'+color.END, validity.replace('                            ', ''))
    print (color.BLUE+'    National Id Number   :'+color.END, national_id)
    print (color.BLUE+'    Registered Number    :'+color.END, ', '.join(registered_numbers))
    print ('\n')
    return [name, balance.replace(' ', ''), validity.replace('                        ', '').replace('                            ', ''), ', '.join(registered_numbers)]

def init_teletalk():
   if os.path.exists('teletalk'):
      detail = login_with_session()
      return detail
   else:
      login = teletalk_login()
      return login

