#! /usr/bin/env python
from bucketeer import uploader
import sys

try:
  with open('config.json'):
    uploader.upload_from_config()
except IOError:
  print 'Configuration file not found. Using command line arguments.'
  uploader.upload(sys.argv[1], sys.argv[2])

print 'Task done.'
