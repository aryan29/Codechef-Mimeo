import requests
import bs4
import re
import os
import time
from getpass import getpass
url = 'https://www.codechef.com/users/'
# Fill in your details here to be posted to the login form.
payload = {
    'form_id': 'new_login_form',
    'op': 'Login'
}
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
# Use 'with' to ensure the session context is closed after use.
err = 0
cc = 0
uncopied = []
uncopiedn = []


def getFileFormat(lang):
    dict = {'C': '.c', 'C++11': '.cpp', 'C++14': '.cpp',
            'C++17': '.cpp', 'PYTH3.6': '.py', 'PYTH': '.py', 'JAVA': '.java'}
    try:
        return dict[lang]
    except:
        return '.txt'


def savefile(codee, users, problemcode, lang):
    x = getFileFormat(lang)
    problemcode = problemcode+x
    dir = os.path.join(os.getcwd(), users, problemcode)
    print(problemcode, ' is copying')
    file = open(dir, 'w')
    print(codee, file=file)


def makingreq(users):
    global err
    global cc
    with requests.Session() as s:
        p = s.get('https://www.codechef.com/', headers=headers)
        # print the html returned or something more intelligent to see if it's a successful login page.
        soup = bs4.BeautifulSoup(p.text, 'html.parser')
        a = soup.find('input', attrs={'name': 'form_build_id'})['value']
        payload['form_build_id'] = a
        s.post('https://www.codechef.com/', data=payload)
        urll = url+users
        req = s.get(urll)
        # print(req.text)
        obj = bs4.BeautifulSoup(req.text, 'html.parser')
        ob = obj.find('section', class_='rating-data-section problems-solved')
        ob = ob.find('div')
        ob = str(ob)
        links = re.compile(r'href="(\S+?)">')
        li1 = links.findall(ob)
        xy = re.compile(r'[/status/](\w+),')
        li = xy.findall(ob)
        # print(li)
        cc = len(li)
        for i in range(len(li)):
            urll = f'https://www.codechef.com{li1[i]}'
            # print(urll)
            reqq = s.get(urll)
            # print(reqq.text)
            objj = bs4.BeautifulSoup(reqq.text, 'html.parser')
            # print(objj)
            # print('\n\n\n')
            o = objj.find('div', class_='tablebox-section l-float')
            try:
                lang = (o.findAll('td'))[6].text
            except:
                lang = 'C++14'
            # print(lang)
            # print(type(o))
            if(type(o) == type(None)):
                print(li[i], ' not able to copy due to error')
                uncopied.append(li1[i])
                uncopiedn.append(li[i])
                err = err+1
                continue
            o = o.find('td')
            code = o.getText()
            # print(code)
            # got the problem code
            purl = f'https://www.codechef.com/viewplaintext/{code}'
            # print(purl)
            soln = s.get(purl)
            mobj = bs4.BeautifulSoup(soln.text, 'html.parser')
            codee = mobj.getText()
            savefile(codee, users, li[i], lang)
        s.get('https://www.codechef.com/logout')


def tryagain(users):
    for i in range(len(uncopied)):
        global err
        req = requests.get(f'https://www.codechef.com{uncopied[i]}')
        objj = bs4.BeautifulSoup(req.text, 'html.parser')
        o = objj.find('div', class_='tablebox-section l-float')
        try:
            lang = (o.findAll('td'))[6].text
        except:
            lang = 'C++14'
        # print(lang)
        # print(type(o))
        if(type(o) == type(None)):
            continue
        err = err-1
        o = o.find('td')
        code = o.getText()
        # print(code)
        # got the problem code
        purl = f'https://www.codechef.com/viewplaintext/{code}'
        # print(purl)
        soln = requests.get(purl)
        mobj = bs4.BeautifulSoup(soln.text, 'html.parser')
        codee = mobj.getText()
        savefile(codee, users, uncopiedn[i], lang)


if __name__ == '__main__':
    users = input("Enter your username ")
    pas = getpass()
    payload['name'] = users
    payload['pass'] = pas
    try:
        os.mkdir(users)
        print("Making a directory named ", users)
    except:
        print(f'Directory with name {users} found')
    makingreq(users)
    print('Total Number of Copied Codes ', cc-err)
    print('Total Number of uncopied codes', err)
    print('Do you want to try copying uncopied codes again(y/n)')
    i = input()
    if(i == 'y'or i == 'Y'):
        print("Uncopied Codes", uncopiedn)
        tryagain(users)
        print("Uncopied codes: ", err)
        print("Uncopied codes maybe due to presenece of maths-answers intead of programming codes")
