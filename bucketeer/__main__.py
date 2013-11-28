#! /usr/bin/env python
from bucketeer import uploader
import sys

def main(bucket = false, directory = false):
  if (not bucket and not directory):
    try:
      with open('config.json'):
        uploader.upload_from_config()
    except IOError:
      print 'Configuration file not found. Using command line arguments.'
      uploader.upload(bucket, directory)

print 'Task done.'

if __name__ == '__main__':
  # Map command line arguments to function arguments
  main(*sys.argv[1:])
