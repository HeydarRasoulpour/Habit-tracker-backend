# Habit Tracker Backend API

## Project Overview

The **Habit Tracker Backend API** is a tracking backend service designed to help users create, manage, and track their habits. It supports **multi-tenancy**, **role-based access control**, habit categorization, reminders, progress tracking, and habit challenges.

---

## Project Goals

- Enable multi-user support with isolated data
- Implement role-based permissions for admins and users
- Track habit progress over time
- Organize habits using categories and challenges
- Provide a clean, scalable backend architecture

---

## Core Features

- User & profile management
- Habit creation and management
- Habit progress tracking
- Habit reminders
- Habit categorization
- Habit challenges
- Role-based access control (Admin / User)

---

## Database Design

- Users 1–1 Profiles
- Habits 1–1 habit_tracking
- Users 1–M Habits
- Users 1–M HabitReminders
- Users M–M HabitChallenges
- Habits M–M HabitCategories via HabitCategoryXref

---

## Database Tables

### Users

- user_id (PK)
- username
- email
- phone
- password
- role (admin, user)
- is_active
- created_at

### Profiles

- profile_id (PK)
- user_id (FK)
- first_name
- last_name
- dob
- bio

### Habits

- habit_id (PK)
- user_id (FK)
- title
- description
- frequency
- is_active
- start_date
- end_date

### HabitTracking

- track_id (PK)
- habit_id (FK)
- status
- note
- unit_completed

### HabitCategories

- category_id (PK)
- category_name
- description

### HabitCategoryXref

- habit_id (FK)
- category_id (FK)

### HabitReminders

- reminder_id (PK)
- habit_id (FK)
- user_id (FK)
- reminder_time
- repeat_days
- message
- created_date
- is_active

### HabitChallenges

- challenge_id (PK)
- challenge_name
- description
- start_date
- end_date
- created_date

---

## Roles & Permissions

### Admin

- Manage users
- Manage categories
- Manage challenges
- View all habits
- Assign habits to categories

### User

- Manage own profile
- Manage own habits
- Track habit progress
- Manage reminders
- Join challenges
- View categories and challenges

---

## API Design Principles

- Clear endpoints
- Role-based authorization
- Ownership validation
- Consistent error handling

---

## ERD Summary

- Users 1–1 Profiles
- Habits 1–1 habit_tracking
- Users 1–M Habits
- Users 1–M HabitReminders
- Users M–M HabitChallenges
- Habits M–M HabitCategories via HabitCategoryXref

---

## Conclusion

This backend provides a scalable, secure foundation for a habit tracking application and can easily be extended with analytics, notifications, or a frontend client.

## My Backend Development Journey - What I Learned This Semester

Throughout this semester, I learned how to build a complete backend application using Python, Flask, SQLAlchemy, and Marshmallow. I gained experience designing a relational database from scratch, creating an ERD, and implementing one-to-one, one-to-many, and many-to-many relationships while supporting multi-tenancy so multiple users can safely manage their own data. I learned how to structure a Flask application using blueprints, separate models, controllers, and schemas, and implement full CRUD functionality for all resources. I also learned how to apply error handling and enforce permissions using user roles, ensuring secure access to different endpoints.

Working on my Habit Tracker capstone project helped me connect everything we learned in class into a real-world application. I learned how to use Marshmallow schemas for validation and serialization, apply reflection in controllers, and build a complete Postman collection for testing all endpoints. My favorite part of the class was seeing how all the pieces fit together—from database design to API testing—and gaining confidence in debugging and building backend systems that follow best practices.
