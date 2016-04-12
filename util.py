import datetime

def strToDate(string):
    string=string.replace("T"," ")
    string = string[:19]
    _datetime = datetime.datetime.strptime(string,"%Y-%m-%d %H:%M:%S")
    return _datetime
