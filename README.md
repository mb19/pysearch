# Database Search Project - CS483

### Description
A basic server in Python using Jinja to implement a basic web interface for searching specified databases in Whoosh! and MongoDB.


### Install Instructions
The server requires an environment using Python 2.7. The required packages can be installed using:
`make install`.

### Running

Make sure you have ran `make install` at least once on your machine. Make a copy of the `server/config/.env.template` and place it in the same directory with the name `.env`. Now, add your credentials to the `server/config/.env` file.

Now, simply run the application using `make server`. The web interface can now be accessed locally with any browser
at `http://127.0.0.1:5000`.

### Rebuilding the index

To completely rebuild the Whoosh! index, run: `make index`.

### Rebuilding the database

To completely rebuild the database, run: `make db`.

### To Start Over

To install the tools, reubuild the database and index, and start the server when done, run `make all`.

### Advanced 
The current version of the application can be found [here](http://docker-lb.trafficmanager.net/). 

The website is deployed to Azure using a Docker container built with the Dockerfile included in this
repository. For fun, this application is hosted on two separate virtual machines using Docker (in swarm mode) 
and an Azure load balancer.

To run the application locally using Docker, run the following command:
```
docker run --rm sonoilmedioco/pysearch:v4
```

The public Docker Hub repo can be found [here](https://hub.docker.com/r/sonoilmedico/pysearch/).
