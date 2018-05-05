from flask import Flask, render_template, request, Response
from uuid import uuid4
import json
from time import sleep
from threading import Thread
app = Flask(__name__)

import psycopg2

from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader = FileSystemLoader ('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def getConnection():
    return psycopg2.connect("dbname='dysfunctional' user='allen' host='localhost' password='anything'")

directions = dict({"-1":"left", "0":"none", "1":"right"})
swapaxes= dict({"left":"up", "right":"down", "none":"none"})


#read queries from file
query = dict()
queryNames = ['teamPicker', 'registerPlayer', 'input', 'data', 'deleteInactive', 'inactiveid']
for queryName in queryNames:
    f = open('queries/' + queryName + '.sql', 'r')
    query[queryName] = f.read()
    f.close()

@app.route("/input", methods=['POST'])
def input():
    direction = directions.get(request.form["direction"])
    id = request.form["id"]
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(query['input'], (id, direction,))
    conn.commit()
    resp = Response("done!")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/register", methods=['GET'])
def register():
    team = decideTeam()
    id = uuid4().hex
    logUser(team,id)
    data = dict({"team":team, "id":id})
    resp = Response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

def decideTeam():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(query['teamPicker'])
    zucc = cursor.fetchone()[0]
    if zucc:
        return "zucc"
    else:
        return "user"

def logUser(team, id):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(query['registerPlayer'], (id, team,))
    conn.commit()

@app.route("/data")
def getData():
    seconds = request.args.get("seconds")
    print(seconds)
    userValues = dict()
    teams = dict()
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(query['data'], (str(seconds) + " seconds",))
    for row in cursor.fetchall():
        userValues[row[0]] = row[2]
        teams[row[0]] = row[3]
    data = dict({"zucc":{"up":0, "none":0, "down":0}, "user":{"up":0, "none":0, "down":0}})
    for userID, direction in userValues.items():
        data[teams[userID]][swapaxes[direction]] += 1
    resp = Response(json.dumps(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp

def sqlFormat(list):
    output = "("
    for element in list:
        output += "'" + element + "',"
    return output[:-1] + ")"


def watchdog():
    while True:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(query['inactiveid'])
        dead = list()
        for row in cursor.fetchall():
            dead.append(row[0])
        conn = getConnection()
        cursor = conn.cursor()
        updateQuery = query['deleteInactive'].replace("<replace>", sqlFormat(dead))
        cursor.execute(updateQuery)
        conn.commit()
        sleep(60)

if __name__ == '__main__':
    thread = Thread(target = watchdog)
    thread.start()
    app.run(debug=True, port=80, host='0.0.0.0')