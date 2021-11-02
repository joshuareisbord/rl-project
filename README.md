# rl-rpoject

## Docker Setup
This will be fixed later and will be run with a docker compose file.
I am also using the docker cli so this may be different if you use docker desktop.

### Install docker 
[Docker getting started.](https://www.docker.com/get-started)

### Docker login
Run `docker login` or `sudo docker login` and enter your account credentials.

### Download the base python image
https://hub.docker.com/_/python
Run `docker pull python` or `sudo docker pull python`
[See more here.](https://hub.docker.com/_/python)

### Create a docker container with the downloaded image
Run `docker create --name ${name of container} python` or `sudo docker create --name ${name of container} python`
The name does not matter it only exists on your machine.

### Build the container
Run `docker build -t ${name of container} .` or `sudo docker build -t ${name of container} .`
Will get a pip warning and a venv warning for now.

### Run the container
Run `docker run -it ${name of container}` or `sudo docker run -it ${name of container}`
The -it flag is used to run the container in a shell so you can see the output.

