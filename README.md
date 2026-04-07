<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=40&duration=2500&pause=1000&color=FFA500&center=true&vCenter=true&width=600&lines=+EventNest+Project" alt="EventNest Typing Title"/>
</p>

**⚡ Event Management System:** Event Management System is a full-featured web application built with Django and Django Templates, styled using Tailwind CSS. The system allows users to manage events, participants, and categories, with optimized queries and a responsive front-end. Admins can manage all data, and users can search, filter, and view event details.

🚀 Features

1. Data Models
   - **Event**: name, description, date, time, location, category 
   - **Participant**: name, email, ManyToMany relationship with Event
   - **Category**: name and description

2. CRUD Operations
   - Full Create, Read, Update, Delete functionality for Events, Participants, and Categories
   - Form validation to prevent invalid submissions

3. Optimized Queries
   - `select_related` for efficient category fetching
   - `prefetch_related` for participants
   - Aggregate queries for total participants
   - Filters by category and date range

4. Responsive UI with Tailwind CSS
   - Mobile-friendly interface
   - Event listings with category and participant count
   - Event details including participants
   - Organizer Dashboard:
     - Stats grid: Total participants, Total events, Upcoming events, Past events
     - Today’s events list
     - Interactive stats updating the data dynamically

5. Search Features
   - Search events by name or location using `request.GET` and `icontains`

6. User Profile and Authentication
   - Custom User model with profile picture and phone number
   - Profile view and edit
   - Password change and email-based reset
   - Secure login/logout system

🛠 Technologies Used

- Django - Web framework
- Django Templates + Tailwind CSS - Frontend
- PostgreSQL / SQLite - Database
- Python-dotenv - Environment variables

⚙️ Installation Instructions

1. Clone the repository:

```bash
git clone https://github.com/yourusername/event-management.git
cd event-management
