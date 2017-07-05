#!/usr/bin/python2.7

import urllib2
import json
from datetime import datetime
import os

SOLRHOST = "localhost:8080"
SOLRCORE = "collection1"
SOLRCOREADM = "/solr/admin/cores"
LOGDIR = "/var/log/solrCorecheck"

def checklog():
    if not os.path.isdir(LOGDIR):
        try:
            os.makedirs(LOGDIR)
        except:
            print "Are you sudo?"
    return

def logIt(msg):
    file = open(LOGDIR+"/check.log","a")
    file.write(str(msg)+" ")
    file.close()
    return



def reloadCore():
    status = urllib2.urlopen("http://"+SOLRHOST+SOLRCOREADM+"?action=RELOAD&wt=json&core="+SOLRCORE).read()
    status = json.loads(status)
    if status['responseHeader']['status'] is 0:
       logIt("Reload Ok")
    else:
       logIt("RELOAD fail:"+status['responseHeader']['status'])

    return

def optimizeCore():
    status = urllib2.urlopen("http://"+SOLRHOST+"/solr/"+SOLRCORE+"/update?optimize=true&waitFlush=true&wt=json").read()
    status = json.loads(status)
    if status['responseHeader']['status'] is 0:
       logIt(" Optimize Ok ")
    else:
       logIt(" OPTIMIZE fail:"+status['responseHeader']['status'])

    return


def main():
    status = urllib2.urlopen("http://"+SOLRHOST+SOLRCOREADM+"?action=STATUS&wt=json&core="+SOLRCORE).read()
    status = json.loads(status)
    timestamp = datetime.now()
    print timestamp
    if status['status']['collection1']['index']['current'] is False:
       logIt(timestamp)
       reloadCore()
       optimizeCore()

    if status['status']['collection1']['index']['hasDeletions'] is True:
       logIt(timestamp)
       optimizeCore()
    
    
if __name__ == '__main__':
    checklog()
    main()
    logIt("\n")

