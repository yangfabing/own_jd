#!/bin/sh

echo "处理财富岛jd_cfd_loop任务。。。"
echo "默认启用jd_cfd_loop杀掉jd_cfd_loop任务，并重启"
eval $(ps -ef | grep "jd_cfd_loop" | grep -v "grep" | awk '{print "kill "$1}')
echo '' >/scripts/logs/jd_cfd_loop.log
# ts-node /scripts/jd_cfd_loop.ts | ts >>/scripts/logs/jd_cfd_loop.log 2>&1 &
# echo "默认jd_cfd_loop重启完成"
