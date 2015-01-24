#!/usr/bin/python
# TESTING SELECTIVE GITHUB UPDATES

import os
import time

version = 1

def update():
	os.system('sudo git fetch')
	os.system('sudo git checkout HEAD pangolin_pad/backup/version')
