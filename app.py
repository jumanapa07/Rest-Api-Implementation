from flask import Flask,jsonify,request

app=Flask(__name__)

users=[
    {"id": 1, "name": "Jumi","email": "jumi@example.com"},
    {"id": 2, "name": "Anu","email": "anu@example.com"},
    {"id": 3, "name": "Sandra","email": "sandra@example.com"},
    {"id": 4, "name": "Aparna","email": "aparna@example.com"}, 
]

products=[]

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

@app.route('/user/<int:user_id>',methods=['GET'])
def get_user(user_id):
    for user in users:
        if user[id] == user_id:
            return jsonify(user)
    return "Not Found User", 404


@app.route('/products',methods=['GET'])
def get_product():
    return jsonify(products)

@app.route('/products',methods=['POST'])
def add_product():
    product=request.json
    products.append(product)
    return jsonify(product), 201

@app.route('/product/<int:product_id>',methods=['PUT'])
def update_product_price(product_id):
    for product in products:
        if product['id'] == product_id:
            product.update(request.json)
            return jsonify(product)
    return "Not Found Error" , 404

@app.route('/product/<int:product_id>',methods=['DELETE'])
def delete_user(product_id):
    global products
    products=[product for product in products if product['id'] != product_id]
    return f"Product deleted Succesfully"

@app.route('/product/<int:product_id>',methods=['GET'])
def get_product(product_id):
    for product in products:
        if product[id] == product_id:
            return jsonify(product)
    return "Not Found Product", 404

if __name__ == '__main__':
    app.run(debug=True)

