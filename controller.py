from flask import Flask, request
import redis

app = Flask(__name__)


@app.route('/flag', methods=['POST'])
def get_flag():
    if request.method=='POST':
        flag = request.form['flag']
        token = request.form['token']
        f = open(token,'a+')
        f.write(flag+'\n')
        f.close()
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.set(token,flag)
        rget = r.get(token)
        print rget
        return "---OK!"+token+" "+flag+"---\n"

@app.route('/submit', methods=['POST'])
def check():
    if request.method=='POST':
        sflag = request.form['flag']
        token = request.form['token']
        r = redis.Redis(host='localhost', port=6379, db=0)
        flag = r.get(token)
        if flag==sflag:
            return "correct\n"
        else:
            return "wrong\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
