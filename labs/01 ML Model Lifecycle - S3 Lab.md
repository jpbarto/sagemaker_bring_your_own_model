01 ML Immersion Day – S3 Lab

Prerequisites:

-   AWS CLI Installed

-   Web browser with AWS console access

Overview:

This lab will walk you through creating a version controlled, encrypted
bucket for hosting S3 objects. You will then upload, using the AWS CLI,
multiple versions of a file to S3 to observe how S3 manages your data.

Follow-on conversation could focus on logging of S3 activity to audit
who has added data, changed data, or deleted data. This could also be
combined with an IAM discussion to illustrate how access to the S3
objects could be controlled.

Steps:

1.  Open a command terminal and from the command prompt use the AWS CLI
    to create a KMS key for encryption of your S3 bucket objects.

2.  Sign into your AWS account using the web-based AWS console.

3.  From the ‘Services’ menu select ‘S3’ under ‘Storage’.

4.  The console should display a list of all S3 buckets which currently
    exist in your account. Create a new bucket by clicking the ‘Create
    bucket’ button.

5.  For ‘Bucket name’ enter a unique bucket name such as
    ‘ml-immersion-day-YOUR\_SURNAME’

6.  For ‘Region’ select a EU (Ireland) and click ‘Next’

7.  Click the ‘Versioning’ options block and select the ‘Enable
    versioning’ radio button. Click ‘Save’.

8.  Click the ‘Default encryption’ options block and select the
    ‘AWS-KMS’ radio button. Select the previously created KMS key to be
    used to for encryption. Click ‘Save’.

9.  Click ‘Next’ to complete the setting of bucket properties.

10. Leave the permissions set to the defaults and click ‘Next’ to review
    your bucket configuration.

11. Click ‘Create bucket’.

12. Back in your command prompt change directory to the directory
    containing the data file associated with this lab.

13. Upload an initial version of the data using the AWS CLI:

14. Now upload an alternative version of the data set using the same
    command but using the ‘iris\_version\_2.csv’ data file.

15. To see the versions for the object in S3 use the following command:

    aws s3api list-object-versions --bucket
    jasbarto-ml-immersion-day-dev

16. Retrieve the latest revision of the data using the following
    command:

17. Now retrieve the earlier version using the version ID listed earlier
    using the same get-object command but with the ‘—version-id’
    parameter to specify.

18.
