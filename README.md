
# curseslistwindow

This python module provides two classes:
- SelectFromListWindow
- MultiColumnListWindow

Each are curses windows for displaying list or tabular data.

The interface is very simple:
- Up and down keys highlight the previous or next row, scrolling one line if at the top or bottom.
- Pageup or pagedown move to the top or bottom of the window, and from there... page up or page down.
- Mouse clicks move to a row, scrollwheel works like up and down keys.
- Spacebar selects a row.
- Everything else passes through.

*SelectFromListWindow*(window, list)
    *window* is a curses window
    *list* is a list of strings

*MultiColumnListWindow*(window, data, colwidths)
    *window* is an curses window
    *data* is a list of lists (of strings)
    *colwidths* is a list of integers, column width in chars, with 0 value meaning "divide remaining"
