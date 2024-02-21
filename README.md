# StoryHub
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

[![Django CI/CD](https://github.com/raykipkorir/storyhub/actions/workflows/django.yml/badge.svg?event=push)](https://github.com/raykipkorir/storyhub/actions/workflows/django.yml)

## Overview
StoryHub is a CMS platform built with Django where its users can read and publish articles.
### Authenticated users priviledges
- Users can follow and unfollow each other
- Users can like and bookmark articles
- Users can write their stories

## Authentication
- Users can sign in via Google.
- Sign in via GitHub coming soon.

## Security
- The site is protected against CSRF attacks. It utilizes Django's Built in CSRF protection.
- Users sensitive information such as passwords are hashed using Django's default password hashing algorithm(which is recommended). 

## Tests
Backend test coverage - 93%

## Contribution
Feel free to contribute to the project to make it better.

Visit [StoryHub](https://storyhub-spaj.onrender.com/)
