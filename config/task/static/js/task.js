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
});    

// 表示
function renderTasks(tasks) {
    const taskList = document.getElementById("task-list");
    taskList.innerHTML = "";

    if (tasks.length === 0) {
    taskList.innerHTML = "<p>該当するタスクはありません。</p>";
    return;
    }


    tasks.forEach(task => {
        taskList.innerHTML += `
            <div class="task">
                <h3>${task.title}</h3>
                <p>${task.description}</p>
                <p>${task.status}</p>
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

    taskList.innerHTML = "";
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

// 作成
async function createTask(e) {
    e.preventDefault();

    const title =
        document.getElementById("title").value;

    const description =
        document.getElementById("description").value;

    const res = await authFetch("/api/tasks/", {
        method: "POST",
        body: JSON.stringify({
            title,
            description,
        }),
    });

    if (res.ok) {
        document.getElementById("task-form").reset();
        loadTasks();
    }
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