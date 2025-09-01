import sys
import os

def get_interactive_input(prompt):
    if sys.stdin.isatty():
        return input(prompt).strip()
    else:
        try:
            with open('/dev/tty', 'r') as tty:
                sys.stdout.write(prompt)
                sys.stdout.flush()
                return tty.readline().strip()