# Persian-twitter-day
Daily analysor  tweets of Persian language

Twitter account :
* https://twitter.com/persian_tw_day


# How TO install :
* First rename local_settings_sample.py to local_settings.py
* update local_settings with require data
* (for iranian user )if you want run this on your local PC , uncomment  PROXY SETTINGS 

# How to run :
* python3.6 manage.py runserver
* celery -A tw_analysis worker -B 
* celery -A tw_analysis beat -l info -S django

# Command :
* generate tweet clouds (from -2 day ago,from -0 hours ,1000 words) : python manage.py words_cloud -2 0 1000
* generate tweet clouds (from 0 day ago - today,from -2.5 hours ,1000 words) : python manage.py words_cloud 0 -2.5 1000
*
# TODO 
*  add sentiment analysis 
*  daily report about what people think and what people say
* add telegram connector for fetch data on telegram group ad channel
* add webservice 
* and more ;)

# Demo:

![Alt text](example/2017-07-18-02:07.png?raw=true "ابر کلمات از 1449 تویت در تاریخ Fri, 09 Tir 1396 18:49:33")