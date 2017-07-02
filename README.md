# persian-twitter-day
daily analysor  tweets of Persian language

twitter account :
* https://twitter.com/persian_tw_day

# Demo:

* text cloud from 1449 tweets on Fri,09 Tir 1396

# How TO install :
* First rename local_settings_sample.py to local_settings.py
* update local_settings with require data
* (for iranian user )if you want run this on your local PC , uncomment  PROXY SETTINGS 

# how to run :
* python3.6 manage.py runserver
* celery -A tw_analysis worker -B 
* celery -A proj beat -l info -S django

![Alt text](example/text-cloud.png?raw=true "ابر کلمات از 1449 تویت در تاریخ Fri, 09 Tir 1396 18:49:33")