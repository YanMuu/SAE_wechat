# -*- coding: utf-8 -*-
import urllib2,json
import random
import md5


def youdao(word):
    appKey = '76c8663b0b1a2345'
    secretKey = 'NhsueEdBZQU6EfOjqfotZdPvSx7EPhBv'
    myurl = r'http://openapi.youdao.com/api'  #要不要加r     
    qword = urllib2.quote(word)
    fromLang = 'EN'
    toLang = 'zh-CHS'
    salt = random.randint(1, 65536)
    
    sign = appKey+word+str(salt)+secretKey #这里确定下是q还是qword
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    
    
    #baseurl =r'http://fanyi.youdao.com/openapi.do?keyfrom=<keyfrom>&key=<key>&type=data&doctype=json&version=1.1&q='
    url = myurl+'?appKey='+appKey+'&q='+qword+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    resp = urllib2.urlopen(url)
    fanyi = json.loads(resp.read())
    if fanyi['errorCode'] == '0':        
        if 'basic' in fanyi.keys():
            trans = u'%s:\n%s\n%s\n网络释义：\n%s'%(fanyi['query'],''.join(fanyi['translation']),' '.join(fanyi['basic']['explains']),''.join(fanyi['web'][0]['value']))
            return trans
        else:
            trans =u'%s:\n基本翻译:%s\n'%(fanyi['query'],''.join(fanyi['translation']))        
            return trans
    elif fanyi['errorCode'] == 103:
        return u'对不起，要翻译的文本过长'
    elif fanyi['errorCode'] == 104:
        return u'对不起，无法进行有效的翻译'
    elif fanyi['errorCode'] == 102:
        return u'对不起，不支持的语言类型'
    else:
        #return 'else'
        return u'对不起，您输入的单词%s无法翻译,请检查拼写'% word    