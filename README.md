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