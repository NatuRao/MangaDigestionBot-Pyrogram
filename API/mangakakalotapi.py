from wsgiref.simple_server import demo_app
import requests
import re
from bs4 import BeautifulSoup

class mangakakalotapi:

    # returns list of tuples cotaining name of manga and its id [(name1, id1), (name2, id2)]
    def get_search_results(query):
        try:
            query = re.sub(r"[' ]", "_", query)
            url = f"https://mangakakalot.com/search/story/{query}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            mangas = soup.find_all('h3', {'class':'story_name'})
            res_search_list = []
            for manga in mangas:
                manganame = manga.text
                tempmanganame = manganame.split("\n")
                manganame = [i for i in tempmanganame if i != ""]
                link = manga.find_all("a", href=True)[0]['href']
                mangaid = link.split("/")[-1]
                result = (manganame[0], mangaid)
                res_search_list.append(result)
            if res_search_list == []:
                return "Nothing Found!"
            return res_search_list
        except requests.exceptions.ConnectionError:
            return "Check the host's network connection"


    # returns list of [Name of manga, Display-image link, list of genres, latest chapter number]
    def get_manga_details(mangaid):

        if mangaid.startswith("read-"):
            url = f"https://mangakakalot.com/{mangaid}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            # Getting image link
            div = soup.find_all('div', {'class':'manga-info-pic'})[0]
            imagelink = div.find_all('img')[0]['src']
            # Getting details
            detailslist = []
            ul = soup.find_all('ul', {'class':'manga-info-text'})[0]
            li = ul.find_all('li')
            for i in li:
                detailslist.append(i.text)
            # Manganame
            temp = detailslist[0].split("\n")
            temp.remove('')
            manganame = temp[0]
            mangaalter = temp[1][14:]
            mangaauthor = detailslist[1].split("\n")[-1]
            mangastatus = detailslist[2].split(" ")[-1]
            mangagenre = detailslist[6].split("\n")[-1]

        elif mangaid.startswith("manga-"):
            url = f"https://readmanganato.com/{mangaid}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            # Getting image link
            span = soup.find_all('span', {'class':'info-image'})[0]
            imagelink = span.find_all('img')[0]['src']
            # Getting details
            detailslist = []
            manganame = soup.find('div', {'class':'story-info-right'}).h1.text
            table = soup.find('table', {'class':'variations-tableInfo'})
            for row in table.find_all('tr'):
                cells = row.find_all('td', 'table-value')
                for values in cells:
                    splitstr = values.text.split("\n")
                    for i in splitstr:
                        if i != "":
                            detailslist.append(i)
            # print(detailslist)
            if len(detailslist) == 4:
                mangaalter = detailslist[0]
                mangaauthor = detailslist[1]
                mangastatus = detailslist[2]
                mangagenre = detailslist[3]
            
            elif len(detailslist) == 3:
                mangaalter = "N/A"
                mangaauthor = detailslist[0]
                mangastatus = detailslist[1]
                mangagenre = detailslist[2]
        else:
            url = f"https://mangakakalot.com/manga/{mangaid}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            # Getting image link
            div = soup.find_all('div', {'class':'manga-info-pic'})[0]
            imagelink = div.find_all('img')[0]['src']
            # Getting details
            detailslist = []
            ul = soup.find_all('ul', {'class':'manga-info-text'})[0]
            li = ul.find_all('li')
            for i in li:
                detailslist.append(i.text)
            # Manganame
            temp = detailslist[0].split("\n")
            temp.remove('')
            manganame = temp[0]
            mangaalter = temp[1][14:]
            mangaauthor = detailslist[1].split("\n")[-1]
            mangastatus = detailslist[2].split(" ")[-1]
            mangagenre = detailslist[6].split("\n")[-1]
        return [imagelink, manganame, mangaalter, mangaauthor, mangastatus, mangagenre]

    # return list of chapter links of entered manga [chapterlink1, chapterlink2, full manga chapter links]
    def get_all_manga_chapter(mangaid):
        
        try:
            if mangaid.startswith('read-'):
                print(mangaid)
                chapterlinks = []
                chapternames = []
                url = f"https://mangakakalot.com/{mangaid}"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                div = soup.find_all('div', {'class':'chapter-list'})
                row_div = div[0].find_all('div', {'class':'row'})
                for row in row_div:
                    span = row.find('span')
                    for i in span:
                        chapterlinks.append(i['href'])
                        chapternames.append(i.text)

                chapterlinks.reverse()
                chapternames.reverse()
                return chapternames, chapterlinks
            
            elif mangaid.startswith('manga-'):
                print(mangaid)
                url = f"https://readmanganato.com/{mangaid}"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                a = soup.find_all('a', {'class':'chapter-name text-nowrap'})
                chapterlinks = [i['href'] for i in a]
                chapternames = [i.text for i in a]
                
                chapterlinks.reverse()
                chapternames.reverse()
                return chapternames, chapterlinks

            else:
                print(mangaid)
                chapterlinks = []
                chapternames = []
                url = f"https://mangakakalot.com/manga/{mangaid}"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                div = soup.find_all('div', {'class':'chapter-list'})
                row_div = div[0].find_all('div', {'class':'row'})
                for row in row_div:
                    span = row.find('span')
                    for i in span:
                        chapterlinks.append(i['href'])
                        chapternames.append(i.text)
                
                chapterlinks.reverse()
                chapternames.reverse()
                return chapternames, chapterlinks
        except AttributeError:
            return "Invalid Mangaid or chapter number"
        except requests.exceptions.ConnectionError:
            return "Check the host's network Connection"

    # returns list of image links of pages of full chapter [imglink1, imglink2, full chapter]
    def get_chapter_pages(chapterid, chapternum):
        a = ''
        try:
            if chapterid.startswith('read-'):
                url = f"https://mangakakalot.com/chapter/{chapterid}/{chapternum}"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                div = soup.find_all('div', {'class':'container-chapter-reader'})
                image = div[0].find_all('img')
                pagelinks = [i['src'] for i in image]
                return pagelinks

            elif chapterid.startswith('manga-'):
                url = f"https://readmanganato.com/{chapterid}/{chapternum}"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                div = soup.find_all('div', {'class':'container-chapter-reader'})
                image = div[0].find_all('img')
                pagelinks = [i['src'] for i in image]
                return pagelinks

            else:
                url = f"https://mangakakalot.com/chapter/{chapterid}/{chapternum}"
                print(url)
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                div = soup.find_all('div', {'class':'container-chapter-reader'})
                image = div[0].find_all('img')
                pagelinks = [i['src'] for i in image]
                return pagelinks
        except AttributeError:
            return "Invalid Mangaid or chapter number"
        except requests.exceptions.ConnectionError:
            return "Check the host's network Connection"