from flask import Flask, jsonify, request, Response
import json, uuid
import numpy as np
import PIL
from PIL import Image
import datetime
import the_best_chatbot as bot

app = Flask(__name__)
model = None

@app.route('/', methods=["GET"])
def api_root():
  return 'Welcome! I am cruxbreaker. How may I help you today?'

@app.errorhandler(404)
def not_found(error=None):
  message = {
          'status': 404,
          'message': 'Not Found: ' + request.url,
  }
  resp = jsonify(message)
  resp.status_code = 404

  return resp

@app.route('/message', methods=["POST"])
def message_api():
  # Preprocess the image so that it matches the training input
  if request.headers['Content-Type'] == 'application/json':
    # print(request.get_json()["message"])
    input_message = request.get_json()["message"]

    # Use the loaded model to generate a prediction.
    global model
    if (model == None):
      model = bot.build_model()
      
    reply_message = bot.chat(model, input_message)

    # Prepare and send the response.
    message = {
      "_id": str(uuid.uuid1()),
      "imput_message": input_message,
      'data': reply_message,
      'timestamp': datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    }
    message = json.dumps(message)
    print(message)

    resp = Response(message, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://cruxbreaker.github.io'

  else:
    resp = Response("415 Unsupported Media Type ;)", status=400, mimetype='application/json')

  return resp

if __name__ == "__main__":
  app.run()