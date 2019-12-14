from flask import Flask, request
import requests

app = Flask(__name__)


@app.route('/api/rooms', methods=['GET'])
def get_fenix():
    # retirar o id do espaço do pedido get
    id = request.args.get('id', '')

    # criar url da api do fenix - teste:2448131360897
    url = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + id

    # fazer o pedido ao fenix
    r = requests.get(url)

    # impirmir os dados
    data = r.json()
    print(data)

    return 'OK'


if __name__ == '__main__':
    app.run()
