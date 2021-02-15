import os
import sys
from pprint import pprint, pformat
import click
from colorama import init as init_term, AnsiToWin32
from termcolor import colored
# colorful terminal initializacion
init_term(wrap=True, autoreset=True)
stream = AnsiToWin32(sys.stderr).stream

'''
utils:
START / RESUME TIMER
pie start

PAUSE CURRENT TIMER (latest)
pie pause
>> echo: "paused <id> timer (current: HH:mm:ss)"

STOP CURRENT TIMER (latest)
pie finish
>> echo: "finished <id> timer (total: HH:mm:ss)"

TIMER NAMING
pie start baruc/vui-123/task-name
CATEGORIES
pie start baruc/vui-123/task-name -kw/--keywords="valiot"
pie start baruc/vui-123/task-name -kw/--keywords="valiot, valiot ui"
pie start baruc/vui-123/task-name -kw/--keywords="programming"
pie start baruc/vui-123/task-name -kw/--keywords="homework"
LIST
pie list
pie list
LIST RUNNING
pie list -r
pie list --running
pie -lr
LIST PAUSED
pie list -p
pie list --paused
pie -lp
LIST FILTER
pie list -f --done/--paused/--running
pie list --filter --done/--paused/--running
pie -lf --done/--paused/--running
pie -lf --regex "vui"
# STATUS: RUNNING
# baruc/vui-123/task-name
# STATUS: PAUSED
# baruc/vui-124/task-2
# baruc/vui-125/task-3
REPORTS
# TODO: enlist Possible report types
'''
home_dir = os.environ['HOME']
cfg_dir = os.path.join(home_dir, '.pietimer')
timers_filename = 'timers.json'
timers_path = os.path.join(cfg_dir, timers_filename)

default_config_data = {
  'status': {
    'last_timer_id': None
  },
  'timers': {}
}

def get_config():
  '''
    timers structure:
    {
      status: {
        last_timer_id: 0
      },
      timers: {
        timer1: {
          status: 'running', # running / paused / finished
          intervals: [
            {
              start_at: '<iso8601_string>',
              end_at: None
            }
          ]
        },
        timer2: {
          status: 'paused', # running / paused / finished
          intervals: [
            {
              start_at: '<iso8601_string>',
              end_at: '<later iso8601_string>'
            }
          ]
        },
        ...
      }
    }
  '''
  import os
  import json
  # validate directories information:
  if not os.path.exists(cfg_dir):
    print(colored('No configuration directory found!! creating...', 'yellow'))
    try:
      os.makedirs(cfg_dir)
    except Exception as e:
      print(colored(f'error creating config directory: \n{e}', 'red'))
      return None # no config dir, no timers to return
    else:
      print(colored('created config directory successfully', 'white'))
  # fetch timers information:
  if not os.path.exists(timers_path):
    print(colored('First timer ever! yaay!', 'green'))
    return default_config_data
  with open(timers_path) as timers_file:
    content = ''.join(timers_file.readlines())
    try:
      parsed_content = json.loads(content)
      return parsed_content
    except Exception as e:
      print(colored(f'error reading configuration file! u sure is a lawful json file?\n{e}'))

def init_config_file(config):
  import json
  serialized_config = json.dumps(config, indent=2)
  with open(timers_path, 'w+') as config_file:
    config_file.write(serialized_config)

def print_timers(timers):
  import pydash as __
  timers_by_status = __.group_by(timers, 'status')
  active_timers = __.filter_(timers_by_status, {'status': 'running'})
  paused_timers = __.filter_(timers_by_status, {'status': 'paused'})
  finished_timers = __.filter_(timers_by_status, {'status': 'finished'})
  if active_timers:
    print(colored(f'ACTIVE TIMERS:', 'green'))
    for timer in active_timers:
      print(colored(f'\ttimer: {timer[]}', 'white'))
  if paused_timers:
    print(colored(f'PAUSED TIMERS:', 'yellow'))
  if finished_timers:
    print(colored(f'FINISHED TIMERS:', 'gray'))

@click.group()
def cli():
  pass

# ! COMMANDS

# * START COMMAND
@click.command(help='start/resume a timer')
@click.option('-n', '--name', help='name of the timer to start (task name/identifier)')
@click.option('-kw', '--keywords', multiple=True, help='categor(y/ies) to put the timer on (ej: work, homework, etc)')
def start(name, keywords):
  import json
  import datetime as dt
  import dateutil.parser
  # 1. check if timer already exists:
  config = get_config()
  if not config:
    print(colored('error reading config file :(\n\naborted mission', 'red'))
    return
  timers = config['timers']
  if not timers:
    init_config_file(config)
  # 2. extract corresponding timer or create a new one:
  if name:
    timer_id = name
  else:
    # get
    timer_id = config['status']['last_timer_id']
    if timer_id:
      if (status:= config['timers'][timer_id]['status']) == 'finished':
        timer_id += 1
    config['status']['last_timer_id'] = timer_id
  # check if timer exists, else initialize it:
  if not timers.get(timer_id):
    timers[timer_id] = {'status': 'initializing', 'intervals': []}
    print(colored('new timer created +++', 'green'))
  if timers[timer_id]['status'] == 'finished':
    print(colored('oops! this timer already finished, goodbye!', 'yellow'))
    return
  if timers[timer_id]['status'] == 'running':
    print(colored('oops! this timer is already running! try finishing it or starting another one!', 'yellow'))
    return
  time = dt.datetime.now()
  if not timers[timer_id]['intervals']:
    timers[timer_id]['intervals'].append({
      'start_at': time.isoformat(),
      'end_at': None
    })
  # be it an initializing or paused timer, move it to running:
  timers[timer_id]['status'] = 'running'
  new_config = json.dumps(config, indent=2)
  with open(timers_path, 'r+') as config_file:
    config_file.seek(0)
    config_file.write(new_config)
    config_file.truncate()
  print(colored(f'timer started successfully! (@ {time.isoformat()})', color='green'))
  
@click.command(help='List all timers, possibly filtered by status / keywords')
def _list():
  import json
  import datetime as dt
  import dateutil.parser
  config = get_config()
  if not config:
    print(colored('error reading config file :(\n\naborted mission', 'red'))
    return
  timers = config['timers']
  if not timers:
    print(colored('no timers ever created, dude', 'yellow'))
  print_timers(timers)


def main():
  cli.add_command(start)
  cli.add_command(_list, name='list')
  cli()

if __name__ == "__main__":
  main()