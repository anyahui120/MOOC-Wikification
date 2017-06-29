#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Created on 2017.3.16
@author: Ann
Modified by Ann at 2017.3.17
'''

import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from courseInfo.models import courseVideo
import time
import html.parser
import structure as st
#import courseInfo
import re
from bs4 import BeautifulSoup
import yaml
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class pageAnalysiser:
    def __init__(self):
        with open('config.yml') as f:
            config = yaml.load(f)
        self.driver = webdriver.PhantomJS()
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

    def analyse(self,courseName,filename):

        try:
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
                        # self.driver.implicitly_wait(5)
                        # element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rc-ItemNavigation")))
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
                                    video_source_name = temp[len(temp) - 1]
                                    new_url = prefix + href_step2
                                    new_str =  courseName + '||' + 'lecture'+ '||' + video_source_name + '||' + new_url + '\n'
                                    filename.write(new_str)
                            else:
                                continue
                    elif 'supplement' in href_split:
                        source_url = prefix + href
                        self.driver.get(source_url)
                        time.sleep(5)
                        html_step2 = self.driver.page_source
                        # self.driver.implicitly_wait(5)
                        # element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rc-ItemNavigation")))
                        html_step2 = str(html_step2)
                        soup = BeautifulSoup(html_step2, 'html.parser')
                        linkss = soup.findAll('a', class_ = 'cml-asset-link')
                        supplement = {}
                        for link in linkss:
                            if link.attrs['class'] == ['cml-asset-link']:
                                supplement[link.contents[0]] = link.attrs['href']
                            else:
                                continue
                        for key in supplement.keys():
                            video_source_name = key
                            href_supp = supplement[key]
                            new_url = href_supp
                            new_str = courseName + '||' + 'slide' + '||' + video_source_name + '||' + new_url + '\n'
                            filename.write(new_str)
                    else:
                        print href
                        print 'Not a lecture or supplement resource.'
                        self.driver.back()
        except Exception,e:
            print e

    def prettyInfo(self,archs):
        names = []
        for item in archs:
            try:
                groups = item.get_attribute("textContent").encode("utf-8").split(" ")
            except Exception:
                groups = item.get_attribute("textContent").encode("ascii").split(" ")
            names.append(groups)
        invalidSet = ('lecture','module','part','video','–','\n','\t','\r','\\n','-','.')
        invalidPattern = re.compile("(\d*\.\d*)|(\d*:\d*)|(\d*-\d*)",re.IGNORECASE)
        for i in range(len(names)):
            for j in range(len(names[i])):
                try:
                    if str(names[i][j]).strip(" \t\n\r-").lower() in invalidSet or invalidPattern.match(str(names[i][j]).strip(" \t\n\r-")):
                        print names[i][j]
                        names[i][j] = ''
                        if str(names[i][j+1])[0].isdigit():
                            names[i][j+1] = ''
                    elif names[i][j][0] == '(':
                        names[i][j] = ''
                        if names[i][j+1][-1] == ')':
                            names[i][j+1] = ''
                except Exception:
                    continue
        prettyName = []
        for groups in names:
            prettyWord = " "
            prettyWord = prettyWord.join(groups)
            prettyName.append(prettyWord.lstrip(' -.:\n').rstrip())
        return prettyName


if __name__ == '__main__':
    pageAnalysis = pageAnalysiser()
    pageAnalysis.driver.implicitly_wait(5)
    pageAnalysis.login()
    time.sleep(2)

    with open('config.yml') as f:
        config = yaml.load(f)
    userId = config['UserId']
    filePath = config['filePath']
    conn = sqlite3.connect('/Users/anyahui/Downloads/lib4moocdata-master/coursera/data/nusdata.db')
    c = conn.cursor()
    courseNames = c.execute('select distinct(coursename) from forum').fetchall()
    for ii in xrange(20,len(courseNames)):
        course = courseNames[ii]
        print 'Processing: %d/%d....'%(ii+1,len(courseNames))
        courseName = course[0]
        file = '/Users/anyahui/Documents/CourseraDeepLearning/courseraSourceInfoData/'+ courseName + '.txt'
        filename = open(file,'w+')
        print courseName
        pageAnalysis.analyse(courseName,filename)
        filename.close()

    pageAnalysis.driver.quit()
# courseVideo.objects.all()