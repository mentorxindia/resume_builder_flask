import pytest
import sqlite3
from app2 import app, init_db

@pytest.fixture
def client():
    # Setup the Flask test client
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test_secret'
    with app.test_client() as client:
        # Reinitialize database for each test
        init_db()
        yield client

def test_register_success(client):
    response = client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

def test_register_duplicate_email(client):
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    response = client.post('/register', json={
        'email': 'test@example.com',
        'password': 'newpassword'
    })
    assert response.status_code == 409
    assert response.get_json()['message'] == 'Email already exists'

def test_login_success(client):
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_failure(client):
    response = client.post('/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Invalid email or password'

def test_dashboard_access(client):
    # Register and log in
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    login_response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    token = login_response.get_json()['access_token']

    # Access dashboard with JWT
    response = client.get('/dashboard', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert 'Welcome to the Dashboard' in response.get_json()['message']

def test_fill_resume(client):
    # Register, log in, and fill resume
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    login_response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    token = login_response.get_json()['access_token']

    response = client.post('/fill_resume', json={
        'details': 'This is my resume details.'
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Resume details saved successfully'

def test_select_template(client):
    # Register, log in, and access templates
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    login_response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    token = login_response.get_json()['access_token']

    response = client.get('/select_template', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert 'templates' in response.get_json()
    assert len(response.get_json()['templates']) == 5

def test_download_unimplemented(client):
    # Register, log in, and access download
    client.post('/register', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    login_response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'test123'
    })
    token = login_response.get_json()['access_token']

    response = client.get('/download', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 501
    assert response.get_json()['message'] == 'PDF generation not implemented yet'
