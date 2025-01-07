from flask import Flask,jsonify,request
from datetime import timedelta
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity,get_jwt,create_refresh_token
app=Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'my-strong-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)
revoked_tokens=set()

users=[
    {"id": 1, "name": "Jumi","email": "jumi@example.com"},
    {"id": 2, "name": "Anu","email": "anu@example.com"},
    {"id": 3, "name": "Sandra","email": "sandra@example.com"},
    {"id": 4, "name": "Aparna","email": "aparna@example.com"}, 
]

products=[
    {"id" : 1, "name": "pen", "category": "stationary","price":10},
    {"id" : 2, "name": "shirt", "category": "cloth","price": 200},
]

@app.route('/login',methods=['POST'])
def login():
    username=request.json.get('username')
    password=request.json.get('password')
    if username == "admin" and password == "admin":
        token=create_access_token(identity=username)
        refresh_token=create_refresh_token(identity=username)
        return jsonify({"access_token": token,"refresg_token":refresh_token})
    return {"error":"Invalid credentials"},401

@app.route('/refresh',methods=['POSt'])
@jwt_required
def refresh():
    current_user=get_jwt_identity
    current_jwt=get_jwt()
    if current_jwt['type'] != 'refresh':
        return {"errro":"Only refresh token acceptable"} , 401
    new_token=create_access_token(identity=current_user)
    return jsonify({"access_token":new_token})

@app.route('/logout',methods=['POST'],endpoint="logout")
@jwt_required()
def logout():
    jti=get_jwt()['jti']
    revoked_tokens.add(jti)
    return {"msg": "Logged out successfully"}, 200

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    return jwt_data['jti'] in revoked_tokens
    
@app.route('/users',methods=['GET'])
def get_user():
    return jsonify(users)

@app.route('/users',methods=['POST'])
@jwt_required()
def add_user():
    data=request.json
    if "id" not in data or "name" not in data or "email" not in data:
        return {"error": "id, name, and email fields are required"}, 400
    users_exist=[user for user in users if user["id"] == data["id"] or user["email"] == data["email"]]
    if users_exist:
        return {"error": "id or email fields already present"}, 400

    users.append(data)
    return jsonify(data), 201

@app.route('/user/<int:user_id>',methods=['PUT'],endpoint="update_user")
@jwt_required()
def update_user(user_id):
    for user in users:
        if user['id'] == user_id:
            user.update(request.json)
            return jsonify(user)
    return "Not Found Error" , 404

@app.route('/user/<int:user_id>',methods=['DELETE'],endpoint="delete_user")
@jwt_required()
def delete_user(user_id):
    global users
    users=[user for user in users if user['id'] != user_id]
    return f"User deleted Succesfully"

@app.route('/user/<int:user_id>',methods=['GET'])
def get_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            return jsonify(user)
    return "Not Found User", 404


@app.route('/products',methods=['GET'])
def get_product():
    return jsonify(products)

@app.route('/products',methods=['POST'],endpoint="add_product")
@jwt_required()
def add_product():
    data=request.json
    if 'id' not in data or 'name' not in data or 'price' not in data:
        return {"error":"Id ,Name  and Price are required fields"},400
    product_exist=[product for product in products if product['id'] == data['id']]
    if product_exist:
        return {"error":"Id already exist"},400
    products.append(data)
    return jsonify(data), 201

@app.route('/product/<int:product_id>',methods=['PUT'],endpoint="update_product_by_price")
@jwt_required()
def update_product_price(product_id):
    for product in products:
        if product['id'] == product_id:
            product.update(request.json)
            return jsonify(product)
    return "Not Found Error" , 404

@app.route('/product/<int:product_id>',methods=['DELETE'],endpoint="delete_product")
@jwt_required()
def delete_product(product_id):
    global products
    products=[product for product in products if product['id'] != product_id]
    return f"Product deleted Succesfully"

@app.route('/product/<int:product_id>',methods=['GET'],endpoint="get_product_by_id")
def get_product_by_id(product_id):
    for product in products:
        if product['id'] == product_id:
            return jsonify(product)
    return "Not Found Product", 404

if __name__ == '__main__':
    app.run(debug=True)

