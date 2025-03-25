#Personal Finance Tracker
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB Connection
def get_db_connection():
    """Establish MongoDB connection"""
    try:
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
        client = MongoClient(mongo_uri)
        db = client.finance_tracker
        return db
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Transaction Model
class TransactionModel:
    @staticmethod
    def validate_transaction(transaction: Dict[str, Any]) -> bool:
        """Validate transaction data"""
        required_fields = ['type', 'amount', 'category', 'date']
        return all(field in transaction for field in required_fields) and \
               transaction['type'] in ['income', 'expense'] and \
               transaction['amount'] > 0

# CRUD Operations
@app.route('/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction"""
    db = get_db_connection()
    transaction = request.json

    # Validate transaction
    if not TransactionModel.validate_transaction(transaction):
        return jsonify({"error": "Invalid transaction data"}), 400

    try:
        # Ensure date is in correct format
        transaction['date'] = datetime.strptime(transaction['date'], '%Y-%m-%d')
        
        # Insert transaction
        result = db.transactions.insert_one(transaction)
        
        # Convert ObjectId to string for JSON serialization
        transaction['_id'] = str(result.inserted_id)
        
        return jsonify(transaction), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transactions', methods=['GET'])
def get_transactions():
    """Retrieve transactions with filtering and pagination"""
    db = get_db_connection()
    
    # Pagination and filtering parameters
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    transaction_type = request.args.get('type')
    category = request.args.get('category')

    # Build query
    query = {}
    if transaction_type:
        query['type'] = transaction_type
    if category:
        query['category'] = category

    try:
        # Retrieve transactions
        transactions = list(db.transactions.find(query)
                            .skip((page - 1) * limit)
                            .limit(limit)
                            .sort('date', -1))
        
        # Convert ObjectId to string
        for transaction in transactions:
            transaction['_id'] = str(transaction['_id'])
        
        # Calculate Summary
        pipeline_income = [
            {'$match': {'type': 'income'}},
            {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
        ]
        pipeline_expense = [
            {'$match': {'type': 'expense'}},
            {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
        ]

        income_total = list(db.transactions.aggregate(pipeline_income))
        expense_total = list(db.transactions.aggregate(pipeline_expense))

        summary = {
            'totalIncome': income_total[0]['total'] if income_total else 0,
            'totalExpense': expense_total[0]['total'] if expense_total else 0,
            'balance': (income_total[0]['total'] if income_total else 0) - 
                       (expense_total[0]['total'] if expense_total else 0)
        }

        return jsonify({
            'transactions': transactions,
            'summary': summary,
            'page': page,
            'limit': limit
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transactions/<transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    """Update an existing transaction"""
    db = get_db_connection()
    update_data = request.json

    try:
        # Validate transaction
        if not TransactionModel.validate_transaction(update_data):
            return jsonify({"error": "Invalid transaction data"}), 400

        # Update transaction
        result = db.transactions.update_one(
            {'_id': ObjectId(transaction_id)},
            {'$set': update_data}
        )

        if result.modified_count:
            # Retrieve updated transaction
            updated_transaction = db.transactions.find_one({'_id': ObjectId(transaction_id)})
            updated_transaction['_id'] = str(updated_transaction['_id'])
            return jsonify(updated_transaction)
        else:
            return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """Delete a transaction"""
    db = get_db_connection()

    try:
        result = db.transactions.delete_one({'_id': ObjectId(transaction_id)})
        
        if result.deleted_count:
            return jsonify({"message": "Transaction deleted successfully"}), 200
        else:
            return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Provide financial analytics"""
    db = get_db_connection()

    try:
        # Category Breakdown
        category_pipeline = [
            {'$group': {
                '_id': '$category',
                'totalAmount': {'$sum': '$amount'},
                'transactionCount': {'$sum': 1}
            }},
            {'$sort': {'totalAmount': -1}}
        ]
        category_breakdown = list(db.transactions.aggregate(category_pipeline))

        # Monthly Trends
        monthly_pipeline = [
            {'$group': {
                '_id': {'$dateToString': {'format': "%Y-%m", 'date': "$date"}},
                'income': {
                    '$sum': {
                        '$cond': [{'$eq': ['$type', 'income']}, '$amount', 0]
                    }
                },
                'expense': {
                    '$sum': {
                        '$cond': [{'$eq': ['$type', 'expense']}, '$amount', 0]
                    }
                }
            }},
            {'$sort': {'_id': 1}}
        ]
        monthly_trends = list(db.transactions.aggregate(monthly_pipeline))

        return jsonify({
            'categoryBreakdown': category_breakdown,
            'monthlyTrends': monthly_trends
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Requirements Configuration
@app.route('/config', methods=['GET'])
def get_config():
    """Provide application configuration"""
    return jsonify({
        'appName': 'Personal Finance Tracker',
        'version': '1.0.0',
        'supportedFeatures': [
            'Transaction Management',
            'Financial Analytics',
            'Filtering and Pagination'
        ]
    })

# Error Handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Requirements file (requirements.txt)
"""
flask==2.1.0
flask-cors==3.0.10
pymongo==4.3.3
python-dotenv==0.20.0
"""