const API_URL = "";

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    if(token) localStorage.setItem('token', token);
    else localStorage.removeItem('token');
}

async function apiLogin(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const res = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
    });
    if (!res.ok) throw new Error("Invalid credentials");
    const data = await res.json();
    setToken(data.access_token);
    return true;
}

async function apiRegister(username, password) {
    const res = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    if (!res.ok) throw new Error("Registration failed. Username may exist.");
    return true;
}

async function getExpenses() {
    const res = await fetch(`${API_URL}/expenses/list`, {
        headers: { 'Authorization': `Bearer ${getToken()}` }
    });
    if (!res.ok) throw new Error("Failed to fetch expenses");
    return await res.json();
}

async function addExpense(expense) {
    const res = await fetch(`${API_URL}/expenses/add`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getToken()}`
        },
        body: JSON.stringify(expense)
    });
    if (!res.ok) throw new Error("Failed to add expense");
    return await res.json();
}

async function deleteExpense(id) {
    const res = await fetch(`${API_URL}/expenses/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${getToken()}` }
    });
    if (!res.ok) throw new Error("Failed to delete expense");
    return true;
}

async function predictCategory(desc) {
    const res = await fetch(`${API_URL}/ml/predict_category`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: desc })
    });
    if (!res.ok) return "Other";
    const data = await res.json();
    return data.category;
}

async function getInsights() {
    const res = await fetch(`${API_URL}/ml/insights`, {
        headers: { 'Authorization': `Bearer ${getToken()}` }
    });
    if (!res.ok) throw new Error("Failed to fetch insights");
    return await res.json();
}
