#!/bin/sh
 set -e

 sudo pip3 install virtualenv
 virtualenv .env
 source .env/bin/activate
 pip install -r requirements.txt