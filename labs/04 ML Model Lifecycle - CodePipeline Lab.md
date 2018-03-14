03 ML Immersion Day – CodePipeline Lab

Summary:

In this lab you will create a CodeCommit repo for your model, build a
CodePipeline hosted pipeline to monitor the repository, and use
CodeBuild to create a Docker image from your repository before sending
it to Amazon SageMaker for training.

Objectives:

1.  Create a CodeCommit repository and check in your model source code

2.  Create a CodePipeline repository to automate deployment of your
    model

3.  Create a CodeBuild project to build the Docker container

Prerequisites:

-   AWS CLI

-   Access to AWS Web Console

-   Amazon ECR repository created

-   Amazon S3 bucket with training data

-   Git command installed

Steps:

Create a CodeCommit repository

1.  Access the AWS CodeCommit management console, click ‘Get Started’

2.  Enter a name for the repository and click ‘Create repository’

3.  Click ‘Skip’ for configuring email notifications

4.  After the repository has been created follow the instructions to
    access your repository from the command line

> git config --global credential.helper '!aws codecommit
> credential-helper \$@'
>
> git config --global credential.UseHttpPath true
>
> git clone
> https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/MyModelRepo

1.  Copy the source files from your model directory created earlier and
    commit the repository, pushing it back to CodeCommit

    git add \*

    git commit -am ‘initial commit’

    git push

2.  Refresh the repository console in your web browser to see your files
    commited to the repository.

> Create a CodePipeline project

1.  Open the CodePipeline console via the AWS console and click ‘Get
    started’

2.  Enter a pipeline name and click ‘Next’

3.  For Source Provider select ‘AWS CodeCommit’

4.  Click the drop down for Repository name and select the repository
    created in the previous steps.

5.  Select ‘master’ for the Branch name

6.  For Change detection accept the default of CloudWatch Events and
    click ‘Next step’

    **Note**: for using other repositories and how to integrate them
    with CodePipeline please see this quickstart:
    <https://aws.amazon.com/quickstart/architecture/git-to-s3-using-webhooks/>

7.  For Build provider select ‘AWS CodeBuild’ and click ‘Create a new
    build project’

8.  Give the build project a name

9.  Use the default managed CodeBuild environment and from the Operating
    System drop down select ‘Ubuntu’

10. Select ‘Docker’ for the runtime and the first version of the runtime
    from the Version drop down

11. Leave the remaining values at their defaults and click ‘Save build
    project’

12. After the build project has been created click ‘Next step’

13. Under ‘Deployment provider’ select ‘No deployment’ and click ‘Next
    step’

14. Enter a role name for your Pipeline to execute as and click ‘Create
    role’

15. In the pop-up window review the IAM policy recommended to be used
    and click ‘Allow’

16. From the Pipeline console click ‘Next step’

17. On the summary page click ‘Create pipeline’

18. The build file in your project (‘buildspec.yml’) will use the ECR
    commands and so will need permissions to invoke the ECR API. Grant
    your build project permissions to communicate with ECR by open the
    AWS CodeBuild web console.

19. Click on the Build project you created in the previous step and
    expand Project details

20. Note the service role name that has been created for your build
    project. Next access the IAM web console.

21. Click ‘Roles’ on the left hand side of the console and enter in the
    first few letters of your service role name.

22. Click on the ‘Role’ for your build project to access its details.

23. On the Permissions tab for the service role you should see a single
    policy. This policy grants your CodeBuild project permissions to
    access things like S3. Click ‘Add Inline policy’ to grant the
    additional permissions needed.

24. For Service enter ‘EC2 Container Registry’

25. Under Access level expand Read and check ‘GetAuthorizationToken’,
    ‘BatchGetImage’, ‘GetDownloadUrlForLayer’, and
    ‘BatchCheckLayerAvailability’

26. Under Access level expand Write and check ‘CompleteLayerUpload’,
    ‘InitiateLayerUpload’, ‘PutImage’, and ‘UploadLayerPart’

27. For Resources click ‘Specific’ and click ‘Add ARN’, copy and paste
    from the ECR console the ARN of the repository created earlier.

28. Click ‘Review policy’

29. Name the policy ‘ECRAccessPolicy’ and click ‘Create policy’
