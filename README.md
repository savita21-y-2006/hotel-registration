# Hotel Registration CRUD App

A simple Flask-based CRUD (Create, Read, Update, Delete) application for managing hotel registrations, using SQLite as the database.

## Features
- Add new hotel records (name, location, rooms available, price per night, rating)
- View all registered hotels in a table
- Update existing hotel details inline
- Delete hotel records
- Flash messages for success/error feedback
- SQLite database via SQLAlchemy ORM
- Safe table creation: if `instance/example.db` already exists (e.g. shared with another app), the `hotel` table is added into it without affecting existing tables or data

## Project Structure
