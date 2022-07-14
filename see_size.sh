#!/bin/bash
#冒号表述死循环 同while (true)
while :; do
  echo "----------------"
  echo "-----file size-----"
  ls -alh "$1"
  echo "----------------"
  echo "-----file lines-----"
  wc -l "$1"
  sleep 30
done
