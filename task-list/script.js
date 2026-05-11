// Local Storage Key
const STORAGE_KEY = 'tasks';
let tasks = [];
let currentCategory = 'all';
let currentSort = 'date';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
    renderTasks();
    setupEventListeners();
});

// Setup Event Listeners
function setupEventListeners() {
    const taskInput = document.getElementById('taskInput');
    
    // Enter key to add task
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTask();
        }
    });

    // Ctrl+N to focus input
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            taskInput.focus();
        }
    });
}

// Load tasks from localStorage
function loadTasks() {
    const stored = localStorage.getItem(STORAGE_KEY);
    tasks = stored ? JSON.parse(stored) : [];
}

// Save tasks to localStorage
function saveTasks() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
}

// Get today's date for due date comparison
function getTodayDate() {
    const today = new Date();
    return today.toISOString().split('T')[0];
}

// Calculate due date
function calculateDueDate(dueDateOption) {
    const today = new Date();
    let dueDate;

    switch (dueDateOption) {
        case 'today':
            dueDate = new Date(today);
            break;
        case 'tomorrow':
            dueDate = new Date(today);
            dueDate.setDate(dueDate.getDate() + 1);
            break;
        case 'week':
            dueDate = new Date(today);
            dueDate.setDate(dueDate.getDate() + 7);
            break;
        case 'month':
            dueDate = new Date(today);
            dueDate.setMonth(dueDate.getMonth() + 1);
            break;
        case 'none':
        default:
            dueDate = null;
    }

    return dueDate ? dueDate.toISOString().split('T')[0] : null;
}

// Check if task is overdue
function isOverdue(dueDate) {
    if (!dueDate) return false;
    return new Date(dueDate) < new Date(getTodayDate());
}

// Add new task
function addTask() {
    const taskInput = document.getElementById('taskInput');
    const categorySelect = document.getElementById('categorySelect');
    const dueDateSelect = document.getElementById('dueDate');
    const description = taskInput.value.trim();
    const category = categorySelect.value;
    const dueDate = calculateDueDate(dueDateSelect.value);

    if (description === '') {
        alert('Please enter a task description!');
        return;
    }

    const newTask = {
        id: Date.now(),
        description: escapeHtml(description),
        category: category,
        dueDate: dueDate,
        completed: false,
        timestamp: new Date().toLocaleString()
    };

    tasks.push(newTask);
    saveTasks();
    
    taskInput.value = '';
    categorySelect.value = 'personal';
    dueDateSelect.value = 'none';
    renderTasks();
    updateStats();
}

// Toggle task completion
function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        saveTasks();
        renderTasks();
        updateStats();
    }
}

// Delete task
function deleteTask(id) {
    tasks = tasks.filter(t => t.id !== id);
    saveTasks();
    renderTasks();
    updateStats();
}

// Clear all completed tasks
function clearCompleted() {
    if (tasks.some(t => t.completed)) {
        if (confirm('Are you sure you want to clear all completed tasks?')) {
            tasks = tasks.filter(t => !t.completed);
            saveTasks();
            renderTasks();
            updateStats();
        }
    } else {
        alert('No completed tasks to clear!');
    }
}

// Filter by category
function filterByCategory(category) {
    currentCategory = category;
    
    // Update active button
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    renderTasks();
}

