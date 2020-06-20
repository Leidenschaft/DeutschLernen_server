from datetime import *
import time
from bs4 import BeautifulSoup
import os
import codecs
import code
from DeutschLernen import settings
import re

def addWord(word,gender,chinese,isAdded=False):
    """
    add a new word to Wordlist_11.xml if isAdded is true,
    otherwise return the length of current category.
    """
    path = settings.STATICFILES_DIRS[0]
    f = codecs.open(os.path.join(path, "Wort", "wordlist.xml"), 'r', encoding='utf-8')
    xml=f.read()
    xml[len(xml)-len('</Wordlist>'):len(xml)]
    f.close()
    soup=BeautifulSoup(xml,"lxml")
    currentNounLen=len(soup.find_all("word",gender=re.compile(".*")))
    if(isAdded):
        append_str='<Word address="'+str(currentNounLen+1)+'.xml" gender="'+gender+'" chinese="'+chinese+'">'+word+'</Word>'
        xml=xml[0:(len(xml)-11)]+append_str+'</Wordlist>'
        f = codecs.open(os.path.join(path, "Wort", "wordlist.xml"), 'w', encoding='utf-8')
        f.write(xml)
        f.close()
        return
    return currentNounLen

def geturl(word):
    path=settings.STATICFILES_DIRS[0]
    f=codecs.open(os.path.join(path, "Wordlist_11.xml"), 'r', encoding='utf-8')
    xml=f.read()
    soup=BeautifulSoup(xml, "lxml")
    node=soup.word
    if (node.string==word):
        find=True
    else:
        find=False
    while not(find):
        node=node.next_sibling
        if (node==None):
            break
        if (node.string==word):
            find=True
    if (find):    
        return (node.attrs['address'],0)
    f.close()
    return ("https://de.wikipedia.org/wiki/" + word, 1)

