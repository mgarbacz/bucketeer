import unittest
import boto
from bucketeer import commit

class BuckeeterTest(unittest.TestCase):

  def setUp(self):
    # Create a bucket with one file
    connection = boto.connect_s3()
    bucket = connection.create_bucket('bucket.exists')

    return

  def tearDown(self):
    # Remove all test-created buckets and files
    connection = boto.connect_s3()
    bucket = connection.delete_bucket('bucket.exists')
    return

  def testMain(self):
    self.assertTrue(commit)

if __name__ == '__main__':
  unittest.main()
