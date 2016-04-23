from flask import Flask,abort,request,jsonify
from models import Loans
from models import analytics
from models import Borrower
from models import admin
from models import connector
from flask.ext.cors import CORS
from datetime import datetime,date,time

app = Flask(__name__)
CORS(app)

@app.route('/login',methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    user = admin.admin.objects(username=username,password=password).single()
    if user is not None:
            return jsonify({"response":"success"})
    else:
        abort(403)

@app.route('/getstats')
def getstats():
    import pdb;pdb.set_trace()
    today = date.today()
    _date = datetime.combine(today,time(13,5))
    print _date
    loans = Loans.Loans.objects(pullD__lt=_date)
    print len(loans)
    print loans[0].id
    return "success"

if __name__ == "__main__":
    app.run()
