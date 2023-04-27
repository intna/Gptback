import requests
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
from pymongo import MongoClient
import threading



app = Flask("gptback")
CORS(app)

#mongoDB全局配置
client = MongoClient('mongodb://cris:Zhang1027.@43.156.132.105:27017/')
db = client['wechat']
collection = db['chatInfo']
#API KEY
openai.api_key = "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"

#请求路由
@app.route("/chat",methods = ['POST'])
def go():
    content = request.json.get("content")
    openid = request.json.get("openid")
    if content.strip() and openid.strip():
        message = {
            'status': 200,
            'message': '已经拿到表单数据'
        }
        thread = threading.Thread(target=chat, args=(content, openid))
        thread.start()
        return jsonify(message)
    else:
        return jsonify({'error': '未拿到有效信息'})

#调用API方法
def chat(content,openid):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",  # gpt-3.5-turbo-0301
        messages=[
            {"role": "system", "content": "you are a helpful assistant"},
            {"role": "user", "content": content}
        ],
        temperature=0.5
    )
    message = str(response.choices[0].message.content)
    result = str({"openid": openid, "content": message})
    results = result.encode("utf-8")
    collection.insert_one({"openid": openid,"content": message})
    return None

@app.route("/test",methods = ['POST'])
def test():
    content = request.json.get("content")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",  # gpt-3.5-turbo-0301
        messages=[
            {"role": "system", "content": "you are a helpful assistant"},
            {"role": "user", "content": content}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content









if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)




