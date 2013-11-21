import unittest, boto, os, time, shutil, json
from bucketeer import uploader

class BuckeeterTest(unittest.TestCase):

  def setUp(self):
    # Init variable values
    self.existing_bucket = 'bucket.exists'
    self.new_bucket = 'bucket.new'
    self.test_dir = 'bucketeer_test_dir'
    self.test_file = 'bucketeer_test_file'
    self.connection = boto.connect_s3()
    self.config_file = 'config.json'

    # Create a bucket to test on existing bucket
    self.connection.create_bucket(self.existing_bucket)

    # Create directory to house test files
    os.makedirs(self.test_dir)

    # Create test file
    path_to_test_file = os.path.join(self.test_dir, self.test_file)
    open(path_to_test_file, 'w').close()

    return

  def tearDown(self):
    # Remove the bucket created for testing
    self.remove_bucket(self.existing_bucket)

    # Remove directory created to house test files and the files inside it
    shutil.rmtree(self.test_dir)

    return

  ### Test Methods

  def test_main(self):
    # True if module loaded successfully, False if not
    self.assertTrue(uploader)

  def test_new_file_upload_to_existing_bucket(self):
    uploader.upload(self.existing_bucket, self.test_dir)

    # True if commit to s3 was successful, False if not
    result = self.check_file_on_s3(self.existing_bucket, self.test_file)
    self.assertTrue(result)

  def test_new_file_upload_to_new_bucket(self):
    uploader.upload(self.new_bucket, self.test_dir)

    # True if commit to s3 was successful, False if not
    result = self.check_file_on_s3(self.new_bucket, self.test_file)
    self.assertTrue(result)

    # Tear down the newly created bucket
    self.remove_bucket(self.new_bucket)

  def test_multiple_file_upload(self):
    # Create a second test file
    path_to_test_file = os.path.join(self.test_dir, self.test_file + '2')
    open(path_to_test_file, 'w').close()

    uploader.upload(self.existing_bucket, self.test_dir)

    # Both True if commit to s3 was successful, False if not
    result1 = self.check_file_on_s3(self.existing_bucket, self.test_file)
    result2 = self.check_file_on_s3(self.existing_bucket, self.test_file + '2')
    self.assertTrue(result1 and result2)

  def test_modified_file_upload(self):
    uploader.upload(self.existing_bucket, self.test_dir)

    # Check timestamp after original upload
    timestamp_1 = self.check_file_timestamp(self.existing_bucket,
                                            self.test_file)

    # Modify the file locally
    path_to_test_file = os.path.join(self.test_dir, self.test_file)
    local_file = open(path_to_test_file, 'w')
    local_file.write('This file has been modified\n')
    local_file.close()

    uploader.upload(self.existing_bucket, self.test_dir)

    # Check the timestamp after second upload
    timestamp_2 = self.check_file_timestamp(self.existing_bucket,
                                            self.test_file)

    # True if file was modified on s3, False if not
    result = timestamp_2 > timestamp_1
    self.assertTrue(result)

  def test_unmodified_file_upload(self):
    uploader.upload(self.existing_bucket, self.test_dir)

    # Check timestamp after original upload
    timestamp_1 = self.check_file_timestamp(self.existing_bucket,
                                            self.test_file)

    uploader.upload(self.existing_bucket, self.test_dir)

    # Check timestamp after second upload
    timestamp_2 = self.check_file_timestamp(self.existing_bucket,
                                            self.test_file)

    # True if file was not modified on s3, False if it has
    result = timestamp_2 == timestamp_1
    self.assertTrue(result)

  def test_deleted_file_delete(self):
    uploader.upload(self.existing_bucket, self.test_dir)

    # Remove the file locally
    path_to_test_file = os.path.join(self.test_dir, self.test_file)
    os.remove(path_to_test_file)

    # Second upload to remove the file
    uploader.upload(self.existing_bucket, self.test_dir)

    # Get the file info from s3
    bucket = self.connection.get_bucket(self.existing_bucket)
    s3_file = bucket.get_key(self.test_file)

    # Ensure the file is gone from s3 and locally
    self.assertTrue(s3_file is None)
    self.assertFalse(os.path.exists(path_to_test_file))

  def test_upload_via_config(self):
    self.set_config()

    # Upload using config for bucket and directory
    uploader.upload_from_config()

    # True if commit to s3 was successful, False if not
    result = self.check_file_on_s3(self.existing_bucket, self.test_file)
    self.assertTrue(result)

    os.remove(self.config_file)

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

  def set_config(self):
    # Create config
    config = { 'bucket': self.existing_bucket, 'dir': self.test_dir }
    with open(self.config_file, 'w') as outfile:
      json.dump(config, outfile)

  ###

if __name__ == '__main__':
  unittest.main(buffer = True)
