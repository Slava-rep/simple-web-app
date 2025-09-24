from flask import Flask, jsonify, request, render_template_string, session, redirect, url_for
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Важно для сессий

# HTML шаблон с Bootstrap 5
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css">
    <style>
        .user-card {
            transition: transform 0.2s;
        }
        .user-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .stats-card {
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .navbar-brand {
            font-weight: 600;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="bi bi-people-fill"></i> UserManager
            </a>
            <div class="navbar-nav ms-auto">
                <span class="navbar-text">
                    <i class="bi bi-person-circle"></i> 
                    {% if session.username %}
                        {{ session.username }}
                    {% else %}
                        Guest
                    {% endif %}
                </span>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="container my-4">
        <!-- Statistics Cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card stats-card">
                    <div class="card-body">
                        <h5><i class="bi bi-people"></i> Total Users</h5>
                        <h3 id="total-users">0</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-success text-white">
                    <div class="card-body">
                        <h5><i class="bi bi-check-circle"></i> Active</h5>
                        <h3 id="active-users">0</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-warning text-dark">
                    <div class="card-body">
                        <h5><i class="bi bi-clock"></i> Recent</h5>
                        <h3 id="recent-users">0</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card bg-info text-white">
                    <div class="card-body">
                        <h5><i class="bi bi-graph-up"></i> Growth</h5>
                        <h3 id="growth-rate">0%</h3>
                    </div>
                </div>
            </div>
        </div>

        <!-- User Management Section -->
        <div class="row">
            <div class="col-md-4">
                <!-- Login Form -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h5><i class="bi bi-box-arrow-in-right"></i> User Login</h5>
                    </div>
                    <div class="card-body">
                        <form id="login-form">
                            <div class="mb-3">
                                <label class="form-label">Username</label>
                                <input type="text" class="form-control" id="login-username" 
                                       placeholder="Enter username" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Password</label>
                                <input type="password" class="form-control" id="login-password" 
                                       placeholder="Enter password" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">
                                <i class="bi bi-box-arrow-in-right"></i> Login
                            </button>
                        </form>
                        <div class="mt-3">
                            <button class="btn btn-outline-secondary w-100" onclick="logout()">
                                <i class="bi bi-box-arrow-right"></i> Logout
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Add User Form -->
                <div class="card">
                    <div class="card-header">
                        <h5><i class="bi bi-person-plus"></i> Add New User</h5>
                    </div>
                    <div class="card-body">
                        <form id="user-form">
                            <div class="mb-3">
                                <label class="form-label">Full Name</label>
                                <input type="text" class="form-control" id="name" 
                                       placeholder="Enter full name" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" id="email" 
                                       placeholder="Enter email" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Department</label>
                                <select class="form-select" id="department">
                                    <option value="Engineering">Engineering</option>
                                    <option value="Marketing">Marketing</option>
                                    <option value="Sales">Sales</option>
                                    <option value="HR">Human Resources</option>
                                </select>
                            </div>
                            <button type="submit" class="btn btn-success w-100">
                                <i class="bi bi-person-plus"></i> Add User
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Users Table -->
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5><i class="bi bi-list-ul"></i> Users List</h5>
                        <div>
                            <button class="btn btn-sm btn-outline-primary" onclick="loadUsers()">
                                <i class="bi bi-arrow-clockwise"></i> Refresh
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover" id="users-table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Name</th>
                                        <th>Email</th>
                                        <th>Department</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody id="users-tbody">
                                    <!-- Users will be loaded here -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Toast for notifications -->
    <div class="toast-container position-fixed top-0 end-0 p-3">
        <div id="liveToast" class="toast" role="alert">
            <div class="toast-header">
                <i class="bi bi-check-circle-fill text-success me-2"></i>
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body" id="toast-message">
                Hello, world! This is a toast message.
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Utility functions
function showToast(message, type = 'success') {
    const toast = new bootstrap.Toast(document.getElementById('liveToast'));
    const toastMessage = document.getElementById('toast-message');
    const toastHeader = document.querySelector('.toast-header i');
    
    toastMessage.textContent = message;
    
    if (type === 'error') {
        toastHeader.className = 'bi bi-exclamation-circle-fill text-danger me-2';
    } else {
        toastHeader.className = 'bi bi-check-circle-fill text-success me-2';
    }
    
    toast.show();
}

// Load users and update statistics
async function loadUsers() {
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        
        // Update statistics
        document.getElementById('total-users').textContent = users.length;
        document.getElementById('active-users').textContent = users.filter(u => u.active).length;
        document.getElementById('recent-users').textContent = users.length; // Simplified
        
        // Update table
        const tbody = document.getElementById('users-tbody');
        tbody.innerHTML = users.map(user => `
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td><span class="badge bg-secondary">${user.department}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="editUser(${user.id})">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteUser(${user.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error loading users:', error);
        showToast('Error loading users', 'error');
    }
}

// Add new user
document.getElementById('user-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const department = document.getElementById('department').value;
    
    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, department })
        });
        
        if (response.ok) {
            showToast('User added successfully!');
            document.getElementById('user-form').reset();
            loadUsers();
        } else {
            const error = await response.json();
            showToast(error.error || 'Error adding user', 'error');
        }
    } catch (error) {
        showToast('Error adding user', 'error');
    }
});

// Login functionality
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            showToast(`Welcome, ${username}!`);
            location.reload();
        } else {
            showToast('Login failed', 'error');
        }
    } catch (error) {
        showToast('Login error', 'error');
    }
});

// Logout functionality
async function logout() {
    try {
        await fetch('/api/logout', { method: 'POST' });
        showToast('Logged out successfully');
        setTimeout(() => location.reload(), 1000);
    } catch (error) {
        showToast('Logout error', 'error');
    }
}

// Delete user
async function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        try {
            const response = await fetch(`/api/users/${userId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                showToast('User deleted successfully');
                loadUsers();
            } else {
                showToast('Error deleting user', 'error');
            }
        } catch (error) {
            showToast('Error deleting user', 'error');
        }
    }
}

// Edit user (placeholder)
function editUser(userId) {
    showToast(`Edit functionality for user ${userId} would go here`, 'info');
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadUsers();
    
    // Check if user is logged in
    fetch('/api/users')
        .then(r => r.json())
        .then(users => {
            document.getElementById('total-users').textContent = users.length;
        });
});
    </script>
