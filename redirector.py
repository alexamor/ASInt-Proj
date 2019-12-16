import json

from flask import Flask, request, render_template
import requests
from json2html import *

app = Flask(__name__)


@app.route('/redirect', methods=['POST', 'GET'])
def redirect():
    # processa o tipo de pedido
    if request.method == 'POST':

        service_id = request.form['service_id']

        # abre os serviços possíveis
        fh = open("microservices.txt", 'r')

        # found microservice
        found = False

        # le todas as linhas
        lines = fh.readlines()
        for line in lines:
            aux = line.split()
            if aux[0] == service_id:
                url = "http://127.0.0.1:5000/api/" + aux[1]
                found = True
                break

        if found:
            data = request.form
            requests.post(url, data=data)
            return 'OK'
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
            #render_template(json2html.convert(r))
            return json2html.convert(response)
            #return json.dumps(r.json())
        else:
            return 'Your request cannot be processed.'
