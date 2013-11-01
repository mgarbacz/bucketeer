import unittest, boto, os
from bucketeer import commit

class BuckeeterTest(unittest.TestCase):

  # Constants - TODO move to config file
  global existing_bucket, test_dir, test_file
  existing_bucket = 'bucket.exists'
  test_dir = 'bucketeer_test_dir'
  test_file = 'bucketeer_test_file'

  def setUp(self):
    connection = boto.connect_s3()

    # Create a bucket to test on existing bucket
    bucket = connection.create_bucket(existing_bucket)

    # Create directory to house test files
    os.makedirs(test_dir)

    # Create test file
    open(test_dir + '/' + test_file, 'w').close()

    return

  def tearDown(self):
    connection = boto.connect_s3()

    # Remove all files uploaded to s3
    bucket = connection.get_bucket(existing_bucket)
    for s3_file in bucket.list():
      bucket.delete_key(s3_file.key)

    # Remove bucket created to test on existing bucket
    bucket = connection.delete_bucket(existing_bucket)

    # Remove test file
    os.remove(test_dir + '/' + test_file)

    # Remove directory created to house test files
    os.rmdir(test_dir)

    return

  def testMain(self):
    self.assertTrue(commit)

  def testNewFileUploadToExistingBucket(self):
    result = commit.commit_to_s3(existing_bucket, test_dir)
    self.assertTrue(result)

if __name__ == '__main__':
  unittest.main()
