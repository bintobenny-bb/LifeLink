// ========================================
// LIFELINK AI CHATBOT
// ========================================

const toggle = document.getElementById("chatbot-toggle");
const chatWindow = document.getElementById("chatbot-window");
const closeBtn = document.getElementById("chatbot-close");

const chatForm = document.getElementById("chatbot-form");
const chatInput = document.getElementById("chatbot-input");
const chatMessages = document.getElementById("chatbot-messages");
const typingIndicator = document.getElementById("typing-indicator");

// Open chatbot
toggle.addEventListener("click", function () {
    chatWindow.style.display = "flex";
});

// Close chatbot
closeBtn.addEventListener("click", function () {
    chatWindow.style.display = "none";
});

// Add message to chat
function addMessage(message, sender) {
    const messageDiv = document.createElement("div");

    messageDiv.className = sender === "user"
        ? "user-message"
        : "bot-message";

    const messageText = document.createElement("div");

    if (sender === "bot" && typeof marked !== "undefined") {
        messageText.innerHTML = DOMPurify.sanitize(marked.parse(message));
    } else {
        messageText.textContent = message;
    }

    const timestamp = document.createElement("span");
    timestamp.className = "message-time";

    timestamp.textContent = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    messageDiv.appendChild(messageText);
    messageDiv.appendChild(timestamp);

    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: "smooth"
    });
}

// Handle message submission
chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const message = chatInput.value.trim();

    if (!message) return;

    addMessage(message, "user");
    chatMessages.appendChild(typingIndicator);
    chatInput.value = "";

    chatWindow.style.display = "flex";

    // Send message to Django AI backend
    try {
        typingIndicator.style.display = "flex";
        chatForm.querySelector("button[type='submit']").disabled = true;

        const response = await fetch("/api/ai/chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();
        typingIndicator.style.display = "none";
        chatInput.disabled = false;
        chatForm.querySelector("button[type='submit']").disabled = false;
        chatInput.focus();

        if (data.success) {
            addMessage(data.response, "bot");
        } else {
            addMessage("Sorry, I couldn't process your message.", "bot");
        }

    } catch (error) {
        typingIndicator.style.display = "none";
        chatInput.disabled = false;
        chatForm.querySelector("button[type='submit']").disabled = false;
        console.error("Chatbot error:", error);
        addMessage("Unable to connect to LifeLink AI. Please try again.", "bot");
    }
});