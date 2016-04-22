from mongoengine import *
from Loans import *

class Analytics(DynamicDocument):
    createD = DateTimeField(default=datetime.datetime.now())
    loanObject = ReferenceField(Loans,reverse_delete_rule=CASCADE)
    postLoanDebtToIncome = FloatField()
    loanToIncome = FloatField()
    selected = BooleanField()
    expDefaultRate = FloatField()
    exposure_Cap = FloatField()
    jpScore = FloatField()
