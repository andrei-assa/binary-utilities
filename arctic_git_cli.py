#! /Users/andrei_assa/bin/bin/python
import os
import sys
from typing import Any, List

import click
import sendgrid
import six
from pyconfigstore import ConfigStore
from PyInquirer import (
    prompt,
    style_from_dict,
)
from pyfiglet import figlet_format

try:
    import colorama

    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


def log(string: str, color: str, font: str = "slant", figlet: bool = False) -> None:
    """Log message to the command line.

    Args:
        string (str): The message to log.
        color (str): [description]
        font (str, optional): Font style to use. Defaults to "slant".
        figlet (bool, optional): Whether to use Figlet formatting. Defaults to False.
    """
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(string, font=font), color))
    else:
        six.print_(string)


class ChoiceGenerator(object):
    def __init__(self) -> None:
        pass

    def _get_file_lines(self, filepath: str) -> List[str]:
        """Get lines from a file.

        Args:
            filepath (str): Absolute or relative path to a TODO.md file.

        Returns:
            List[str]: List of tasks in the TODO.md file.
        """
        with open(filepath) as f:
            file_lines = f.readlines()
        return file_lines

    def _format_lines(self, line: str, output_list: List[str]) -> None:
        line = line.strip()
        if line.endswith("."):
            line = line[:-1]
        if line.startswith("- [ ]"):
            line = line[6:]
            output_list.append(line)

    def get_choices(self, filepath: str) -> List[str]:
        output_list: List[str] = []
        file_lines = self._get_file_lines(filepath=filepath)
        for line in file_lines:
            self._format_lines(line=line, output_list=output_list)
        return output_list


def ask_question() -> Any:

    choice_generator = ChoiceGenerator()

    cwd = os.getcwd()
    filepath = f"{cwd}/TODO.md"
    choices = choice_generator.get_choices(filepath=filepath)
    choices.append("Exit")

    questions = [
        {
            "type": "list",
            "name": "tasks",
            "message": "Which task did you complete?",
            "choices": choices,
        },
    ]
    answers = prompt(questions)
    return answers


def modify_template(task_name: str) -> None:
    home = os.path.expanduser("~")
    with open(f"{home}/.gitmessage_template") as f:
        template = f.read()
    template = template.replace("<TASK>", task_name)
    with open(f"{home}/.gitmessage", "w") as f:
        f.write(template)


@click.command()
def main() -> None:
    """Main program function."""
    log("Arctic Git CLI", "blue", figlet=True)

    answer = ask_question()
    tasks = answer["tasks"]
    if tasks == "Exit":
        print("Bye")
        sys.exit(0)
    modify_template(tasks)
    os.system("git commit")


if __name__ == "__main__":
    main()
