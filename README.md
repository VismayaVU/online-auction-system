# Online Auction Platform

This is a full-stack **Online Auction Platform** built using the Django web framework, MySQL for the backend database, and HTML/CSS for the frontend. It allows users to create and participate in auctions while providing administrative oversight for managing the auction ecosystem.

## Features

### 🧑‍💻 User Features
1. **User Registration and Authentication**:  
   - Users can register on the platform.
   - Secure login/logout system using Django's authentication framework.

2. **Auction Dashboard**:  
   - Users can view all ongoing and approved auctions.
   - Live bidding feature to place bids on auctions.

3. **Create Auction**:  
   - Users can create new auctions by registering items.
   - Set a starting price and auction timeline.
   - Auctions will only be listed after admin approval.

4. **Profile Management**:  
   - Users can update their profile information (e.g., username).

5. **Auction Details View**:  
   - Real-time highest bidder and highest bid amount shown for each auction.

### 🛡️ Admin Features
1. **Django Admin Panel**:
   - View and manage all users, auctions, bids, deleted auctions, and deleted bids.
   - Approve or reject user-created auctions.

## 🧰 Tech Stack

- **Framework**: Django
- **Database**: MySQL
- **Frontend**: HTML5, CSS3
- **Admin Interface**: Django Admin

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MySQL
- pip (Python package manager)

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/online-auction-system.git
cd online-auction-system
```

2. **Create and Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure MySQL Database**
- Create a database named `onlineauctiondb` in MySQL.
- Update the `DATABASES` setting in `settings.py` with your DB credentials.

5. **Apply Migrations and Create Superuser**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Run the Development Server**
```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`

---

© 2025 Online Auction Platform — Built with Django 🐍 and ❤️