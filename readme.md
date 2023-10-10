# Chat App

![chatapp](https://github.com/Aryanpal20/Python_Chating_app/assets/99199495/7f050245-7224-48f7-a16c-c0bd69900906)


## Overview

The Chat App is a real-time chat application that enables users to engage in instant conversations. It's built using React for the frontend and Python Django for the backend. WebSocket is used to provide real-time messaging capabilities, making it ideal for users who want to communicate in real-time.

## Features

- **Real-time Chat:** Enjoy seamless real-time chat with other users.
- **User Authentication:** Users can sign up, log in, and have personalized chat experiences.
- **Multiple Chat Rooms:** Create and join chat rooms for specific topics or groups.
- **Notifications:** Receive notifications for new messages and chat room activity.
- **Responsive Design:** The application is responsive and works well on both desktop and mobile devices.

## Getting Started

### Prerequisites

- Node.js and npm installed on your machine.
- Python and pip installed on your machine.
- PostgreSQL database (or you can configure a different database of your choice).

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Aryanpal20/Python_Chating_app.git
2. **Frontend Setup:**

    ```bash
    cd chat-app/frontend
    npm install
3. **Backend Setup:**

    ```bash
    cd ../backend
    pip install -r requirements.txt
4. **Database Configuration:**
    
    ```bash
    Create a PostgreSQL database and configure the database settings in backend/settings.py.
5. **Migrate the Database:**
    
    ```bash
    python manage.py makemigrations
    python manage.py migrate
6. **Start the Backend Server:**
    
    ```bash
    python manage.py runserver 
7. **Start the Frontend Development Server:**
    
    ```bash
    cd ../frontend
    npm run dev
Access the application in your web browser at http://localhost:3000.

## Usage

- Register a new account or log in if you already have an account.
- Start chatting in real-time with other users.
- Enjoy the seamless chat experience!


## Contributing

Contributions are welcome! Please follow the Contributing Guidelines to contribute to this project.

### Acknowledgments

Special thanks to WebSocket for enabling real-time communication.
This project was inspired by the need for real-time chat applications in various online communities.
