#!/bin/bash
cd /home/zhangyoufu/WebCrawler/
cfx xpi
cfx run --profiledir='/home/zhangyoufu/profile_1/' &
sleep 5000
pkill firefox
