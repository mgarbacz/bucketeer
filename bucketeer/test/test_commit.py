import unittest, boto, os, time
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

  ### Test Methods

  def test_main(self):
    # True if module loaded successfully, False if not
    self.assertTrue(commit)

  def test_new_file_upload_to_existing_bucket(self):
    commit.commit_to_s3(self.existing_bucket, self.test_dir)

    # True if commit to s3 was successful, False if not
    result = self.check_file_on_s3(self.existing_bucket, self.test_file)
    self.assertTrue(result)

  def test_new_file_upload_to_new_bucket(self):
    commit.commit_to_s3(self.new_bucket, self.test_dir)

    # True if commit to s3 was successful, False if not
    result = self.check_file_on_s3(self.new_bucket, self.test_file)
    self.assertTrue(result)

    # Tear down the newly created bucket
    self.remove_bucket(self.new_bucket)

  def test_multiple_file_upload(self):
    # Create a second test file
    open(self.test_dir + '/' + self.test_file + '2', 'w').close()

    commit.commit_to_s3(self.existing_bucket, self.test_dir)

    # Both True if commit to s3 was successful, False if not
    result1 = self.check_file_on_s3(self.existing_bucket, self.test_file)
    result2 = self.check_file_on_s3(self.existing_bucket, self.test_file + '2')
    self.assertTrue(result1 and result2)

    # Remove the second test file locally
    os.remove(self.test_dir + '/' + self.test_file + '2')

  def test_modified_file_upload(self):
    commit.commit_to_s3(self.existing_bucket, self.test_dir)

    # Check timestamp after original upload
    timestamp_1 = self.check_file_timestamp(self.existing_bucket,
                                            self.test_file)

    # Modify the file locally
    local_file = open(self.test_dir + '/' + self.test_file, 'w')
    local_file.write('This file has been modified\n')
    local_file.close()

    commit.commit_to_s3(self.existing_bucket, self.test_dir)

    # Let S3 catch up with itself
    time.sleep(2)

    # Check the timestamp after second upload
    timestamp_2 = self.check_file_timestamp(self.existing_bucket,
                                            self.test_file)

    # True if file was modified on s3, False if not
    result = timestamp_2 > timestamp_1
    self.assertTrue(result)

  def test_unmodified_file_upload(self):
    commit.commit_to_s3(self.existing_bucket, self.test_dir)

    # Check timestamp after original upload
    timestamp_1 = self.check_file_timestamp(self.existing_bucket,
                                            self.test_file)

    commit.commit_to_s3(self.existing_bucket, self.test_dir)

    # Check timestamp after second upload
    timestamp_2 = self.check_file_timestamp(self.existing_bucket,
                                            self.test_file)

    # Let S3 catch up with itself
    time.sleep(2)

    # True if file was not modified on s3, False if it has
    result = timestamp_2 == timestamp_1
    self.assertTrue(result)

  ###

  ### Helper methods

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

  def check_file_timestamp(self, bucket_name, file_name):
    # Return timestamp of last file modification
    bucket = self.connection.get_bucket(bucket_name)
    return bucket.get_key(file_name).last_modified

  ###

if __name__ == '__main__':
  unittest.main(buffer = True)
