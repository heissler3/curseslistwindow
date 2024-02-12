#
# curseslistwindow.py
#
# Henry Eissler III
#
# July 14th, 2020
#
import curses

class SelectFromListWindow():
    """
    single column curses window.
    data is a list of strings.
    keypress function returns True if handled, False if not
    methods 'draw_window' and 'refresh_list' mostly exist
      to be overridden by derived classes.
    """

    def __init__(self, window, data, border=False):
        self.win = window
        self.list = data
        self.list_length = len(self.list)
        self.offset = 0
        self.current = 0
        self.line_count = 0
        self.width = 0
        self.drawborder = border
        self.selected = [False for x in range(self.list_length)]
        (self.dy, self.dx) = self.win.getbegyx()
        if self.drawborder:
            self.dy += 1
            self.dx += 1

    def draw_window(self):
        self.win.clear()
        (maxrows, maxcols) = self.win.getmaxyx()
        self.line_count = min(self.list_length, maxrows)
        self.width = maxcols
        self.draw_list()

    def write_row(self, index):
        outputstring = self.list[index]
        line = index - self.offset
        if line < 0 or line > (self.line_count - 1):
            return
        attr = (curses.color_pair(3)|curses.A_BOLD) if (index == self.current) else 0
        if self.selected[index]:
            attr |= curses.A_BOLD
        self.win.move(line, 0)
        self.win.clrtoeol()
        if len(outputstring) > self.width:
            self.win.insnstr(outputstring, self.width, attr)
        else:
            self.win.insstr(outputstring, attr)

    def draw_list(self):
        if self.list_length > 0:
            bottom = self.offset + self.line_count
            for idx in range(self.offset, bottom):
                self.write_row(idx)
            self.refresh_list()

    def refresh_list(self):
        self.win.noutrefresh()
        curses.doupdate()

    def new_data(self, data):
        self.list = data
        self.list_length = len(data)
        self.selected = [False for x in range(self.list_length)]
        self.line_count = min(self.list_length, self.win.getmaxyx()[0])

    def keypress(self, key):
        if key in [curses.KEY_UP, ord('k')]:
            self.key_up()
            return True

        elif key in [curses.KEY_DOWN, ord('j')]:
            self.key_down()
            return True

        elif key == curses.KEY_PPAGE:
            if self.current > self.offset:
                old_item = self.current
                self.current = self.offset
                self.write_row(old_item)
                self.write_row(self.current)
                self.refresh_list()
            elif self.offset > 0:
                if self.offset > self.line_count:
                    self.offset -= self.line_count
                    self.current -= self.line_count
                    self.draw_list()
                else:
                    self.current = self.offset = 0
                    self.draw_list()
            return True

        elif key == curses.KEY_NPAGE:
            bottomline = self.offset + self.line_count -1
            if self.current < bottomline:
                old_item = self.current
                self.current = bottomline
                self.write_row(old_item)
                self.write_row(self.current)
                self.refresh_list()
            elif (self.offset + self.line_count) < self.list_length:
                if (self.offset + (self.line_count * 2)) < self.list_length:
                    self.offset += self.line_count
                    self.current += self.line_count
                    self.draw_list()
                else:
                    self.offset = self.list_length - self.line_count
                    self.current = self.list_length - 1
                    self.draw_list()
            return True

        elif key == curses.KEY_HOME:
            self.current = self.offset = 0
            self.draw_list()
            return True

        elif key in [curses.KEY_END, ord('G')]:
            self.offset = self.list_length - self.line_count
            self.current = self.list_length - 1
            self.draw_list()
            return True

        elif key == curses.KEY_MOUSE:
            try:
                (_, x, y, _, bstate) = curses.getmouse()
                # write_status("{:08x}".format(bstate))
                if (bstate & (curses.BUTTON1_CLICKED|curses.BUTTON1_PRESSED)):
                    old_item = self.current
                    clickline = (y - self.dy) + self.offset
                    if (clickline <= self.offset + self.line_count):
                        self.current = clickline
                    else:
                        self.current = self.offset + self.line_count - 1
                    self.write_row(old_item)
                    self.write_row(self.current)
                    self.refresh_list()
                if (bstate & 0x00010000):           # scroll up
                    self.key_up()
                if (bstate & 0x00200000):           # scroll down
                    self.key_down()
                return True
            except curses.error as ce:
                # write_status("curses.error: "+str(ce)+str(curses.ERR))
                return False

        elif key == ord(' '):
            self.selected[self.current] = not self.selected[self.current]
            if self.current < (self.offset + self.line_count - 1):
                self.current += 1
                self.write_row(self.current - 1)
                self.write_row(self.current)
                self.refresh_list()
            elif (self.offset + self.line_count) < self.list_length:
                self.offset += 1
                self.current += 1
                self.draw_list()
            else:
                self.write_row(self.current)
                self.refresh_list()
            return False

        elif key in (ord('\n'), curses.KEY_ENTER):
            if True not in self.selected:
                self.selected[self.current] = True
            return False
        else:
            return False

    def key_up(self):
        if self.current > self.offset:
            self.current -= 1
            self.write_row(self.current + 1)
            self.write_row(self.current)
            self.refresh_list()
        elif self.offset > 0:
            self.offset -= 1
            self.current -= 1
            self.draw_list()

    def key_down(self):
        if self.current < (self.offset + self.line_count - 1):
            self.current += 1
            self.write_row(self.current - 1)
            self.write_row(self.current)
            self.refresh_list()
        elif (self.offset + self.line_count) < self.list_length:
            self.offset += 1
            self.current += 1
            self.draw_list()

