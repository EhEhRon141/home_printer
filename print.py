import subprocess as sp
import datetime as dt
import random
import requests
import json
import os
import tempfile
import cups
#import win32api
#import win32print

def calc_year(who,today):
    if(
        today.month == who.month
        and today.day >= who.day
        or today.month > who.month
    ):
        nextBirthdayYear = today.year + 1
    else:
        nextBirthdayYear = today.year

    nextBirthday = dt.date(
        nextBirthdayYear,who.month,who.day
    )
    return nextBirthday

def get_quote():
    file = open('quotes.txt')
    quotes = file.read()
    number = 360
    count = 0
    start = 0
    end = 0
    howmany = 0
    todaysQuote = random.randint(1,number)
    for i in quotes:
        if(i == "-" and c == "-"):
            howmany += 1
        c = i
        count +=1
        if(howmany == todaysQuote - 1 and start == 0 and i == '\n'):
            start = count
        elif(howmany == todaysQuote and end == 0 and i == '\n'):
            end = count

    count = 0
    str = ''
    for i in quotes:
        count += 1
        if(count > start and count < end):
            str += i

    file.close()
    return str

def get_pokemon():
    url = 'https://pokeapi.co/api/v2/pokemon/'
    dex = random.randint(1,802)
    url = url + str(dex) + '/'
    json_data = requests.get(url).json()
    return json_data

def poke_info(json_data):
    data = ''
    url1 = ''
    url2 = ''

    url1 += json_data['sprites']['front_default']
    try:
        url2 += json_data['sprites']['back_default']

    except:
        print('No FIle Found!\n')

    for i in json_data['forms']:
        data += 'Name: ' + i['name'].capitalize()
    t = str(json_data['id'])
    data += '\nDex Number: ' + t

    newpath = r'sprites/' + t
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    picName = t + 'f.png'
    f = open('sprites/' + t +'/' + picName,'wb')
    f.write(requests.get(url1).content)
    f.close()

    try:
        picName = t + 'b.png'
        f = open('sprites/' + t +'/' + picName,'wb')
        f.write(requests.get(url2).content)
        f.close()
    except:
        print('\nNope\n')


    #sp.call(['notepad','/p', 'sprites/' + t +'/' + picName])
    return data

today = dt.date.today()

christmas = dt.date(dt.date.today().year ,12,25) - today
aaron = calc_year(dt.date(1997,6,12),today) - today
emily = calc_year(dt.date(1999,12,17),today) - today
dad = calc_year(dt.date(1963,6,2),today) - today
mom = calc_year(dt.date(1966,12,26),today) - today
tan = calc_year(dt.date(2000,8,6),today) - today
cam = calc_year(dt.date(2002,5,19),today) - today

#Inspirational Quote
quote = get_quote()

#Pokemon and Info
pokemon = get_pokemon()
pokeStats = poke_info(pokemon)
#Prints all of the things
f = open('today.txt','w+')

f.write("Christmas is %s days away!\n" %christmas.days)
f.write("Emily's Birthday is %s days away!\n" %emily.days)
f.write("Aaron's Birthday is %s days away!\n" %aaron.days)
f.write("Tanners's Birthday is %s days away!\n" %tan.days)
f.write("Cameron's Birthday is %s days away!\n" %cam.days)
f.write("Mom's Birthday is %s days away!\n" %mom.days)
f.write("Dad's Birthday is %s days away!\n\n" %dad.days)
f.write("Inspirational Quote of the day:\n%s\n\n" %quote)
f.write("Pokemon of the day is:\n%s\n\n" %pokeStats)


f.close()

conn = cups.Connection()
printers = conn.getPrinters()
for printer in printers:
    print printer, printers[printer]["device-uri"]

printer_name=printers.keys()[0]
printFile(printer_name,'today.txt',"Daily Print",{}) 

#sp.call(['notepad','/p', 'today'])
