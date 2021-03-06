#!/usr/bin/env python3

###########################
#                         #
# Created by @Alireza6677 #
#                         #
###########################

import os , sys , subprocess, platform , html , zipfile
try:
    import bs4
    import requests
    import urllib
except:
    print("You need beautifulsoup4 & urllib & requests to run this script")
    print("Install them using 'pip install beautifulsoup4 urllib requests'")
    exit(1)

#from random import randint

def usage():
    print("SubtitleGet.py version 1.1 by @Alireza6677 (Using sub.salamdl.biz).")
    print("Usage : ./SubtitleGet.py 'Movie/Serial Name'\n")
    exit(1)

def getPageContent(url):
    page = ""
    try:
        page = requests.get(url) #, proxies={"http" : "http://127.0.0.1:8787"})
        #page.close()
        return page.content
    except:
        print("Connection error !\nCheck your internet connection and try again.")
        exit(1)

def downloadFile(url, path):
    resp = ""
    try:
        resp = urllib.request.urlopen(url).read()
    except:
        print("Error downloading the file.\nCheck your internet connection and try agian")
        exit(1)
    try:
        output =  open(path , "wb")
        output.write(resp)
        output.close()
    except:
        print("Error saving the file.\nCheck your disk space or this path:\n"+path)
        exit(1)

def main():
    movie = ""
    if len(sys.argv) > 1:
        i = 1
        while i < len(sys.argv):
            movie += " " + sys.argv[i]
            i += 1
    else:
        usage()

    page = getPageContent("http://sub.salamdl.biz/subtitles/title?q=" + movie)
    bs = bs4.BeautifulSoup(page , "html.parser")

    items = bs.find_all("div" , {"class" : "title"})
    names = []
    links = []

    for item in items:
        names.append(item.a.decode_contents(formatter="html"))
        links.append(item.a['href'])

    if len(names) == 0:
        print("Error : Movie not found !")
        exit(1)

    i = len(names) - 1
    while i >= 0:
        #item = "[%d] " % i+1
        print(" ["+str(i+1)+"] " + names[i])
        i -= 1
    inp = input("\nChoose one of the movies above (1 - %d): " % len(names)).strip()

    try:
        inp = int(inp)
    except:
        print("Error : Wrong input")
        exit(1)

    if inp < 1 or inp > len(names):
        print("Error : Input out of range")
        exit(1)
    for i in range(3):
        print("\n")

    link = "http://sub.salamdl.biz/" + links[inp - 1] + "/farsi_persian"
    bs2 = bs4.BeautifulSoup(getPageContent(link)  , "html.parser")
    h = bs2.find_all("span" , {"class" : "positive-icon"})
    for i in h:
        i.decompose()

    h = bs2.find_all("span" , {"class" : "neutral-icon"})
    for i in h:
        i.decompose()

    subs = bs2.find_all("td" , {"class" : "a1"})
    subtitles = []
    sublinks = []
    for i in subs:
        subtitles.append(i.a.span.decode_contents(formatter="html").strip())
        sublinks.append(i.a['href'])

    if len(subtitles) < 1:
        print("No persian subtitles found :(")
        exit()

    i = len(subtitles) - 1
    while i >= 0:
        print(" ["+str(i+1)+"] " + subtitles[i])
        i -= 1

    inp2 = input("\nChoose one or some of subtitles above (1 - %d) {ex: 2 or 1,2,3 or All}: " % len(subtitles)).strip()

    choice_list = []
    num_list = []

    if inp2 == 'All' or inp2 == 'all':
        i = 0
        while i < len(subtitles):
            choice_list.append(str(i+1))
            i+=1
    else:
        choice_list = inp2.split(',')

    for item in choice_list:
        try:
            num = int(item)
            num_list.append(int(item))
        except:
            print("Error : Wrong input")
            exit(1)

        if num < 1 or num > len(subtitles):
            print("Error : Input out of range")
            exit(1)



    print("Downloading...")

    index = 0
    sep=os.sep

    save_path = os.path.expanduser("~")+sep+"Downloads"+sep+"SubtitleGet"+sep
    if not os.path.isdir(save_path):
        try:
            os.mkdir(save_path)
        except:
            print("Failed to create directory :\n"+save_path)
            exit(1)

    zips = []
    for num in num_list:
        link2 = "http://sub.salamdl.biz/"  + sublinks[num - 1]
        name2 = subtitles[num - 1]

        bs3 = bs4.BeautifulSoup(getPageContent(link2) , "html.parser")
        downloadLink = "http://sub.salamdl.biz" +  bs3.find("a" , {"id":"downloadButton"})['href']
        path = save_path + name2 + ".zip"
        zips.append(name2 + '.zip')
        downloadFile(downloadLink , path)
        index += 1
        print("Downloaded {0} of {1}:".format(index , len(num_list)))
        print(path)

    print("Extracting...")
    select_file=""
    for zip_file in zips:
        zipref = zipfile.ZipFile(save_path + zip_file , 'r')
        if len(zipref.namelist()) > 1:
            path = save_path + zip_file[:-4]
            os.mkdir(path)
            zipref.extractall(path)
            select_file=zip_file[:-4]+sep
        else:
            zipref.extractall(save_path)
            select_file=zipref.namelist()[0]

        zipref.close()
        os.remove(save_path + zip_file)

    print("\n\nAll Done.\nSaved to : "+ save_path)

    filemanager = ""
    select = ""

    syst=platform.system()
    if syst == 'Linux':
        filemanager="nautilus"
        select="-s"
    elif syst == "Windows":
        filemanager="explorer"
        select="/select,"
    elif syst == "Darwin":
        filemanager = "open"
        select = "-R"

    subprocess.Popen([filemanager , select , save_path + select_file])
    #+ html.unescape(subtitles[num_list[0]-1]) + ".zip"])

if __name__ == "__main__":
    main()
