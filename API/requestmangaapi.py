import gspread
from datetime import date

# Configuring Google Spread Sheets Key
ss = gspread.service_account('gspreadkey/mangadigestionbot.json')
sh = ss.open('MangaRequests')
wks = sh.worksheet('Sheet1')

class requestmangaapi:

    # def next_available_row(wks):
    #     str_list = list(filter(None, wks.col_values(1)))
    #     return str(len(str_list)+1)
    
    # Adding fetched requests to Google Sheet
    def add_manganame(manga_name, name, username):
        manga_name_list = manga_name.split(",")
        for manga_name in manga_name_list:
            today = date.today()
            date1 = today.strftime("%B %d, %Y")
            str_list = list(filter(None, wks.col_values(1)))
            next_row = str(len(str_list)+1)
            wks.update(f'A{next_row}', manga_name)
            wks.update(f'B{next_row}', date1)
            wks.update(f'C{next_row}', name)
            wks.update(f'D{next_row}', username)
