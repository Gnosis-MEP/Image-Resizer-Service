# Image Resizer Service
This is a general image resizer service. Uses a default resizing method or cloudseg as alternative.
Implementation of the CloudSeg component for re-creating a HD image from a lowres one.

**ps**: Using Cloudseg as a service in the CE domain, just to simplify its use on the framework.
it should actually be added in the dataflow before the scheduling because
it seems to belong more to the business domain of stream management rather than the content extraction domain
but again, just to simplify running this evaluation...

# Commands Stream
## Inputs
...

## Outputs
...

# Data Stream
## inputs
...

## Outputs
...

# Installation

## Configure .env
Copy the `example.env` file to `.env`, and inside it replace `SIT_PYPI_USER` and `SIT_PYPI_PASS` with the correct information.

## Installing Dependencies

### Using pip
Install first the `requirements-torch.txt`:
```
$ pip install -r requirements-torch.txt
```

Then install the rest:
```
$ pip install  -r requirements.txt
```

# Running
Enter project python environment (virtualenv or conda environment)

**ps**: It's required to have the .env variables loaded into the shell so that the project can run properly. An easy way of doing this is using `pipenv shell` to start the python environment with the `.env` file loaded or using the `source load_env.sh` command inside your preferable python environment (eg: conda).

Then, run the service with:
```
$ ./image_resizer_service/run.py
```

# Testing
Run the script `run_tests.sh`, it will run all tests defined in the **tests** directory.

Also, there's a python script at `./image_resizer_service/send_msgs_test.py` to do some simple manual testing, by sending msgs to the service stream key. This will send the low resolution example image.


# Docker
## Manual Build (not recommended)
Build the docker image using: `docker-compose build`

**ps**: It's required to have the .env variables loaded into the shell so that the container can build properly. An easy way of doing this is using `pipenv shell` to start the python environment with the `.env` file loaded or using the `source load_env.sh` command inside your preferable python environment (eg: conda).

## Run
Use `docker-compose run --rm service` to run the docker image


## Gitlab CI auto-build and tests

This is automatically enabled for this project (using the `.gitlab-ci.yml` present in this project root folder).

By default it will build the Dockerfile with every commit sent to the origin repository and tag it as 'dev'.

Afterwards, it will use this newly builty image to run the tests using the `./run_tests.sh` script.

But in order to make the automatic docker image build work, you'll need to set the `SIT_PYPI_USER` and `SIT_PYPI_PASS` variables in the Gitlab CI setting page: [Image Resizer Service CI Setting Page](https://gitlab.insight-centre.org/sit/mps/image-resizer-service/settings/ci_cd). (Or make sure the project is set under a Gitlab group that has this setup for all projects in that group).

And, in order to make the automatic tests work, you should also set the rest of the environement variables required by your service, in the this projects `.gitlab-ci.yml` file, in the `variables` section. But don't add sensitive information to this file, such as passwords, this should be set through the Gitlab CI settings page, just like the `SIT_PYPI_USER`.

## Benchmark Tests
To run the benchmark tests one needs to manually start the Benchmark stage in the CI pipeline, it shoud be enabled after the tests stage is done. Only by passing the benchmark tests shoud the image be tagged with 'latest', to show that it is a stable docker image.