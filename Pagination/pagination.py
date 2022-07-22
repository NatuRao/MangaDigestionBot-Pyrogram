from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class pagination:
    ch_linkname = []
    current_page = 1
    chapterid = ''
    mangaid = ''
    manganame = ''
    perrow = 10
    chapterlen = None

    def send_buttons(self):
        self.current_page = 1
        button = []
        button.append([InlineKeyboardButton('--Download All--', f'rkalotall:{self.mangaid}'), InlineKeyboardButton('--Download This Page--', f'rkalotpage:')])
        for name, link in self.ch_linkname[self.current_page - 1].items():
            link = link.split('/')
            self.chapterid = link[-2]
            button.append([InlineKeyboardButton(name, f'rkalot:{link[-1]}')])
        next_ = InlineKeyboardButton('>', 'next_')
        last_ = InlineKeyboardButton('>>', 'last_')
        if self.current_page == 1:
            button.append([next_, last_])

        return InlineKeyboardMarkup(button)

    def next_button(self):
        self.current_page += 1
        button = []
        button.append([InlineKeyboardButton('--Download This Page--', f'rkalotpage:{self.mangaid}')])
        for name, link in self.ch_linkname[self.current_page - 1].items():
            link = link.split('/')
            self.chapterid = link[-2]
            button.append([InlineKeyboardButton(name, f'rkalot:{link[-1]}')])
        prev_ = InlineKeyboardButton('<', 'prev_')
        next_ = InlineKeyboardButton('>', 'next_')
        first_ = InlineKeyboardButton('<<', 'first_')
        last_ = InlineKeyboardButton('>>', 'last_')
        if self.current_page == 1:
            button.append([next_, last_])
        elif self.current_page == len(self.ch_linkname):
            button.append([first_, prev_])
        elif self.current_page > 1:
            button.append([first_, prev_, next_, last_])

        return InlineKeyboardMarkup(button)

    def prev_button(self):
        self.current_page -= 1
        button = []
        button.append([InlineKeyboardButton('--Download This Page--', f'rkalotpage:{self.mangaid}')])
        for name, link in self.ch_linkname[self.current_page - 1].items():
            link = link.split('/')
            self.chapterid = link[-2]
            button.append([InlineKeyboardButton(name, f'rkalot:{link[-1]}')])
        prev_ = InlineKeyboardButton('<', 'prev_')
        next_ = InlineKeyboardButton('>', 'next_')
        first_ = InlineKeyboardButton('<<', 'first_')
        last_ = InlineKeyboardButton('>>', 'last_')
        if self.current_page == 1:
            button.pop(0)
            button.insert(0, [InlineKeyboardButton('--Download All--', f'rkalotall:{self.mangaid}'), InlineKeyboardButton('--Download This Page--', f'rkalotpage:')])
            button.append([next_, last_])
        elif self.current_page > 1:
            button.append([first_, prev_, next_, last_])

        return InlineKeyboardMarkup(button)

    def first_button(self):
        self.current_page = 1
        button = []
        button.append([InlineKeyboardButton('--Download All--', f'rkalotall:{self.mangaid}'), InlineKeyboardButton('--Download This Page--', f'rkalotpage:{self.mangaid}')])
        for name, link in self.ch_linkname[self.current_page - 1].items():
            link = link.split('/')
            self.chapterid = link[-2]
            button.append([InlineKeyboardButton(name, f'rkalot:{link[-1]}')])
        next_ = InlineKeyboardButton('>', 'next_')
        last_ = InlineKeyboardButton('>>', 'last_')
        if self.current_page == 1:
            button.append([next_, last_])

        return InlineKeyboardMarkup(button)

    def last_button(self):
        self.current_page = len(self.ch_linkname)
        button = []
        button.append([InlineKeyboardButton('--Download This Page--', f'rkalotpage:{self.mangaid}')])
        for name, link in self.ch_linkname[self.current_page - 1].items():
            link = link.split('/')
            self.chapterid = link[-2]
            button.append([InlineKeyboardButton(name, f'rkalot:{link[-1]}')])
        prev_ = InlineKeyboardButton('<', 'prev_')
        first_ = InlineKeyboardButton('<<', 'first_')
        if self.current_page == len(self.ch_linkname):
            button.append([first_, prev_])

        return InlineKeyboardMarkup(button)
