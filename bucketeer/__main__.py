#! /usr/bin/env python
import sys, json
from bucketeer import uploader

def main(bucket = False, directory = False):
  if bucket and directory:
    uploader.upload(bucket, directory)
  else:
    try:
      config = json.loads(open('bucketeer.json').read())
      print 'Configuration file found.'
      uploader.upload(config['bucket'], config['directory'])
    except IOError:
      print 'Configuration file not found. Nothing to do...'
    except KeyError as e:
      print 'Configuration file incorrect. Missing:', e

  print 'Task done.'

if __name__ == '__main__':
  # Map command line arguments to function arguments
  main(*sys.argv[1:])
