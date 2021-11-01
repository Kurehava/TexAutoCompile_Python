#!/usr/bin/env python3
import os,platform,getpass,time,re,sys,subprocess
hispath=str(subprocess.Popen("echo ~",stdout=subprocess.PIPE,shell=True).communicate()).split(",")[0].split("'")[1].split("\\")[0]+"/.tachistory.his"
homepath=str(subprocess.Popen("echo ~",stdout=subprocess.PIPE,shell=True).communicate()).split(",")[0].split("'")[1].split("\\")[0]
err=0;navichk=1;abspath=relpath=osname=relname=""
osname=platform.system()
if osname == 'Windows':os.system("mode con：cols=400 lines=400");clearswich="cls"
elif osname == "Linux" or osname == "Darwin":os.system("printf '\033[8;20;78t'");clearswich="clear";os.system("while sleep 1;do tput sc;tput cup 0 $(($(tput cols)-40));date;tput rc;done&")
sciuser=getpass.getuser()
scipath=os.path.dirname(os.path.abspath(__file__))+"/"
#relname=os.path.splitext(os.path.basename(__file__))[0]
rope="------------------------------------------"
banner=(
    "\033[41;30mTAC-Python Ver 0.9.2 powered by oriki                                 \033[0;96m\n\033[33m"
    "=============================================================================\n"
    "  _____             _         _         ____                      _ _        \n"
    " |_   _|____  __   / \  _   _| |_ ___  / ___|___  _ __ ___  _ __ (_) | ___   \n"
    "   | |/ _ \ \/ /  / _ \| | | | __/ _ \| |   / _ \| '_ ' _ \| '_ \| | |/ _ |  \n"
    "   | |  __/>  <  / ___ \ |_| | || (_) | |__| (_) | | | | | | |_) | | |  __/  \n"
    "   |_|\___/_/\_\/_/   \_\__,_|\__\___/ \____\___/|_| |_| |_| .__/|_|_|\___|  \n"
    "                                                           |_|               \n"
    "============================================================================="
"\033[96m")
scibanner=("Script User : %s \nScript Path : %s \n%s" % (sciuser,scipath,rope))
maintip=("[E]exit\n[D]delete extras file\n[H]history\n%s" % rope)
def navigation(num):
    if num==1:autochkfile()
    elif num==2:mainmenu()
    elif num==3:compilechk()
    elif num==4:tachistory()
    elif num==5:compile()
    elif num==6:submenu()
    
def inputcheck(comment,banners,strings,argv='',args=''):
    global err
    while 1:
        os.system(clearswich);print(banners)
        if err==1:print("{\033[31m%s\033[96m} is Illegal input, Please reinput." % inputchk);err=0
        inputchk=input(comment)
        if argv!="":
            if str(re.search(argv,inputchk))!="None":
                print(re.search(argv,inputchk));err=1
            else:
                if int(inputchk)>args:err=1
                else:return inputchk
        else:
            if not inputchk in strings:err=1;continue
            else:return inputchk

def sciexit():
    if osname in {"Windows","Linux"}:os.system(clearswich);sys.exit(0)
    elif osname == "Darwin":os.system("osascript -e 'tell application \"Terminal\" to close first window' & exit")

def fnprocess(argv):
    global relpath;global relname;global abspath
    relpath=argv
    abspath=os.path.dirname(argv)+"/"
    relname=os.path.splitext(relpath)[0]
    if not os.path.exists(hispath):
        if osname=="Darwin":open(hispath,"w").close()
        elif osname in {"Linux","Windows"}:os.mknod(hispath)
    with open(hispath, "a") as sources:sources.write(argv)

def cleanner(argv):
    ext=["aux","dvi","log","nav","out","snm","toc","fls","fdb_latexmk","synctex.gz","vrb","bcf","blg","bbl","run.xml"]
    if argv == "know":
        for extit in ext:
            if os.path.exists(relname+"."+extit):os.remove(relname+"."+extit)
        os.system(clearswich)
    elif argv == "non":
        for listfn in os.listdir(scipath):
            if os.path.splitext(listfn)[1]=="."+ext:os.remove(scipath+listfn)
        os.system(clearswich)

def compile():
    global navichk
    os.system("cd '%s' && platex '%s'.tex" % (abspath,relname))
    os.system("cd '%s' && pbibtex '%s'.tex" % (abspath,relname))
    os.system("cd '%s' && platex '%s'.tex && platex '%s'.tex && dvipdfmx '%s'.dvi" % (abspath,relname,relname,relname))
    if osname == "Windows":os.system("start '%s'" % relname)
    elif osname == "Linux":os.system("evince '%s'.pdf 2>/dev/null &" % relname)
    elif osname == "Darwin":os.system("open '%s'.pdf" % relname)
    cleanner("know");navichk=6

