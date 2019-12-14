from flask import Flask, request
import requests

app = Flask(__name__)


@app.route('/api/canteen', methods=['GET'])
def get_fenix():
    # retirar o dia do pedido get
    day = request.args.get('day', '')

    # enviar pedido get à api do tecnico
    url = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen/"
    r = requests.get(url)

    print(r.status_code)

    # recebe os dados do fenix
    data = r.json()

    print(data)

    return 'OK'


if __name__ == '__main__':
    app.debug = False
    app.run()
