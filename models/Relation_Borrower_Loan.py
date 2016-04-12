from mongoengine import *
from Borrower import *
from Loans import *

class Borrower_AND_Loan(DynamicDocument):
    borrower = ReferenceField(Borrower)
    loan = ReferenceField(Loans)
