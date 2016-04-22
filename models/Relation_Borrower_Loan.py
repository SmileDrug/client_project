from mongoengine import *
from Borrower import *
from Loans import *

class Borrower_AND_Loan(DynamicDocument):
    borrower = ReferenceField(Borrower,reverse_delete_rule=mongoengine.CASCADE)
    loan = ReferenceField(Loans,reverse_delete_rule=mongoengine.CASCADE)
