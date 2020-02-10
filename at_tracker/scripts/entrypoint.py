import os
import argparse
from shutil import which

loglevel = os.environ.get('LOGLEVEL', 'debug').lower()


celery_cmd = [
    'celery',
    '-A', 'at_tracker.celery.app',
    f'--loglevel={loglevel}'
]

cmds = {
    'api': ['uvicorn', 'at_tracker.api.main:app',
            '--workers', '2', '--host', '0.0.0.0',
            f'--log-level={loglevel}'],
    'celery_worker': celery_cmd + ['worker'],
    'celery_beat': celery_cmd + ['beat']
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd',
                        help='the cmd to run',
                        choices=[k for k in cmds.keys()],
                        type=str)
    args = parser.parse_args()

    print(which(cmds[args.cmd][0]))
    os.execv(which(cmds[args.cmd][0]), cmds[args.cmd])