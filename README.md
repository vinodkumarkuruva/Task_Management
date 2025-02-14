# Title -  Task Management System

   Welcome to the Django Authentication Starter project! This project provides a solid foundation for building web applications with user authentication features, including user registration, login, logout, forgot password, password reset, and email confirmation. And To manage and track tasks efficiently. Users can create, update, and manage tasks with priority and status tracking.

## Features : 

- **User Registration:** Allow users to create new accounts by providing basic information. 

- **Email Confirmation:** Send a confirmation email to verify user accounts. 

- **Login:** Secure user authentication. Logout: Allow users to log out securely from their accounts. 

- **Forgot Password:** Enable users to reset their passwords via email. 

- **Password Reset:** Allow users to set a new password after forgetting the old one. 

- **Tasks:** Task creation with priority and due dates. Update task details and status. Filter and search tasks. Responsive user interface using Bootstrap.

## Technologies Used  :

**Backend   :**  Django

**Frontend :**  HTML, CSS, Bootstrap

**Database:**  SQLite (default) or PostgreSQL

**Authentication:** Django's built-in authentication system

## Prerequisites :

- Python 3.8+
- pip (Python package installer)
- Git

## Installation & Setup : 

1. Clone the Repository -
```
   git clone https://github.com/vinodkumarkuruva/Task_Management.git
   cd Task_Management
```

2. Set Up a Virtual Environment (Optional but Recommended) -

```
python -m venv env
env\Scripts\activate         # On Windows
```

3. Install Required Dependencies -
   
   ```
   pip install -r requirements.txt
   ```
   
 4. Configure the Database -
    
   ```
      By default, the app uses SQLite.
      For PostgreSQL:
      Update the DATABASES setting in settings.py.
   ```

5. Apply Database Migrations -

   ```
   python manage.py migrate
   python manage.py makemigrations <app_name>
   python manage.py migrate
   ```

6. Create a Superuser -

   ```
   python manage.py createsuperuser
   ```
   
7. Run the Server -
   ```
   python manage.py runserver
   Access the application at : http://127.0.0.1:8000/
 ```

## Setting up Email Backend

The Email Backend will let you send emails to users for email confirmation, password reset, etc. To set up the email backend, follow these steps:

- To get email app password : Go to https://myaccount.google.com/

- Click on Security

- Set up your 2-Step Verification

- Click on App Passwords

- Input an App Name and click on Create

- Copy the generated password

- Make sure you have to following in your settings.py file
