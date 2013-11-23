import boto, os, hashlib, json

# Upload modified files with bucket and directory specified in config.json
def upload_from_config():
  config = json.loads(open('config.json').read())

  upload(config['bucket'], config['dir'])

# Upload modified files in src_folder to the s3 bucket named
def upload(bucket_name, src_folder):
  success = False

  try:
    # Requires S3 creds, which are set as environment variables
    connection = boto.connect_s3();
    bucket = connection.lookup(bucket_name)

    if bucket == None:
      # Create the bucket if we don't have it
      print 'Bucket ' + bucket_name + ' not found. Creating...'
      bucket = connection.create_bucket(bucket_name)
      print 'Bucket ' + bucket_name + ' created.'

    # Iterating over all files in the src folder
    for directory, subdirectories, files in os.walk(src_folder):

      # Delete each s3 file not present locally
      for s3_file in bucket.list():
        if s3_file.key not in files:
          print s3_file.key + ' is being deleted from s3...'
          bucket.delete_key(s3_file.key)
          print s3_file.key + ' has been deleted from s3.'

      # Upload each local file in files
      for filename in files:
        upload_file(filename, directory, src_folder, bucket)

    # If we got here with no exceptions, changes have been committed
    success = True

  # Boto provides little in the way of exception handling, need a blanket
  except Exception, e:
    print e

  if success:
    print('Changes committed')
  else:
    print('Changes not committed')

  return success

def upload_file(filename, directory, src_folder, bucket):
  # Set up file paths and get s3 file
  local_file_path = os.path.join(directory, filename)
  # For s3, we don't want the 'public' part of file path
  s3_file_path = local_file_path[len(src_folder)+1:]
  s3_file = bucket.get_key(s3_file_path)

  # If file exists: compare hashes, else: force unmatching hashes
  if s3_file != None:
    # s3 surround hash with quotes, so we need to include them
    local_hash = '\"%s\"' % (
      hashlib.md5(open(local_file_path, 'rb').read()).hexdigest() )
    s3_hash = s3_file.etag
  else:
    local_hash = 0
    s3_hash = 1

  # If the hashes are different, we need to upload the file
  if local_hash != s3_hash:
    print filename + ' is uploading...'
    key_file = boto.s3.key.Key(bucket)
    key_file.key = s3_file_path
    key_file.set_contents_from_filename(local_file_path)
    key_file.make_public()

  # Will print after update or if no update was required
  print filename + ' is up to date.'
