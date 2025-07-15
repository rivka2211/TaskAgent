from flask import Flask, request, jsonify
from exanple import agent

app = Flask(__name__)


# @app.route('/api/resource', methods=['POST'])
# async def create_resource():
#     data = request.json
#     response= await openai_chat_completion("אני צריכה לקפל היום כביסה")
#     print(response)
#     return jsonify({'message': 'Resource created!', 'data': data}), 201

@app.route('/api/resource', methods=['GET'])
async def  get_resource():
    print("in get function")
    response =  agent("אני צריכה לקפל היום כביסה")
    print("after openai_chat_completion")
    print(response)
    return jsonify({"message": "Resource created!", "data": "good-day"}), 200

if __name__ == '__main__':
    app.run(debug=True)