// Sort tasks
function sortTasks(sortBy) {
    currentSort = sortBy;
    
    // Update active button
    document.querySelectorAll('.sort-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    renderTasks();
}

// Get filtered and sorted tasks
function getFilteredAndSortedTasks() {
    let filtered = tasks;

    // Filter by category
    if (currentCategory !== 'all') {
        filtered = filtered.filter(t => t.category === currentCategory);
    }

    // Sort tasks
    filtered.sort((a, b) => {
        switch (currentSort) {
            case 'date':
                // Overdue first, then by due date
                if (a.dueDate && b.dueDate) {
                    if (isOverdue(a.dueDate) && !isOverdue(b.dueDate)) return -1;
                    if (!isOverdue(a.dueDate) && isOverdue(b.dueDate)) return 1;
                    return new Date(a.dueDate) - new Date(b.dueDate);
                }
                if (a.dueDate) return -1;
                if (b.dueDate) return 1;
                return 0;
            case 'priority':
                // Completed tasks go to the end
                if (a.completed && !b.completed) return 1;
                if (!a.completed && b.completed) return -1;
                // Then by overdue status
                if (isOverdue(a.dueDate) && !isOverdue(b.dueDate)) return -1;
                if (!isOverdue(a.dueDate) && isOverdue(b.dueDate)) return 1;
                return 0;
            case 'category':
                const categoryOrder = { work: 0, personal: 1, shopping: 2, health: 3 };
                return (categoryOrder[a.category] || 4) - (categoryOrder[b.category] || 4);
            default:
                return 0;
        }
    });

    return filtered;
}

// Get due date badge info
function getDueDateBadgeInfo(dueDate) {
    if (!dueDate) return null;

    const today = getTodayDate();
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomorrowStr = tomorrow.toISOString().split('T')[0];

    if (isOverdue(dueDate)) {
        return { label: 'OVERDUE', class: 'overdue' };
    }
    if (dueDate === today) {
        return { label: 'TODAY', class: 'today' };
    }
    if (dueDate === tomorrowStr) {
        return { label: 'TOMORROW', class: 'tomorrow' };
    }
    if (new Date(dueDate) - new Date(today) <= 7 * 24 * 60 * 60 * 1000) {
        return { label: 'THIS WEEK', class: 'week' };
    }
    return { label: 'THIS MONTH', class: 'month' };
}

// Render tasks to DOM
function renderTasks() {
    const taskList = document.getElementById('taskList');
    const filtered = getFilteredAndSortedTasks();

    if (filtered.length === 0) {
        taskList.innerHTML = '<div class="empty-state">📝 No tasks yet. Create one to get started!</div>';
        return;
    }

    taskList.innerHTML = filtered.map(task => {
        const badgeInfo = getDueDateBadgeInfo(task.dueDate);
        const isTaskOverdue = isOverdue(task.dueDate);
        const categoryEmoji = {
            work: '💼',
            personal: '🏠',
            shopping: '🛒',
            health: '💪'
        };

        return `
            <div class="task-item ${task.completed ? 'completed' : ''} ${isTaskOverdue ? 'overdue' : ''}">
                <input 
                    type="checkbox" 
                    class="task-checkbox" 
                    ${task.completed ? 'checked' : ''}
                    onchange="toggleTask(${task.id})"
                >
                <div class="task-content">
                    <div class="task-text">${task.description}</div>
                    <div class="task-meta">
                        <span class="category-badge">${categoryEmoji[task.category]} ${task.category.charAt(0).toUpperCase() + task.category.slice(1)}</span>
                        ${badgeInfo ? `<span class="due-date-badge ${badgeInfo.class}">${badgeInfo.label}</span>` : ''}
                    </div>
                </div>
                <button class="btn-delete" onclick="deleteTask(${task.id})">Delete</button>
            </div>
        `;
    }).join('');
}

// Update statistics
function updateStats() {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const pending = total - completed;
    const overdue = tasks.filter(t => !t.completed && isOverdue(t.dueDate)).length;

    document.getElementById('statTotal').textContent = total;
    document.getElementById('statCompleted').textContent = completed;
    document.getElementById('statPending').textContent = pending;
    document.getElementById('statOverdue').textContent = overdue;
}

// Export tasks to JSON
function exportTasks() {
    if (tasks.length === 0) {
        alert('No tasks to export!');
        return;
    }

    const dataStr = JSON.stringify(tasks, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `tasks-backup-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

// Import tasks from JSON
function importTasks(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const imported = JSON.parse(e.target.result);
            
            if (!Array.isArray(imported)) {
                alert('Invalid file format! Please import a valid tasks backup.');
                return;
            }

            if (confirm('Import will replace all current tasks. Continue?')) {
                tasks = imported;
                saveTasks();
                currentCategory = 'all';
                currentSort = 'date';
                
                document.querySelectorAll('.category-btn')[0].classList.add('active');
                document.querySelectorAll('.category-btn').forEach((btn, i) => {
                    if (i !== 0) btn.classList.remove('active');
                });
                
                document.querySelectorAll('.sort-btn')[0].classList.add('active');
                document.querySelectorAll('.sort-btn').forEach((btn, i) => {
                    if (i !== 0) btn.classList.remove('active');
                });
                
                renderTasks();
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
renderTasks();
updateStats();
