# Database Search Project - CS483

### Description
A basic server in Python using Jinja to implement a basic web interface for searching specified databases in Whoosh! and MongoDB.


### Install Instructions
The server requires an environment using Python 2.7. The required packages can be installed using:
`make install`

### Running

Copy the file `server/config/.env.template` to be  `server/config/.env`. Add your credentials to the newly created `.env` file.
Now, simply run the application using `make server`. The web interface can now be accessed locally with any browser
at `http://127.0.0.1:5000`.

### Rebuilding the index

To completely rebuild the Whoosh! index, run: `make index`.

### Rebuilding the database

To completely rebuild the database, run: `make db`.

### To Start Over

To install the tools, reubuild the database and index, and start the server when done, run `make all`.


### Files and Folders
* server.py - Main server file
* /templates - html files for user interface
* /static - Static files including style sheets
* README

### Documentation
* [Jinja](http://jinja.pocoo.org/docs/2.9/)
* [Flask](http://flask.pocoo.org/)
