# -*- coding: utf-8 -*-
import sys
import time, ast
import subprocess

## Testing Environment Variables:
# Path to file containing test data.  Each line contains a list of parameters for the test command.
testpath = ""
# Test Data file (found in testpath dir).
testdata = "data.txt"
# Command to execute, using test data as parameters.
testcmd = "echo"
# Meaningful name to be used in resultFile name.
testname = "autostop"
# Filename of CSV containing test results, for later reference.  Results are also output on screen.
resultFile = "results_" + testname + "_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

expected = None
actual = None

def logger(s):
  s = str(s)
  log.write(s)
  sys.stdout.write(s)
    
def run():
  fname = testpath + testdata

  sys.stdout.write("Beginning Test Run\n")
  sys.stdout.write("Using data file: " + fname + "\n")
  sys.stdout.write("Using command: " + testcmd + "\n")
  sys.stdout.write("Results File: " + resultFile + "\n")
  sys.stdout.write("\n")

  f = open(fname, 'r')
  for line in f:
    data = line.split(';')
    test_case = data[0]
    test_input = data[1]
    expected = data[2]

    logger(test_case + ";")
    logger("Expected: " + expected + ";")
    output1 = subprocess.check_output([testcmd, test_input])

    actual = "pass"
    #output2 = subprocess.check_output('check-bidder-process', 'CID')
    #if CID in output2:
    #  actual = "pass"
    #else:
    #  actual = "fail"
    logger("Actual: " + actual + ";")
               
    if expected == actual:
      logger("Result: pass;")
    else:
      logger("Result: fail;")

    logger(output1)
    logger("\n")
                
if __name__ == '__main__':
  log = open(resultFile, "w")
  run()
  log.close()
