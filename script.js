const contactForm = document.getElementById("contactForm");
const formMessage = document.getElementById("formMessage");

contactForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const formData = new FormData(contactForm);

    try {

        const response = await fetch("http://127.0.0.1:5000/contact", {
            method: "POST",
            body: formData
        });

        const result = await response.text();

        formMessage.textContent = "Message sent successfully! 💗";
        formMessage.style.color = "#ff4fd8";

        contactForm.reset();

    } catch (error) {

        formMessage.textContent = "Something went wrong. Please try again.";
        formMessage.style.color = "red";

    }

});




















function showVideo(thumbId, videoId) {

    const thumbnail = document.getElementById(thumbId);
    const video = document.getElementById(videoId);

    if (thumbnail) {
        thumbnail.style.display = "none";
    }

    if (video) {
        video.style.display = "block";
    }
}







/* =========================================
   PROFESSIONAL VIDEO POPUP
========================================= */

function openVideo(videoURL) {

    const popup = document.getElementById("videoPopup");

    const frame = document.getElementById("videoPopupFrame");

    frame.src = videoURL;

    popup.classList.add("active");

    document.body.style.overflow = "hidden";
}


function closeVideo() {

    const popup = document.getElementById("videoPopup");

    const frame = document.getElementById("videoPopupFrame");

    frame.src = "";

    popup.classList.remove("active");

    document.body.style.overflow = "";
}


/* CLICK OUTSIDE TO CLOSE */

document.getElementById("videoPopup").addEventListener(
    "click",
    function(event) {

        if (event.target === this) {
            closeVideo();
        }

    }
);


/* ESC KEY TO CLOSE */

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Escape") {
            closeVideo();
        }

    }
);









async function sendAIMessage() {

    const input = document.getElementById("aiInput");
    const messages = document.getElementById("aiMessages");

    const userMessage = input.value.trim();

    if (!userMessage) return;

    // Show user message
    messages.innerHTML += `
        <div class="ai-message">
            <span class="ai-icon">👤</span>
            <div>
                <strong>You</strong>
                <p>${userMessage}</p>
            </div>
        </div>
    `;

    input.value = "";

    // Temporary loading message
    const loading = document.createElement("div");
    loading.className = "ai-message ai-bot";
    loading.innerHTML = `
        <span class="ai-icon">🤖</span>
        <div>
            <strong>Sai AI</strong>
            <p>Thinking...</p>
        </div>
    `;

    messages.appendChild(loading);

    try {

         const response = await fetch("https://divine-moon-79fc.leka6084.workers.dev/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: userMessage
            })
        });

        const data = await response.json();
        console.log("AI RESPONSE:", data);

        loading.querySelector("p").textContent =
            data.reply || "Sorry, I couldn't answer that.";
    //    if (data.video_id) {
    //        console.log("VIDEO ID:", data.video_id); 

    //     const videoURL =
    //         "https://www.youtube.com/embed/" +
    //          data.video_id +
    //          "?autoplay=1&mute=1&rel=0";
    //         openVideo(videoURL);
    //     }
   // Display multiple video buttons
if (Array.isArray(data.videos) && data.videos.length > 0) {

    const videoContainer = document.createElement("div");
    videoContainer.className = "ai-video-list";

    data.videos.forEach((video) => {

        const button = document.createElement("button");
        button.type = "button";
        button.className = "ai-video-card";
        button.textContent = "▶ " + video.title;

        button.addEventListener("click", () => {
            const videoURL =
                "https://www.youtube.com/embed/" +
                encodeURIComponent(video.video_id) +
                "?autoplay=1&rel=0&playsinline=1";

            openVideo(videoURL);
        });

        videoContainer.appendChild(button);
    });

    loading.appendChild(videoContainer);

} else if (data.video_id) {

    const videoURL =
        "https://www.youtube.com/embed/" +
        encodeURIComponent(data.video_id) +
        "?autoplay=1&rel=0&playsinline=1";

    openVideo(videoURL);
}

    } catch (error) {

        loading.querySelector("p").textContent =
            "AI service is currently unavailable.";

        console.error(error);
    }

    messages.scrollTop = messages.scrollHeight;
}

document.getElementById("aiInput")?.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        sendAIMessage();
    }

});