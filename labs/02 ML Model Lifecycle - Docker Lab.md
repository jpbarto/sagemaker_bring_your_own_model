**02 ML Immersion Day – Docker Lab**

**Prerequisites:**

-   Docker daemon and CLI installed

-   AWS CLI installed

**Objectives:**

This lab will introduce you to the packaging of a Python-based machine
learning model using Docker for use with SageMaker. You will build a
Docker image using provided source code, test the image locally, and
then publish the image to ECR for use with later labs.

**Steps:**

1.  Download the image source code associated with this lab

2.  From a command line interface perform a directory listing which
    should look similar to the following:

3.  Inspect the contents of the Dockerfile to understand its
    instructions and how it will build your image. For more information
    about Dockerfile syntax visit Docker’s
    [documentation](https://docs.docker.com/engine/reference/builder/).

    cat Dockerfile

4.  Execute \`docker build\` to build your Docker image

    docker build . -t sagemaker\_model:v1

5.  If you now execute \`docker images\` you should see your
    sagemaker\_model:v1 listed in the results.

6.  Lets now test the docker-ized model to ensure it will train and
    serve results effectively. Change directory into the \`local\_test\`
    directory and execute \`train\_local.sh\`.

7.  The script will run your Docker container using in the same way as
    SageMaker would, mapping the test\_dir sub-directories to ‘/opt/ml’
    within your container. Your model then reads these inputs, trains on
    the training data, and produces an output model that can be used on
    later invocations of the container. After training a model.pkl file
    should reside in ‘test\_dir/model’.

8.  With your model trained, now host the model for execution and ensure
    that it makes accurate predictions. Open a second terminal and from
    the test\_dir directory execute ‘serve\_local.sh’ to host the model
    as SageMaker would.

9.  From the first terminal execute ‘predict.sh’ and observe the
    results.

10. If the model is performing as expected push the model to ECR for
    later use with SageMaker. Inspect the contents of
    ‘build\_and\_push.sh’ to understand how it authenticates the Docker
    CLI with ECR before pushing your container into its own ECR
    repository.

11. Now push the container image to ECR using the ‘build\_and\_push.sh’
    script.