</body>
</html>
'''

# API endpoints remain the same as before...
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/users', methods=['GET', 'POST'])
def users_api():
    if request.method == 'GET':
        return jsonify(users)
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400
        
        if users:
            max_id = max(user['id'] for user in users)
        else:
            max_id = 0
        
        new_user = {
            'id': max_id + 1,
            'name': data['name'],
            'email': data['email'],
            'department': data.get('department', 'Engineering'),
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        users.append(new_user)
        return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['GET', 'DELETE'])
def user_operations(user_id):
    global users
    
    if request.method == 'GET':
        user = next((u for u in users if u['id'] == user_id), None)
        if user:
            return jsonify(user)
        return jsonify({'error': 'User not found'}), 404
    
    elif request.method == 'DELETE':
        
        user = next((u for u in users if u['id'] == user_id), None)
        if user:
            users.remove(user)
            return jsonify({'status': 'user deleted'})
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if username:
        session['username'] = username
        return jsonify({'status': 'success', 'username': username})
    return jsonify({'error': 'Username is required'}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'status': 'success'})

@app.route('/api/reset', methods=['POST'])
def reset_data():
    global users
    users.clear()
    users.extend([
        {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@test.com', 'department': 'Engineering', 'active': True, 'created_at': datetime.now().isoformat()},
        {'id': 2, 'name': 'Bob Smith', 'email': 'bob@test.com', 'department': 'Marketing', 'active': True, 'created_at': datetime.now().isoformat()}
    ])
    return jsonify({'status': 'data reset successfully'})

# Initialize users
users = [
    {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@test.com', 'department': 'Engineering', 'active': True, 'created_at': datetime.now().isoformat()},
    {'id': 2, 'name': 'Bob Smith', 'email': 'bob@test.com', 'department': 'Marketing', 'active': True, 'created_at': datetime.now().isoformat()}
]

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # коммент чтобы проверить github actions fffffвввв