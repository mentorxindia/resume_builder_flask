
CREATE TABLE IF NOT EXISTS user_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

INSERT OR IGNORE INTO user_roles (name, description) VALUES
('user', 'Regular user with basic access'),
('admin', 'Administrator with full access'),
('customer_support', 'Customer Support with limited admin access');


-- ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    password TEXT NOT NULL,
    salt TEXT NOT NULL,
    gender TEXT NOT NULL,
    role_id INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN DEFAULT 1,
    profile_image TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES user_roles(id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS blacklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    about TEXT,                   
    profile TEXT,                  
    profile_image TEXT,           
    education TEXT,              
    skills TEXT,                  
    hobbies TEXT,                 
    experience TEXT,               
    languages TEXT,                
    projects TEXT,                 
    achievements TEXT,
    resume_template TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

