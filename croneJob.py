import schedule

def job():

    print "yahh"

i=1
schedule.every().day.at("13:00").do(job)
schedule.every().day.at("09:00").do(job)
schedule.every().day.at("21:00").do(job)
schedule.every().day.at("17:00").do(job)

def start():
    while i==1:
        schedule.run_pending()

def stop():
    i=2

if __name__ ==  "__main__":
    while i==1:
        schedule.run_pending()
