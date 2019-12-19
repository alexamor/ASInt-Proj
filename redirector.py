import json
from datetime import datetime

from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import requests
from json2html import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/redirect', methods=['POST', 'GET'])
@cross_origin()
def redirect():
    # processa o tipo de pedido
    if request.method == 'POST':

        service_id = request.form['serviceId']

        # abre os serviços possíveis
        fh = open("microservices.txt", 'r')

        # found microservice
        found = False

        # le todas as linhas
        lines = fh.readlines()
        for line in lines:
            aux = line.split()
            if aux[0] == service_id:
                print(aux[1])
                port = str(5000 + int(service_id))
                ### ADD LOG ###
                addLog("POST Request microservice " + aux[1].strip('\n'), "-")
                url = "http://127.0.0.1:" + port + "/api/" + aux[1].strip('\n')
                found = True
                break

        if found:
            data = request.form
            r = requests.post(url, data=data)
            return json2html.convert(r.json())
        else:
            return 'Your request cannot be processed.'
    elif request.method == 'GET':

        service_id = request.args.get('serviceId', 'id')
        # abre os serviços possíveis
        fh = open("microservices.txt", 'r')

        # found microservice
        found = False

        # le todas as linhas
        lines = fh.readlines()
        for line in lines:
            aux = line.split()
            if aux[0] == service_id:
                print(aux[1])
                port = str(5000 + int(service_id))

                ### ADD LOG ###
                addLog("GET Request microservice " + aux[1].strip('\n'), "-")

                url = "http://127.0.0.1:" + port + "/api/" + aux[1].strip('\n')
                found = True
                break

        if found:
            data = request.args.to_dict()
            print(data)
            r = requests.get(url, params=data)
            print(r.status_code)
            response = r.json()
            print(response)
            # render_template(json2html.convert(r))
            return json2html.convert(response)
            #return json.dumps(r.json())
        else:
            return 'Your request cannot be processed.'

def addLog(type, id):
    fh = open("logs.txt", 'a')
    auxString = "Type: " + type + ":  id: " + id + ":  time: " + str(datetime.now()) + "\n"
    fh.write(auxString)
    fh.close()