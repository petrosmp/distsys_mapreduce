document.getElementById('register-button').addEventListener('click', async () => {
    await register();
});
document.getElementById('login-button').addEventListener('click', async () => {
    await login();
});
document.getElementById('logout-button').addEventListener('click', async () => {
    await logout();
});

// Helper functions to show or hide a view
function hideView(element) {
    element.classList.add('hidden');
    element.classList.remove('visible');
}

function showView(element) {
    element.classList.remove('hidden');
    element.classList.add('visible');
}

// Function to show the registration view and hide the welcome view
function showRegister() {
    const welcomeView = document.querySelector('.welcome');
    const registerView = document.getElementById('register-view');

    hideView(welcomeView);
    showView(registerView);
}

// Function to show the login view and hide the welcome view
function showLogin() {
    const welcomeView = document.querySelector('.welcome');
    const loginView = document.getElementById('login-view');

    hideView(welcomeView);
    showView(loginView);
}

// Function to show the welcome view and hide both the registration and login views
function showWelcome() {
    const welcomeView = document.querySelector('.welcome');
    const registerView = document.getElementById('register-view');
    const loginView = document.getElementById('login-view');

    showView(welcomeView);
    hideView(registerView);
    hideView(loginView);
}

// Function to handle user registration
const register = async () => {
    // Get the username and password values from the input fields
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;
    const roles = ["read_storage", "write_storage", "submit_jobs", "track_jobs"];

    // Make a POST request to the backend register endpoint
    const response = await fetch('http://localhost:7777/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username, password, roles})
    });
    // Parse the JSON response from the server
    const data = await response.json();

    if (data.status === 'ok') {
        displayImage("https://i.insider.com/602ee9ced3ad27001837f2ac?width=700");
        // If the registration is successful, store the token in local storage
        alert('Register successful');
    } else if (data.message === 'user with such data already exists') {
        alert('User ' + data.username + ' already exists.');
    }
}

// Function to handle user login
const login = async () => {
    // Get the username and password values from the form
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    // Make a POST request to the backend login endpoint
    const response = await fetch('http://localhost:7777/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    // Parse the JSON response from the server
    const data = await response.json();

    // If the login is successful, store the token in local storage
    if (response.status === 200) {
        alert('Welcome, ' + username);
        localStorage.setItem('access_token', data.token);
        showWelcome();
        updateWelcomeMessage(username);
    } else {
        // Display an error message if the login fails
        alert(data.message);
    }
}

const displayImage = (imageUrl) => {
    // Create a new image element
    const img = document.createElement('img');
    img.src = imageUrl;  // Set the source of the image
    img.alt = 'Displayed Image';  // Set the alternate text for the image

    // Set some styles for the image (optional)
    img.style.width = '300px';  // Set the width of the image
    img.style.height = 'auto';  // Maintain the aspect ratio

    // Append the image to the body
    document.body.appendChild(img);
};

// Function to handle user logout
const logout = async () => {
    // Get the token from local storage
    const token = localStorage.getItem('access_token');

    // Make a POST request to the backend logout endpoint
    const response = await fetch('http://localhost:7777/auth/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });

    // Parse the JSON response from the server
    const data = await response.json();

    // If the logout is successful, remove the token from local storage
    if (response.status === 200) {
        alert('Logout successful');
        localStorage.removeItem('access_token');
        showWelcome();
    } else {
        // Display an error message if the logout fails
        alert(data.message);
    }
}

const updateWelcomeMessage = (username) => {
    const welcomeElement = document.getElementById('welcome_username');
    welcomeElement.textContent = `Welcome, ${username}`;
}
