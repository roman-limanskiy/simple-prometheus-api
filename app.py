#!/usr/bin/env python3


from flask import Flask
from flask import request
import json
import subprocess
import yaml


app = Flask(__name__)
workdir = '/opt/prometheus/alerting/'

@app.route('/v1/alerting/', methods=['POST'])

def main():
        request_data = request.get_json(force=True)
        result = {}

        for key in request_data.keys():

                if request_data[key]['action'] == 'create':
                        alert_rule = { 'groups': [ { 'name': 'alert.rules', 'rules': [ { 'alert': 'InstanceDown', 'expr': 'probe_success{instance = "' + key + '"} == 0', 'for': request_data[key]['pending_time'] + 's' } ] } ] }
                        with open( workdir + key + '.yaml', 'w') as outfile:
                                yaml.dump( alert_rule, outfile )
                        result[key] = 'created'

                elif request_data[key]['action'] == 'update':
                        alert_rule = { 'groups': { 'name': 'alert.rules', 'rules': { 'alert': 'InstanceDown', 'expr': 'probe_success{instance = "' + key + '"} == 0', 'for': request_data[key]['pending_time'] + 's' } } }
                        with open( workdir + key + '.yaml', 'w') as outfile:
                                yaml.dump( alert_rule, outfile )
                        result[key] = 'updated'

                elif request_data[key]['action'] == 'delete':
                        subprocess.run( [ "rm", "-rf", workdir + key + ".yaml" ] )
                        result[key] = 'deleted'

                else:
                        result[key] = 'unknown method'

        return result

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=9095)
