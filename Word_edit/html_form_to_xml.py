import os
import re

from bs4 import BeautifulSoup
from lxml import etree

from DeutschLernen import settings

xml_header = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n'
wordlist_header = '<?xml-stylesheet type="text/xsl" href="navigation.xslt"?>\n'

def format_xml(xml_str):
    root = etree.fromstring(xml_str.encode('utf-8'))
    return etree.tostring(root, encoding='utf-8', pretty_print=True).decode('utf-8')

def next_word_address(word_type='Substantiv'):
    '''
    get the address string of the next word of current category.
    '''
    path = settings.STATICFILES_DIRS[0]
    locale = settings.LOCALE
    f = open(os.path.join(path, 'Wort', locale, "wordlist.xml"))
    xml = f.read()
    soup = BeautifulSoup(xml, "lxml")
    if word_type == 'Substantiv':
        currentLen = len(soup.find_all(
            "word", address=re.compile("^[0-9]+.xml")))
    elif word_type == 'Verben':
        currentLen = len(soup.find_all("word", address=re.compile("V.*")))
    else:
        currentLen = len(soup.find_all("word", address=re.compile("A.*")))
    potential_address = str(currentLen + 1)
    if word_type == 'Verben':
        potential_address = 'V' + potential_address
    elif word_type != 'Substantiv':
        potential_address = 'A' + potential_address
    return potential_address

def addWord(word, gender, chinese, word_type='Substantiv'):
    """
    add a new word to wordlist.xml if isAdded is true,
    """
    path = settings.STATICFILES_DIRS[0]
    locale = settings.LOCALE
    f = open(os.path.join(path, 'Wort', locale, "wordlist.xml"))
    xml = f.read()
    soup = BeautifulSoup(xml, "lxml")
    if word_type == 'Substantiv':
        currentLen = len(soup.find_all(
            "word", address=re.compile("^[0-9]+.xml")))
    elif word_type == 'Verben':
        currentLen = len(soup.find_all("word", address=re.compile("V.*")))
    else:
        currentLen = len(soup.find_all("word", address=re.compile("A.*")))
    potential_address = str(currentLen + 1)
    if word_type == 'Verben':
        potential_address = 'V' + potential_address
    elif word_type != 'Substantiv':
        potential_address = 'A' + potential_address

    root = etree.fromstring(xml.encode('utf-8'))
    sub_element = etree.SubElement(root, 'Word')
    sub_element.set('address', potential_address + '.xml')
    sub_element.set('chinese', chinese)
    sub_element.text = word
    if word_type == 'Substantiv':
        if gender is not None:
            sub_element.set('gender', gender)
    elif word_type == 'Verben':
        sub_element.set('address', potential_address + '.xml')
    else:
        sub_element.set('address', potential_address + '.xml')
    xml_string = etree.tostring(
        root, pretty_print=True, encoding='utf-8').decode('utf-8')
    f = open(os.path.join(path, 'Wort', locale,
                          "wordlist.xml"), 'w', encoding='utf-8')
    f.write(xml_header + wordlist_header)
    f.write(xml_string)
    f.close()


def geturl(word):
    path = settings.STATICFILES_DIRS[0]
    locale = settings.LOCALE
    f = open(os.path.join(path, 'Wort', locale, "wordlist.xml"))
    xml = f.read()
    soup = BeautifulSoup(xml, "lxml")
    node = soup.word
    find = bool(node.string == word)
    while not find:
        node = node.next_sibling
        if node is None:
            break
        if node.string == word:
            find = True
    if find:
        return (node.attrs['address'], 0)
    f.close()
    return ("https://de.wikipedia.org/wiki/" + word, 1)


def get_new_address(category):
    return 'Wort/' + settings.LOCALE + '/' + next_word_address(word_type=category) + '.xml'


