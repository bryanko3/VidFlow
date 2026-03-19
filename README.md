![VidFlow Banner](./screenshots/banner.png)

## VidFlow

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)

**VidFlow** is a aimple video-sharing web platform. Built with Flask, it enables users to upload and interact with videos in a dynamic and scalable environment.

---

## Key Highlights

- Video upload based on HLS support  
- Real-time user interaction (likes, comments, subscriptions)  
- Search based on the keywords/categories you want  
- Modular backend architecture (Flask-based)  
- Watermark processing for media protection  

---

## Project Preview

### Home Feed
![Home](./screenshots/home.png)

### Login Page
![Login](./screenshots/login.png)

### Register Page
![Register](./screenshots/register.png)

### Video Player
![Watch](./screenshots/watch.png)

### Search Results
![Search](./screenshots/search.png)

### User Profile
![Profile](./screenshots/profile.png)

### Upload Interface
![Upload](./screenshots/upload.png)

---

## System Overview

VidFlow follows a **modular MVC-inspired architecture**, separating logic and functionality clearly across layers.

## Tech Stack

### Backend
- Python (Flask)
- SQLite
- RESTful API

### Frontend
- HTML / CSS / JavaScript

### Media Processing
- HLS video uploading
- Video Watermarking  

---

## Project Structure

VidFlow/

│── app.py

│── config.py

│

├── core/          # Database & utilities

├── models/        # Data models

├── routes/        # API endpoints

├── services/      # Business logic

│

├── static/        # CSS, JS, images

├── templates/     # HTML templates

│

└── requirements.txt


---

## Installation

```bash
git clone https://github.com/bryanko3/VidFlow.git
cd VidFlow
pip install -r requirements.txt
python app.py
```

## Core Features Breakdown

### Authentication System
- Secure login & registration  
- Password hashing for user safety  

### Video Engine
- Upload and store contents via **HLS (HTTP Live Streaming)**  
- Apply watermark to uploaded videos  

### Social Interaction
- Like / Unlike functionality  
- Comment system  
- Channel subscription  

### Search System
- Keyword-based content search  
- Scalable query structure for larger datasets  

---

## Key Engineering Decisions

- **Service Layer Separation** → Improved scalability and maintainability  
- **HLS-based video uploading** → Efficient, modern delivery of video content  
- **Modular Routing** → Clean separation of features and improved debugging  

---

## What I Learned from VidFlow

- Built a simple video-sharing platform from scratch  
- Designed a scalable backend architecture  
- Implemented HLS-based uploading system
- Enhanced debugging and system design skills  

---

## Why VidFlow?

VidFlow was created to simulate a **real-world content platform** and push the limits of full-stack web development.  
It showcases scalability, feature depth, and hands-on media engineering experience.

## Contact

Email: dongyek4@uci.edu

GitHub: https://github.com/bryanko3
