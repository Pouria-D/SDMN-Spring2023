from flask import Flask, json, request

status = {"status": "OK"}

api = Flask(__name__)

@api.route('/api/v1/status', methods=['GET'])
def get_status():
	return json.dumps(status), 200

@api.route('/api/v1/status', methods=['POST'])
def post_status():
	global status
	status = request.get_json()
	return json.dumps(status), 201


if __name__ == '__main__':
	api.run(host="0.0.0.0", port=8000)

