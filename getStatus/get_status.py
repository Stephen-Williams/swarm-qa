import logging
import sys
import json
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, http.client
import traceback
import os
import time, ast, pprint

# Testing Environment Variables:
testpath = "."
testfile = "pid"
filename = "results_get-status-" + testpath.replace("/", "-") + "_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

port = "8071"
server = "ssh-dev.swarmdsp.com" # QA Environment
#server = "192.168.0.184"       # My BOSS
#server = "192.168.1.28"        # Dave's BOSS
#server = "192.168.1.26"        # James's BOSS

testlog = open(filename, "w")
expected = None
actual = None

def web_call(url, args, expected) :
    res = None
    
    try:
        data = urllib.parse.urlencode(args)
        data = data.encode('utf-8')
        request = urllib.request.Request(url, data=data)
        server_content = urllib.request.urlopen(request, timeout=60)
        res = server_content.read().decode()
    except:
        why, why_val, why_trace = sys.exc_info()
        trace = traceback.format_tb(why_trace, limit=20)
        reason = 'exception\n{}\n{}\n{}'.format(why, why_val, trace)
        res = logging.error(reason)

    if '\"result\": true' in res:
        actual = "True"
    else:
        actual = "False"

    testlog.write("Actual: " + actual + ";")

    if actual == expected: 
        testlog.write("Result: Pass;")
    else:
        testlog.write("Result: Fail;")

    return res

def get(nid, expected):

#    arg = { 'NECTAR_CRID' : nid } # Calls Get Status with a Nectar CRID
    arg = { 'NECTAR_ALLOCATION' : nid } # Calls Get Status with a Nectar Allocation ID

    try:
        answer = json.loads(web_call(r'http://{}:{}/swarm/campaign/getstatus'.format(server, port), arg, expected))

        pp = pprint.PrettyPrinter()
        pp.pprint(answer)
    except:
        answer = 'none'

    testlog.write(str(answer) + "\n")
    logging.debug(answer)
    
    return answer

def run(root_dir='.'):
    format = '%(levelname)s - %(message)s - %(funcName)s - %(filename)s - %(lineno)s'
    logging.basicConfig(stream=sys.stderr,format=format)
    logging.getLogger('').setLevel(logging.DEBUG)

    for root, dirs, files in os.walk(testpath):
        for f in files:
            if f.startswith(testfile):
                p = os.path.join(root, f)

                testlog.write(p + ";")
                if f.endswith('f.py'):
                    expected = "False"
                if f.endswith('p.py'):
                    expected = "True"
             
                testlog.write("Expected: " + expected + ";")

                with open(p,'r') as f:
                    for line in f:
                        cr = ast.literal_eval(line)
                        logging.debug('querying status for CRID: ' + str(cr))
                        get(cr, expected)
                        logging.debug('sent')
                        time.sleep(2)
    
if __name__ == '__main__' :
    run()
    testlog.close()
