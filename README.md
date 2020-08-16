# Sh-reNet

Full stack webapp: A database exchange system where users can post their unused items and request items they require. Other users can use a built-in email function to respond to posts/requests.

# Features

Registration/Login system </br>
Search bar with filtering based on name, location, categories, and dates for available items, item requests, and organizations. </br>
Discover page which displays available items as well as item requests based on category </br>
User's personal item/item request management page where they can delete and add to the database </br>
Custom home page and organization profile page </br>
Detailed page displays of items, item requests, and organizations </br>
Built-in email function with predefined email subject </br>

# Requirements to run
```
Check requirements.txt file
```
# Installing
```
% git init
% git remote add origin https://github.com/williamrx05/Sh-reNet/
% git pull origin master
% cd DbExchangeSystem
% pip install -r requirements.txt
% django-admin.py startproject ShareNet ~/DbExchangeSystem
% python manage.py makemigrations
% python manage.py migrate
% python manage.py runserver
```
# Deployment

For the purposes of this project(Hackathon: Africa Hacks), it was temporarily deployed on a Digital Ocean Droplet virtual machine. Can be deployed through gunicorn.

# Built With

Django - Python Web Framework

# Authors

[William Xu] (https://github.com/williamrx05 "williamrx05 GitHub Profile")
[Aaditya Yadav] (https://github.com/aadityayadav "aadityayadav GitHub Profile")
