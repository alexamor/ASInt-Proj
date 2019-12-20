import json

from flask import Flask, request
import requests

app = Flask(__name__)

class Room:
    def __init__(self, campi):
        self.campi = campi
        self.building = ''
        self.events = []

    def __str__(self):
        auxstr = '\n'
        for e in self.events:
            auxstr = auxstr + str(e) + '\n'
        return "Campus: " +  self.campi + " Building: " + self.building + " Events: " + auxstr

class Event:
    def __init__(self, type, start, end, weekday, day):
        self.type = type
        self.start = start
        self.end = end
        self.weekday = weekday
        self.day = day
        self.name = ''

    def __str__(self):
        return "Type: " + self.type + " start: " + self.start +  " end: " + self.end + " weekday: " + self.weekday + " day: " + self.day + " name: " + self.name


@app.route('/api/rooms', methods=['GET'])
def get_fenix():
    # retirar o id do espaço do pedido get
    id = request.args.get('roomid', '')

    # criar url da api do fenix - teste:2448131360897
    url = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + id

    # fazer o pedido ao fenix
    r = requests.get(url)

    # imprimir os dados
    data = r.json()

    print(data)
    if('parentSpace'in data.keys()):
        print("\n\nteste:" + data['parentSpace']['id'])

        buildingDataURL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + str(data['parentSpace']['id'])
        buildingData = requests.get(buildingDataURL).json()
        print(buildingData)
        if 'parentSpace' in buildingData.keys():
            data['parentSpace']['id'] = buildingData['parentSpace']['id']
            data['parentSpace']['name'] = buildingData['parentSpace']['name']
            data['parentSpace']['type'] = buildingData['parentSpace']['type']


    # selRoom = Room(data['topLevelSpace']['name'])
    #
    # for l in data['events']:
    #     auxEvent = Event(l['type'], l['start'], l['end'], l['weekday'], l['day'])
    #
    #     if auxEvent.type == 'GENERIC':
    #         auxEvent.name = l['title']
    #     elif auxEvent.type == 'LESSON':
    #         auxEvent.name = l['course']['name']
    #     elif auxEvent.type == 'TEST':
    #         auxEvent.name = l['courses'][0]['name']
    #
    #     selRoom.events.append(auxEvent)
    #
    # print(selRoom)

    return json.dumps(data)


if __name__ == '__main__':
    app.run()
