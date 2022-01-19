# Time table API
import json
import os
import shutil

from handler import Storage_Handler
from flask import Flask, jsonify, request, render_template

# create a flask app

app = Flask(__name__)
port = os.enironment("PORT",5000)

# create a route for the app to show all endpoints
@app.route('/')
def index():
    return """
    API VERSION : v1
    <br>"""


# variable endpoint for each user
@app.route('/api/v1/<userid>/timetable', methods=['GET', 'POST', 'DELETE'])
def user(userid):
    if request.headers.get('Content-Type') == 'application/json':
        pass

    with open(f'storage/{userid}/user.json', 'r') as f:
        user_data = json.load(f)
        user_token = user_data.get("token")
        if user_token == request.headers.get('Authorization'):
            pass
        else:
            return jsonify({"message": "Unauthorized", "status": "401"})

    if request.method == "GET":
        with open(f"storage/{userid}/timetable.json") as json_file:
            data = json.load(json_file)
            data.update({"status": "200"})
            return jsonify(data)

    elif request.method == "POST":
        with open(os.getcwd() + f"/storage/{userid}/timetable.json", "w") as json_file:
            json.dump(request.get_json(), json_file, indent=4)

        return jsonify({'message': 'Timetable added successfully', 'status': '200'})

    elif request.method == "DELETE":
        with open(f"storage/{userid}/timetable.json") as json_file:
            data = json.load(json_file)
            data.pop(0)
        with open(f"storage/{userid}/timetable.json", "w") as json_file:
            json.dump(data, json_file)
        return jsonify({'message': 'Timetable deleted successfully', 'status': '200'})


# check if user followed the time table for each day
@app.route('/api/v1/<userid>/timetable/<day>', methods=['GET', 'POST'])
def timetable(userid, day):
    with open(f'storage/{userid}/user.json', 'r') as f:
        user_data = json.load(f)
        user_token = user_data.get("token")
        if user_token == request.headers.get('Authorization'):
            pass
        else:
            return jsonify({"message": "Unauthorized", "status": "401"})

    # if user follows the timetable for each day then update it with the new data
    if request.method == "POST":
        with open(os.getcwd() + f"/storage/{userid}/timetable/{day}.json", "w") as json_file:
            json.dump(request.get_json(), json_file,indent=4)
        return jsonify({'message': 'Timetable updated successfully', 'status': '200'})

    # send the timetable for each day
    elif request.method == "GET":
        with open(f"storage/{userid}/timetable/{day}.json") as json_file:
            data = json.load(json_file)
            return jsonify(data)


# create user
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if request.headers.get('Content-Type') == 'application/json':
        pass

    # create a new user
    if request.method == "POST":
        user_data = request.get_json()
        user_id = user_data.get('userid')
        user_token = user_data.get('token')
        timestamp = user_data.get('timestamp')
        user_data = {"token": user_token, "user_created": timestamp}
        os.mkdir(f'storage/{user_id}')
        os.mkdir(f'storage/{user_id}/timetable')
        with open(f'storage/{user_id}/user.json', 'w') as f:
            json.dump(user_data, f)
        return jsonify({'message': 'User created successfully', 'status': '200'})


# delete user
@app.route('/api/v1/users/<userid>', methods=['DELETE'])
def delete_user(userid):
    with open(f'storage/{userid}/user.json', 'r') as f:
        user_data = json.load(f)
        user_token = user_data.get("token")
        if user_token == request.headers.get('Authorization'):
            pass
        else:
            return jsonify({"message": "Unauthorized", "status": "401"})

    # delete a user
    if request.method == "DELETE":
        shutil.rmtree(f'storage/{userid}')
        os.rmdir(f'storage/{userid}')

        return jsonify({'message': 'User deleted successfully', 'status': '200'})


# server a page for admins
@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port = port)
