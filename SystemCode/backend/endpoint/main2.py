from tabnanny import filename_only
from flask import Flask, request, jsonify, send_file, make_response
import base64
import io
import json
#from NUS_ISS_chatbot.chatbot import load_chain
from NUS_ISS_chatbot.chatbot_gpt4 import load_chain
from NUS_ISS_chatbot.understandimages import clearAndLoadTextTokensFromFile
from NUS_ISS_chatbot.understandimages import findSuitableImage2

from flask_cors import CORS

app = Flask("__name__")
CORS(app)

chat_history = []
text_tokens = {}
chain = load_chain()
global_parameter1 = 0
global_parameter2 = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global global_parameter1, global_parameter2
    if request.method == 'POST':
        global_parameter1 = request.form.get('parameter1')
        global_parameter2 = request.form.get('parameter2')
        return f"Parameters updated successfully. Parameter 1: {global_parameter1}, Parameter 2: {global_parameter2}"
    return render_template('index.html')


@app.route('/api/chat/')
def chat():

    question = request.args.get('data') 
    print ("Received from caller: " + str(question))

    similarimage = findSuitableImage2(str(question), text_tokens)
    print(similarimage)

    result = chain({"question": str(question), "chat_history": chat_history})
    chat_history.append((question, result['answer']))
    responseMessage = result['answer']
     
    # If there is an image
    filename = similarimage#'image/sample.png'
    with open(filename, 'rb') as f:
        image_data = f.read()
    
    encoded_img = base64.b64encode(image_data).decode('utf-8')
    
    response = {'image':encoded_img, 'answer':responseMessage}

    
    return jsonify(response)

if __name__ == '__main__':
    text_tokens = clearAndLoadTextTokensFromFile()
    app.run()
