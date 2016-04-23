class Analytics:
    step1 = []
    step2 = []
    CONST_1 = 509
    CONST_2 = 816
    X = 1
    ATTRIBUTE_1 = 'revolUtil'

    def __init__(self,loanObject):
        #step1
        self.step1 = []
        self.step2 = []
        self.table = []
        self.CONST_1 = 509
        self.CONST_2 = 816
        self.X = 1
        self.ATTRIBUTE_1 = 'revolUtil'
        with open('limits.txt','r') as fp:
            for line in fp:
                l = line.split(' ')
                limit = {}
                limit['lower'] = float(l[0])
                limit['variable'] = l[1]
                limit['higher'] = float(l[2])
                self.step1.append(limit)
        #step2
        # #import pdb;pdb.set_trace()
        with open('weights.txt','r') as fp:
            for line in fp:
                l = line.split(' ')
                weights = []
                for w in l:
                    weights.append(float(w))
                self.step2.append(weights)
        self.loanObject = loanObject

        with open('selection_table.txt','r') as fp:
            for line in fp:
                l = line.split(' ')
                row = {}
                row['min'] = float(l[0])
                row['max'] = float(l[1])
                row['rating'] = float(l[2])
                row['drate'] = float(l[3])
                row['ecap'] = float(l[4])
                self.table.append(row)

    def calcScore(self,loan, dummy, weight, const):
        # import pdb;pdb.set_trace()
        score = const
        for i in range(len(dummy)):
            score += dummy[i]*weight[i]
        return score

    def calc_exposure_Cap(self,l):
    	for t in self.table:
    		if l['JPscore'] >= t['min'] and l['JPscore'] <= t['max']:
    			l['Rating'] = t['rating']
    			l['Default_Rate'] = t['drate']
    			l['Exposure_Cap'] = t['ecap']


    def performAnalytics(self):
        #-------------------Calculating JPscore-------------------------#
        dummy = []
        l = self.loanObject
        l["loanToIncome"] = 100*l['loanAmount']/max(0.1, l['annualInc'])
        l["postLoanDebtToIncome"] = 100*(l['installment'] \
        + (l['dti']/100)*(l['annualInc']/12))/max(0.001, l['annualInc']/12)

        for i in self.step1:
            var = i["variable"]
            if l[var] >= i['lower'] and l[var] < i['higher']:
                dummy.append(1)
            else:
                dummy.append(0)
        if l[self.ATTRIBUTE_1] is None:
            l[self.ATTRIBUTE_1] = 0.0
        if float(l[self.ATTRIBUTE_1]) <= 50:
            l["JPscore"] = self.calcScore(l, dummy, self.step2[0], self.CONST_1)
        else:
            l["JPscore"] = self.calcScore(l, dummy, self.step2[1], self.CONST_2)
            #---------------------End Calculating JPscore -------------------#

            #-------------------------------Selected or Not-------------------------------
        # if l["JPscore"] < self.X:
        #     self.selected = True
        # else:
        #     self.selected = False

        self.calc_exposure_Cap(l)
    	if l['Default_Rate'] == None:
            self.selected = False
    	elif l['intRate'] - l['Default_Rate'] > self.X:
            self.selected = True
    	else:
            self.selected = False

        self.JPscore = l["JPscore"]
        self.expDefaultRate = l["expDefaultRate"]
        self.exposure_Cap = l["Exposure_Cap"]
        self.loanToIncome = l["loanToIncome"]
        self.postLoanDebtToIncome =l["postLoanDebtToIncome"]
