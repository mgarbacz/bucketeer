import unittest
import boto
from bucketeer import commit

class BuckeeterTest(unittest.TestCase):

  global existing_bucket
  existing_bucket = 'bucket.exists'

  def setUp(self):
    # Create a bucket with one file
    connection = boto.connect_s3()
    bucket = connection.create_bucket(existing_bucket)

    return

  def tearDown(self):
    # Remove all test-created buckets and files
    connection = boto.connect_s3()
    bucket = connection.delete_bucket(existing_bucket)
    return

  def testMain(self):
    self.assertTrue(commit)

if __name__ == '__main__':
  unittest.main()
