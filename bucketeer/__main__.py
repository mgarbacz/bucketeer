#! /usr/bin/env python
import sys, json
from bucketeer import uploader

def main(bucket = False, directory = False):
  uploader.upload(bucket, directory)
  print 'Task done.'

if __name__ == '__main__':
  # Map command line arguments to function arguments
  main(*sys.argv[1:])
