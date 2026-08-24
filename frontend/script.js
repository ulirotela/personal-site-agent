// Nav background/blur toggle, driven by scroll position. Only used on
// index.html — blog pages don't include this file (their nav is styled
// permanently "on" via body.blog-page in styles.css). Scroll-to-top is
// handled by the mascot button (onclick, in index.html), so there's no
// separate #back-to-top element anymore.

const API_BASE =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://localhost:8000"
    : "https://personal-site-agent.onrender.com";

const nav = document.getElementById("nav");

const threadId = localStorage.getItem("threadId") || crypto.randomUUID();
localStorage.setItem("threadId", threadId);

window.addEventListener("scroll", () => {
  const scrolled = window.scrollY > 20;
  nav.classList.toggle("scrolled", scrolled);
});

// --- In-page nav links (#expertise, #work, etc.) scroll to the section
// manually instead of letting the browser jump via the URL hash — that's
// what keeps #expertise/#work/#experience/#contact out of the address bar.
document.querySelectorAll('.nav-links a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    const target = document.getElementById(link.getAttribute("href").slice(1));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth" });
    history.replaceState(null, "", window.location.pathname);
  });
});

// Same idea, but for when the page *loads* with a #hash already in the URL
// — e.g. clicking "Contact" from a blog page navigates to "../#contact",
// a real page load, not a click we can intercept. Scroll there, then strip
// the hash so it doesn't linger in the address bar.
if (window.location.hash) {
  const target = document.getElementById(window.location.hash.slice(1));
  if (target) {
    target.scrollIntoView();
    history.replaceState(null, "", window.location.pathname);
  }
}

// --- Chat widget JS goes here---

const chatToggle = document.getElementById("chat-toggle");
const chatPanel = document.getElementById("chat-panel");

//-- submit form
const chatForm = document.getElementById("chat-form")
const chatInput = document.getElementById("chat-input")
const chatMessages = document.getElementById("chat-messages")

// The agent already remembers past messages server-side (Postgres, keyed by
// threadId) even after a full page reload — but the visible chat bubbles
// don't, since they're just DOM elements that get wiped on reload. The
// first time the panel opens, fetch the saved history and repaint it so
// the UI catches up to what the agent already knows.
let historyLoaded = false;

chatToggle.addEventListener("click", () => {
  chatPanel.classList.toggle("open");

  if (chatPanel.classList.contains("open") && !historyLoaded) {
    historyLoaded = true;
    loadHistory();
  }
})

function loadHistory() {
  fetch(`${API_BASE}/chat/history/${threadId}`)
    .then((response) => {
      if (!response.ok) throw new Error("Server error");
      return response.json();
    })
    .then((data) => {
      data.messages.forEach((msg) => addMessage(msg.content, msg.role));
    })
    .catch(() => {
      // No previous history, or the request failed — chat just starts
      // empty, same as before this feature existed.
    });
}

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





