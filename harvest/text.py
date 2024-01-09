from rich.console import Console
from rich.text import Text, Style
console = Console()


def output(text: str, **style) -> str:
    result = Text(text=text,
                  style=Style(**style))

    return result


if __name__ == '__main__':
    console.print(output("Test", color='#000087'))
    console.print(output("Test", color='#005f00'))
    console.print(output("Test", color='#00d7af'))
    console.print(output("Test", color='#870000'))
