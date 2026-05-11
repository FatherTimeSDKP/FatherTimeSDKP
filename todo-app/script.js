// Local Storage Key
const STORAGE_KEY = 'todos';
let todos = [];
let currentFilter = 'all';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTodos();
    renderTodos();
    setupEventListeners();
});

// Setup Event Listeners
function setupEventListeners() {
    const todoInput = document.getElementById('todoInput');
    
    // Enter key to add todo
    todoInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTodo();
        }
    });

    // Ctrl+N to focus input
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            todoInput.focus();
        }
    });
}

// Load todos from localStorage
function loadTodos() {
    const stored = localStorage.getItem(STORAGE_KEY);
    todos = stored ? JSON.parse(stored) : [];
}

// Save todos to localStorage
function saveTodos() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}

// Add new todo
function addTodo() {
    const todoInput = document.getElementById('todoInput');
    const prioritySelect = document.getElementById('prioritySelect');
    const text = todoInput.value.trim();
    const priority = prioritySelect.value;

    if (text === '') {
        alert('Please enter a task!');
        return;
    }

    const newTodo = {
        id: Date.now(),
        text: escapeHtml(text),
        completed: false,
        priority: priority,
        timestamp: new Date().toLocaleString()
    };

    todos.push(newTodo);
    saveTodos();
    
    todoInput.value = '';
    prioritySelect.value = 'medium';
    renderTodos();
    updateStats();
}

// Toggle todo completion
function toggleTodo(id) {
    const todo = todos.find(t => t.id === id);
    if (todo) {
        todo.completed = !todo.completed;
        saveTodos();
        renderTodos();
        updateStats();
    }
}

// Delete todo
function deleteTodo(id) {
    todos = todos.filter(t => t.id !== id);
    saveTodos();
    renderTodos();
    updateStats();
}

// Clear all completed todos
function clearCompleted() {
    if (todos.some(t => t.completed)) {
        if (confirm('Are you sure you want to clear all completed tasks?')) {
            todos = todos.filter(t => !t.completed);
            saveTodos();
            renderTodos();
            updateStats();
        }
    } else {
        alert('No completed tasks to clear!');
    }
}

// Clear all todos
function clearAllTodos() {
    if (todos.length > 0) {
        if (confirm('Are you sure you want to delete ALL tasks? This cannot be undone!')) {
            todos = [];
            saveTodos();
            renderTodos();
            updateStats();
        }
    } else {
        alert('No tasks to clear!');
    }
}

// Filter todos
function filterTodos(filter) {
    currentFilter = filter;
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    renderTodos();
}

// Get filtered todos
function getFilteredTodos() {
    switch (currentFilter) {
        case 'active':
            return todos.filter(t => !t.completed);
        case 'completed':
            return todos.filter(t => t.completed);
        default:
            return todos;
    }
}

// Render todos to DOM
function renderTodos() {
    const todoList = document.getElementById('todoList');
    const filtered = getFilteredTodos();

    if (filtered.length === 0) {
        todoList.innerHTML = '<div class="empty-state">✨ No tasks yet. Add one to get started!</div>';
        return;
    }

    todoList.innerHTML = filtered.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}">
            <input 
                type="checkbox" 
                class="todo-checkbox" 
                ${todo.completed ? 'checked' : ''}
                onchange="toggleTodo(${todo.id})"
            >
            <div class="todo-text">${todo.text}</div>
            <span class="priority-badge ${todo.priority}">${todo.priority}</span>
            <span class="todo-time">${todo.timestamp}</span>
            <button class="btn-delete" onclick="deleteTodo(${todo.id})">Delete</button>
        </div>
    `).join('');
}

// Update statistics
function updateStats() {
    const total = todos.length;
    const completed = todos.filter(t => t.completed).length;
    const active = total - completed;

    document.getElementById('totalTasks').textContent = total;
    document.getElementById('completedTasks').textContent = completed;
    document.getElementById('activeTasks').textContent = active;
}

// Export todos to JSON
function exportTodos() {
    if (todos.length === 0) {
        alert('No tasks to export!');
        return;
    }

    const dataStr = JSON.stringify(todos, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `todos-backup-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

// Import todos from JSON
function importTodos(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const imported = JSON.parse(e.target.result);
            
            if (!Array.isArray(imported)) {
                alert('Invalid file format! Please import a valid todos backup.');
                return;
            }

            if (confirm('Import will replace all current tasks. Continue?')) {
                todos = imported;
                saveTodos();
                currentFilter = 'all';
                document.querySelectorAll('.filter-btn')[0].classList.add('active');
                document.querySelectorAll('.filter-btn').forEach((btn, i) => {
                    if (i !== 0) btn.classList.remove('active');
                });
                renderTodos();
                updateStats();
                alert('Tasks imported successfully!');
            }
        } catch (error) {
            alert('Error importing file! Please check the file format.');
            console.error('Import error:', error);
        }
    };
    reader.readAsText(file);
    
    // Reset file input
    event.target.value = '';
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initial render
renderTodos();
updateStats();
