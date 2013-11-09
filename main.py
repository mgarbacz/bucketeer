#! /usr/bin/env python
from bucketeer import uploader
import sys

uploader.upload(sys.argv[1], sys.argv[2])

print 'Task done.'