def savedit(entry):
    #t=datetime.now()
    #s=t.strftime("%Y%m%d%H%M%S")
    wordform=entry[0]
    genus=entry[1]
    plural=entry[2]
    genitiv=entry[3]
    unittype=entry[4]
    anteil=entry[5]
    username=entry[6]
    explist=entry[7]
    symlist=entry[8]
    anmlist=entry[9]
    comlist=entry[10]
    drvlist=entry[11]
    collist=entry[12]
    wordAddr=entry[13]
    is_created=entry[14]
    if(is_created and explist and explist[0]):
        addWord(wordform,genus,explist[0][0],True)
    #filename=wordform+"_"+username+"_"+s+".xml"
    #indexfile=codecs.open(path+"edit_record.txt",'a','utf-8')
    #indexfile.write(filename+",")
    #indexfile.close()
    s='''<Entry category="Substantiv">\n'''
    s=s+'''<Stichwort>'''+wordform+'''</Stichwort>\n'''
    s=s+'''<Einheit>'''+unittype+'''</Einheit>\n'''
    s=s+'''<Anteil>'''+anteil+'''</Anteil>\n'''
    s=s+'''<Genus>'''+genus+'''</Genus>\n'''
    s=s+'''<Pluralform>'''+plural+'''</Pluralform>\n'''
    s=s+'''<GenitivSingular>'''+genitiv+'''</GenitivSingular>\n'''
    s=s+'''<zusammengesetzteWörter>\n'''
    s=s+'''<KompositaCollection>\n'''
    for com in comlist:
        if (com[1]==""):
            s=s+'''<K_>'''+com[0]+'''</K_>\n'''
        else:
            s=s+'''<K_ link="'''+geturl(com[1])[0]+'''">'''+com[0]+'''</K_>\n'''
    s=s+'''</KompositaCollection>\n'''
    s=s+'''<abgeleiteteWörter>\n'''
    for drv in drvlist:
        if (drv[2]==""):
            s=s+'''<hierzu category="'''+drv[1]+'''">'''+drv[0]+'''</hierzu>\n'''
        else:
            s=s+'''<hierzu category="'''+drv[1]+'''" link="'''+geturl(drv[2])[0]+'''">'''+drv[0]+'''</hierzu>\n'''
    s=s+'''</abgeleiteteWörter>\n'''
    s=s+'''</zusammengesetzteWörter>\n'''
    s=s+'''<Synonymegruppe>\n'''
    for sym in symlist:
        if (sym[1]==""):
            s=s+'''<Sym>'''+sym[0]+'''</Sym>\n'''
        else:
            s=s+'''<Sym link="'''+geturl(sym[1])[0]+'''">'''+sym[0]+'''</Sym>\n'''
    s=s+'''</Synonymegruppe>\n'''
    s=s+'''<Antonymegruppe>\n'''
    for anm in anmlist:
        if (anm[1]==""):
            s=s+'''<Anm>'''+anm[0]+'''</Anm>\n'''
        else:
            s=s+'''<Anm link="'''+geturl(anm[1])[0]+'''">'''+anm[0]+'''</Anm>\n'''
    s=s+'''</Antonymegruppe>\n'''
    s=s+'''<Kollokationen>\n'''
    for col in collist:
        s=s+'''<K>'''+col+'''</K>\n'''
    s=s+'''</Kollokationen>\n'''
    s=s+'''<AllgemeineErläuterungen>\n'''
    for exptuple in explist:
        s=s+'''<Eintrag>\n'''
        s=s+'''<Chinesisch>'''+exptuple[0]+'''</Chinesisch>\n'''
        s=s+'''<BeispielSammlung>\n'''
        for samptuple in exptuple[1]:
            s=s+'''<Beispiel>\n'''
            s=s+'''<Satz>'''+samptuple[0]+'''</Satz>\n'''
            s=s+'''<Übersetzung>'''+samptuple[1]+'''</Übersetzung>\n'''
            s=s+'''</Beispiel>\n'''
        s=s+'''</BeispielSammlung>\n'''
        s=s+'''</Eintrag>\n'''
    s=s+'''</AllgemeineErläuterungen>\n'''

    s=s+'''</Entry>\n'''
    path = settings.STATICFILES_DIRS[0]   #possible some entry is not parsed!
    f = open(path + wordAddr, 'wb')
    #if is Substantiv
    s_pre = '<?xml version="1.0" encoding="utf-8" standalone="no"?>'
    s_pre += '<!DOCTYPE Entry SYSTEM "NounModel.dtd">'
    s_pre += '<?xml-stylesheet type="text/xsl" href="NounRenderTemplate.xslt"?>'
    s = s_pre + s
    f.write(s.encode('utf-8'))
    f.close()
    return s

def parsegen(rq):
    err = 0
    wordform = rq.get('Stichwort',  '$0')
    genus = rq.get('Genus', '$1')
    plural = rq.get('Pluralform', '$2')
    genitiv= rq.get('GenitivSingular', '$3')
    unittype=rq.get('unittype', '$4')
    anteil=rq.get('Anteil', '$5')
    username=rq.get('UserName', '$6')
    is_created=rq.get('isCreated')
    word_addr=rq.get('wordAddr', '$7')
    if wordform == '$0':
        err = 1
        err_str = 'empty wordform'
        reqsheet = []
        return (reqsheet, err, err_str)
    explanation_list = parseexp(rq)
    if len(explanation_list) == 0:
        err = 2
        err_str = 'empty explanation'
        reqsheet = []
        return (reqsheet, err, err_str)
    reqsheet = [wordform,genus,plural,genitiv,unittype,anteil,username,explanation_list,parsesym(rq),parseanm(rq),parsecom(rq),parsedrv(rq),parsecol(rq),word_addr,is_created]
    return (reqsheet, err, '')

