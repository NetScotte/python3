# -*- coding: utf-8 -*-
"""
功能： curses是linux终端下的图形库，用于在终端中写出好看的图形程序
设计：
备注：
时间：
"""
import curses

def main(stdscr):
    stdscr.clear()
    for i in range(0, 11):
        v = i - 10
        stdscr.addstr(i, 0, "10 divided by {} is {}".format(v, 10/v))
    stdscr.refresh()
    stdscr.getkey()
    pass

# 初始化屏幕
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

curses.wrapper(main)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()