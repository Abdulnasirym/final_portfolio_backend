# MumCare Web Application

## Introduction
**MumCare** is an antenatal tracker designed to monitor pregnant women's antenatal visits to the hospital and an immunization tracker to keep track of children's immunization visits from birth. The platform is designed to ensure timely reminders for healthcare milestones. Health providers are responsible for profiling women on the platform. Women receive email notifications about their next visits, which are powered by Twilio's notification services.

---

## Target Audience

### Primary Users
- Healthcare providers responsible for profiling and managing patient data.

### Indirect Beneficiaries
- Pregnant women
- Nursing mothers

---

## Key Features

1. **Antenatal Visit Tracker**
   - Tracks scheduled antenatal visits for pregnant women.

2. **Immunization Tracker**
   - Monitors children's immunization schedules from birth.

3. **Email Notifications**
   - Women are notified of their next visits via email using Twilio.

4. **Provider-Managed Profiling**
   - Health providers register and manage user profiles on the platform.

5. **Educational Resources**
   - Evidence-based content on maternal and child health.

---

## Impact Goals

- Improve maternal and child health by ensuring adherence to scheduled healthcare visits.
- Enhance the efficiency of healthcare providers in tracking and managing patient schedules.
- Provide timely notifications to reduce missed visits.

---

## Technology Stack

### Frontend Development
- **Frameworks:** React Native
- **Languages:** JavaScript
- **UI Design:** Material UI, Bootstrap

### Backend Development
- **Frameworks:** Flask
- **Languages:** Python

### Database
- **Relational Database:** SQLite
- **ORM:** SQLite ORM (e.g., SQLAlchemy)

### APIs
- **RESTful APIs:** Manage communication between the frontend and backend.
- **Notification Service:** Twilio for email notifications.

---

## Installation Guide

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)
- Node.js and npm (for React Native development)

### Environment Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Abdulnasirym/final_portfolio_backend/tree/main
2. **Navigate to the Project Directory:**
   ```bash
   cd final_portfolio_backend
   ```

3. **Backend Setup:**
   - Navigate to the backend directory:
     ```bash
     cd backend
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

4. **Frontend Setup:**
   - Navigate to the frontend directory:
     ```bash
     cd frontend
     ```
   - Install dependencies:
     ```bash
     npm install
     ```

---

## Database Configuration
MumCare uses SQLite, which is included with Flask. No additional database setup is required.

---

## Running the Application

### Backend
1. Initialize the database schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Start the backend server:
   ```bash
   python manage.py runserver
   ```

### Frontend
1. Start the frontend server:
   ```bash
   npm start
   ```
2. Open your web browser and navigate to:
   ```
   http://localhost:5000/
   ```
   to access the MumCare application.

---

## How to Use
1. **Health Providers**:
   - Register pregnant women on the platform.
   - Input antenatal and immunization schedules for each user.
2. **Pregnant Women**:
   - Receive email notifications about upcoming antenatal visits.
   - Track immunization schedules for their children.

---

## Contributing
Your contributions are welcome! If you'd like to improve the MumCare Web Application, please:
- Review our contributing guidelines.
- Check out the open issues to identify areas where you can help.

---

## License


---

## Contact Information
For queries or feedback, please reach out to us at:
- **Email:** support@mumcareapp.com
- **GitHub:** https://github.com/Abdulnasirym/final_portfolio_backend/tree/main

