from flask import Flask, render_template, request, Response
from uuid import uuid4
import json
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

#read queries from file
query = dict()
f = open('queries/teamPicker.sql', 'r')
query['teamPicker'] = f.read()
f.close()
f = open('queries/registerPlayer.sql', 'r')
query['registerPlayer'] = f.read()
f.close()

@app.route("/input", methods=['POST'])
def input():
    print(request.form)
    return "input"

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

@app.route("/")
def hello():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')