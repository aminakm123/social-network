# Social Networking API

This is a social networking API built using Django Rest Framework (DRF) with functionalities like user signup, login, searching users, sending/accepting/rejecting friend requests, and listing friends. It also includes rate-limiting for friend requests to prevent spamming.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)

## Features

- User Signup: Users can sign up with their email.
- User Login: Users can log in using their email and password.
- User Search: Search other users by email or part of their name (pagination support).
- Friend Requests: Send, accept, and reject friend requests.
- Friends List: View a list of friends who have accepted the friend request.
- Pending Requests: View a list of pending friend requests.
- Rate Limiting: Prevent sending more than 3 friend requests within a minute.

## Technologies Used

- Django: Backend web framework
- Django Rest Framework (DRF): For building the REST API
- SQLite: Database 
- Docker: Containerization of the application

## Installation

Step-by-step instructions to install and set up your project locally.

1. Clone the repo:
    ```bash
    git clone https://github.com/yourusername/projectname.git
    ```
2. Create and Activate Virtual Environment
     ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Navigate to the project directory:
    ```bash
    cd social_network
    ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt  
    ```

5. Run the application:
    ```bash
    python manage.py runserver 
    ```
6. Using Docker
To containerize the application, run:
    ```bash
    docker-compose up --build
    ```
## Usage

```bash
python manage.py makemigrations
python manage.py migrate  # Run database migrations
python manage.py createsuperuser  # Create a new superuser for Django
python manage.py runserver  # Start the development server
```

## API Endpoints

1. User Signup - URL: /register/
2. User Login- URL: /
3. Refresh Token- URL: /token/refresh/
4. Search Users URL: /search/?q=<search_term>
5. Send Friend Request URL: /friend-request/send/<to_user_id>/
6. Accept Friend Request URL: /friend-request/accept/<from_user_id>/
7. Decline Friend Request URL: /friend-request/reject/<from_user_id>/
8. List Friends URL: /friends/
9. List Pending Friend Requests URL: /pending-requests/


## API Documentation

https://documenter.getpostman.com/view/23916144/2sAXqngQqr to view the api documentation