from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# HTML шаблон для UI
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Test App</title>
</head>
<body>
    <h1>Welcome to Test App</h1>
    <form id="user-form">
        <input type="text" id="name" name="name" placeholder="Enter your name">
        <input type="email" id="email" name="email" placeholder="Enter your email">
        <button type="submit">Submit</button>
    </form>
    <div id="result"></div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/users', methods=['GET', 'POST'])
def users_api():
    if request.method == 'GET':
        # ИСПРАВЛЕНИЕ: возвращаем актуальный список пользователей
        return jsonify(users)
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400
        
        # УЛУЧШЕННАЯ логика генерации ID
        if users:
            max_id = max(user['id'] for user in users)
        else:
            max_id = 0
        
        new_user = {
            'id': max_id + 1,
            'name': data['name'],
            'email': data['email']
        }
        users.append(new_user)
        return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/reset', methods=['POST'])
def reset_data():
    """Endpoint для сброса данных к исходному состоянию (для тестов)"""
    global users
    users.clear()
    users.extend([
        {'id': 1, 'name': 'Alice', 'email': 'alice@test.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@test.com'}
    ])
    return jsonify({'status': 'data reset successfully'})

# In-memory "database"
users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@test.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@test.com'}
]

if __name__ == '__main__':
    app.run(debug=True, port=5000)