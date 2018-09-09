
import Calculation
import Class
import tasks


# Example to add a daily task to the schduler
from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler

def QT_Engineering():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tasks.task1, 'interval', seconds=1)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()

QT_Engineering()