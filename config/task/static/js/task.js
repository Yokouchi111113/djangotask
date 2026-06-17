document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access");

    if (!token) {
        location.href = "/signin/";
        return;
    }

    // loadTasks() など
});


document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access");

    if (!token) {
        location.href = "/signin/";
        return;
    }

    loadTasks();
});    




//一覧取得
async function loadTasks() {
    const res = await authFetch("/api/tasks/");
    const data = await res.json();

    console.log(data);
}

async function loadTasks() {
    const res = await authFetch("/api/tasks/");
    const tasks = await res.json();

    const taskList = document.getElementById("task-list");
    taskList.innerHTML = "";

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

// 作成
document
    .getElementById("task-form")
    .addEventListener("submit", createTask);

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
        loadTasks();
    }
}