def tachistory():
    failfilelist=[];alllist=(banner+"\n");count=1;global navichk
    if os.path.exists(hispath):
        with open(hispath, "r") as sources:lines = sources.readlines()
        for pathcheck in lines:
            if not os.path.exists(pathcheck):
                failfilelist.append(pathcheck)
                alllist=(alllist+"\033[31m"+str(count)+"."+pathcheck+"\033[96m")
                count+=1
                print("\033[31m"+str(count)+"."+pathcheck+"\033[96m")
            else:
                alllist=(alllist+str(count)+"."+pathcheck)
                count+=1
                print(str(count)+"."+pathcheck)
        if len(failfilelist)!=0:
            value=inputcheck("Detected invalid directories in the history, do you want to remove them?(Y/N)",banner,"YyNn")
            if value in "Yy":
                for name in failfilelist:
                    with open(hispath, "r") as sources:lines = sources.readlines()
                    with open(hispath, "w") as sources:
                        for line in lines:sources.write(re.sub(name, "", line))
                with open(hispath, "r") as sources:lines = sources.readlines()
                with open("/home/oriki/.tachistory.histmp","w+") as tmp:
                    for tmpline in lines:
                        if tmpline!="\n":tmp.write(tmpline)
                os.remove(hispath);os.rename(homepath+".tachistory.histmp",hispath);failfilelist.clear()
        value=inputcheck(rope+"\nInput list number to compile, or input 0 to menu.>>",alllist,"",r"\D",count-1)
        if value=="0":navichk=2
        elif lines[int(value)] in failfilelist:
            valuec=inputcheck("The directory you selected does not exist, do you want to remove it?(Y/N)",banner,"YyNn")
            if valuec in "Yy":
                with open(hispath, "r") as sources:linesq = sources.readlines()
                with open(hispath, "w") as sources:
                        for line in linesq:sources.write(re.sub(lines[int(value)], "", line))
            else:navichk=4
        else:fnprocess(lines[int(value)]);navichk=3
    else:os.system(clearswich);print(banner+"\n"+scibanner);print("No history is detected, return to the main menu after 3 seconds.");time.sleep(3);navichk=2

def autochkfile():
    nowtime=time.time();fakerelpath=[];os.system(clearswich);print(banner+"\n"+scibanner);global navichk;global relpath;global err
    if osname=="Windows":chkpath="c:\\users\\"
    elif osname in {"Linux","Darwin"}:chkpath=str(subprocess.Popen("echo ~",stdout=subprocess.PIPE,shell=True).communicate()).split(",")[0].split("'")[1].split("\\")[0]
    for path,dir_list,file_list in os.walk(chkpath):  
        for dir_name in file_list:
            relpath=os.path.join(path, dir_name)
            if os.path.splitext(dir_name)[1]==".tex" and os.path.exists(relpath) and nowtime - os.path.getmtime(relpath) < 120:
                fakerelpath.append(relpath)
    
    if len(fakerelpath)>0:
        inputbaner=(banner+"\n"+scibanner+"\n")
        for cunter in range(len(fakerelpath)):inputbaner=(inputbaner+str(cunter+1)+"."+fakerelpath[cunter])
        strin=inputcheck(rope+"\n"+"If you want to compile list file input the file number or input '0' to mainmenu.>>",inputbaner,"",r"\D",len(fakerelpath))
        if strin=="0":navichk=2
        elif strin=="":fnprocess(fakerelpath[1]);navichk=3
        else:fnprocess(fakerelpath[int(strin)-1]);navichk=3
    else:
        navichk=2

def mainmenu():
    while 1:
        os.system(clearswich);print(banner+"\n"+scibanner);global navichk;global err
        print(maintip)
        if err==1:print("{\033[31m%s\033[96m} is not a .Tex file or can't found." % inputpath);err=0
        inputpath=input("Put your Tex file or Input your Tex file path in this windows.(E/D/H/Path)\n>>").rstrip()
        if inputpath.count("'")>=2:inputpath=inputpath.split("'")[1]
        if inputpath in {"E","e","Ｅ","ｅ"}:sciexit()
        elif inputpath in {"D","d","Ｄ","ｄ"}:cleanner("non")
        elif inputpath in {"H","h","ｈ","Ｈ"}:navichk=4;break
        elif not os.path.exists(inputpath):err=1;continue
        elif os.path.splitext(inputpath)[1]==".tex" and os.path.exists(inputpath):fnprocess(inputpath);navichk=3;break

def compilechk():
    while 1:
        os.system(clearswich);print(banner+"\n"+scibanner);global navichk;global err
        print("Filename : %s\nPathname : %s/\n%s" % (os.path.basename(relpath),os.path.dirname(relpath),rope))
        if err==1:print("{\033[31m%s\033[96m} is Illegal input. Please reinput.>> " % inputselect);err=0
        inputselect=input("Do you want compile this file or Delete extras files? [Y/N/D]: ")
        if inputselect in {"Y","y","Ｙ","ｙ",""}:navichk=5;break
        elif inputselect in {"D","d","Ｄ","ｄ"}:cleanner("know")
        elif inputselect in {"N","n","Ｎ","ｎ"}:navichk=2;break
        else :err=1

def submenu():
    while 1:
        os.system(clearswich);print(banner+"\n"+scibanner);global navichk;global err
        print("Filename : %s\nPathname : %s/\n%s" % (os.path.basename(relpath),os.path.dirname(relpath),rope))
        if err==1:print("{\033[31m%s\033[96m} is Illegal input. Please reinput.>> " % inputselect);err=0
        inputselect=input("Do you want Recompile or Exit? [R/E/D/B]: ")
        if inputselect in {"R","r","Ｒ","ｒ",""}:navichk=5;break
        elif inputselect in {"E","e","Ｅ","ｅ"}:sciexit()
        elif inputselect in {"D","d","Ｄ","ｄ"}:cleanner("know")
        elif inputselect in {"B","b","Ｂ","ｂ"}:navichk=1;break
        else :err=1

if __name__=='__main__':
    while 1:
        navigation(navichk)