bumbletweet
===========

![Bumble not included](https://flic.kr/p/dz2cqT "Bumble on the job")

watch twitter for a certain hashtag and send it to festival voice synthesis!

Quick Start
-----------

0. configure enviroment
    `virtualenv --no-site-packages virt`
    `source virt/bin/activate`
    `pip install -r requirements.txt`
    `cp local_settings.example.py local_settings.py`
    `edit local_settings.py`

1. FOR LINUX : Start your [festival](http://www.cstr.ed.ac.uk/projects/festival/) server

    `festival --server`

1. FOR MAC : start speak_bumble_speak.sh

    `bash ./speak_bumble_speak.sh`

2. Run bumbletweet

    `python bumbletweet.py`


Issues
-------

currently ^C doesn't kill bumbletweet.py... don't know if i care enought to find out why.
