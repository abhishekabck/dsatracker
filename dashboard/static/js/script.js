const baseURL = "http://localhost:8000/dashboard/";
const loader = document.getElementById('page-loader');
let reloadStartTime = null;
let reloadTimeout = null;

function startReload() {
    loader.style.display = "flex";
    loader.style.zIndex = "1000";
    reloadStartTime = Date.now();

    // Clear any previous timeout
    if (reloadTimeout) {
        clearTimeout(reloadTimeout);
        reloadTimeout = null;
    }
}

function stopReload() {
    const elapsed = Date.now() - reloadStartTime;
    const minDuration = 1000; // 1 seconds

    if (elapsed >= minDuration) {
        // Task took longer than 3s → stop immediately
        loader.style.display = "none";
        loader.style.zIndex = "-1000";
    } else {
        // Task finished early → wait until 3s total
        const remaining = minDuration - elapsed;
        reloadTimeout = setTimeout(() => {
            loader.style.display = "none";
            loader.style.zIndex = "-1000";
            reloadTimeout = null;
        }, remaining);
    }
}
async function updateQuestionStatus(questionId, statusValue) {
    const url = `${baseURL}update_status/${questionId}/`;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    await startReload();
    try {
        const response = await fetch(url, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({ status: statusValue })
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Updated:", data);
        } else {
            console.error("Error:", response.status, response.statusText);
        }
    } catch (error) {
        console.error("Network error:", error);
    }
    stopReload();
}


async function updateQuestionURL(questionId) {
    const url = `${baseURL}update_url/${questionId}/`
    const newURL = document.getElementById(`url-${questionId}`).value;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
        const response = await fetch(
            url, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({ url: newURL })
            }
        )

        if (response.ok) {
            const data = await response.json();
            document.getElementById(`question-link-${questionId}`).href = newURL;
            document.getElementById(`up-url-${questionId}`).style.display = "none";
            const problemCell = document.getElementById(`problem-${questionId}`);
            if (problemCell) {
                problemCell.setAttribute("colspan", "2");   // correct way
                problemCell.style.width = "70%";            // style works fine
            }
        } else {
            console.error("Error:", response.status, response.statusText);
        }
    } catch (error) {
        console.error("Network error:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("cm-btn");
    const circle = document.getElementById("cm-btn-circle");

    // Theme toggle handler
    btn.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");

        const isDarkMode = document.body.classList.contains("dark-mode");
        localStorage.setItem("theme", isDarkMode ? "dark" : "light");
        // circle.style.left = isDarkMode ? "2.5px" : "2.5px";
    });

    // Load saved theme on page load
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        // circle.style.left = "2.5px";
    }
});