def parseexp(rq):
    explist=list([])
    expcount=0
    expcur=rq.get('explanation_'+str(expcount+1),'$exp')
    while not expcur=='$exp':
        expcount=expcount+1
        samplist=list([])
        sampcount=0
        oricur=rq.get('original_'+str(expcount)+'_'+str(sampcount+1),'$samp')
        while not oricur=='$samp':
            sampcount=sampcount+1
            transcur=rq.get('translation_'+str(expcount)+'_'+str(sampcount),'$samp')
            samptuple=[oricur,transcur]
            if(samptuple[0]):
                if not (samptuple[0][0]=="请"):
                    samplist.append(samptuple)
                oricur=rq.get('original_'+str(expcount)+'_'+str(sampcount+1),'$samp')
            else:
                break
        exptuple=[expcur,samplist]
        if(exptuple[0]):
            if not (exptuple[0][0]=="请"):
                explist.append(exptuple)
            expcur=rq.get('explanation_'+str(expcount+1),'$exp')
        else:
            break
    return explist

def parsesym(rq):
    symlist=list([])
    symcount=0
    symcur=rq.get('Sym_'+str(symcount+1),'$sym')
    while not symcur=='$sym':
        symcount=symcount+1
        symlink=rq.get('Sym_Link_'+str(symcount),'$sym')
        symtuple=[symcur,symlink]
        symlist.append(symtuple)
        symcur=rq.get('Sym_'+str(symcount+1),'$sym')
    if len(symlist)==0:
        return symlist
    if (symlist[len(symlist)-1][0][0]=="请"):
        symlist.pop()
    return symlist

def parseanm(rq):
    anmlist=list([])
    anmcount=0
    anmcur=rq.get('Anm_'+str(anmcount+1),'$anm')
    while not anmcur=='$anm':
        anmcount=anmcount+1
        anmlink=rq.get('Anm_Link_'+str(anmcount),'$anm')
        anmtuple=[anmcur,anmlink]
        anmlist.append(anmtuple)
        anmcur=rq.get('Anm_'+str(anmcount+1),'$anm')
    if len(anmlist)==0:
        return anmlist
    if (anmlist[len(anmlist)-1][0][0]=="请"):
        anmlist.pop()
    return anmlist

def parsecom(rq):
    comlist=list([])
    comcount=0
    comcur=rq.get('compound_'+str(comcount+1),'$com')
    while not comcur=='$com':
        comcount=comcount+1
        comlink=rq.get('compound_Link_'+str(comcount),'$com')
        comtuple=[comcur,comlink]
        comlist.append(comtuple)
        comcur=rq.get('compound_'+str(comcount+1),'$com')
    if len(comlist)==0:
        return comlist
    if (comlist[len(comlist)-1][0][0]=="请"):
        comlist.pop()
    return comlist

def parsedrv(rq):
    drvlist=list([])
    drvcount=0
    drvcur=rq.get('derivative_'+str(drvcount+1),'$drv')
    while not drvcur=='$drv':
        drvcount=drvcount+1
        temp=rq.get('derivative_category_'+str(drvcount),'$drv')
        if temp=="名词":
            drvc="Substantiv"
        if temp=="动词":
            drvc="Verben"
        if temp=="形容词":
            drvc="Adjektiv"
        drvlink=rq.get('derivative_Link_'+str(drvcount),'$drv')
        drvtuple=[drvcur,drvc,drvlink]
        drvlist.append(drvtuple)
        drvcur=rq.get('derivative_'+str(drvcount+1),'$drv')
    if len(drvlist)==0:
        return drvlist
    if (drvlist[len(drvlist)-1][0][0]=="请"):
        drvlist.pop()
    return drvlist

def parsecol(rq):
    collist=list([])
    colcount=0
    colcur=rq.get('collocation_'+str(colcount+1),'$col')
    while not colcur=='$col':
        colcount=colcount+1
        collist.append(colcur)
        colcur=rq.get('collocation_'+str(colcount+1),'$col')
    if len(collist)==0:
        return collist
    if (collist[len(collist)-1][0]=="请"):
        collist.pop()
    return collist
