#! /usr/bin/env python

import subprocess
import time

import npstat_settings as settings

"""
Events Queue Producer for npstat
"""

def scan_events(event_queue, event_flag, sleep=10):
    """Scan and queue system events"""
    while(not event_flag.is_set()):
      scan_ssh(event_queue)
      for i in range(sleep * 2):
        if event_flag.is_set():
          break
        time.sleep(0.5)


def scan_ssh(event_queue):
    """Scan and queue system events"""
    try:
      ssh_pids = subprocess.check_output(['pgrep', '-f', 'pts/'])
    except Exception as e:
      ssh_pids = '0'
    ssh_pids = ssh_pids.splitlines()
    for pid in ssh_pids:
      if int(pid) > 0:
        ssh_event = settings.event('ssh', int(pid), [54, 0, 102], 1)
        event_queue.put(ssh_event)
