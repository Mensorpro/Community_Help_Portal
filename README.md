# Community Help Portal

## I. Introduction
The Community Help Portal is a Django web application designed to facilitate mutual assistance within a community. It allows users to post requests for help, view and respond to existing requests, manage their user profiles, and stay informed through community announcements. The platform aims to connect those in need with those willing to offer support, fostering a stronger, more collaborative community.

## II. Features
-   **User Authentication**: Secure user registration, login, and logout.
-   **User Profiles**:
    -   View and edit user profiles.
    -   Profile pictures.
-   **Help Requests (Requests App)**:
    -   Create, view, update, and delete help requests (CRUD).
    -   Categorize requests (e.g., Tutoring, Delivery, Technical Support).
    -   Track request status (Open, In Progress, Closed).
    -   List and filter requests by category and status.
    -   Users can respond to help requests.
-   **Announcements (Announcements App)**:
    -   View community-wide announcements.
    -   Categorize announcements.
    -   Admin interface for managing announcements and categories.
-   **Responsive Design**: Basic responsiveness for usability on different screen sizes.
-   **Dark/Light Theme**: User-selectable theme for improved accessibility and preference.
-   **Admin Interface**:
    -   Customized Django admin for managing users, profiles, requests, responses, and announcements.
    -   Enhanced list displays, filters, and search capabilities for core models.

## III. Technology Stack
-   **Backend**: Django (Python 3.10+)
-   **Database**: SQLite3 (development)
-   **Frontend**: HTML5, CSS3 (with CSS Variables), Django Template Language (DTL)
-   **Version Control**: Git & GitHub

## IV. Project Structure
The project is organized into the following Django applications:

-   `core`: Handles the main landing page (home page) and site-wide base templates.
-   `accounts`: Manages user registration, login, logout, and user profiles (`UserProfile` model extending Django's `User`).
-   `requests`: Manages help requests (`RequestPost`, `RequestCategory` models) and responses to them (`Response` model).
-   `announcements`: Manages community-wide announcements (`Announcement`, `AnnouncementCategory` models).

## V. Setup and Installation
### Prerequisites
-   Python (3.10 or higher recommended)
-   pip (Python package installer)
-   Git

### Steps
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Mensorpro/Community_Help_Portal
    cd community-help-portal
    ```
    

2.  **Create and Activate a Virtual Environment**:

    On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    On Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    A `requirements.txt` file  included in the project. This file lists all the necessary Python packages for the project.
    To install the dependencies, run:
    ```bash
    pip install -r requirements.txt
    ```
    (Key dependencies will include Django, Pillow for image handling, etc.)

4.  **Apply Database Migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser (for Admin Access)**:
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create an admin username and password.

6.  **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```
    The application will typically be available at `http://127.0.0.1:8000/`.

## VI. Usage
-   **Register/Login**: New users can register for an account. Existing users can log in.
-   **Home Page**: Displays recent announcements and help requests.
-   **Requests**:
    -   View a list of all help requests.
    -   Filter requests by category or status.
    -   Click on a request to view its details and any responses.
    -   Authenticated users can create new help requests.
    -   Authenticated users can respond to open requests (if they are not the requester).
    -   Requesters can edit or delete their own requests.
-   **Announcements**: View a list of community announcements and their details.
    -  Admin users can create, edit, or delete announcements.
    

-   **Profile**: Authenticated users can view their profile and edit their profile information (including profile picture).
-   **Theme Toggle**: Use the moon/sun icon in the navbar to switch between dark and light themes.

## VII. Admin Site
-   Access the Django admin site at `/admin/` (e.g., `http://127.0.0.1:8000/admin/`).
-   Log in with the superuser credentials created during setup.
-   Manage users, user profiles, request posts, responses, request categories, announcements, and announcement categories.

## VIII. Models and Relationships
Unable to Render Diagram

## IX. Future Enhancements (Optional)
-   Email notifications for new responses or important announcements.
-   Real-time chat or messaging for request discussions.
-   Advanced search and filtering capabilities.
-   User reputation system.

This README provides an overview of the Community Help Portal, its features, and instructions for setup and usage.