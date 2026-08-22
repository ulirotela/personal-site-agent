// Nav background/blur toggle + back-to-top button visibility, both driven
// by scroll position. Only used on index.html — blog pages don't include
// this file (their nav is styled permanently "on" via body.blog-page in
// styles.css, and they have no #back-to-top button).

const API_BASE =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://localhost:8000"
    : "https://personal-site-agent.onrender.com";

const nav = document.getElementById("nav");
const backToTop = document.getElementById("back-to-top");

const threadId= crypto.randomUUID();

window.addEventListener("scroll", () => {
  const scrolled = window.scrollY > 20;
  nav.classList.toggle("scrolled", scrolled);
  backToTop.classList.toggle("visible", window.scrollY > 400);
});

backToTop.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

// --- Chat widget JS goes here---

const chatToggle = document.getElementById("chat-toggle");
const chatPanel = document.getElementById("chat-panel");

chatToggle.addEventListener("click", ()=> {
  chatPanel.classList.toggle("open");
})

//-- submit form
const chatForm = document.getElementById("chat-form")
const chatInput = document.getElementById("chat-input")
const chatMessages = document.getElementById("chat-messages")

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const message = chatInput.value.trim();
  if(!message) return;
  chatInput.value = "";
  chatInput.disabled = true;
  addMessage(message, "user");
  const typing = showTyping();

  fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, thread_id: threadId }),
  })
    .then((response) => {
      if (!response.ok) throw new Error("Server error");
      return response.json();
    })
    .then((data) => {
      typing.remove();
      addMessage(data.response, "bot");
      chatInput.disabled = false;
      chatInput.focus();
    })
    .catch(() => {
      typing.remove();
      addMessage("Sorry, something went wrong. Please try again.", "bot");
      chatInput.disabled = false;
      chatInput.focus();
    });
});

//-- user message---
function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.className = `chat-msg chat-msg-${sender}`;
  msg.textContent = text;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

//-- showing typing
function showTyping() {
  const typing = document.createElement("div");
  typing.className = "chat-typing";
  typing.innerHTML = "<span></span><span></span><span></span>";
  chatMessages.appendChild(typing);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return typing;
}





