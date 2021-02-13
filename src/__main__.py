import sys
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

def get_timers():
  import os
  if not os.path.exists('~/.pietimer'):
    print(colored('No configuration directory found!! creating...', 'yellow'))

@click.group()
def cli():
    pass

# ! COMMANDS

# * START COMMAND
@click.command(help='start/resume a timer')
@click.option('-n', '--name', help='name of the timer to start (task name/identifier)')
@click.option('-kw', '--keywords', multiple=True, help='categor(y/ies) to put the timer on (ej: work, homework, etc)')
def start(name, keywords):
  import datetime as dt
  # 1. check if timer already exists:
  timers = get_timers()
  time = dt.datetime.now()
  print(colored(f'''started { "'" + name + "' " if name else ""}timer. Keywords: {", ".join(keywords) if keywords else ""}''', color='green'))
  print(colored(time.isoformat(), color='green'))

def main():
    cli.add_command(start)
    cli()

if __name__ == "__main__":
  main()