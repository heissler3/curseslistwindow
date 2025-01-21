
# curseslistwindow

This python module provides two classes:
+ __SelectFromListWindow__
+ __MultiColumnListWindow__

Each are curses windows for displaying list or tabular data.

curses color pairs 13, 14, and 15 are used, and can be set before (or after) instantiation if the default colors aren't preferred.

The interface is very simple.  Keystrokes are passed to the __keypress()__ method:
+ Up and down keys highlight the previous or next row, scrolling one line if at the top or bottom.
+ Pageup or pagedown move to the top or bottom of the window, and from there... page up or page down.
+ Mouse clicks move to a row, scrollwheel works like up and down keys.
+ Spacebar selects a row.
+ Everything else passes through. (Responds with False)

***SelectFromListWindow***(window, list, border)
-    __window__ is a curses window
-    __list__ is a list of strings
-    __border__ is a boolean value of whether or not to draw a surrounding border.  Defaults to False

***MultiColumnListWindow***(window, data, border, colwidths)
-    __window__ is an curses window
-    __data__ is a list of lists (of strings)
-    __border__ is a boolean value of whether or not to draw a surrounding border.  Defaults to True
-    __colwidths__ is a list of integers, column width in chars, with 0 value meaning "divide remaining"
