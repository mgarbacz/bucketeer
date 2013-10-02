#! /usr/bin/env python
from bucketeer import commit
import sys

commit.commit_to_s3(sys.argv[1], sys.argv[2])

print 'Task done.'
