const baseURL = "http://127.0.0.1:8000/";
async function updateQuestionStatus(questionId, statusValue) {
    const url = `${baseURL}dsa-tracker/update_status/${questionId}/`;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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
}


async function updateQuestionURL(questionId) {
    const url = `${baseURL}dsa-tracker/update_url/${questionId}/`
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
        circle.style.marginLeft = isDarkMode ? "-20px" : "0px";
    });

    // Load saved theme on page load
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        circle.style.marginLeft = "-20px";
    }
});