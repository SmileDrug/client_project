import requests
import json
import os
from settings import *
import json
import pdb
from models import Borrower,Embedded_Documents,connector,Loans,Relation_Borrower_Loan,analytics as analytics_mongo
import datetime
from util import *
from analytics import *
import schedule
import time
from datetime import datetime

def getDataFromAPI():
    payload = {'showAll' : 'false'}
    requests.HTTPError
    resp = requests.get(loanListURL, headers = header, params = payload)
    resp.raise_for_status()
    return resp.json()['loans']
# 81562703
def JSONTODB(_JSON):
    if _JSON is not None:
        #First lets work with borrower
        data = _JSON
        for d in data:
            #First lets work with borrower
            # import pdb;pdb.set_trace()
            memberId = d["memberId"]
            borrower = Borrower.Borrower.objects(memberId=memberId).first()
            if borrower is None:
                borrower = Borrower.Borrower()
            print d["memberId"]
            borrower["borrower_objectId"] = "LC-" + str(d["memberId"])
            borrower["memberId"] = d["memberId"]
            borrower["addrState"] = d["addrZip"]
            try:
                borrower["empLength"] = float(d["empLength"])
            except:
                pass
            borrower["empTitle"] = d["empTitle"]
            borrower["homeOwnership"] = d["homeOwnership"]
            try:
                borrower["annualIncJoint"] = float(d["annualIncJoint"])
            except:
                pass
            borrower["desc"] = d["desc"]
            borrower["purpose"] = d["purpose"]
            borrower["applicationType"] = d["applicationType"]
            credit_buereu = Embedded_Documents.CreditBureau()
            for c in credit_buereu:
                try:
                    credit_buereu[c] = float(d[c])
                except:
                    pass
            borrower["credit_buereu"] = credit_buereu
            borrower.save()
            #Now its time by Loan
            loan = Loans.Loans()
            loan["id_obtained_from_platform"] = str(d["id"])
            loan["creditPullD"] = strToDate(d["creditPullD"])
            loan["expD"] = strToDate(d["creditPullD"])
            loan["listD"] = strToDate(d["listD"])
            try:
                loan["isIncVJoint"] = strToDate(d["isIncVJoint"])
            except:
                pass
            loan["acceptD"] = strToDate(d["acceptD"])
            loan["initialListStatus"] = d["initialListStatus"]
  #          import pdb;pdb.set_trace()
            try:
                loan["reviewStatusD"] = strToDate(d["reviewStatusD"])
            except:
                loan["reviewStatusD"] = None
            loan["fundedAmount"] = float(d["fundedAmount"])
            loan["reviewStatus"] = d["reviewStatus"]
            if d["isIncV"] == "VERIFIED":
                loan["isIncv"] = True
            else:
                loan["isIncv"] = False
            try:
                loan["investorCount"] = float(d["investorCount"])
            except:
                pass
            platform = Embedded_Documents.Platform_Underwriting()
            try:
                platform["dtiJoint"] = float(d["dtiJoint"])
            except:
                pass
            platform["dti"] = float(d["dti"])
            # pdb.set_trace()
            try:
                platform["Rating"] = str(d["Rating"])
                platform["Default_Rate"] = str(d["Default_Rate"])
            except:
                pass

            platform["grade"] = str(d["grade"])
            platform["subGrade"] = str(d["subGrade"])
            loan["platform_underwriting"] = platform
            terms = Embedded_Documents.Terms()
            for t in terms:
                terms[t] = float(d[t])
            loan["terms"] = terms
    	    loan["pullD"] = datetime.now()
            loan.save()
    	    # pd = toEST(pd)
            # print pd
    	    loan = loan.save()
            #Below function will perform will perform analytics on a single loan object
            analyticsObject = analytics_mongo.Analytics()
            analyticsBrain = Analytics(d)
            analyticsBrain.performAnalytics()
            analyticsObject.loanObject = loan

            analyticsObject.postLoanDebtToIncome = analyticsBrain.postLoanDebtToIncome
            analyticsObject.loanToIncome = analyticsBrain.loanToIncome
            analyticsObject.selected = analyticsBrain.selected
            analyticsObject.expDefaultRate = analyticsBrain.expDefaultRate
            analyticsObject.exposure_Cap = analyticsBrain.exposure_Cap
            analyticsObject.jpScore = analyticsBrain.JPscore
            analyticsObject.save()
            # analyticsObject.createD = toEST(analyticsObject.id.generation_time)
    	    # analyticsObject.save()
            #Many to many relationship between Loan and borrower
            relation = Relation_Borrower_Loan.Borrower_AND_Loan()
            relation.borrower = borrower
            relation.loan = loan
            relation.save()
    else:
        print "nothing json found"

def job():
    json_data = getDataFromAPI()
    JSONTODB(json_data)

schedule.every().day.at("09:00").do(job)
schedule.every().day.at("13:00").do(job)
schedule.every().day.at("17:00").do(job)
schedule.every().day.at("21:00").do(job)

while 1:
    print "started again"
    schedule.run_pending()
    print "ended"
    time.sleep(1)
