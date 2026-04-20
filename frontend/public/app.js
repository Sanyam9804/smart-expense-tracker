// State
let authMode = 'login';
let currentView = 'dashboard';
let expenses = [];
let charts = {};

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    if (getToken()) {
        showApp();
    } else {
        showAuth();
    }
    
    // Set default date to today
    document.getElementById('exp-date').valueAsDate = new Date();
});

// Auth Logic
function switchAuthTab(mode) {
    authMode = mode;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById('auth-submit-btn').textContent = mode === 'login' ? 'Sign In' : 'Sign Up';
    document.getElementById('auth-message').textContent = '';
}

async function handleAuth(e) {
    e.preventDefault();
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    const msgEl = document.getElementById('auth-message');
    
    msgEl.textContent = 'Please wait...';
    msgEl.className = 'message';

    try {
        if (authMode === 'login') {
            await apiLogin(user, pass);
            showApp();
        } else {
            await apiRegister(user, pass);
            msgEl.textContent = 'Account created! Please log in.';
            msgEl.className = 'message msg-success';
            switchAuthTab('login');
            // Mock click on login tab
            document.querySelectorAll('.tab-btn')[0].click();
        }
    } catch (err) {
        msgEl.textContent = err.message;
        msgEl.className = 'message msg-error';
    }
}

function logout() {
    setToken(null);
    showAuth();
}

// Navigation
function showAuth() {
    document.getElementById('app-container').classList.add('hidden');
    document.getElementById('app-container').classList.remove('active');
    document.getElementById('auth-container').classList.remove('hidden');
    document.getElementById('auth-container').classList.add('active');
}

async function showApp() {
    document.getElementById('auth-container').classList.add('hidden');
    document.getElementById('auth-container').classList.remove('active');
    document.getElementById('app-container').classList.remove('hidden');
    document.getElementById('app-container').classList.add('active');
    navigate('dashboard');
}

function navigate(view) {
    currentView = view;
    // Update Sidebar
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    document.querySelector(`[onclick="navigate('${view}')"]`).classList.add('active');
    
    // Update View
    document.querySelectorAll('.view').forEach(v => {
        v.classList.remove('active');
        v.classList.add('hidden');
        // trigger animation again by removing and re-adding fade-in classes
        const fadeElements = v.querySelectorAll('.fade-in');
        fadeElements.forEach(el => {
            el.style.animation = 'none';
            el.offsetHeight; // trigger reflow
            el.style.animation = null; 
        });
    });
    
    document.getElementById(`${view}-view`).classList.add('active');
    document.getElementById(`${view}-view`).classList.remove('hidden');
    
    const titles = { 'dashboard': 'Dashboard', 'add-expense': 'Record New Expense', 'analytics': 'Analytics & Insights' };
    document.getElementById('current-view-title').textContent = titles[view];

    loadDataForView(view);
}

// Data loading
async function loadDataForView(view) {
    try {
        if (view === 'dashboard' || view === 'analytics') {
            expenses = await getExpenses();
        }
        
        if (view === 'dashboard') renderDashboard();
        if (view === 'analytics') renderAnalytics();
    } catch (e) {
        if (e.message.includes('fetch')) {
            logout(); // token might be bad
        }
        console.error(e);
    }
}

