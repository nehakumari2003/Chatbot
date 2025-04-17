let dark = true;

function toggleTheme() {
  document.body.classList.toggle("dark");
  document.body.classList.toggle("light");

  const emoji = document.getElementById("themeToggle");
  dark = !dark;
  emoji.innerText = dark ? "🌙" : "☀️";
}

async function sendMessage() {
  const input = document.getElementById("userInput");
  const text = input.value.trim();
  if (!text) return;

  const chat = document.getElementById("messages");
  chat.innerHTML += `<div class="bubble user">🧑: ${text}</div>`;
  input.value = "";

  const res = await fetch("http://localhost:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text }),
  });

  const data = await res.json();
  chat.innerHTML += `<div class="bubble bot">🤖 Neo: ${data.response}</div>`;
}

document.getElementById("pdfInput").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("pdf", file);

  const res = await fetch("http://localhost:5000/upload_pdf", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  alert(data.message);
});

// ✅ Clear PDF context on page load
window.addEventListener('load', async () => {
  try {
    const res = await fetch("http://localhost:5000/reset_pdf", {
      method: "POST"
    });
    const data = await res.json();
    console.log("🧹 Reset PDF:", data.message);
  } catch (err) {
    console.error("❌ Failed to reset PDF context:", err);
  }
});
