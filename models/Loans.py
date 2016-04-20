from mongoengine import *
import datetime
from Embedded_Documents import *

class Loans(DynamicDocument):
    pullD = DateTimeField(default=datetime.datetime.now()) #This is the date and time when the loan was pulled by our system
    platform = StringField(default="LC")
    id_obtained_from_platform = StringField()
    creditPullD = DateTimeField() #Credit Pull date time obtained from platform
    expD = DateTimeField()
    listD = DateTimeField()
    isIncVJoint = BooleanField()
    acceptD = DateTimeField()
    initialListStatus = StringField()
    reviewStatusD = DateTimeField(default=None)
    fundedAmount = FloatField()
    reviewStatus = StringField()
    isIncV = BooleanField()
    investorCount = FloatField()
    platform_underwriting = EmbeddedDocumentField(Platform_Underwriting)
    terms = EmbeddedDocumentField(Terms)
