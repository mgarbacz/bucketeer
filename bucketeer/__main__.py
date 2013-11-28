#! /usr/bin/env python
from bucketeer import uploader
import sys, json

def main(bucket = False, directory = False):
  if (not bucket and not directory):
    try:
      config = json.loads(open('config.json').read())
      print 'Configuration file found.'
      uploader.upload(config['bucket'], config['dir'])
    except IOError:
      print 'Configuration file not found. Nothing to do...'
  else:
    uploader.upload(bucket, directory)
  print 'Task done.'

if __name__ == '__main__':
  # Map command line arguments to function arguments
  main(*sys.argv[1:])
