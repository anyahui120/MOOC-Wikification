#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
@author: Ann
'''

import sqlite3
from selenium import webdriver
import time
import html.parser
from bs4 import BeautifulSoup
import yaml
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class pageAnalysiser:
    def __init__(self):
        with open('config.yml') as f:
            config = yaml.load(f)
        self.driver = webdriver.PhantomJS('/Users/anyahui/Documents/国外工作/Wikifier-master/bin/phantomjs')
        self.email = config['UserName']
        self.password = config['Password']
        self.courses = []

    def login(self):
        self.driver.get('https://www.coursera.org/?authMode=login')
        email_field = self.driver.find_element_by_name("email")
        password_field = self.driver.find_element_by_name("password")
        email_field.send_keys(self.email)
        password_field.send_keys(self.password)
        password_field.submit()

    def analyse(self,courseName):

        try:
            courseVideo = []
            courseSupplement = []
            site = "https://www.coursera.org/learn/" + courseName + "/home/welcome"
            print site
            first_step = self.driver.get(site)
            time.sleep(5)
            # self.driver.implicitly_wait(5)
            # element = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "rc-GuidedCourseHome")))
            html = self.driver.page_source
            html = str(html)
            soup = BeautifulSoup(html, 'html.parser')
            contents = soup.findAll('ul')
            content = contents[len(contents)-1]
            if content.attrs == {'class': ['rc-HomeWeekCards', 'nostyle']}:
                links = content.findAll('a')
                hrefs = []
                for link in links:
                    if link.attrs['class'] == ['rc-UngradedItemProgress', 'horizontal-box', 'align-items-vertical-center']:
                        hrefs.append(link.attrs['href'])
                prefix = 'https://www.coursera.org'
                for j in xrange(len(hrefs)):
                    href = hrefs[j]
                    href_split = href.split('/')
                    if 'lecture' in href_split:
                        source_url = prefix + href
                        self.driver.get(source_url)
                        time.sleep(5)
                        html_step2 = self.driver.page_source
                        html_step2 = str(html_step2)
                        soup = BeautifulSoup(html_step2, 'html.parser')
                        linkss = soup.findAll('ul')
                        for link in linkss:
                            if link.attrs['class'] == ['rc-LessonItems', 'nostyle']:
                                urls = link.findAll('a')
                                hrefs_step2 = []
                                for url in urls:
                                    if url.attrs['class'] == ['rc-ItemLink', 'nostyle']:
                                        hrefs_step2.append(url.attrs['href'])
                                for k in xrange(len(hrefs_step2)):
                                    href_step2 = hrefs_step2[k]
                                    temp = href_step2.split('/')
                                    source_name = temp[len(temp) - 1]
                                    source_id = temp[len(temp) - 2]
                                    source_type = temp[len(temp)-3]
                                    coursename = temp[len(temp) -4]
                                    courseVideo.append([coursename,source_type,source_id,source_name,href_step2])
                            else:
                                continue
                    elif 'supplement' in href_split:
                        courseSupplement.append([href_split[len(href_split)-4],href_split[len(href_split)-3], href_split[len(href_split)-2], href_split[len(href_split)-1],href])
                    elif 'quiz' in href_split:
                        courseSupplement.append([href_split[len(href_split) - 4], href_split[len(href_split) - 3],
                                                 href_split[len(href_split) - 2], href_split[len(href_split) - 1],
                                                 href])
                    elif 'discussionPrompt' or 'peer' or 'ungradedLti' in href_split:
                        courseSupplement.append([href_split[len(href_split) - 4], href_split[len(href_split) - 3],
                                                 href_split[len(href_split) - 2], href_split[len(href_split) - 1],
                                                 href])
                    else:
                        print href
                        print 'Not a lecture or supplement resource.'
                        self.driver.back()
            return courseVideo,courseSupplement
        except Exception,e:
            print e
            return 0


if __name__ == '__main__':
    pageAnalysis = pageAnalysiser()
    pageAnalysis.driver.implicitly_wait(10)
    pageAnalysis.login()
    time.sleep(3)

    with open('config.yml') as f:
        config = yaml.load(f)
    userId = config['UserId']
    filePath = config['filePath']
    conn = sqlite3.connect('/Users/anyahui/Downloads/lib4moocdata-master/coursera/data/nusdata.db')
    c = conn.cursor()
    courseNames = c.execute('select distinct(coursename) from forum').fetchall()
    conn.commit()
    conn.close()

    conn = sqlite3.connect('/Users/anyahui/Documents/国外工作/MOOCWikification/courseVideo.db')
    c = conn.cursor()
    c.execute('drop table if exists courseVideo')
    c.execute('''CREATE TABLE courseVideo ( \
    coursename text, \
    sourcetype text, \
    sourceid text, \
    sourcename text, \
    sourceurl text, \
    primary key(sourcename,sourceid))
    ''')

    for ii in xrange(len(courseNames)-145):
        try:
            course = courseNames[ii]
            print 'Processing: %d/%d....'%(ii+1,len(courseNames))
            courseName = course[0]
            print courseName
            courses,coursesupp = pageAnalysis.analyse(courseName)
            for iii in xrange(len(courses)):
                courseVideo = courses[iii]
                coursen, source_type, source_id, source_name, source_url = courseVideo[0], courseVideo[1], courseVideo[2], \
                                                                       courseVideo[3], courseVideo[4]
                # sourcenum_list = source_name.split('-')
                # if sourcenum_list[-1].isdigital() == True:
                #     if sourcenum_list[-2].isdigital() == True:
                #         sourcenum = ''.join([sourcenum_list[-2],'.',[sourcenum_list[-1]]])
                #     else:
                #         sourcenum = sourcenum_list[-1]
                # else:
                #     sourcenum = 0

                c.execute('insert OR IGNORE into courseVideo values(?,?,?,?,?)',
                      (coursen, source_type, source_id, source_name, source_url,))
            for jjj in xrange(len(coursesupp)):
                courseSPP = coursesupp[jjj]
                coursen, source_type, source_id, source_name, source_url = courseSPP[0], courseSPP[1], courseSPP[2], \
                                                                       courseSPP[3], courseSPP[4]
                c.execute('insert OR IGNORE into courseVideo values(?,?,?,?,?)',
                      (coursen, source_type, source_id, source_name, source_url,))

        except Exception,e:
            print e
            continue
        finally:
            print "Finished!"
    conn.commit()
    conn.close()
    pageAnalysis.driver.quit()
# courseVideo.objects.all()