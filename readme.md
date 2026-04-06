Hey there! This is a little web app I put together to learn about user authentication and building full-stack applications. It's called a CRUD authentication app, but really it's just a simple system where people can create accounts, log in, and delete account with full CRUD operations.

I built it using Flask because I wanted something lightweight that wouldn't complicate things, and SQLite for the database since it's perfect for small projects like this. The whole authentication thing uses sessions and password hashing so it's actually secure - no storing passwords in plain text here! The authentication system itself implements CRUD operations for user account management.

When users sign up, they get a unique username and their password gets properly hashed. Then they can log in and see their personal dashboard with a friendly "Hello [their name]" message.  There's also this account detection feature where you can check if a username exists, and even delete accounts if needed, which handles the delete part of CRUD for user accounts.

The frontend is super basic - just HTML and CSS - but it gets the job done. I organized everything nicely with separate files for the app logic, database setup, and templates. To run it, you just need Python installed, then `pip install flask werkzeug` and run `python app.py`. Boom, local server up and running.

I learned a ton building this - how sessions work, why password hashing matters, and the basics of connecting a web app to a database with CRUD operations. 