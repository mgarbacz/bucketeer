Bucketeer
========

Syncs a local directory to a bucket in Amazon's S3


Usage
-----

`python bucketeer/main.py '<bucket-name>' '<directory-name>'`

or create a `config.json` file and add the bucket name and directory name:

    {
      "bucket": "<bucket-name>",
      "dir": "<directory-name>"
    }

then you can just `python bucketeer/main.py`

Note: brackets (< >) signify your custom input and shouldn't be included

License
-------
[MIT License](LICENSE.md)
