from django.db import models

# # Create your models here.
# class courseVideo(models.Model):
#     courseName = models.CharField(max_length = 50)
#     videoName = models.CharField(max_length = 50)
#     resource_link = models.URLField()
    # CREATE TABLE myapp_coursevideo(
    # "coursename" varchar(50) NOT NULL PRIMARY KEY,
    # "videoname" varchar(50) NOT NULL,
    # "resource_link" XXX NOT NULL );

class courseVideo(models.Model):
    coursename = models.CharField(max_length = 50)
    sourcetype = models.CharField(max_length= 50)
    sourceid = models.CharField(max_length= 50)
    sourcename = models.CharField(max_length = 50)
    sourceurl = models.URLField()