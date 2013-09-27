#! /usr/bin/env python
from bucketeer import main
import sys

main.commit_to_s3(sys.argv[1], sys.argv[2])

print 'Task done.'
