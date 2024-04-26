# `banner` Command
This command prints the Harvest banner along with any footer rules that are configured for that banner.

# Usage
```
Usage: banner [-h] [--text TEXT] [names ...]

Positional Arguments:
  names        The name of the report to display. When not provided, all banners are displayed.

Optional Arguments:
  -h, --help   show this help message and exit
  --text TEXT  Allows the user to display arbitrary text using the banner code.
```

# Example
In this example, the `lgbt` and `summer` banners are displayed.

```
[harvest] banner lgbt summer 

 lgbt----------
██╗  ██╗█████╗  ██████╗ ██╗   ██╗███████╗███████╗████████╗
██║  ██║██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
███████║███████║██████╔╝██║   ██║█████╗  ███████╗   ██║   
██╔══██║██╔══██║██╔══██╗╚██╗ ██╔╝██╔══╝  ╚════██║   ██║   
██║  ██║██║  ██║██║  ██║ ╚████╔╝ ███████╗███████║   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚══════╝   ╚═╝   
date: "YYYY-06-*":
It's Pride Month! Take a moment to learn about the LGBTQIA+ community:
https://en.wikipedia.org/wiki/LGBT


 summer----------
██╗  ██╗█████╗  ██████╗ ██╗   ██╗███████╗███████╗████████╗
██║  ██║██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
███████║███████║██████╔╝██║   ██║█████╗  ███████╗   ██║   
██╔══██║██╔══██║██╔══██╗╚██╗ ██╔╝██╔══╝  ╚════██║   ██║   
██║  ██║██║  ██║██║  ██║ ╚████╔╝ ███████╗███████║   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚══════╝   ╚═╝   
date between: "YYYY-06-21" and "YYYY-09-22":
(no footer)
```