
import datetime as dt
import random
import requests
import json
import os
import tempfile
import cups
#import subprocess as sp For windows print

#   Function: calc_year
#   Input: birthdate, todays date
#   Output: The correct year one's next birthday is

def calc_year(who,today):
    if(
        today.month == who.month
        and today.day >= who.day #determines whether their birthday was already past this month
        or today.month > who.month #determines if birthday month has already past
    ):
        nextBirthdayYear = today.year + 1 #if so, adds a year to their next birth date
    else:
        nextBirthdayYear = today.year #else, year stays the same

    nextBirthday = dt.date( #This is the next birthday for that person
        nextBirthdayYear,who.month,who.day
    )
    return nextBirthday

#   Function: get_quote
#   Input: None
#   Output: Reads text file, finds random quote from file and passes it back

def get_quote():
    file = open('/home/pi/Desktop/print/home_printer/quotes.txt') #file path
    quotes = file.read() #open file for reading
    number = 360 #number of quotes in file
    count = 0
    start = 0
    end = 0
    howmany = 0
    todaysQuote = random.randint(1,number) #gets randoml quote number
    for i in quotes: #finds the quote start and end
        if(i == "-" and c == "-"):
            howmany += 1
        c = i
        count +=1
        if(howmany == todaysQuote - 1 and start == 0 and i == '\n'): #determines start character of quote
            start = count
        elif(howmany == todaysQuote and end == 0 and i == '\n'): #determines end character of quote
            end = count

    count = 0
    str = ''

    #There's gotta be a better way of doing this...???
    for i in quotes: #records the characters into a string that are between the start and end of a quote
        count += 1
        if(count > start and count < end): #starts adding to string once at the point of start until the end
            str += i

    file.close() #proper closure of file
    return str #return quote

#   Function: get_pokemon
#   Input: None
#   Output: Picks a random pokemon (from pokeapi), gets the json file, returns it
def get_pokemon():
    url = 'https://pokeapi.co/api/v2/pokemon/'
    dex = random.randint(1,802) #802 pokemon on the api
    url = url + str(dex) + '/' #builds proper url
    json_data = requests.get(url).json() #gets json form url
    return json_data

#   Function: poke_info
#   Input: json_data
#   Output: gets name, dex numnber, and downloads sprites (if they exist)
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

    return data

today = dt.date.today() #today's date

#How many days until each birthday
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

#Prints all of the things to a text file
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

#closes the file properly
f.close()

#Uses CUPS to print this on the Raspberry Pi
conn = cups.Connection()
printers = conn.getPrinters()
printer_name=printers.keys()[0]

cups.setUser('pi')

#The actual printing is done below
conn.printFile(printer_name,'/home/pi/Desktop/print/home_printer/today.txt',"Daily Print",{})

#sp.call(['notepad','/p', 'today']) This is what I used on Windows
