# import dependencies
import os
from flask import Flask
from flask import jsonify
import pymongo

import http.client, urllib.parse
import json

import subprocess
import shlex
import json
import datetime
import time
import bitmath

# bootstrap the app
app = Flask(__name__)

# set the port dynamically with a default of 3000 for local development
port = int(os.getenv('PORT', '4000'))

def httpPost(url,resource,params):
    headers = {
        "Content-type" : "application/x-www-form-urlencoded",
    }
    try :
        conn = http.client.HTTPSConnection(url, timeout=10)
        temp_params = urllib.parse.urlencode(params)
        conn.request("POST", resource, temp_params, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        params.clear()
        conn.close()
        return data
    except:
    # except Exception,e:  
        # print(Exception,":",e)
        traceback.print_exc()
        return False

def httpGet(url,resource,params, headers):
    try :
        conn = http.client.HTTPSConnection(url, timeout=10)
        temp_params = urllib.parse.urlencode(params)
        conn.request("GET", resource, temp_params, headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        params.clear()
        conn.close()
        return data
    except:
    # except Exception,e:  
        # print(Exception,":",e)
        traceback.print_exc()
        return False

# our base route which just returns a string
@app.route('/')
def hello_world():
    return 'Welcome to monitoring flask api, I am running on cloud'

@app.route('/mongoTest')
def hello_world_mongo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["local"]
    mycol = mydb['sample']
    mydict = { "name": "John", "address": "Highway 37" }
    x = mycol.insert_one(mydict)
    print(x)
    return "mongo "+ str(x.inserted_id)

@app.route('/mongoRead')
def hello_world_mongo_read():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["local"]
    mycol = mydb['student']
    x = mycol.find_one()
    print(x)
    return "mongo "+ str(x)

@app.route('/pcf_app_usage')
def pcf_apps_usage():
    
    foundry_list = {'foundry-1': ['https://api.run.pivotal.io', 'Lakshmiredz@gmail.com', 'Pooja@123', 'concourse2', 'ci', "console.run.pivotal.io"]}
    login_params = {'username': 'lakshmiredz@gmail.com', 'password':'Pooja@123', 'grant_type':'password', 'response_type':'token', 'client_id':'cf', 'client_secret':''}
    res = httpPost('login.run.pivotal.io', '/oauth/token', login_params)
    token = 'Bearer ' + json.loads(res)['access_token']

    for foundry in foundry_list:
        flist = foundry_list[foundry]
        api = flist[0]
        user = flist[1]
        pwd = flist[2]
        org = flist[3]
        space = flist[4]

        raw_org_json = httpGet('api.run.pivotal.io', '/v2/organizations?results-per-page=100', {}, {'Authorization': token})
        
        org_json = json.loads(raw_org_json)
        return jsonify(raw_org_json)
        #org_json = json.loads(raw_org_json)
        #print(org_json['total_results'])
        #return org_json
    #return 'Sample flask app running perfectly in cloud'

# start the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
