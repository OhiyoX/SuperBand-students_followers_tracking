from superband import Superband
from apscheduler.schedulers.blocking import BlockingScheduler
import json

def run():
    mz.get_followers()

if __name__ == '__main__':
    mz = Superband()
    with open('config.json',encoding="UTF-8") as f:
        config = json.load(f)
    if config['test_mode']:
        mz.get_followers()
    else:
        scheduler = BlockingScheduler()
        scheduler.add_job(run, 'interval', hours=3)
        try:
            print('clock running')
            scheduler.start()
        except(SystemExit, KeyboardInterrupt):
            pass
