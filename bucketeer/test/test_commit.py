import unittest, boto, os
from bucketeer import commit

class BuckeeterTest(unittest.TestCase):

  def setUp(self):
    # Init variable values
    self.existing_bucket = 'bucket.exists'
    self.new_bucket = 'bucket.new'
    self.test_dir = 'bucketeer_test_dir'
    self.test_file = 'bucketeer_test_file'
    self.connection = boto.connect_s3()

    # Create a bucket to test on existing bucket
    self.connection.create_bucket(self.existing_bucket)

    # Create directory to house test files
    os.makedirs(self.test_dir)

    # Create test file
    open(self.test_dir + '/' + self.test_file, 'w').close()

    return

  def tearDown(self):
    # Remove the bucket created for testing
    self.remove_bucket(self.existing_bucket)

    # Remove test file
    os.remove(self.test_dir + '/' + self.test_file)

    # Remove directory created to house test files
    os.rmdir(self.test_dir)

    return

  def check_file_on_s3(self, bucket_name, file_name):
    # Get the file object from s3
    bucket = self.connection.get_bucket(bucket_name)
    s3_file = bucket.get_key(file_name)

    # True if it exists on s3, False if it does not
    return s3_file.exists()

  def remove_bucket(self, bucket_name):
    # Delete all files in the bucket
    bucket = self.connection.get_bucket(bucket_name)
    for s3_file in bucket.list():
      bucket.delete_key(s3_file.key)

    # Delete the bucket
    self.connection.delete_bucket(bucket_name)

  def test_main(self):
    self.assertTrue(commit)

  def test_new_file_upload_to_existing_bucket(self):
    result = commit.commit_to_s3(self.existing_bucket, self.test_dir)
    self.assertTrue(self.check_file_on_s3(self.existing_bucket, self.test_file))

  def test_new_file_upload_to_new_bucket(self):
    result = commit.commit_to_s3(self.new_bucket, self.test_dir)
    self.assertTrue(result)

    # Tear down the upload
    self.remove_bucket(self.new_bucket)

  def test_multiple_file_upload(self):
    # Create second file
    open(self.test_dir + '/' + self.test_file + '2', 'w').close()

    result = commit.commit_to_s3(self.existing_bucket, self.test_dir)
    self.assertTrue(result)

    # Remove second file
    os.remove(self.test_dir + '/' + self.test_file + '2')


if __name__ == '__main__':
  unittest.main(buffer = True)
