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
- 📊 **Progress Insights**: View total workouts completed and hours exercised.  
- 🛠️ **Custom Admin Panel**: Enhanced with search, sorting, filtering, and role management.

---

## 🛠️ **Setup Instructions**

Follow these steps to set up and run the project locally:

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

### . Create Superuser

python manage.py createsuperuser<br>

### 7. Start the Development Server

python manage.py runserver<br>

### . Access the Application

User Interface: http://127.0.0.1:8000/<br>
Admin Panel: http://127.0.0.1:8000/admin/<br>

