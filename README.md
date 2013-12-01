Bucketeer
========

Syncs a local directory to a bucket in Amazon's S3


Installation
------------

// TODO: Installation instructions

// TODO: Amazon client secret setup

Usage
-----

    python -m bucketeer <bucket-name> <directory-name>

or create a `bucketeer.json` file and add the bucket name and directory name:

    {
      "bucket": "<bucket-name>",
      "directory": "<directory-name>"
    }

then you can just `python -m bucketeer`

_Note: `<` and `>` signify your custom input and shouldn't be included_

If you only specify one argument, Bucketeer will default to using the
`bucketeer.json` config file. If it doesn't exist or is missing values,
Bucketeer will let you know what is needed.


License
-------
[MIT License](LICENSE.md)
