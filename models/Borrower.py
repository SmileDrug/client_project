from mongoengine import *
import datetime
from Embedded_Documents import *

class Borrower(DynamicDocument):
    pullId = DateTimeField(default=datetime.datetime.now()) #This is the date and time when the first loan for the borrower was pulled by our system
    borrower_objectId = StringField(unique=True) #LC-memberId
    memberId = FloatField(unique=True) #Id of member obtained from lending club
    addrState = StringField(default=None)
    addrZip = StringField(default=None)
    empLength = FloatField(default=None)
    empTitle = StringField(default=None)
    homeOwnership = StringField(default=None)
    annualIncJoint = FloatField(default=None)
    desc = StringField(default=None)
    purpose = StringField(default=None)
    applicationType = StringField(default=None)
    credit_bureau = EmbeddedDocumentField(CreditBureau,default=None)
