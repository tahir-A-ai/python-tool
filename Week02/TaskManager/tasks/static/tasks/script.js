const API_URL = '/api/tasks/';
const CAT_URL = '/api/categories/';

let currentEditId = null;

document.addEventListener('DOMContentLoaded', () => {
    fetchCategories();
    fetchTasks();
});

// 1. Fetch Categories
async function fetchCategories() {
    try {
        const response = await fetch(CAT_URL);
        if (!response.ok) throw new Error("Failed to fetch");
        const categories = await response.json();

        const select = document.getElementById('category-select');
        select.innerHTML = '<option value="" disabled selected>Category...</option>';

        categories.forEach(cat => {
            select.innerHTML += `<option value="${cat.id}">${cat.categ_name}</option>`;
        });
    } catch (error) {
        console.error("Category Error:", error);
    }
}

// 2. Fetch and Render Tasks
async function fetchTasks() {
    const response = await fetch(API_URL);
    const tasks = await response.json();

    const container = document.getElementById('task-list');
    container.innerHTML = '';

    tasks.forEach(task => {
        // Determine Badge Colors
        const statusBadge = task.status === 'COMP'
            ? '<span class="badge badge-soft bg-soft-success">Completed</span>'
            : '<span class="badge badge-soft bg-soft-warning">Pending</span>';

        const priorityColor = task.priority === 'HIGH' ? 'bg-soft-danger' : (task.priority === 'MED' ? 'bg-soft-info' : 'bg-soft-success');

        // Render Card
        const card = `
            <div class="col-12">
                <div class="card custom-card task-card p-3">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <div class="d-flex align-items-center gap-2 mb-2">
                                <h5 class="fw-bold m-0 ${task.status === 'COMP' ? 'text-decoration-line-through text-muted' : ''}">${task.title}</h5>
                                ${statusBadge}
                            </div>
                            <p class="text-muted mb-2 text-sm">${task.description || 'No description provided.'}</p>
                            
                            <div class="d-flex gap-2 mt-3">
                                <span class="badge badge-soft ${priorityColor}">Priority: ${task.priority}</span>
                                <span class="badge badge-soft bg-light text-dark border">📅 ${task.due_date || 'No Date'}</span>
                            </div>
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button onclick="enableEditMode(${task.id})" class="btn btn-sm btn-outline-primary rounded-circle" style="width:32px; height:32px; padding:0;">✎</button>
                            <button onclick="deleteTask(${task.id})" class="btn btn-sm btn-outline-danger rounded-circle" style="width:32px; height:32px; padding:0;">✕</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += card;
    });
}

// 3. Handle Form Submit
document.getElementById('task-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get values from ALL inputs
    const title = document.getElementById('title').value;
    const priority = document.getElementById('priority').value;
    const category = document.getElementById('category-select').value;
    const status = document.getElementById('status-select').value;
    const description = document.getElementById('description').value;
    const dueDate = document.getElementById('due-date').value;

    // Validate Due Date
    const data = {
        title: title,
        priority: priority,
        category: category,
        status: status,
        description: description,
        due_date: dueDate || null // Send null if empty
    };

    try {
        const url = currentEditId ? `${API_URL}${currentEditId}/` : API_URL;
        const method = currentEditId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errData = await response.json();
            alert("Error: " + JSON.stringify(errData));
            return;
        }
        alert("Data create Successfully")

        resetForm();
        fetchTasks();
    } catch (error) {
        console.error("Error:", error);
    }
});

// 4. Delete Task
async function deleteTask(id) {
    if (confirm("Delete this task?")) {
        await fetch(`${API_URL}${id}/`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        fetchTasks();
    }
}

// 5. Enable Edit Mode
// We fetch the single task details first to ensure we populate all fields correctly
async function enableEditMode(id) {
    currentEditId = id;

    // Fetch fresh data for this specific task
    const response = await fetch(`${API_URL}${id}/`);
    const task = await response.json();

    // Fill inputs
    document.getElementById('title').value = task.title;
    document.getElementById('priority').value = task.priority;
    document.getElementById('status-select').value = task.status;
    document.getElementById('category-select').value = task.category;
    document.getElementById('description').value = task.description || '';
    document.getElementById('due-date').value = task.due_date || '';

    // Change UI to Edit Mode
    const btn = document.getElementById('submit-btn');
    btn.innerText = "Update Task";
    btn.classList.replace('btn-primary-custom', 'btn-warning');

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Helper: Reset Form
function resetForm() {
    currentEditId = null;
    document.getElementById('task-form').reset();
    const btn = document.getElementById('submit-btn');
    btn.innerText = "+ Create Task";
    btn.classList.replace('btn-warning', 'btn-primary-custom');
}

// Helper: CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}