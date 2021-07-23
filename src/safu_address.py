import csv
import time
import pyperclip
import difflib

from rich.console import Console
from rich.pretty import pprint
from rich.progress import Progress
from rich.table import Table
from rich.panel import Panel

console = Console()


class Scanner():
    def scan(self, target):
        with Progress() as progress:
            pyperclip.copy(target[1])
            console.print(
                f'Copied the address [bold cyan]{target[1]}[/] to the clipboard.')
            scanCoin = progress.add_task(
                f'[gray]Scanning for [bold]{target[0]} [/]hijacking...', total=5)
            for i in range(5):
                progress.update(scanCoin, advance=1)
                data = pyperclip.paste()
                if(data != target[1]):
                    progress.update(
                        scanCoin, description=f'Scanned [bold]{target[0]}[/]: [bold red] INFECTED[/].\n')
                    return False, data
                time.sleep(1)
            progress.update(
                scanCoin, description=f'Scanned [bold]{target[0]}[/]: [bold green] SAFE[/].\n')
        return True, target[1]


scanner = Scanner()


def init():
    title = '''
   _____       ____            ___       __    __                   
  / ___/____ _/ __/_  __      /   | ____/ /___/ /_______  __________
  \__ \/ __ `/ /_/ / / /_____/ /| |/ __  / __  / ___/ _ \/ ___/ ___/
 ___/ / /_/ / __/ /_/ /_____/ ___ / /_/ / /_/ / /  /  __(__  |__  ) 
/____/\__,_/_/  \__,_/     /_/  |_\__,_/\__,_/_/   \___/____/____/  
                                                                    '''
    console.print(f'[bold white]{title}\n')
    console.print(
        '[!] The addresses mentioned below are donation addresses. \
        \nFeel free to[bold green] donate [/]if you think this tool has helped you.\n')


def loadCoins():
    f = open('../data/samples.csv', 'r')
    contents = csv.reader(f, delimiter=',')
    coins = list(contents)[1:]
    table = Table(title="Loaded donations addresses", show_lines=True)
    table.add_column('Coin')
    table.add_column('Address')
    for c in coins:
        table.add_row(*c)
    console.print(table)
    return coins


def askPermission():
    options = ['YES', 'NO', 'N', 'Y']
    response = ''
    while response.upper() not in options:
        response = console.input(
            '[bold red][*] The scanner will delete everything you have copied before, continue? (Y/N)')
    return response.upper() in ['Y', 'YES']


if __name__ == '__main__':
    init()
    coins = loadCoins()
    if askPermission():
        # Empty line
        console.print()
        for c in coins:
            results = scanner.scan(c)
            if(results[0] is False):
                msg = f'[bold][!] Your computer may be infected, we copied the {c[0]} address [cyan]{c[1]}[/] but it got replaced by [red]{results[1]}[/] instead.'
                infected = Panel(msg,title='[bold red]Infected')
                console.print(infected)
                exit(1)
        console.print(Panel(
            f'Your device seems to be [bold green]safe[/].\nYou can close the application now.\n[♥] Feel free to [bold green]donate[/] if this tool has helped you.',title='[bold]Results'))
