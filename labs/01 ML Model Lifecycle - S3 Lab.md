# 01 ML Immersion Day – S3 Lab

## Prerequisites:

-   AWS CLI Installed
-   Web browser with AWS console access

## Overview:

This lab will walk you through creating a version controlled, encrypted
bucket for hosting S3 objects. You will then upload, using the AWS CLI,
multiple versions of a file to S3 to observe how S3 manages your data.

Follow-on conversation could focus on logging of S3 activity to audit
who has added data, changed data, or deleted data. This could also be
combined with an IAM discussion to illustrate how access to the S3
objects could be controlled.

## Steps:

1.  From a command prompt use the AWS CLI to create a KMS key for encryption of your S3 bucket objects.  Make a note of the Arn and KeyID for the newly created key.
```bash
$ aws kms create-key --description 'S3 ML encryption key'
```

2.  Sign into your AWS account using the web-based AWS console.
3.  From the `Services` menu select `S3` under **Storage**.
4.  The console should display a list of all S3 buckets which currently
    exist in your account. Create a new bucket by clicking the `Create
    bucket` button.
5.  For **Bucket name** enter a unique bucket name such as
    `ml-lifecycle-day-YOUR-SURNAME`
6.  For **Region** select `EU (Ireland)` and click `Next`.
7.  Click the **Versioning** options block and select the `Enable versioning` radio button. Click `Save`.
8.  Click the **Default encryption** options block and select the
    `AWS-KMS` radio button. In the key dropdown find your KMS key by its ARN and select it. Click `Save`.
9.  Click `Next` to complete the setting of bucket properties.
10. Leave the permissions set to the defaults and click `Next` to review
    your bucket configuration.
11. Click `Create bucket`.
12. Back in your command prompt change directory to the directory
    containing the data file associated with this lab.
```bash
$ cd ~/SageMaker/sagemaker_model_lifecycle/model_data
```
13. Upload an initial version of the training data using the AWS CLI:
```bash
$ aws s3api put-object --bucket YOUR-BUCKET-NAME --key 'train/train_data.csv' --body train_data.csv
$ aws s3api put-object --bucket YOUR-BUCKET-NAME --key 'train/test_data.csv' --body test_data.csv
```
14. Now shuffle the records in the training data and upload an alternative version of the data set using the same command but using the shuffled data file.
```bash
$ shuf train_data.csv > train_data_shuffle.csv
$ aws s3api put-object --bucket YOUR-BUCKET-NAME --key 'train/train_data.csv' --body train_data_shuffle.csv
```

15. To see the versions for the object in S3 use the following command:
```bash
$ aws s3api list-object-versions --bucket YOUR-BUCKET-NAME --prefix 'train/train_data.csv'
```

16. Retrieve the latest revision of the data using the following
    command:
```bash
$ aws s3api get-object --bucket YOUR-BUCKET-NAME --key 'train/train_data.csv' s3_new_train_data.csv
```

17. Now retrieve the earlier version using the version ID listed earlier
    using the same get-object command but with the ‘—version-id’
    parameter to specify.
```bash
$ aws s3api get-object --bucket YOUR-BUCKET-NAME --key '/train/train_data.csv' --version-id OLDER-VERSION-ID s3_old_train_data.csv
```
