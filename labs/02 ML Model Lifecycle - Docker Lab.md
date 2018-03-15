# 02 ML Immersion Day – Docker Lab

## Prerequisites:
-   Docker daemon and CLI installed
-   AWS CLI installed

## Objectives:

This lab will introduce you to the packaging of a Python-based machine
learning model using Docker for use with SageMaker. You will build a
Docker image using provided source code, test the image locally, and
then publish the image to ECR for use with later labs.

## Steps:
1.  From the command line interface change into the `model_container` directory of the `sagemaker_model_lifecycle` project.  Performing a directory listing should look similar to the following:
```bash
├── Dockerfile
├── build_and_push.sh
├── local_test
│   ├── payload-labels.csv
│   ├── payload.csv
│   ├── predict.sh
│   ├── serve_local.sh
│   ├── test_dir
│   │   ├── input
│   │   │   ├── config
│   │   │   │   ├── hyperparameters.json
│   │   │   │   └── resourceConfig.json
│   │   │   └── data
│   │   │       └── train
│   │   │           ├── test_data.csv
│   │   │           └── train_data.csv
│   │   ├── model
│   │   └── output
│   └── train_local.sh
└── model_src
    ├── nginx.conf
    ├── predictor.py
    ├── serve
    ├── train
    └── wsgi.py
```
2.  Inspect the contents of the Dockerfile to understand its instructions and how it will build your image. For more information about Dockerfile syntax visit Docker’s [documentation](https://docs.docker.com/engine/reference/builder/).
```bash
$ cat Dockerfile
```

3. Execute `docker build` to build your Docker image from the `Dockerfile`
```bash
$ docker build . -t sagemaker_model:v1
```

4.  If you now execute `docker images` you should see your `sagemaker_model:v1` listed in the results.

1. Take a look at at the `hyperparameters.json` file in `local_test/test_dir/input/config` to examine the parameter values that  will be used during training. It includes information around where to find training data and test data as well as how many epochs to run during training.
```bash    
$ cat local_test/test_dir/input/config/hyperparameters.json
```

6.  Lets now test the docker-ized model to ensure it will train and
    serve results effectively. Change directory into the `local_test`
    directory and execute `train_local.sh`.
```bash
$ cd local_test
$ ./train_local sagemaker_model:v1
```

7.  The `train_local.sh` script will run your Docker container in the same way as SageMaker would, mapping the test\_dir sub-directories to `/opt/ml` within your container. Your model then reads these inputs, trains on the training data, and produces an output model that can be used on later invocations of the container. After training a model export file should reside in `test_dir/model`.

1.  With your model trained, now host the model for execution and ensure
    that it makes accurate predictions. Open a second terminal and from
    the `local_test` directory execute `serve_local.sh` to host the model
    as SageMaker would.
```bash
$ ./serve_local.sh sagemaker_model:v1
```

9.  From the first terminal execute `predict.sh` and observe the
    results.  For comparison the labels for all 4 samples are in `payload-labels.csv`.
```bash
$ ./predict.sh payload.csv
$ cat payload-labels.csv
```

10. If the model is performing as expected push the model to ECR for
    later use with SageMaker. Inspect the contents of
    `build_and_push.sh` to understand how it authenticates the Docker
    CLI with ECR before pushing your container into its own ECR
    repository.

1. Now push the container image to ECR using the `build_and_push.sh`
    script.  The script will create an EC2 Container Registry repository and push your image to the repository.  It will print the output repository to the screen (for example `776347499999.dkr.ecr.eu-west-1.amazonaws.com/sagemaker_model`).
```bash
$ ./build_and_push.sh sagemaker_model:v1
```