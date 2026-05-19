from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import random

app = Flask(__name__)

# Sample user data
users = [
    {"id": 1001, "username": "john_doe", "email": "john@example.com", "role": "user", "name": "John Doe"},
    {"id": 1002, "username": "jane_smith", "email": "jane@example.com", "role": "user", "name": "Jane Smith"},
    {"id": 1003, "username": "alex_wong", "email": "alex@example.com", "role": "user", "name": "Alex Wong"},
    {"id": 1004, "username": "sarah_connor", "email": "sarah@example.com", "role": "user", "name": "Sarah Connor"},
    {"id": 1005, "username": "mike_tyson", "email": "mike@example.com", "role": "user", "name": "Mike Tyson"},
    {"id": 1006, "username": "emma_watson", "email": "emma@example.com", "role": "user", "name": "Emma Watson"},
    {"id": 1007, "username": "chris_evans", "email": "chris@example.com", "role": "user", "name": "Chris Evans"},
    {"id": 1008, "username": "lisa_ray", "email": "lisa@example.com", "role": "moderator", "name": "Lisa Ray"},
    {"id": 1009, "username": "david_beck", "email": "david@example.com", "role": "user", "name": "David Beck"},
    {"id": 1010, "username": "amy_adams", "email": "amy@example.com", "role": "user", "name": "Amy Adams"},
    {"id": 1078, "username": "admin_system", "email": "admin@system.local", "role": "admin", "name": "System Administrator"}
]

# Flag
FLAG = "xorion{M9!@Z$2Q7pKX8#W0FLr}"

@app.route('/')
def index():
    """Home page - Blog/E-commerce front"""
    blog_posts = [
        {"title": "Welcome to Our Tech Blog", "content": "Discover the latest in technology..."},
        {"title": "Web Security Best Practices", "content": "Learn how to secure your web applications..."},
        {"title": "API Development Guide", "content": "A comprehensive guide to REST API development..."}
    ]
    return render_template('index.html', posts=blog_posts)

@app.route('/robots.txt')
def robots():
    """Robots.txt file hinting at API documentation"""
    return render_template('robots.txt')

@app.route('/api/document')
def api_document():
    """API Documentation page"""
    return render_template('api_document.html')

# ===== V2 API Endpoints (Unauthorized) =====
@app.route('/api/v2/users', methods=['GET'])
def v2_users():
    return jsonify({"error": "Unauthorized access", "message": "This API version requires authentication"}), 403

@app.route('/api/v2/user/<int:user_id>', methods=['GET'])
def v2_user(user_id):
    return jsonify({"error": "Unauthorized access", "message": "This API version requires authentication"}), 403

@app.route('/api/v2/user/flag', methods=['POST'])
def v2_flag():
    return jsonify({"error": "Unauthorized access", "message": "This API version requires authentication"}), 403

# ===== V1 API Endpoints (Vulnerable) =====
@app.route('/api/v1/users', methods=['GET'])
def v1_users():
    """List all users (IDOR vulnerability - should be restricted)"""
    return jsonify([{"id": u["id"], "username": u["username"]} for u in users])

@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def v1_user(user_id):
    """Get specific user by ID (IDOR vulnerability)"""
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/api/v1/user/flag', methods=['POST'])
def v1_flag():
    """Flag endpoint - requires specific body content"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Check for required fields
    if not data or 'user' not in data or 'role' not in data:
        return jsonify({"error": "Data not available", "hint": "Check the request body format"}), 400

    # Check if it's the admin user
    if data.get('user') == 'admin_system' and data.get('role') == 'admin':
        return jsonify({
            "message": "Access granted! Here's your flag:",
            "flag": FLAG,
            "note": "Congratulations! You found the API misconfiguration and IDOR vulnerability!"
        })

    # Return random user data for incorrect attempts
    random_user = random.choice([u for u in users if u["role"] != "admin"])
    return jsonify({
        "message": "Access denied",
        "data": random_user,
        "hint": "Try different credentials"
    })

@app.route('/api/v1/user/flag', methods=['GET'])
def v1_flag_get():
    """GET method should not work"""
    return jsonify({
        "error": "Method not allowed",
        "message": "Use POST request with appropriate body"
    }), 405

# ===== Debug endpoint for testing =====
@app.route('/debug/users')
def debug_users():
    """Debug endpoint to see all users (for testing only)"""
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