class MultiColumnListWindow(SelectFromListWindow):
    """
    multicolumn curses list window
    'data' is a list of lists of strings:
      no error checking for list lengths,
      they must all be the same length as 'colwidths'
    'colwidths' is a list of integers:
      a '0' in colwidths means divide remaining columns
      among all with '0' value equally.
    """

    def __init__(self, window, data, border=True, colwidths=[0]):
        super().__init__(window, data, border)
        self.colwidths = colwidths
        self.numcols = len(self.colwidths)
        self.subwin = [None for n in range(self.numcols)]

    def draw_window(self):
        self.win.clear()
        (maxrows, maxcols) = self.win.getmaxyx()
        ddx = self.dx
        if self.drawborder:
            maxrows -= 2
            maxcols -= 2
            self.win.border()
        self.line_count = min(self.list_length, maxrows)
        self.width = maxcols
        widthsum = sum(self.colwidths)
        leftover = maxcols - widthsum - (self.numcols - 1)
        undefined_cols = [ (c == 0) for c in self.colwidths ]
        divisor = sum(undefined_cols)
        for c in range(self.numcols):
            if undefined_cols[c]:
                w = int(leftover / divisor)
                self.colwidths[c] = w
                leftover -= w
                divisor -= 1
        for i, cols in enumerate(self.colwidths):
            if self.subwin[i]:
                self.subwin[i].resize(maxrows, cols)
                self.subwin[i].mvwin(self.dy, ddx)
            else:
                # self.subwin[i] = curses.subwin(maxrows, self.colwidths[i], self.dy, ddx)
                self.subwin[i] = curses.newwin(maxrows, cols, self.dy, ddx)
            ddx += cols
            if ddx < maxcols:
                self.win.vline(1, ddx, curses.ACS_VLINE, maxrows)
                if self.drawborder:
                    self.win.addch(0, ddx, curses.ACS_TTEE)
                    self.win.addch(maxrows+1, ddx, curses.ACS_BTEE)
                ddx += 1
        self.win.noutrefresh()
        self.draw_list()

    def write_row(self, index):
        details = self.list[index]
        line = index - self.offset
        if line < 0 or line > (self.line_count - 1):
            return
        attr = (curses.color_pair(3)|curses.A_BOLD) if (index == self.current) else 0
        if self.selected[index]:
            attr |= color_pair(4)
        for i, det in enumerate(details):
            self.subwin[i].move(line, 0)
            self.subwin[i].clrtoeol()
            if len(det) > self.colwidths[i]:
                self.subwin[i].insnstr(det, self.colwidths[i], attr)
            elif len(det) > 1:
                self.subwin[i].insstr(det, attr)
            else:
                self.subwin[i].insch(det, attr)

    def draw_list(self):
        if self.list_length > 0:
            bottom = self.offset + self.line_count
            for sw in range(self.numcols):
                self.subwin[sw].clear()
            for idx in range(self.offset, bottom):
                self.write_row(idx)
        self.refresh_list()

    def refresh_list(self):
        for sw in range(self.numcols):
            self.subwin[sw].noutrefresh()
        curses.doupdate()
