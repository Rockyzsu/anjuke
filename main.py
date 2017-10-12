# coding: utf-8
import codecs
import json
import subprocess
import time

'''
fp = codecs.open('anjuke_city','r')
str_data = fp.read()
js = json.loads(str_data)
'''
std_fp = open('spider1.log', 'a')
err_fp = open('spider_err1.log', 'a')
'''
for k, v in js.items():

    cmd = 'scrapy crawl anjuke_m -a city=%s' % k
    print cmd
    p = subprocess.Popen(cmd, stdout=std_fp, stderr=err_fp, shell=True)
    p.communicate()
    p.wait()
    time.sleep(120)
'''

fp2=open('anjuke_rent.txt', 'r')
city_chinese_name = fp2.readlines()
city_chinese_name=map(lambda x:x.strip(),city_chinese_name)

while len(city_chinese_name)>0:

    city= city_chinese_name.pop()
    try:
        cmd = 'scrapy crawl anjuke_rent -a city=%s' %city
        #print cmd
        p = subprocess.Popen(cmd, stdout=std_fp, stderr=err_fp, shell=True)
        p.communicate()
        p.wait()
    except Exception,e:
        fp2.close()

        fp3=open('anjuke_rent.txt', 'w')
        for i in city_chinese_name:
            fp3.write(i)
            fp3.write('\n')
        fp3.close()

        break

#fp2.close()
std_fp.close()
err_fp.close()
