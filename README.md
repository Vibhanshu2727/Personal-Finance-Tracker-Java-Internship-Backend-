# Personal Finance Tracker

## Overview
Personal Finance Tracker is a Flask-based web application for managing personal financial transactions. It provides comprehensive features for tracking income, expenses, and generating financial analytics.

## Features
- Create, Read, Update, and Delete (CRUD) transactions
- Transaction filtering and pagination
- Financial analytics and reporting
- Category-based transaction tracking
- Monthly income and expense trends

## Technologies Used
- Python
- Flask
- MongoDB
- Flask-CORS
- python-dotenv

## Prerequisites
- Python 3.8+
- MongoDB
- pip (Python package manager)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/personal-finance-tracker.git
cd personal-finance-tracker
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root with the following content:
```
MONGODB_URI=mongodb://localhost:27017
```
Replace the URI with your MongoDB connection string if different.

## Running the Application
```bash
python app.py
```
The server will start at `http://localhost:5000`

## API Endpoints

### Transactions
- `POST /transactions`: Create a new transaction
- `GET /transactions`: Retrieve transactions (with optional filtering)
- `PUT /transactions/<transaction_id>`: Update a transaction
- `DELETE /transactions/<transaction_id>`: Delete a transaction

### Analytics
- `GET /analytics`: Get financial analytics and trends

### Configuration
- `GET /config`: Get application configuration

## Testing
(Add testing instructions or include a testing framework)

## Deployment Options
1. **Heroku**:
   - Create a `Procfile` with: `web: gunicorn app:app`
   - Install `gunicorn`: `pip install gunicorn`
   - Follow Heroku CLI deployment steps

2. **MongoDB Atlas**:
   - Create a free cluster
   - Get connection string
   - Update `.env` with Atlas connection URI

3. **AWS Elastic Beanstalk**:
   - Create a new application
   - Upload your project files
   - Configure environment variables

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/personal-finance-tracker](https://github.com/yourusername/personal-finance-tracker)
