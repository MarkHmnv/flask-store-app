# Store REST API

This is a pet project built with Flask. The Stores REST API allows you to create, update, and delete stores, items, tags, and users. The application is implemented with JWT authentication and all the items and tags are nested within a store.

## Technologies Used

* Python 3.11.5
* Flask
* Flask-JWT-Extended (for JWT-based Authentication)
* Flask-Smorest (for handling routes and views)
* SQLAlchemy (for ORM, all the data are stored in SQLite database)
* Marshmallow (for object serialization/deserialization, validation)
* bcrypt (for password hashing and checking)

## How to Build and Run

To run project execute this docker command:
```bash
docker-compose up --build
````

## API Endpoints

1. User Management
* POST users/register: Registers a new user
* POST users/login: Authenticates a user and returns token
* POST users/refresh: Refreshes access token after user has been authenticated
* POST users/logout: Logs out a user and adds token to blacklist for users that are not logged in
* GET/DELETE users/{id}: Gets a user based on the ID, deleting is permitted only if user is authenticated

2. Store Management
* GET/POST stores: Gets all stores or creates a new store if logged in
* GET/DELETE stores/{id}: Gets or deletes a store based on the ID

3. Item Management
* GET/POST items: Gets all items or creates a new item if logged in
* GET/DELETE/PUT items/{id}: Gets, deletes or updates an item based on the ID

4. Tag Management
* GET/POST stores/{id}/tags: Get all tags of a store or create a new tag if logged in
* GET/DELETE tags/{id}: Gets or deletes a tag based on the ID if there are no items associated with the tag