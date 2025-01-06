from flask import Flask,jsonify,request

app=Flask(__name__)

users=[
    {"id": 1, "name": "Jumi"},
    {"id": 2, "name": "Anu"},
    {"id": 3, "name": "Sandra"},
    {"id": 4, "name": "Aparna"}, 
]

@app.route('/users',methods=['GET'])
def get_user():
    return jsonify(users)

@app.route('/users',methods=['POST'])
def add_user():
    user=request.json
    users.append(user)
    return jsonify(user), 201

@app.route('/user/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    for user in users:
        print(user)
        if user['id'] == user_id:
            user.update(request.json)
            return jsonify(user)
    return "Not Found Error" , 404

@app.route('/user/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    global users
    users=[user for user in users if user['id'] != user_id]
    return f"User deleted Succesfully"

if __name__ == '__main__':
    app.run(debug=True)

