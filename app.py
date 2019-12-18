import random

from flask import Flask, render_template, request, jsonify, redirect, session
import requests

class User:
    def __init__(self, name, photo, token):
        self.name = name
        self.token = token
        self.photo = photo
        self.secret = None

redirect_uri = "http://127.0.0.1:8000/userAuth" # this is the address of the page on this app

client_id= "570015174623373" # copy value from the app registration
clientSecret = "rcub4Vdgb20G+14SbCKdktzN8pmP8xW/40OxvQSg0Mxo8lcsGQl1sOfflV0Vuhgj4Qknmg/wmE+eCdE/TmteXA==" # copy value from the app registration

fenixLoginpage= "https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=%s&redirect_uri=%s"
fenixacesstokenpage = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

#loginName = []
#userToken = []
userList = []
code = False
app = Flask(__name__)
app.secret_key = "ASINT"


@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/add_secretariat')
def add_secretariat():
    return render_template('add_secretariat.html')

@app.route('/canteen')
def canteen():
    return render_template('canteen.html')


@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/qr')
def qr():
    return render_template('qr.html')

######### FENIX LOGIN #################
@app.route('/readsecret', methods=['POST', 'GET'])
def readsecret():
    if request.method == 'POST':
        selSecret = request.form['secret']
        print("sel: " + selSecret + "  type:  " + type(selSecret))
        friend = None

        for x in userList:
            if x.secret == int(selSecret):
                print("x.secret: " + x.secret + "  type:  " + type(x.secret))
                friend = x
                return render_template('showUser.html', name=friend.name, photo=friend.photo)

        return "Secret not found"

    else:
        return render_template('readsecret.html')

@app.route('/getsecret')
def getsecret():
    if session.get('token') is None:
        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirects the user to the FENIX login page
        return redirect(redPage)
    else:
        secret = random.randint(1, 10000000)

        for x in userList:
            if x.token == session.get('token'):
                x.secret = secret
                break

        return render_template('getsecret.html', secret=secret)

@app.route('/private')
def private_page():
    #this page can only be accessed by a authenticated username

    if session.get('token') is None:
        #if the user is not authenticated

        redPage = fenixLoginpage % (client_id, redirect_uri)
        # the app redirecte the user to the FENIX login page
        return redirect(redPage)
    else:
        #if the user ir authenticated
        print(session.get('token'))

        #we can use the userToken to access the fenix

        params = {'access_token': session.get('token')}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

        if (resp.status_code == 200):
            r_info = resp.json()
            print( r_info)

            #i= 0
            for x in userList:
                if x.token == session.get('token'):
                    istid = x.name
                    break
                #i += 1

            #istid = loginName[i]

            return render_template("privPage.html", username=istid, name=r_info['name'])
        else:
            return "oops"

@app.route('/userAuth')
def userAuthenticated():
    #This page is accessed when the user is authenticated by the fenix login pagesetup

    #first we get the secret code retuner by the FENIX login
    code = request.args['code']
    print ("code "+request.args['code'])


    # we now retrieve a fenix access token
    payload = {'client_id': client_id, 'client_secret': clientSecret, 'redirect_uri' : redirect_uri, 'code' : code, 'grant_type': 'authorization_code'}
    response = requests.post(fenixacesstokenpage, params = payload)
    print (response.url)
    print (response.status_code)
    if(response.status_code == 200):
        #if we receive the token
        print ('getting user info')
        r_token = response.json()
        print(r_token)

        params = {'access_token': r_token['access_token']}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)
        r_info = resp.json()
        print( r_info)

        # we store it
        global userList
        userList.append(User(r_info['displayName'], r_info['photo']['data'], r_token['access_token']))
        #global loginName
        #loginName.append(r_info['username'])
        #global userToken
        #userToken.append(r_token['access_token'])

        session['key'] = r_token['access_token']
        session['token'] = r_token['access_token']

        #now the user has done the login
        return jsonify(r_info)
        #we show the returned infomration
        #but we could redirect the user to the private page
        #return redirect('/private') #comment the return jsonify....
    else:
        return 'oops'

@app.route('/admin')
def admin():
    #i = 0
    for x in userList:
        if x.token == session.get('token'):
            istid = x.name
            break
        #i += 1

    #istid = loginName[i]
    return render_template("appPage.html", username=istid)

if __name__ == '__main__':
    app.run()


