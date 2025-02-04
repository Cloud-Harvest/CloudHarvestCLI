#!/usr/bin/env python
from app import Harvest


if __name__ == '__main__':
    with Harvest() as harvest:
        harvest.cmdloop()

    print('Goodbye!')
