from flask import Flask, request
import redis

app = Flask(__name__)


@app.route('/flag', methods=['POST'])
def get_flag():
    if request.method=='POST':
        flag = request.form['flag']
        token = request.form['token']
        #f = open(token,'a+')
        #f.write(flag+'\n')
        #f.close()
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.set(flag,token)
        r.set(token,flag)
        rget = r.get(flag)
        print rget+" current flag is "+flag+"\n"
        return "---OK!"+token+" "+flag+"---\n"

@app.route('/submit', methods=['POST'])
def check():
    if request.method=='POST':
        submit_flag = request.form['flag']
        submit_token = request.form['token']
        r = redis.Redis(host='localhost', port=6379, db=0)
        pwned_token=r.get(submit_flag)

        if pwned_token == None:
            return "Incorrect Flag!\n"
        elif pwned_token != None:
            true_flag=r.get(pwned_token)
            if pwned_token == submit_token:
                return "You can't submit your own flag\n"
            elif true_flag == submit_flag:
                return "Congratulation! You have pwned "+pwned_token+"\n"
            else:
                return "Something wrong!\n"
        else:
            return "Something wrong!\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
