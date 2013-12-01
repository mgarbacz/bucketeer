import boto, os, hashlib, json

# Upload modified files in src_directory to the given s3 bucket
def upload(bucket_name, src_directory):
  success = False

  if not (bucket_name and src_directory):
    try:
      config = json.loads(open('bucketeer.json').read())
      print 'Configuration file found.'
      bucket_name = config['bucket']
      src_directory = config['directory']
    except IOError:
      print 'Configuration file not found. Nothing to do...'
      return
    except KeyError as e:
      print 'Configuration file incorrect. Missing:', e
      return

  print 'Attempting to upload %s to %s' % (src_directory, bucket_name)
  try:
    # Requires S3 creds, which are set as environment variables
    connection = boto.connect_s3();
    bucket = connection.lookup(bucket_name)

    if bucket == None:
      # Create the bucket if we don't have it
      print 'Bucket %s not found. Creating...' % bucket_name
      bucket = connection.create_bucket(bucket_name)
      print 'Bucket %s created.' % bucket_name

    delete_files(src_directory, bucket)

    # Iterating over all files in the src folder
    for directory, subdirectories, files in os.walk(src_directory):

      # Upload each local file in files
      for filename in files:
        upload_file(filename, directory, src_directory, bucket)

    # If we got here with no exceptions, changes have been committed
    success = True

  # Boto provides little in the way of exception handling, need a blanket
  except Exception, e:
    print e

  if success:
    print 'Changes uploaded.'
  else:
    print 'Changes not uploaded.'

  return success

def upload_file(filename, directory, src_directory, bucket):
  # Set up file paths and get s3 file
  local_file_path = os.path.join(directory, filename)
  # For s3, we don't want the 'public' part of file path
  s3_file_path = local_file_path[len(src_directory)+1:]
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
    print  '%s is uploading...' % filename
    key_file = boto.s3.key.Key(bucket)
    key_file.key = s3_file_path
    key_file.set_contents_from_filename(local_file_path)
    key_file.make_public()

  # Will print after update or if no update was required
  print '%s is up to date.' % filename

def delete_files(src_directory, bucket):
  # Delete each s3 file not present locally
  for s3_file in bucket.list():
    try:
      with open(os.path.join(src_directory, s3_file.key)):
        print '%s exists locally.' % s3_file.key
    except IOError:
      print '%s is being deleted from s3...' % s3_file.key
      bucket.delete_key(s3_file.key)
      print '%s has been deleted from s3.' % s3_file.key

