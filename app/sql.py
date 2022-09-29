from boto.s3.connection import S3Connection
import os

s3 = S3Connection(os.environ['DATABASE_URL'])