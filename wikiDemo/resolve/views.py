#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @Author  : Ann
# @Time    :

from django.shortcuts import render
from learn.urldecode import decode
from django.http import HttpResponseRedirect
from courseInfo.models import courseVideo
import django
import re
import json
def getId(sourceName):
    pass
# def redirect(request,para):
#     print "redirect"
#     para = para.split('/')
#     post = {}
#     if list(para).count('section') != 0:
#         print para
#         post['course'] = para[0]
#         post['object'] = para[1]
#         post['chapter'] = para[list(para).index('section')-1]
#         post['section'] = para[list(para).index('section')+1]
#         lst = []
#         lst.append(int(post['chapter'].encode("utf-8")))
#         lst.append(int(post['section'].encode("utf-8")))
#         post['section']  = lst
#         print post['section']
#         id = decode(post)
#         return HttpResponseRedirect("https://class.coursera.org/"+post['course']+"/"+post['object']+"/"+id)
#     elif list(para).count('week') != 0 :
#         post['course'] = para[0]
#         post['object'] = para[1]
#         return HttpResponseRedirect("https://www.coursera.org/learn/"+post['course']+"/"+"home/week/1")
#     elif list(para).count('lecture') != 0 and len(para) == 3:
#         post['course'] = para[0]
#         post['object'] = para[1]
#         post['chapter'] = para[2]
#         if post['chapter'].isdigit() is False:
#             try:
#                 link = courseVideo.objects.filter(courseName = post['course'],videoName = post['chapter'])[0].resource_link
#                 return HttpResponseRedirect(link)
#             except:
#                 pass
#         else:
#             return HttpResponseRedirect("https://class.coursera.org/"+post['course']+"/"+"lecture")
#
#     elif list(para).count('lecture') != 0 and para.count('slide') !=0:
#         post['course'] = para[0]
#         post['object'] = para[1]
#         post['chapter'] = para[2].encode('utf-8')
#         post['subObject'] = para[3]
#         post['page'] = para[4].encode('utf-8')
#         print post['page']
#         return HttpResponseRedirect("https://www.coursera.org/learn/"+post['course']+"/supplement/"+ "SuCGj/pdf-of-lecture-slides")
#         # return HttpResponseRedirect("https://d3c33hcgiwev3.cloudfront.net/"+post['course']+"/docs/slides/Lecture"+post['chapter']+".pdf#page="+post['page'])

#*****************************Ann's design for Coursera 2017******************************#
def redirect(request,para):
    print "redirect"
    para = para.split('/')
    print para
    post = {}
    if list(para).count('section') != 0:
        print para
        post['course'] = para[0]
        post['object'] = para[1]
        post['chapter'] = para[list(para).index('section')-1]
        post['section'] = para[list(para).index('section')+1]
        lst = []
        lst.append(int(post['chapter'].encode("utf-8")))
        lst.append(int(post['section'].encode("utf-8")))
        post['section']  = lst
        print post['section']
        id = decode(post)
        return HttpResponseRedirect("https://class.coursera.org/"+post['course']+"/"+post['object']+"/"+id)
    elif list(para).count('week') != 0 :
        post['course'] = para[0]
        post['object'] = para[1]
        return HttpResponseRedirect("https://www.coursera.org/learn/"+post['course']+"/"+"home/week/1")
    elif list(para).count('lecture') != 0 and len(para) == 3:
        post['course'] = para[0]
        post['object'] = para[1]
        post['chapter'] = para[2]
        if post['chapter'].isdigit() is False:
            try:
                link = courseVideo.objects.filter(courseName = post['course'],videoName = post['chapter'])[0].resource_link
                return HttpResponseRedirect(link)
            except:
                pass
        else:
            return HttpResponseRedirect("https://class.coursera.org/"+post['course']+"/"+"lecture")

    elif list(para).count('slide') != 0:
        post['course'] = para[0]
        post['object'] = para[1]
        post['slice'] = para[2]
        return HttpResponseRedirect("https://www.coursera.org/learn/" + post['course'] + "/" + "home/week/1")
    elif list(para).count('lecture') != 0 and para.count('slide') !=0:
        post['course'] = para[0]
        post['object'] = para[1]
        post['chapter'] = para[2].encode('utf-8')
        post['subObject'] = para[3]
        post['page'] = para[4].encode('utf-8')
        print post['page']
        return HttpResponseRedirect("https://www.coursera.org/learn/"+post['course']+"/supplement/"+ "SuCGj/pdf-of-lecture-slides")
        # return HttpResponseRedirect("https://d3c33hcgiwev3.cloudfront.net/"+post['course']+"/docs/slides/Lecture"+post['chapter']+".pdf#page="+post['page'])
    elif list(para).count('video') != 0:
        #http://127.0.0.1:8000/resolve//learn/accounting-analytics/discussions/weeks/1?sort=lastActivityAtDesc&page=1&q=/video/1.5
        post['course'] = para[1]
        post['object'] = para[5]
        post['chapter'] = para[6]
        print para[1], para[5], para[6]

        if post['chapter'].isdigit() is False:
            try:

                link = courseVideo.objects.filter(coursename = post['course'], sourcetype= 'lecture', sourcename = 'ratio-analysis-profitability-and-turnover-ratios-1-5')[0].sourceurl
                return HttpResponseRedirect(link)
            except:
                pass
        else:
            try:

                link = courseVideo.objects.filter(coursename = post['course'], sourcetype= 'lecture', sourcename = 'ratio-analysis-profitability-and-turnover-ratios-1-5')[0].sourceurl
                return HttpResponseRedirect(link)
            except:
                pass
            return HttpResponseRedirect("https://class.coursera.org/"+post['course']+"/"+"lecture")


