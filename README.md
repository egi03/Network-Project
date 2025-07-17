# Network - Social Media Platform

A Twitter-like social network web application built with Django that allows users to create posts, follow other users, and interact with content through likes and comments.

## 🎥 Demo

[View Live Demo](https://www.youtube.com/watch?v=EQMHLYRR2-0)

## 📋 Project Specifications

This project was built as part of [CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/projects/4/network/) course.

## ✨ Features

### Core Functionality
- **User Authentication**: Register, login, and logout functionality
- **Post Creation**: Users can create new text posts
- **Post Editing**: Users can edit their own posts inline
- **Like System**: Users can like and unlike posts with real-time updates
- **Following System**: Users can follow and unfollow other users
- **User Profiles**: Individual profile pages showing user statistics and posts
- **Following Feed**: Dedicated page to view posts from followed users only
- **Pagination**: Posts are paginated (10 posts per page) for better performance

### Interactive Features
- **Real-time Updates**: JavaScript-powered interactions for liking and editing posts
- **Responsive Design**: Clean, modern UI that works across devices
- **Dynamic Content Loading**: Posts load dynamically with user interactions

## 🛠️ Technologies Used

- **Backend**: Django 5.2, Python 3.x
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite (default Django setup)
- **Styling**: Bootstrap 4.4.1 + Custom CSS
- **Authentication**: Django's built-in authentication system

## 🏗️ Project Structure

```
network/
├── project4/                    # Django project directory
│   ├── manage.py               # Django management script
│   ├── project4/               # Project settings
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py            # Main URL configuration
│   │   └── wsgi.py            # WSGI configuration
│   └── network/                # Main application
│       ├── models.py           # Database models (User, Post, Like, Follow)
│       ├── views.py            # View functions
│       ├── urls.py             # App URL configuration
│       ├── admin.py            # Django admin configuration
│       ├── templates/network/  # HTML templates
│       │   ├── layout.html     # Base template
│       │   ├── index.html      # All posts page
│       │   ├── profile.html    # User profile page
│       │   ├── following.html  # Following feed page
│       │   ├── login.html      # Login page
│       │   └── register.html   # Registration page
│       └── static/network/     # Static files
│           ├── styles.css      # Custom CSS styling
│           ├── index.js        # Main page JavaScript
│           ├── profile.js      # Profile page JavaScript
│           └── load_posts.js   # Post loading JavaScript
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Django 5.2+

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd network
   ```

2. **Navigate to the project directory**
   ```bash
   cd project4
   ```

3. **Install Django** (if not already installed)
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations network
   python manage.py migrate
   ```

5. **Create a superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and go to `http://127.0.0.1:8000`

## 💾 Database Models

### User
- Extends Django's AbstractUser
- Standard user authentication fields

### Post
- `user`: Foreign key to User (author)
- `content`: Text content of the post
- `date`: Timestamp of creation

### Like
- `user`: Foreign key to User (who liked)
- `post`: Foreign key to Post (which post was liked)
- `date`: Timestamp of the like

### Follow
- `follower`: Foreign key to User (who is following)
- `subject`: Foreign key to User (who is being followed)
- `date`: Timestamp of the follow relationship

## 🔧 API Endpoints

- `GET /` - All posts (index page)
- `GET /profile/<username>` - User profile page
- `GET /following` - Posts from followed users
- `POST /create_post` - Create a new post
- `POST /toggle_follow` - Follow/unfollow a user
- `POST /edit_post` - Edit a post (AJAX)
- `PUT /edit_post` - Like/unlike a post (AJAX)

## 🎨 Features in Detail

### Post Management
- Users can create posts with text content
- Post authors can edit their posts inline using JavaScript
- Real-time editing without page refresh

### Social Interactions
- Like/unlike posts with instant UI feedback
- Follow/unfollow users from their profile pages
- View personalized feed of posts from followed users

### User Interface
- Clean, modern design with custom CSS
- Responsive layout that works on mobile and desktop
- Intuitive navigation with Bootstrap components
- Pagination for better performance with large datasets

## 🔒 Security Features

- CSRF protection on all forms and AJAX requests
- User authentication required for posting and interactions
- Authorization checks to ensure users can only edit their own posts
- Django's built-in security features

## 📱 Browser Compatibility

- Modern browsers with JavaScript ES6+ support
- Responsive design for mobile and desktop
- Tested with Chrome, Firefox, Safari, and Edge