def savedit(entry):
    wordform = entry['wordform']
    pronunciation = entry['pronunciation']
    genus = entry['genus']
    plural = entry['plural']
    genitiv = entry['genitiv']
    unittype = entry['unittype']
    anteil = entry['anteil']
    explist = entry['explist']
    symlist = entry['symlist']
    anmlist = entry['anmlist']
    comlist = entry['comlist']
    drvlist = entry['drvlist']
    collist = entry['collist']
    wordAddr = entry['wordAddr']
    if wordAddr is None:
        wordAddr = get_new_address(entry['category'])
    is_created = entry['is_created']
    if(is_created and explist and explist[0]):
        addWord(wordform, genus, explist[0][0],
                word_type=entry['category'])

    s = '''<Entry category="%s">''' % entry['category']
    s = s + '''<Stichwort>''' + wordform + '''</Stichwort>'''
    if pronunciation is not None:
        s = s + '''<Aussprache>''' + pronunciation + '''</Aussprache>'''
    if unittype is not None:
        s = s + '''<Einheit>''' + unittype + '''</Einheit>'''
    if anteil is not None:
        s = s + '''<Anteil>''' + anteil + '''</Anteil>'''
    if genus is not None:
        s = s + '''<Genus>''' + genus + '''</Genus>'''
    if plural is not None:
        s = s + '''<Pluralform>''' + plural + '''</Pluralform>'''
    if genitiv is not None:
        s = s + '''<GenitivSingular>''' + genitiv + '''</GenitivSingular>'''
    s = s + '''<zusammengesetzteWörter>'''
    s = s + '''<KompositaCollection>'''
    for com in comlist:
        if com[1] == "":
            s = s + '''<K_>''' + com[0] + '''</K_>'''
        else:
            s = s + '''<K_ link="''' + \
                geturl(com[1])[0] + '''">''' + com[0] + '''</K_>'''
    s = s + '''</KompositaCollection>'''
    s = s + '''<abgeleiteteWörter>'''
    for drv in drvlist:
        if drv[2] == "":
            s = s + '''<hierzu category="''' + \
                drv[1] + '''">''' + drv[0] + '''</hierzu>'''
        else:
            s = s + '''<hierzu category="''' + \
                drv[1] + '''" link="''' + \
                geturl(drv[2])[0] + '''">''' + drv[0] + '''</hierzu>'''
    s = s+'''</abgeleiteteWörter>'''
    s = s+'''</zusammengesetzteWörter>'''
    s = s+'''<Synonymegruppe>'''
    for sym in symlist:
        if sym[1] == "":
            s = s + '''<Sym>''' + sym[0] + '''</Sym>'''
        else:
            s = s + '''<Sym link="''' + \
                geturl(sym[1])[0] + '''">''' + sym[0] + '''</Sym>'''
    s = s+'''</Synonymegruppe>'''
    s = s+'''<Antonymegruppe>'''
    for anm in anmlist:
        if anm[1] == "":
            s = s+'''<Anm>'''+anm[0]+'''</Anm>'''
        else:
            s = s+'''<Anm link="''' + \
                geturl(anm[1])[0]+'''">'''+anm[0]+'''</Anm>'''
    s = s + '''</Antonymegruppe>'''
    s = s + '''<Kollokationen>'''
    for col in collist:
        s = s+'''<K>''' + col + '''</K>'''
    s = s + '''</Kollokationen>'''
    s = s + '''<AllgemeineErläuterungen>'''
    for exptuple in explist:
        s = s+'''<Eintrag>'''
        s = s+'''<Chinesisch>''' + exptuple[0] + '''</Chinesisch>'''
        s = s+'''<BeispielSammlung>'''
        for samptuple in exptuple[1]:
            s = s + '''<Beispiel>'''
            s = s + '''<Satz>''' + samptuple[0] + '''</Satz>'''
            s = s + '''<Übersetzung>''' + samptuple[1] + '''</Übersetzung>'''
            s = s + '''</Beispiel>'''
        s = s + '''</BeispielSammlung>'''
        s = s + '''</Eintrag>'''
    s = s + '''</AllgemeineErläuterungen>'''

    s = s + '''</Entry>'''
    path = settings.STATICFILES_DIRS[0]   # possible some entry is not parsed!
    # fix deployment issue, apache default to ascii
    f = open(os.path.join(path, wordAddr), 'w', encoding='utf-8')
    # if is Substantiv
    s_pre = xml_header
    if entry["category"] == 'Substantiv':
        template_name = 'Noun'
        stylesheet_name = 'Noun'
    elif entry["category"] == 'Verben':
        template_name = 'Verben'
        stylesheet_name = 'Verb'
    else:
        template_name = 'Adj'
        stylesheet_name = 'Adj'

    s = format_xml(s)
    s_pre += '<!DOCTYPE Entry SYSTEM "%sModel.dtd">\n' % template_name
    s_pre += '<?xml-stylesheet type="text/xsl" href="%sRenderTemplate.xslt"?>\n' % stylesheet_name
    s = s_pre + s
    f.write(s)
    f.close()
    return s


def parsegen(rq):
    err = 0
    reqsheet = {}
    reqsheet['category'] = rq.get('category', 'Substantiv')
    reqsheet['pronunciation'] = rq.get('Aussprache', None)
    reqsheet['wordform'] = rq.get('Stichwort', None)
    reqsheet['genus'] = rq.get('Genus', None)
    if reqsheet['genus'] == '':
        reqsheet['genus'] = None
    reqsheet['plural'] = rq.get('Pluralform', None)
    if reqsheet['plural'] == '':
        reqsheet['plural'] = None
    reqsheet['genitiv'] = rq.get('GenitivSingular', None)
    if reqsheet['genitiv'] == '':
        reqsheet['genitiv'] = None
    reqsheet['unittype'] = rq.get('unittype', None)
    if reqsheet['unittype'] == 'None':
        reqsheet['unittype'] = None
    reqsheet['anteil'] = rq.get('Anteil', None)
    if reqsheet['anteil'] == 'None':
        reqsheet['anteil'] = None
    reqsheet['is_created'] = rq.get('isCreated', False)
    reqsheet['wordAddr'] = rq.get('wordAddr', None)
    if reqsheet['wordAddr'] == 'None':
        reqsheet['wordAddr'] = None
    elif isinstance(reqsheet['wordAddr'], str):
        reqsheet['wordAddr'] = reqsheet['wordAddr'].lstrip('/')
    if reqsheet['wordform'] is None:
        err = 1
        err_str = 'empty wordform'
        return (reqsheet, err, err_str)
    reqsheet['explist'] = parseexp(rq)
    if len(reqsheet['explist']) == 0:
        err = 2
        err_str = 'empty explanation'
        return (reqsheet, err, err_str)

    reqsheet['symlist'] = parsesym(rq)
    reqsheet['anmlist'] = parseanm(rq)
    reqsheet['comlist'] = parsecom(rq)
    reqsheet['drvlist'] = parsedrv(rq)
    reqsheet['collist'] = parsecol(rq)
    return (reqsheet, err, '')


