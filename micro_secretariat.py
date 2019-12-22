from flask import Flask, request, jsonify, json
from fileinput import FileInput

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
        id = request.form['id']
        name = request.form['name']
        description = request.form['description']
        location = request.form['location']
        opening_hours = request.form['open_hours']
        print(description)
        print(id + str(type(id)))
        print(name)
        print(location)
        print(opening_hours)

        auxid=0

        # abrir o ficheiro e escrever, se ainda não existir o id
        fh = open("secretariats.txt", 'r')
        found = False
        lines = fh.readlines()
        for line in lines:
            print("line   " + line)
            strings = line.split(": ")
            if strings[0] == 'id':
                print(strings[1].rstrip('\n'))
                print(id)
                if strings[1].rstrip('\n') == id:
                    print("FOUND" + strings[1].rstrip('\n'))
                    found = True
                    break
                else:
                    auxid = int(strings[1].rstrip('\n')) + 1
                    found = False

        fh.close()

        # caso seja adicionar uma secretariat
        if not found:
            fh = open("secretariats.txt", 'a')
            newLines = []
            newLines.append("id: " + str(auxid) + '\n')
            newLines.append("name: " + name + '\n')
            newLines.append("description: " + description + '\n')
            newLines.append("location: " + location + '\n')
            newLines.append("opening hours: " + opening_hours + '\n')

            fh.writelines(newLines)

            fh.close()
            id = auxid
        else:
            foundLine = False
            fh = open("secretariats.txt","r")

            lines = fh.readlines()

            fh.close()


            fh = open("secretariats.txt", "w")
            for line in lines:
                auxLine = line.split(': ')
                if(auxLine[0] == 'id' and auxLine[1].rstrip('\n') == id):
                    foundLine = True
                    fh.write(line)
                if foundLine:
                    if auxLine[0] == 'name':
                        fh.write('name: ' + name + '\n')
                    elif auxLine[0] == 'location':
                        fh.write('location: ' + location + '\n')
                    elif auxLine[0] == 'description':
                        fh.write('description: ' + description + '\n')
                    elif auxLine[0] == 'opening hours':
                        fh.write('opening hours: ' + opening_hours + '\n')
                        foundLine = False
                else:
                    fh.write(line)



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
                    found = False
                    print(open_hours)
        fh.close()

        if name != '':
            return jsonify(Name=name,Description=description, Location=location, OpeningHours=open_hours)
        else:
            return jsonify(error='Secretariat not found!')


    return 'OK'


if __name__ == '__main__':
    app.run()
