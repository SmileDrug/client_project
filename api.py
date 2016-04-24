from flask import Flask,abort,request,jsonify
from models import Loans
from models import analytics
from models import Borrower
from models import admin
from models import connector
from flask.ext.cors import CORS
from datetime import datetime,date,time
import pdb
import json

app = Flask(__name__)
CORS(app)

@app.route('/login',methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    user = admin.admin.objects(username=username,password=password).first()
    if user is not None:
            return jsonify({"response":"success"})
    else:
        abort(401)

@app.route('/getstats')
def getstats():
    today = date.today()
    lt_9 = datetime.combine(today,time(9,5))
    gt_9 = datetime.combine(today,time(9,0))

    lt_13 = datetime.combine(today,time(13,5))
    gt_13 = datetime.combine(today,time(13,0))

    lt_17 = datetime.combine(today,time(17,5))
    gt_17 = datetime.combine(today,time(17,0))

    lt_21 = datetime.combine(today,time(21,5))
    gt_21 = datetime.combine(today,time(21,0))

    gt_all = datetime.combine(today,time(9,0))
    lt_all = datetime.combine(today,time(21,0))
    analytics_9 = analytics.Analytics.objects(createD__lt=lt_9,createD__gt=gt_9)
    analytics_13 = analytics.Analytics.objects(createD__lt=lt_13,createD__gt=gt_13)
    analytics_17 = analytics.Analytics.objects(createD__lt=lt_17,createD__gt=gt_17)
    analytics_21 = analytics.Analytics.objects(createD__lt=lt_21,createD__gt=gt_21)
    analytics_today = analytics.Analytics.objects(createD__lt=lt_all,createD__gt=gt_all)
    # pdb.set_trace()
    analytics_today_selected = getSelected(analytics_today)

    summary = getTotalAmount(analytics_today)
    chart_9 = getTotalAmount(analytics_9)
    chart_13 = getTotalAmount(analytics_13)
    chart_17 = getTotalAmount(analytics_17)
    chart_21 = getTotalAmount(analytics_21)

    avg_intRate = calcAverageInterestRate(analytics_today_selected)
    annLoss = calcAnnLosses(analytics_today_selected)
    expected_return = calcExpectedReturn(analytics_today_selected)
    stats = {}
    stats["summary"] = summary
    stats["chart_9"] = chart_9
    stats["chart_13"] = chart_13
    stats["chart_17"] = chart_17
    stats["chart_21"] = chart_21
    stats["avg_intRate"] = avg_intRate
    stats["annLoss"] = annLoss
    stats["expected_return"] = expected_return
    return jsonify(stats)

def getSelected(dataset):
    selected = []
    for d in dataset:
        if d.selected:
            selected.append(d)
    return selected


def getExpectedReturn(dataset):
    pass

def calcAnnLosses(dataset):
    # pdb.set_trace()
    try:
        annLoss = str(sum([float(l.expDefaultRate * l.loanObject.terms.loanAmount) for l in dataset]) / sum([float(l.loanObject.terms.loanAmount) for l in dataset]))
    except:
        return 0
    return round(float(annLoss),2)

def calcAverageInterestRate(dataset):
    # pdb.set_trace()
    try:
        averageInterestRate = str(sum([float(l.loanObject.terms['intRate'] * l.loanObject.terms.loanAmount) for l in dataset]) / sum([float(l.loanObject.terms.loanAmount) for l in dataset]))
    except:
        return 0

    return round(float(averageInterestRate),2)

def calcExpectedReturn(dataset):
    # pdb.set_trace()
    try:
        expectedReturn = str(sum([float(float(l.loanObject.terms['intRate'] - l.expDefaultRate) * l.loanObject.terms.loanAmount) for l in dataset]) / sum([float(l.loanObject.terms.loanAmount) for l in dataset]))
    except:
        return 0
    return round(float(expectedReturn),2)

def getTotalAmount(dataset):
    selected = []
    not_selected = []
    selected_amount =[]
    not_selected_amount=[]
    for d in dataset:
        if d.selected:
            selected.append(d)
            selected_amount.append(d.loanObject.fundedAmount)
        else:
            not_selected.append(d)
            not_selected_amount.append(d.loanObject.fundedAmount)
    totalSelected = sum(selected_amount)
    totalNotSelected = sum(not_selected_amount)
    total = totalSelected + totalNotSelected
    return json.dumps({"selected":str(totalSelected),"not_selected":str(totalNotSelected),"total":str(total)})

if __name__ == "__main__":
    app.run(debug=True)
