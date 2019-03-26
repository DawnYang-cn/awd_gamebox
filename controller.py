from flask import Flask, request, render_template
import redis
import os
import re
import logging

logging.basicConfig(filename='awd.log',format='[%(asctime)s-%(levelname)s:%(message)s]',level=logging.DEBUG,filemode='a')
app = Flask(__name__)



@app.route('/flag', methods=['POST'])
def get_flag():
    if request.method=='POST':
        flag = request.form['flag']
        token = request.form['token']
	cha = request.form['cha']
	roundnum = request.form['round']
	logging.info("Round "+roundnum+" begin!")
        #f = open(token,'a+')
        #f.write(flag+'\n')
        #f.close()
        r = redis.Redis(host='localhost', port=6379, db=0)
	r.set("round",roundnum)
        r.set(flag,token+"_"+cha)
        r.set(token+"_"+cha,flag)
        #rget = r.get(flag)
	r.set(token+"_"+cha+"_was_attacked_by",",")
	logging.info("Round "+roundnum+" "+token+" "+cha+" current flag is "+flag)
        #print token+" "+cha+" current flag is "+flag+"\n"
        return "---OK!"+token+" "+cha+" "+flag+"---\n"

@app.route('/submit', methods=['POST'])
def check():
    if request.method=='POST':
        submit_flag = request.form['flag']
        submit_token = request.form['token']
	submit_cha = request.form['cha']
        r = redis.Redis(host='localhost', port=6379, db=0)
        pwned_token_cha=r.get(submit_flag)

        if pwned_token_cha == None:
	    logging.info(submit_token+" submit a incorrect flag")
            return "Incorrect Flag!\n"
        elif pwned_token_cha != None:
            true_flag=r.get(pwned_token_cha)
            if pwned_token_cha == submit_token+"_"+submit_cha:
		logging.info(submit_token+" submit his own flag")
                return "You can't submit your own flag\n"
            elif true_flag == submit_flag:
		winner=r.get(pwned_token_cha+"_was_attacked_by")
		winnerlist=winner.split(",")
		print winnerlist
		if submit_token in winnerlist:
		    logging.info(submit_token+" submit flag of "+pwned_token_cha+" again no score")
		    #print submit_token+" submit flag of "+pwned_token_cha+" again"
		    return "Sorry you have already submmited flag of "+pwned_token_cha+" in this round\n"
		else:
		    f=open(submit_token+"_score","r+")
		    score = int(f.readline())
		    score = score+1
		    logging.info(submit_token+" current score is "+score)
		    #print submit_token+":"+str(score)
		    f.seek(0)
		    f.truncate()
		    f.write(str(score))
		    f.close()
		    g=open(pwned_token_cha[0:5]+"_score","r+")
		    score = int(g.readline())
		    score = score-1
		    logging.info(pwned_token_cha[0:5]+" current score is "+score)
		    #print pwned_token_cha+":"+str(score)
		    g.seek(0)
		    g.truncate()
		    g.write(str(score))
		    g.close()
		    winner = winner+submit_token+","
		    r.set(pwned_token_cha+"_was_attacked_by",winner)
		    logging.info(submit_token+" pwned "+ pwned_token_cha)
                    return "Congratulation! You have pwned "+pwned_token_cha+"\n"
            else:
                return "Be careful!You will be punished!\n"
        else:
            return "Be careful!You will be punished!\n"
@app.route('/score',methods=['GET'])
def score():
    if request.method=='GET':
	items = os.listdir(".")
	display=""
	for item in items:
	    if re.match(r'team.*score',item):
		f= open(item,'r')
		display = display+"<th>"+item+"</th>"+"<td>"+f.readline()+"</td>\n"
		f.close()
	    else:
		continue
	#print display
	return render_template('score.html',jy=display)
        


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
