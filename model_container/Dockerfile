FROM tensorflow/tensorflow:latest

# Update package list and install nginx

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    nginx \
    && rm -fr /var/lib/apt/lists/*

# Install required pip packages. clear pip cache which leaves the install caches populated using a significant amount of space.
RUN pip install flask gunicorn gevent pandas numpy \
    && rm -rf /root/.cache 

     
# PYTHONUNBUFFERED keeps Python from buffering our standard output stream, which means that logs can be delivered to the user quickly. 
# PYTHONDONTWRITEBYTECODE keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

#Copy the serving files on this notebook instance to an existing locaiton on the container
COPY model_src /opt/program
WORKDIR /opt/program
