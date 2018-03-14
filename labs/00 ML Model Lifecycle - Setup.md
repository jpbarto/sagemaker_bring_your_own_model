ML Model Lifecycle Immersion Day – Setup

Overview

The following steps walk a user through creating a SageMaker notebook
instance for use with the ML Model Lifecycle Immersion Day lab
materials.

Steps:

1.  Sign into the AWS console and open the Amazon SageMaker console

2.  From the SageMaker dashboard click ‘Create notebook instance’

3.  Give the instance a name and for ‘Notebook instance type’ select
    ‘ml.m4.xlarge’ from the drop down menu

4.  For IAM role click ‘Create a new role’ from the drop down menu

5.  For ‘S3 buckets you specify’ select ‘Any S3 bucket’ and click
    ‘Create role’

6.  Click the resulting link for the newly created EC2 instance role

7.  On the IAM console for the Role, on the ‘Permissions’ tab click
    ‘Attach policy’

8.  Search for the managed policy ‘AmazonEC2ContainerRegistryPowerUser’
    and select the checkbox next to the policy and click ‘Attach policy’

9.  Return to the SageMaker console and accept the remaining defaults by
    clicking ‘Create notebook instance’

10. After approximately 5 minutes the notebook instance should
    transition from the ‘Pending’ status to ‘InService’

11. Click ‘Open’ to launch the Notebook instance’s Jupyter interface

12. On the upper right-hand side of the Jupyter notebook interface click
    ‘New’ -&gt; ‘Terminal’ to obtain shell level access to the instance

13. From the command line ‘cd’ into the ‘SageMaker’ directory and clone
    the Git repository associated with this lab:

cd SageMaker

git clone <https://github.com/jpbarto/sagemaker_model_lifecycle.git>

cd sagemaker\_model\_lifecycle

1.  You are now ready to begin lab 01
