import unittest, boto, os
from bucketeer import commit

class BuckeeterTest(unittest.TestCase):

  # Constants - TODO move to config file
  global existing_bucket, new_bucket, test_dir, test_file
  existing_bucket = 'bucket.exists'
  new_bucket = 'bucket.new'
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
    # Remove the bucket created for testing
    self.remove_bucket(existing_bucket)

    # Remove test file
    os.remove(test_dir + '/' + test_file)

    # Remove directory created to house test files
    os.rmdir(test_dir)

    return

  def remove_bucket(self, bucket_name):
    connection = boto.connect_s3()

    # Delete all files in the bucket
    bucket = connection.get_bucket(bucket_name)
    for s3_file in bucket.list():
      bucket.delete_key(s3_file.key)

    # Delete the bucket
    connection.delete_bucket(bucket_name)

  def test_main(self):
    self.assertTrue(commit)

  def test_new_file_upload_to_existing_bucket(self):
    result = commit.commit_to_s3(existing_bucket, test_dir)
    self.assertTrue(result)

  def test_new_file_upload_to_new_bucket(self):
    result = commit.commit_to_s3(new_bucket, test_dir)
    self.assertTrue(result)

    # Tear down the upload
    self.remove_bucket(new_bucket)

if __name__ == '__main__':
  unittest.main(buffer = True)
