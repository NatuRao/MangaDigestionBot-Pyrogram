from sys import platform
from PIL import Image
import requests
from fpdf import FPDF
from io import BytesIO
from pathlib import Path
import os
import gc
from Pagination.pagination import pagination as pagi


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Referer': 'https://mangakakalot.com'
}

# Setting pdf name
def manga_chapter_pdf(nameid, chapter_num, list_of_links, manganame):

    list_of_links.insert(0, 'https://i.postimg.cc/wvmvthSz/Intro.png')
    
    # with open('mangakakalot_value.csv', newline='') as f:
    #     reader = csv.reader(f)
    #     data = list(reader)

    # nameid = pagi.mangaid
    # print(nameid)
    # print(f"NAME ID: {nameid}")
    # for i in data:
    #     print(f"I: {i}")
    #     if i[0] == nameid:
    #         manganame = i[1]
    #         break

    if '-' in chapter_num:
        chapter_num = chapter_num.split('-')[-1]
    elif '_' in chapter_num:
        chapter_num = chapter_num.split('_')[-1]

    manganame = f"{manganame} - Chapter {chapter_num} - @MangaDigestion"
    print(manganame)
    manganame = manganame.split('\n')
    manganame = ''.join(manganame)
    pages_pdf_conversion(manganame, list_of_links)
    return manganame

# detecting webp image
def pil_image(path: Path) -> BytesIO:
  img = Image.open(requests.get(path, headers=headers, stream=True).raw).convert('RGB')
  try:
    membuf = BytesIO()
    suffix = path.split('.')[-1]
    suffix = "." + suffix
    print(suffix)
    if suffix == '.webp' or suffix == '.jpg' or suffix == '.png':
      img.save(membuf, format='jpeg')
    else:
      img.save(membuf)
  finally:
    img.close()
  del img
  del suffix
  gc.collect()
  return membuf

# Converting with fpdf
def pages_pdf_conversion(manganame, list_of_links):
    try:
        os.mkdir(f"pdf_files/")
        print("pdf_files making...")
    except:
        print("PDF Directory already exists!")
    print(list_of_links)
    pdf = FPDF('P', 'pt')
    for link in list_of_links:
        print(link)
        file = Image.open(requests.get(link, headers=headers, stream=True).raw).convert('RGB')
        width, height = file.size
        print(width, height)
        pdf.add_page(format=(width, height))
        img_bytes = pil_image(link)
        pdf.image(img_bytes, 0, 0, width, height)
        img_bytes.close()

        del img_bytes
        del width
        del height
        del link
        del file
        gc.collect()
    del list_of_links
    gc.collect()

    pdf.output(f'pdf_files/{manganame}.pdf', "F")
    pdf.close()

# Converting list of pages to pdf
def old_pages_pdf_conversion(manganame, list_of_links):

    try:
        os.mkdir(f"pdf_files/")
        print("pdf_files making...")
    except:
        print("PDF Directory already exists!")

    pdf_output_path_and_name = f'pdf_files/{manganame}.pdf'

    img_obj_list = []
    print(list_of_links)
    for link in list_of_links:
        print(link)
        img_obj_list.append(Image.open(requests.get(link, headers=headers, stream=True).raw))
    intro_image_obj = Image.open(f"intro_img/Intro.png")
    img_obj_list.insert(0, intro_image_obj)
    img_obj_list_2 = []

    # Converting the pages to rgb to avoid errors
    for x in img_obj_list:
        x1 = x.convert('RGB')
        img_obj_list_2.append(x1)

    # Main Logic of converting images to pdfs
    # first_key = list(Img_Obj_dict.values())[0]
    print(f"Object: {img_obj_list_2[0]}")
    img_obj_list_2[0].save(pdf_output_path_and_name, "PDF", resolution=100.0, save_all=True,
                    append_images=img_obj_list_2[1:])
    print(f"Conversion completed!")
    print()
    del img_obj_list
    del img_obj_list_2
    del x
    del list_of_links
    del x1
    gc.collect()
    print("Garbage Cleared")
    return