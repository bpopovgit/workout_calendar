# **TEMPOTRACK - Workout Calendar Application**

---

## **Overview**
TEMPOTRACK is a powerful and user-friendly Workout Calendar application that enables users to **schedule workouts**, **set goals**, **track their progress**, and manage their fitness routines. It is built using **Django** with a responsive and visually appealing UI.

---

## **Table of Contents**

1. [Features](#features)  
2. [Technologies Used](#technologies-used)  
3. [Setup Instructions](#setup-instructions)  
4. [Database Configuration](#database-configuration)  
5. [User Roles and Permissions](#user-roles-and-permissions)  
6. [Admin Site Customization](#admin-site-customization)  
7. [Screenshots](#screenshots)  

---

## **Features**

1. **User Management**
   - User registration with profile management.  
   - Secure login/logout functionality.  
   - Password management and validation.

2. **Workout Scheduling**
   - Users can add, edit, and delete workouts.  
   - View workouts in a calendar format or list view.  

3. **Goal Management**
   - Set fitness goals (e.g., number of workouts per month).  
   - Monitor progress and achievements.  

4. **Admin Role Management**
   - Superusers can perform full CRUD operations.  
   - Staff users have limited permissions.  
   - Role management available in the Django admin panel.

5. **Custom Admin Site**
   - Fully customized admin site for managing users, workouts, and goals.  
   - Enhanced functionality with filters, list displays, and ordering.

6. **Dynamic UI/UX**
   - Responsive design for seamless experience across devices.  
   - Clean and modern interface with custom styling.  

---

## **Technologies Used**

The following technologies, libraries, and dependencies were used in TEMPOTRACK:

### **Backend**
- **Django 5.1.3** - High-level Python web framework.
- **psycopg2 2.9.10** - PostgreSQL adapter for Python.

### **Frontend**
- **HTML5/CSS3** - Modern web structure and styling.  
- **Bootstrap 5.3** - Responsive UI components.  
- **Google Fonts** - Custom font integration.  

### **Forms and Styling**
- **django-crispy-forms 2.3** - For form rendering.  
- **crispy-bootstrap5 2024.10** - Integrates crispy forms with Bootstrap 5.  

### **Utilities**
- **itsdangerous 2.2.0** - Token generation for secure links.  
- **python-dotenv 1.0.1** - Environment variable management.  

### **Image and PDF Support**
- **Pillow 11.0.0** - Image processing for profile pictures.  
- **reportlab 4.2.5** - PDF generation library.

