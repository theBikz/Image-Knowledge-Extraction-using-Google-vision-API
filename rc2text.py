import os, io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import datetime
import nltk
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk import ne_chunk
from openpyxl import Workbook
import openpyxl

for data in os.listdir("C:/Users/BIPIN/Documents/Python Venv/RC2Text/RC"):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =  r'RCtoText.json'
    client = vision.ImageAnnotatorClient()
    FILE_NAME = data
    FOLDER_PATH = r'C:\Users\BIPIN\Documents\Python Venv\RC2Text\RC'

    with io.open(os.path.join(FOLDER_PATH,FILE_NAME), 'rb') as image_file:
        content = image_file.read()

    image =  vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    df = pd.DataFrame(columns=['locale','description'])

    for text in texts:
        df = df.append(dict(locale=text.locale,description=text.description),ignore_index=True)

    details_list = df['description'].values.tolist()
    dt = details_list
    dt.remove(dt[0])


    date_format = '%d/%m/%Y'
    mfg_date_format = '%m/%Y'
    flag = 0
    flag2 = 0
    date_list = []
    date_obj = ""
    _string_ = "" 
    names = []
    count = 0
    cha_no = ''
    eng_no = ''
    reg_no = ''
    name = ''

    
    rem_list = []
    rem_list = ['REGN. NO','REG. DT','CH. NO','E NO','O SNO','MFG CD','COLOUR','CLASS','MUL','L.M.V.','NAME','SWID OF',
                'S/W/D OF','ADDRESS','HP/LEASE','MODEL','BODY','WHEEL BASE','MFG.DT.','FUEL','REG.UPTO','TAX UPTO',
               'Registering Authority','Registering','Authority','SALOON','NO. OF CYL','UNLADEN WT','SEATING C','SEATING',
               'STANDING','STANDING C','CU.CAP','Signature','GOVERNMENT','OF','HARYANA','CERTIFICATE','REGISTRATION','RULE',
           'NO.','Registration','No.','Name','Address','Regd','Owner','Previous','Chasis','Engine','Manufacture','Capacity',
           'Seating','including','(including',':']
    
    for block in rem_list:
        for word in dt:
            if block == word:
                dt.remove(word)

    extract_name = dt[0]
    dt.remove(dt[0])

    for i in dt:
        try:
            date_obj = datetime.datetime.strptime(i, date_format)
            newformat = date_obj.strftime('%Y-%m-%d')
            date_list.append(newformat)
        except ValueError:
            continue

    for i in dt:
        try:
            date_obj = datetime.datetime.strptime(i, mfg_date_format)
            newformat = date_obj.strftime('%Y-%m')
            date_list.append(newformat)
        except ValueError:
            continue

    date_list = sorted(date_list)

    for i in range(2):
        date_list.append('')

    extract_name = extract_name.replace('\n',' ')
    extract_name = extract_name.replace(':',' ')
    def Convert(string):
        li = list(string.split(" "))
        return li
    extract_list = Convert(extract_name)
    for i in extract_list:
        if(i==''):
            extract_list.remove(i)

    for i in extract_list:
        if(i == 'Name &Address' or i == '&Address' or i == '&ADDRESS' or i == 'L.M.V.' or i == 'NAME'):
            if flag ==0:
                flag = 1
                continue
        if(flag == 1):
            name = i
            flag = 2
    

    for i in dt:
        if(len(i)==17 and i.isalnum()):
            if i and i[0].isalpha() and i[len(i)-1].isdigit():
                cha_no = i
                print("Chassis Number: {}" .format(cha_no))
        if(len(i)==10 and i.isalnum()):
            if i and i[0].isalpha() and i[1].isalpha() and i[len(i)-1].isdigit():
                reg_no = i
                print("Regn Number: {}" .format(reg_no))
        if((len(i)==11 or len(i)==12)):
            if i and i[0].isalpha() and i[4]=='-' and i[len(i)-1].isdigit():
                reg_no = i
                print("Regn Number: {}" .format(reg_no))
        if(len(i)==12):
            if i and i[0].isalpha() and i[len(i)-1].isdigit():
                eng_no = i
                print("Engine Number: {}" .format(eng_no))

    print("Name: {}" .format(name))
    print("MFD: {}" .format(date_list[0]))
    print("Date of Regn: {}" .format(date_list[1]))

    workbook_obj = openpyxl.load_workbook("RC_details.xlsx")
    book = workbook_obj.active
    #sheet = book.active
    rows = ((reg_no,cha_no,eng_no,name,date_list[0],date_list[1]),)
    for row in rows:
        book.append(row)
    workbook_obj.save("C:/Users/BIPIN/Documents/Python Venv/RC2Text/RC_details.xlsx")