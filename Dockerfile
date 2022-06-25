# For more information, please refer to https://aka.ms/vscode-docker-python
#FROM --platform=linux/arm64
#FROM scratch
#ADD ubuntu-focal-oci-amd64-root.tar.gz /
#CMD ["bash"]
#FROM --platform=arm64 ubuntu

FROM scratch
ADD ubuntu-jammy-oci-arm64-root.tar.gz /
CMD ["bash"]

FROM python:3.9-slim


# Warning: A port below 1024 has been exposed. This requires the image to run as a root user which is not a best practice.
# For more information, please refer to https://aka.ms/vscode-docker-python-user-rights`
EXPOSE 90

#RUN ping google.com
#RUN apt-get install build-base
RUN /usr/local/bin/python -m pip install --upgrade pip

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1 

RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev python-dev && rm -rf /var/lib/apt/lists/*

#RUN apt-get install
#RUN apt-get install 

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:80", "main:app"]

