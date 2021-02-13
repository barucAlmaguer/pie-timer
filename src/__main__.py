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

@click.group()
def cli():
    pass

# ! COMMANDS

# * START COMMAND
@click.command()
@click.option('--start', default=None, help='Graphql schema file to clean')
@click.option('--dst', default=None, help='Graphql schema file path to store the new file')
def start(src, dst):


def main():
    cli.add_command(cleanup)
    cli.add_command(validate_schema)
    cli.add_command(build_classes)
    cli()

if __name__ == "__main__":
  main()