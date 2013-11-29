Bucketeer
========

Syncs a local directory to a bucket in Amazon's S3


Usage
-----

    python -m bucketeer <bucket-name> <directory-name>

or create a `bucketeer.json` file and add the bucket name and directory name:

    {
      "bucket": "<bucket-name>",
      "directory": "<directory-name>"
    }

then you can just `python -m bucketeer`

If you only specify one argument, Bucketeer will default to using the
`bucketeer.json`

_Note: `<` and `>` signify your custom input and shouldn't be included_

License
-------
[MIT License](LICENSE.md)
