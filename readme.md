# 🎯 **TEMPOTRACK** - Your Ultimate Workout & Goal Tracker  

**TEMPOTRACK** is a web application designed to help you **organize, plan, and achieve your fitness goals**. Whether you’re managing workouts, tracking progress, or setting fitness goals, TEMPOTRACK keeps you motivated and on track! 💪  

---

## 🚀 **Key Features**

- 🏋️ **Workout Management**: Schedule workouts with descriptions, dates, and times.  
- 📅 **Interactive Calendar**: Visualize and track workouts on a user-friendly calendar.  
- 🎯 **Goal Tracking**: Set goals and monitor progress with insightful stats.  
- 🔑 **Role-Based Permissions**:  
   - **Superusers**: Full CRUD access.  
   - **Staff**: Limited access for managing workouts and goals.  
- 👤 **Standard Users**:
  - **Personalized Dashboard**: View and manage your own workouts, goals, and schedules.
  - **Workout Management**: Add, edit, and delete workouts specific to their account.
  - **Goal Tracking**: Set personal fitness goals and monitor progress with clear statistics.
  - **Progress Insights**: Access individual stats like total workouts completed, hours exercised, and goal completion rates.
  - **Secure Access**: Manage personal account settings, including passwords and profile details.
  - **Interactive Calendar**: View upcoming workouts and track completed workouts in a user-friendly calendar format. 
- 📊 **Progress Insights**: View total workouts completed and hours exercised.  
- 🛠️ **Custom Admin Panel**: Enhanced with search, sorting, filtering, and role management.

---

## 🛠️ **Setup Instructions**

### 1. Clone the Repository

git clone https://github.com/bpopovgit/workout_calendar.git<br>
cd workout_calendar<br>
### 2. Create a Virtual Environment

python -m venv venv<br>
source venv/bin/activate   # For Linux/Mac<br>
venv\Scripts\activate      # For Windows<br>

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Up Environment Variables

Create a .env file in the root directory and add the following variables:<br>

SECRET_KEY=your-secret-key<br>
DEBUG=True<br>
DATABASE_NAME=your-db-name<br>
DATABASE_USER=your-db-user<br>
DATABASE_PASSWORD=your-db-password<br>
DATABASE_HOST=localhost<br>
DATABASE_PORT=5432<br>

### 5. Run Migrations

python manage.py makemigrations<br>
python manage.py migrate<br>

### 6. Create Superuser

python manage.py createsuperuser<br>

### 7. Start the Development Server

python manage.py runserver<br>

### 8. Access the Application

User Interface: http://127.0.0.1:8000/<br>
Admin Panel: http://127.0.0.1:8000/admin/<br>

