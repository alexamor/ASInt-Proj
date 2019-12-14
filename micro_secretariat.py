from flask import Flask, request

app = Flask(__name__)


@app.route('/api/secretariats', methods=['GET', 'POST'])
def get_secretariat():
    if request.method == 'POST':

        # retirar o id que se quer colocar
        id_post = request.form['id']
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
                if strings[1].rstrip('\n') == id_post:
                    return 'Secretariat already inserted'

        fh.close()

        fh = open("secretariats.txt", 'a')
        newLines = []
        newLines.append("id: " + id_post + '\n')
        newLines.append("name: " + name + '\n')
        newLines.append("description: " + description + '\n')
        newLines.append("location: " + location + '\n')
        newLines.append("opening hours: " + opening_hours + '\n')

        fh.writelines(newLines)

        fh.close()

        return 'Secretariat inserted!'

    elif request.method == 'GET':

        found = False
        # retirar o id da secretaria
        id = request.args.get('id', '')

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
                if strings[0] == 'name:':
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

    return 'OK'


if __name__ == '__main__':
    app.run()
