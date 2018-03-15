# ML Model Lifecycle Immersion Day – Setup

## Overview

The following steps walk a user through creating a SageMaker notebook
instance for use with the ML Model Lifecycle Immersion Day lab
materials.

## Steps:

1.  Sign into the AWS console and open the Amazon SageMaker console
1.  From the SageMaker dashboard click `Create notebook instance`
1.  Give the instance a name and for **Notebook instance type** select
    `ml.m4.xlarge` from the drop down menu
1.  For IAM role click `Create a new role` from the drop down menu
1.  For **S3 buckets you specify** select `Any S3 bucket` and click
    `Create role`
1.  Click the resulting link for the newly created EC2 instance role
1.  On the IAM console for the Role, on the **Permissions** tab click
    `Add inline policy`
1. For **Service** enter `EC2 Container Registry`
1. For **Actions** click `All EC2 Container Registry actions`
1. For **Resources** click `All resources`
1. Click `Add additional permissions`
1. For **Service** enter `KMS`
1. For **Action** click `All KMS actions`
1. For **Resources** click `All resources`
1. Click `Review policy`
1. Give the new policy a name and click `Create policy`
1.  Return to the SageMaker console and accept the remaining defaults by
    clicking `Create notebook instance`
1. After approximately 5 minutes the notebook instance should
    transition from the `Pending` status to `InService`
1. Click `Open` to launch the Notebook instance’s Jupyter interface
1. On the upper right-hand side of the Jupyter notebook interface click
    `New` -&gt; `Terminal` to obtain shell level access to the instance
1. From the command line `cd` into the `SageMaker` directory and clone
    the Git repository associated with this lab:

```bash
$ cd SageMaker
$ git clone https://github.com/jpbarto/sagemaker_model_lifecycle.git
$ cd sagemaker_model_lifecycle
```

22.  You are now ready to begin lab 01