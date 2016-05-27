#!/usr/local/bin/python
# coding:utf-8


import docclass

cl = docclass.naivebayes(docclass.getwords)
docclass.sampletrain(cl)
print cl.prob('quick rabbit', 'good')
print  cl.prob('quick rabbit', 'bad')
print cl.prob('quick money', 'good')
print  cl.prob('quick money', 'bad')

print cl.classify('quick rabbit', default='unknown')
print cl.classify('quick money', default='unknown')

cl.setthresholds('bad', 3.0)
print cl.classify('quick money', default='unknown')
print cl.classify('quick rabbit', default='unknown')
for i in range(10):
    docclass.sampletrain(cl)
print cl.classify('quick money', default='unknown')
print cl.prob('quick money', 'good')
print  cl.prob('quick money', 'bad')

print "*******************fisher classify******************"
reload(docclass)
cl2 = docclass.fisherclassifier(docclass.getwords)
docclass.sampletrain(cl2)
print cl2.cprob('quick', 'good')
print cl2.fisherprob('quick rabbit', 'good')
print cl2.fisherprob('quick rabbit', 'bad')

print cl2.classify("quick rabbit")
print cl2.classify("quick money")

cl2.setminimum('bad', 0.8)
print cl2.classify("quick money")
cl2.setminimum('good', 0.4)
print cl2.classify("quick money")

