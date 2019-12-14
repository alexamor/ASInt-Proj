from flask import Flask, request
import requests
import json

app = Flask(__name__)


class Meal:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __str__(self):
        return '(Type: ' + self.type + ' name: ' + self.name + ')'


@app.route('/api/canteen', methods=['GET'])
def get_fenix():
    # retirar o dia do pedido get
    auxday = request.args.get('day', '')

    day = auxday.replace('-','/')
    print(day)
    # enviar pedido get à api do tecnico
    url = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen/"
    r = requests.get(url)

    print(r.status_code)

    # recebe os dados do fenix
    data = r.json()

    lunch = []
    dinner = []

    for m in data:
        if m['day'] == day:
            # print(m)
            for me in m['meal']:
                if me['type'] == 'Almoço':
                    auxMeal = lunch
                else:
                    auxMeal = dinner

                for pl in me['info']:
                    auxMeal.append(Meal(pl['type'], pl['name']))

    retStr = ''
    for m in lunch:
        retStr = retStr + str(m) + '\n'

    #return {'res':retStr}
    return json.dumps(r.json())

if __name__ == '__main__':
    app.debug = True
    app.run()