// Dashboard View
function renderDashboard() {
    const total = expenses.reduce((sum, e) => sum + e.amount, 0);
    const thisMonth = expenses.filter(e => new Date(e.date).getMonth() === new Date().getMonth())
                              .reduce((sum, e) => sum + e.amount, 0);
    
    document.getElementById('total-expenses-val').textContent = `₹${total.toFixed(2)}`;
    document.getElementById('month-expenses-val').textContent = `₹${thisMonth.toFixed(2)}`;
    document.getElementById('transaction-count-val').textContent = expenses.length;

    const tbody = document.getElementById('transaction-tbody');
    tbody.innerHTML = '';
    
    // Just showing top 10 recent
    const recent = [...expenses].sort((a,b) => new Date(b.date) - new Date(a.date)).slice(0, 10);
    
    recent.forEach(e => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${e.date}</td>
            <td><strong>${e.description}</strong></td>
            <td><span style="background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 4px; font-size:0.8rem;">${e.category}</span></td>
            <td>${e.payment_mode}</td>
            <td style="font-weight:600;">₹${e.amount.toFixed(2)}</td>
            <td><button class="del-btn" onclick="trDelete(${e.id})">🗑️</button></td>
        `;
        tbody.appendChild(tr);
    });
}

async function trDelete(id) {
    if(confirm("Delete this expense?")) {
        await deleteExpense(id);
        loadDataForView('dashboard');
    }
}

// Add Expense View
async function autoCategorize() {
    const desc = document.getElementById('desc').value;
    if(!desc) return alert("Enter a description first!");
    
    const cat = await predictCategory(desc);
    document.getElementById('cat').value = cat;
}

async function handleAddExpense(e) {
    e.preventDefault();
    const msgEl = document.getElementById('add-expense-msg');
    
    const expense = {
        description: document.getElementById('desc').value,
        amount: parseFloat(document.getElementById('amt').value),
        category: document.getElementById('cat').value,
        date: document.getElementById('exp-date').value,
        payment_mode: document.getElementById('payment-mode').value
    };

    try {
        await addExpense(expense);
        msgEl.textContent = 'Expense added successfully!';
        msgEl.className = 'message msg-success';
        document.getElementById('add-expense-form').reset();
        document.getElementById('exp-date').valueAsDate = new Date(); // reset date
        setTimeout(() => msgEl.textContent='', 3000);
    } catch {
        msgEl.textContent = 'Failed to add expense.';
        msgEl.className = 'message msg-error';
    }
}

// Analytics View
async function renderAnalytics() {
    // 1. Fetch AI Insights
    try {
        const data = await getInsights();
        document.getElementById('next-month-pred').textContent = `₹${data.predicted_next_month.toFixed(2)}`;
        
        const list = document.getElementById('insights-list');
        list.innerHTML = '';
        data.insights.forEach(ins => {
            const li = document.createElement('li');
            li.innerHTML = ins.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            list.appendChild(li);
        });
    } catch(e) { console.error(e); }

    // 2. Render Charts
    if(expenses.length === 0) return;

    // Destroy old charts to prevent overlapping
    if(charts.cat) charts.cat.destroy();
    if(charts.trend) charts.trend.destroy();

    // Aggregations
    const catData = {};
    expenses.forEach(e => catData[e.category] = (catData[e.category] || 0) + e.amount);
    
    const trendData = {};
    [...expenses].sort((a,b)=>new Date(a.date)-new Date(b.date)).forEach(e => {
        trendData[e.date] = (trendData[e.date] || 0) + e.amount;
    });

    // Color palette matching dark aesthetic
    const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16'];
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Inter', sans-serif";

    const ctxCat = document.getElementById('categoryChart').getContext('2d');
    charts.cat = new Chart(ctxCat, {
        type: 'doughnut',
        data: {
            labels: Object.keys(catData),
            datasets: [{
                data: Object.values(catData),
                backgroundColor: colors,
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            plugins: { legend: { position: 'right' } },
            cutout: '70%'
        }
    });

    const ctxTrend = document.getElementById('trendChart').getContext('2d');
    
    // Create gradient
    let gradient = ctxTrend.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.5)');   
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');

    charts.trend = new Chart(ctxTrend, {
        type: 'line',
        data: {
            labels: Object.keys(trendData),
            datasets: [{
                label: 'Daily Spent (₹)',
                data: Object.values(trendData),
                borderColor: '#3b82f6',
                backgroundColor: gradient,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                x: { grid: { display: false } }
            }
        }
    });
}
