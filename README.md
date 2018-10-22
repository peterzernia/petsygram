# petsygram

petsygram is an Instagram clone made using Django.



## Features

Register, Login/Logout & Reset password (email link)

Post photos to petsygram with caption and location set by user, author and time
set automatically

Post image size reduced to a width of 450px with proportional height to save
room on server

Image file deleted when post is deleted

Home Page showing posts of users the authenticated user follows

Post Detail Page for users, with 'Edit Post' and 'Delete Post' buttons visible
for post author

jQuery/AJAX 'Like' button accesses REST API to toggle 'Like' and update like
count

Post commenting: displays truncated comments on the Home Page, and full comments
on Post Detail Page

Search Page with ability to search for users or hashtags used in a published
post

Notification Page showing when other users have interacted with a post (likes or
comments), and when other users have started following you

Profile Page for users showing profile image (with default image), number of
followers, bio, website and posts, jQuery AJAX follow/unfollow button if not the
authenticated user, otherwise 'Edit Profile' and 'Logout' button

Edit Profile Page to edit username, email, website, bio, and profile image

Profile image reduced to 150px x 150px to save space on the server

Direct messaging system with inbox and links to individual message threads with
other users

Infinite scrolling on Home Page



## Getting Started

Follow these instructions to get a copy running on your local machine for
development and testing purposes


### Prerequisites

Python 3.6 & git


### Installing

1. Open up Terminal, and go into the directory where you want your local copy,
e.g.
```
cd projects
```

2. Download a copy
```
git clone https://github.com/peterzernia/petsygram.git
```

3. Install a virtual environment
```
pip install virtualenv
```

4. Make a folder for your virtual environments e.g.
```
mkdir ~/venvs
```

5. Make a new virtual environment for this project
```
virtualenv --system-site-packages ~/venvs/petsygram
```

6. Start the virtual environment
```
source ~/venvs/petsygram/bin/activate
```

7. Generate a secret key for your django app using
```
python
```
  **then**
```
from django.utils.crypto import get_random_string
```
  **then**
```
chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
```
  **then**
```
get_random_string(50, chars)
```
  **and lastly**
```
quit()
```

8. Copy this result and in your petsygram/petsygram/setting.py file replace
```
SECRET_KEY = os.environ.get('PETSYGRAM')
```
  **with**
```
SECRET_KEY = 'your newly generated secret key here'
```

9. Go into the directory containing 'requirements.txt'
```
cd petsygram
```

10. Install the Python requirements
```
pip install -r requirements.txt
```

11. Make migrations to set up the database
```
python manage.py makemigrations
```

12. When this has completed, run these migrations
```
python manage.py migrate
```

13. Create a user profile to login with
```
python manage.py createsuperuser
```

14. Once you have followed the instructions to create a user, run the server
```
python manage.py runserver
```

15. If there were no errors anywhere, you can now go to http://localhost:8000/
in your browser to view a local copy of petsygram



## What I learned

Petsygram was both my first big Django project, as well as my first substantive
Python project. Petsygram explored the Django web framework, looking at basic
components such as setting up a user login/logout system, as well as more
complex frameworks like a small REST API for 'like' and 'subscribe' accessed
through jQuery/AJAX buttons. Deploying petsygram with the help of PythonAnywhere
allowed me insight into the broader picture of web development. Up until this
project I had mainly worked on small, individual scripts, but with petsygram, I
tied together a python web framework and MySQL database (sqlite for testing),
and even dug up my html/css front end knowledge from middle school to create a
cohesive web app.



## Built With

* [Django](https://www.djangoproject.com/) - Web Framework
* [Boostrap](https://getbootstrap.com/) - HTML & CSS
* [Material Design](http://forms.viewflow.io/) - Forms & CSS
* [jQuery](https://jquery.com/) - JS
* [Waypoints](http://imakewebthings.com/waypoints/) - JS


## Author

* **Peter Zernia** - (https://github.com/peterzernia)
