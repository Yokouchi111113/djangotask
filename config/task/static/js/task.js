let currentTasks = [];
let editingTaskId = null;

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access");

    if (!token) {
        location.href = "/signin/";
        return;
    }

    loadTasks();

    document
        .getElementById("search-form")
        .addEventListener("submit", searchTasks);

    document
        .getElementById("task-form")
        .addEventListener("submit", createTask);

    document
        .getElementById("cancel-edit-btn")
        .addEventListener("click", exitEditMode);
});    


// 表示
function renderTasks(tasks) {
    currentTasks = tasks;

    const taskList = document.getElementById("task-list");
    taskList.innerHTML = "";

    if (tasks.length === 0) {
    taskList.innerHTML = "<p>該当するタスクはありません。</p>";
    return;
    }

    
    

    tasks.forEach(task => {

        let dueText = "";

        if (task.days_until_due > 0) {
            dueText = `残り ${task.days_until_due} 日`;
        } else if (task.days_until_due === 0) {
            dueText = "今日まで";
        } else if (task.days_until_due !== null) {
            dueText = `${Math.abs(task.days_until_due)} 日超過`;
        }

        taskList.innerHTML += `
            <div class="task">
                <h3 class="task-title" title="${task.title}">
                    ${task.title}
                </h3>
                <p class="task-description" title="${task.description}">
                    ${task.description}
                </p>
                <p>${task.status_display}</p>
                <p>期限: ${task.due_date || "期限なし"}</p>
                <p>${dueText}</p>
                <div class="button">
                <button onclick="startEdit(${task.id})" name="startEdit">
                    編集
                </button>
                <button onclick="deleteTask(${task.id})" name="deleteTask">
                    削除
                </button>
                </div>
            </div>
        `;
    });
}


// 取得
async function loadTasks() {
    const res = await authFetch("/api/tasks/");
    

    if (res.status === 401) {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        location.href = "/signin/";
        return;
    }


    const taskList = document.getElementById("task-list");
    const tasks = await res.json();
    renderTasks(tasks);

}


// 検索
async function searchTasks(e) {
    e.preventDefault();

    const q = document.getElementById("search").value;
    const dueWithin =
        document.getElementById("due-within").value;

    let url = "/api/tasks/?";

    if (q) {
        url += `q=${encodeURIComponent(q)}&`;
    }

    if (dueWithin) {
        url += `due_within=${dueWithin}`;
    }

    const res = await authFetch(url);
    const tasks = await res.json();

    renderTasks(tasks);
}


function startEdit(taskId) {

    const task = currentTasks.find(
        t => t.id === taskId
    );

    document.getElementById("title").value =
        task.title;

    document.getElementById("description").value =
        task.description;

    document.getElementById("status").value =
        task.status;    

    document.getElementById("due_date").value =
        task.due_date || null;

    editingTaskId = task.id;

    enterEditMode();
}


// 作成　と　編集
async function createTask(e) {
    e.preventDefault();

    const title =
        document.getElementById("title").value;

    const description =
        document.getElementById("description").value;

    const status =
        document.getElementById("status").value;
    
    const due_date = 
        document.getElementById("due_date").value;

    const taskDate = {
        title,
        description,
        status,
        due_date: due_date || null,
    };

    let res;

    if (editingTaskId !== null) {
        res = await authFetch(
            `/api/tasks/${editingTaskId}/`,
            {
                method: "PATCH",
                body: JSON.stringify(taskDate),
            }
        );
    } else {
        res = await authFetch("/api/tasks/", {
            method: "POST",
            body: JSON.stringify(taskDate),
        });
    }

    if (res.ok) {

        exitEditMode();

        loadTasks();
    } else {
        const errorData = await res.json();
        console.error(
            "更新失敗",
            res.status
        );
        console.error(errorData);
    }
}

// 削除
async function deleteTask(taskId) {
    const res = await authFetch(
        `/api/tasks/${taskId}/`,
        {
            method: "DELETE",
        }
    );

    if (!confirm("削除しますか？")) {
    return;
    }

    if (res.ok) {
        loadTasks();
    }
}



// btn処理
function enterEditMode() {

    document.getElementById("submit-btn")
        .textContent = "更新";
    
    document.getElementById("cancel-edit-btn")
        .hidden = false;
}

function exitEditMode() {
    editingTaskId = null;

    document.getElementById("task-form").reset();

    document.getElementById("submit-btn")
        .textContent = "作成";
    
    document.getElementById("cancel-edit-btn")
        .hidden = true;
}







// CSRF取得
        function getCookie(name) {
          let cookieValue = null;
          if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
              cookie = cookie.trim();
              if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
              }
            }
          }
          return cookieValue;
        }