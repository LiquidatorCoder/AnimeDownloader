import easygui as eg
import pandas
import openpyxl
import mechanize
from clint.textui import progress
import requests
import re
import os
import keyboard
import time
import sys
fnop=0
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True )
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
def login():
    try:
        resp0=br.open("https://otakustream.tv/user/login/")
        br.select_form(nr=1)
        br.form["log"] = 'strawberryabak@gmail.com'
        br.form["pwd"] = 'june302000'
        br.submit()
        print "Login Successful"
    except:
        print "Can't Login"
def fetchl():
    try:
        global no
        no=input("Enter the episode number from where you want to download till present : ")
        epl1=("https://otakustream.tv/anime/detective-conan/episode-"+str(no)+"/")
        return epl1
    except:
        print "Can't fetch links"
        return None
def getfnm(cd):
    if not cd:
        return "Anonymous"
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return "Anonymous"
    return fname[0]
def alreadydc():
    cwd=os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".mp4"):
            if file==nfilename:
                return "Exists"
            else:
                pass
def renamer():
    DCIndex=pandas.read_excel('DCIndex.xlsx')
    JPN=list(DCIndex['Jpn'].values)
    S=list(DCIndex['Season'].values)
    ET=list(DCIndex['Episode title'].values)
    try:
        name=int(filenamewoq[0:3])
        fnop=0
    except:
        fnop=1
    if fnop==0:
        for i in range(len(JPN)):
            if JPN[i]==name:
                name2=ET[i]
                sname=str(S[i])
                break
            else:
                name2=''
        name3=''
        for i in name2:
            if i==":":
                name3+="-"
            elif i in ["*","?","<",">","|",'"',"/"]:
                name3+=" "
            else:
                name3+=i
        global nfilename
        nfilename="Season "+sname+" Episode "+str(name)+" "+name3+".mp4"
def downloader(url):
    global filenamewq,filenamewoq
    try:
        r= requests.get(url,stream=True,allow_redirects=True,timeout=120)
    except:
        time.sleep(10)
        r= requests.get(url,stream=True,allow_redirects=True,timeout=120)
    filenamewq = getfnm(r.headers.get('content-disposition'))
    filenamewoq = filenamewq[1:len(filenamewq)-1:1]
    renamer()
    cv=alreadydc()
    if cv == "Exists":
        print "File already downloaded or a file with same name is present."
    else:
        print "Downloading\n",nfilename
        with open(nfilename, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            ddl=0
            start = time.clock()
            if total_length is None:
                f.write(r.content)
            else:
                try:
                    for chunk in progress.bar(r.iter_content(chunk_size=128), expected_size=(total_length/128) + 1):
                        try:
                            if keyboard.is_pressed('esc'):
                                f.close()
                                cwd=os.getcwd()
                                pc=0
                                for file in os.listdir(cwd):
                                    if file.endswith(".part") and nfilename in file:
                                        filesplit=file.split(".")
                                        for i in filesplit:
                                            if i=="part":
                                                pc+=1
                                            else:
                                                pass
                                ppc=".part"*(pc+1)
                                os.rename(nfilename,nfilename+ppc)                            
                                break
                            elif chunk:
                                ddl += len(chunk)
                                done = int(50 * ddl / total_length)
                                sys.stdout.write("\r[%s%s] %s bps" % ('=' * done, ' ' * (50-done), ddl//(time.clock() - start)))
                                print ''
                                f.flush()
                                f.write(chunk)
                                f.flush()
                        except:
                            f.close()
                            os.rename(nfilename,nfilename+".part")
                            break
                except:
                    f.close()
                    cwd=os.getcwd()
                    pc=0
                    for file in os.listdir(cwd):
                        if file.endswith(".part") and nfilename in file:
                            filesplit=file.split(".")
                            for i in filesplit:
                                if i=="part":
                                    pc+=1
                                else:
                                    pass
                    ppc=".part"*(pc+1)
                    os.rename(nfilename,nfilename+ppc)
                
def eplc():
    global gepl
    l=gepl.split("/")
    xx=l[5]
    yy=xx.split("-")
    z=yy[1]
    global p
    p=int(z)
    q=p+1
    gepl="https://otakustream.tv/anime/detective-conan/episode-"+str(q)
def epld():
    global gepl
    resp2=br.open(gepl)
    o=resp2.read()
    a=o.split('onclick="window.open(')
    b=a[1]
    c=b.split(",")
    d=c[0]
    e=d[1:len(d)-1]
    f="https://otakustream.tv"+e
    print "Downloading from --"+f
    return f
try:
    print "Welcome to Detective Conan Downloader."
    print "Opening OtakuStream.tv"
    login()
    gepl=fetchl()
    print "Starting Download"
    print time.asctime()
    while True:
        if gepl!=None:
            g=epld()
            resp3=br.open(g)
            content = resp3.get_data()
            content2=content.split("https://www.rapidvideo.com/")
            try:
                content3=content2[1]
            except IndexError:
                print "Link not found"
            else:
                content4=content3.split('"')
                content5=content4[0]
                linkf="https://www.rapidvideo.com/"+content5
                resp4=br.open(linkf)
                target_text2="Download"
                for link2 in br.links():
                    if target_text2 in link2.text:
                        dow=link2.url
                        break
                resp5=br.open(dow)
                for link3 in br.links():
                    if "480p" in link3.text:
                        dl=link3.url
                        break
                    else:
                        if "720p" in link3.text:
                            dl=link3.url
                            break
                        else:
                            if "1080p" in link3.text:
                                dl=link3.url
                                break
                            else:
                                if "360p" in link3.text:
                                    dl=link3.url
                                    break
                                else:
                                    dl=None
                if dl!=None:
                    if fnop==0:
                        downloader(dl)
                    else:
                        break
                    print time.asctime()
                    eplc()
                else:
                    eplc()
        else:
            eplc()
except:
    eg.exceptionbox("Error", "Error")
    print time.asctime()
    er=raw_input("An Error Occured")