def parseexp(rq):
    explist = list([])
    expcount = 0
    expcur = rq.get('explanation_'+str(expcount+1), '$exp')
    while not expcur == '$exp':
        expcount = expcount+1
        samplist = list([])
        sampcount = 0
        oricur = rq.get('original_'+str(expcount) +
                        '_'+str(sampcount+1), '$samp')
        while not oricur == '$samp':
            sampcount = sampcount+1
            transcur = rq.get('translation_'+str(expcount) +
                              '_'+str(sampcount), '$samp')
            samptuple = [oricur, transcur]
            if samptuple[0]:
                if not samptuple[0][0] == "请":
                    samplist.append(samptuple)
                oricur = rq.get('original_'+str(expcount) +
                                '_'+str(sampcount+1), '$samp')
            else:
                break
        exptuple = [expcur, samplist]
        if exptuple[0]:
            if not exptuple[0][0] == "请":
                explist.append(exptuple)
            expcur = rq.get('explanation_'+str(expcount+1), '$exp')
        else:
            break
    return explist


def parsesym(rq):
    symlist = list([])
    symcount = 0
    symcur = rq.get('Sym_'+str(symcount+1), '$sym')
    while not symcur == '$sym':
        symcount = symcount+1
        symlink = rq.get('Sym_Link_'+str(symcount), '$sym')
        symtuple = [symcur, symlink]
        symlist.append(symtuple)
        symcur = rq.get('Sym_'+str(symcount+1), '$sym')
    if len(symlist) == 0:
        return symlist
    if symlist[len(symlist)-1][0][0] == "请":
        symlist.pop()
    return symlist


def parseanm(rq):
    anmlist = list([])
    anmcount = 0
    anmcur = rq.get('Anm_' + str(anmcount + 1), '$anm')
    while not anmcur == '$anm':
        anmcount = anmcount+1
        anmlink = rq.get('Anm_Link_' + str(anmcount), '$anm')
        anmtuple = [anmcur, anmlink]
        anmlist.append(anmtuple)
        anmcur = rq.get('Anm_'+str(anmcount+1), '$anm')
    if len(anmlist) == 0:
        return anmlist
    if anmlist[len(anmlist)-1][0][0] == "请":
        anmlist.pop()
    return anmlist


def parsecom(rq):
    comlist = list([])
    comcount = 0
    comcur = rq.get('compound_'+str(comcount+1), '$com')
    while not comcur == '$com':
        comcount = comcount+1
        comlink = rq.get('compound_Link_'+str(comcount), '$com')
        comtuple = [comcur, comlink]
        comlist.append(comtuple)
        comcur = rq.get('compound_'+str(comcount+1), '$com')
    if len(comlist) == 0:
        return comlist
    if comlist[len(comlist)-1][0][0] == "请":
        comlist.pop()
    return comlist


def parsedrv(rq):
    drvlist = list([])
    drvcount = 0
    drvcur = rq.get('derivative_'+str(drvcount+1), '$drv')
    while not drvcur == '$drv':
        drvcount = drvcount + 1
        temp = rq.get('derivative_category_' + str(drvcount), '$drv')
        if temp == "名词":
            drvc = "Substantiv"
        if temp == "动词":
            drvc = "Verben"
        if temp == "形容词":
            drvc = "Adjektiv"
        drvlink = rq.get('derivative_Link_' + str(drvcount), '$drv')
        drvtuple = [drvcur, drvc, drvlink]
        drvlist.append(drvtuple)
        drvcur = rq.get('derivative_' + str(drvcount + 1), '$drv')
    if len(drvlist) == 0:
        return drvlist
    if drvlist[len(drvlist)-1][0][0] == "请":
        drvlist.pop()
    return drvlist


def parsecol(rq):
    collist = list([])
    colcount = 0
    colcur = rq.get('collocation_' + str(colcount + 1), '$col')
    while not colcur == '$col':
        colcount = colcount + 1
        collist.append(colcur)
        colcur = rq.get('collocation_'+str(colcount+1), '$col')
    if len(collist) == 0:
        return collist
    if collist[len(collist)-1][0] == "请":
        collist.pop()
    return collist
