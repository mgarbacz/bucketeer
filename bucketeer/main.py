import boto, os, time

def print_result(subject, action, success):
  modifier = ' not '
  if success == True:
    modifier = ' '
  print subject + modifier + action + '.'

# We want to commit all modified files to the s3 bucket for the site
def commit_to_s3(bucket_name, src_folder):
  success = False

  try:
    # Requires S3 creds, which I set as environment variables
    connection = boto.connect_s3();
    bucket = connection.lookup(bucket_name)

    if bucket == None:
      # Create the bucket if we don't have it
      print 'Bucket ' + bucket_name + ' not found. Creating...'
      bucket = connection.create_bucket(bucket_name)
      print 'Bucket ' + bucket_name + ' created.'
    else:
      # Iterating over all files in the web-content folder
      for directory, subdirectories, files in os.walk(src_folder):
        for filename in files:
          # We want the path to get each file
          local_file_path = os.path.join(directory, filename)
          # For s3, we don't want the 'public' part of file path
          s3_file_path = local_file_path[len(src_folder)+1:]

          remote_file = bucket.get_key(s3_file_path)

          print filename + ' is uploading...'
          key_file = boto.s3.key.Key(bucket)
          key_file.key = s3_file_path
          key_file.set_contents_from_filename(local_file_path)
          key_file.make_public()

          # Will print after update or if no update was required
          print filename + ' is up to date.'

    # If we got here with no exceptions, changes have been committed
    success = True

  # Boto provides little in the way of exception handling, need a blanket
  except Exception, e:
    print e

  return print_result('Changes', 'committed', success)
