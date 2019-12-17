from flask import Flask, request, jsonify

app = Flask(__name__)

class Secretary:
    def __init__(self, id, name, description, location, openingHours):
        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.openingHours = openingHours



@app.route('/api/secretariats', methods=['GET', 'POST'])
def get_secretariat():
    if request.method == 'POST':

        # parametros que se vao colocar
        name = request.form['name']
        description = request.form['description']
        location = request.form['location']
        opening_hours = request.form['open_hours']
        # print(description)
        # print(id)
        # print(name)
        # print(location)
        # print(opening_hours)

        # abrir o ficheiro e escrever, se ainda não existir o id
        fh = open("secretariats.txt", 'r')
        lines = fh.readlines()
        for line in lines:
            strings = line.split(": ")
            if strings[0] == 'id':
                id = int(strings[1].rstrip('\n')) + 1

        fh.close()

        fh = open("secretariats.txt", 'a')
        newLines = []
        newLines.append("id: " + str(id) + '\n')
        newLines.append("name: " + name + '\n')
        newLines.append("description: " + description + '\n')
        newLines.append("location: " + location + '\n')
        newLines.append("opening hours: " + opening_hours + '\n')

        fh.writelines(newLines)

        fh.close()

        return jsonify(id=id, name=name, description=description, location=location, openingHours=opening_hours)

    elif request.method == 'GET':

        found = False
        # retirar o id da secretaria
        id = request.args.get('secrid', '')
        name = ''
        description = ''
        location = ''
        open_hours = ''

        # abrir o ficheiro e procurar a secretaria que se quer
        fh = open("secretariats.txt", 'r')
        lines = fh.readlines()
        for line in lines:
            strings = line.split(": ")
            if strings[0] == 'id':
                print(strings[1])
                if strings[1].rstrip('\n') == id:
                    found = True
            if found:
                if strings[0] == 'name':
                    name = strings[1].rstrip('\n')
                    print(name)
                elif strings[0] == 'description':
                    description = strings[1].rstrip('\n')
                    print(description)
                elif strings[0] == 'location':
                    location = strings[1].rstrip('\n')
                    print(location)
                elif strings[0] == 'opening hours':
                    open_hours = strings[1].rstrip('\n')
                    print(open_hours)
        fh.close()

        if found:
            return jsonify(Name=name,Description=description, Location=location, OpeningHours=open_hours)
        else:
            return jsonify(error='missing')


    return 'OK'


if __name__ == '__main__':
    app.run()
