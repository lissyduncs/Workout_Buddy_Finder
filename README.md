# R1

Staying committed to your fitness goals can be a a challenge, especially when you’re having to work out solo. Working out with a partner makes people more accountable to show up consistently for their training session as they’re held accountable when they have to meet up with someone, however many people struggle to find a workout partner that has a similar interest in workout preference as well as matching locations, schedules and fitness levels. This can be a challenge for people who might have moved to a new area or don’t have an established network 
The Workout Buddy Finder allows users to input their workout preferences, geographical location, fitness level and time preference in order to match and connect with other users that have compatible preferences. The app allows users to browse workout sessions created by other users and request to join one. Once users are connected, they can communicate directly through the messaging function which helps coordinate workout plans and form friendships.

# R2

At the beginning of the project, the tasks were broken down into more specific and manageable tasks which were each feature of functionality and were assigned it’s own card on a Trello board. For example, creating user authentication or designing the workout session model. These cards were organised into lists like ‘To Do,’ ‘In Progress,’ and ‘Completed.’ Labels were added to each card to specify task types such as Database Setup or Testing. To make sure that each task was easy to identify.
During the project, tasks were moved from one list to another as they became ‘In Progress’ or ‘Completed’ so that it was easy to see the current status of each task.
Each task had checklists for sub tasks.
I used Trello throughout this project to organise everything and track progress and changes along the way and I moved each card from ‘To Do’ to finally ‘Completed’ once successfully done.
Using Trello was important to be able to lay all the tasks out and have clarity over what needed to be prioritised first and then break it down into sections to focus in at each time.

# R3

Flask is the framework to create the API, which is essential for routing HTTP requests and managing interactions between the client and server and provides the functionality of handling requests and responses in the API, which includes routing different endpoints

SQLAlchemy for database interactions. This simplifies the way to interact with the relational database (PostgreSQL) by mapping Python objects to database tables and also handling CRUD operations for entities.

Flask-JWT-Extended is an authentication package for handling JWT and it’s used to generate and verify access tokens during the user login as well as routes that require authentication.

Bcrypt is a security measure used for hashing passwords during registration and then compare them during login for verification

PostgreSQL is the relational database management system that stores structured data and and retrieves the data and is manipulated by SQLAlchemy in the app.

Psycopg2 is used to enable Python and Flask to be able to communicate with the PostgreSQL database.

Marshmallow schemas are used for serialization/deserialization the data that’s passed through the API endpoints.

Flask-Migrate helped apply the changes to the database schema in a controlled way during development.

# R4

The underlying database system for the Workout Buddy Finder is PostgreSQL, which is an excellent choice because of its scalability and being robust
Some benefits include:
- ACID compliance which ensures reliable operations and makes sure the data stays consistent, even in the case of failures
- It's compatible with SQLAlchemy ORM which makes the interaction with the database efficient through Python models
- It's highly scalable which makes it suitable for apps with growing user bases
- It can be easily expanded with add-ons to include more advanced features

Drawbacks:
- PostgreSQL requires more complex setup than other simpler databases
- It can be more resource-heavy in terms of CPU and memory, especially for small projects

# R5

The ORM system that’s used in this app is SQLAlchemy which connects Python code and the PostgreSQL database
Features:
- SQLAlchemy lets developers work with with database tables as if they are working with regular Python objects, which the code easier to understand and work with. Instead of writing complex SQL queries, SQLAlchemy actually simplifies these into more basic Python code, which also makes the process more manageable. It also manages relationships between tables efficiently without needing complex SQL, so makes managing and working with the database easier and more efficient which helps the app handle data in a simpler way.
Purpose:
- The purpose of SQLAlchemy is to make it easy to work with the database without needing to write complicated SQL, which speeds up development and makes the code easier to manage
Functionalities:
- SQLAlchemy has several simple functionalities. It turns Python objects into database tables (and back), so data is easy to store as well as retrieve. It also makes querying the database easier because there are built-in tools for filtering and modifying data. It also manages processes automatically, which makes sure changes are saved correctly or undone if there’s an error which all make working with the database faster and simpler.

# R6

The ERD for the Workout Buddy Finder is designed to ensure that that each piece of data is stored only once to avoid redundancy. For example in User and Workout Sessions, one user can be linked to many workout sessions and by storing user data separately, we only keep it once and refer to it using foreign keys. 
Without this 3NF normalisation, we might end up repeating the user’s details in every session, which wastes space and makes updating harder. In the same way, requests are stored in their own table, which means we don’t have to duplicate session information when users request to join multiple sessions. This way, each session only exists once. See attachment in docs for ERD.

# R7

These relationships help ensure that the database is organised and prevents repeating the same information in multiple places. By keeping the user’s information in one place and linking to other tables, the system stays efficient as well as scalable, which helps make it easier to handle updates and changes as the app grows.
The relationships help make data searches and management more simple because everything is connected and easy to find.