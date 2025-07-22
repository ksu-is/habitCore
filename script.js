console.log("✅ script.js is running");

const API_URL = "http://localhost:3000/api/habits";

const habitForm = document.getElementById("habitForm");
const habitInput = document.getElementById("habitInput");
const habitList = document.getElementById("habitList");

async function loadHabits() {
  const res = await fetch(API_URL);
  const habits = await res.json();
  habitList.innerHTML = "";

  habits.forEach(habit => {
    const li = document.createElement("li");

    // Move calendar map logic outside the template
    const days = ["Su", "M", "Tu", "W", "Th", "F", "Sa"];  // Sunday = index 0
const calendarHTML = (habit.calendar || []).map((marked, index) => {
  const day = days[index];
  return `<span class="day ${marked ? "marked" : ""}">${day}</span>`;
}).join("");


    li.innerHTML = `
      <div>
        <strong>${habit.name}</strong> <em>(${habit.category})</em> - 🔥 Streak: ${habit.streak}<br>
        ${habit.badge ? `<span>${habit.badge}</span><br>` : ""}
        ${habit.message ? `<div class="habit-message"><em>${habit.message}</em></div>` : ""}

        <div class="calendar">${calendarHTML}</div>

        <div class="progress-container">
          <div class="progress-bar" style="width: ${Math.min((habit.streak / 14) * 100, 100)}%"></div>
        </div>
        <small>${habit.streak}/14 days</small>
      </div>
      <button onclick="completeHabit(${habit.id})">✔️</button>
      
    `;

    habitList.appendChild(li);
  });
}

habitForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = habitInput.value;
  const category = document.getElementById("habitCategory").value;
  
  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, category })
  });

  habitInput.value = "";
  document.getElementById("habitCategory").value = "";
  loadHabits();
});
async function completeHabit(id) {
  await fetch(`${API_URL}/${id}/complete`, { method: "POST" });
  loadHabits();
  loadStats();
}

async function loadStats() {
  const res = await fetch("http://localhost:3000/api/stats");
  const stats = await res.json();
  const statBox = document.getElementById("habitStats");
  statBox.innerText = `✅ ${stats.completedToday} of ${stats.totalHabits} habits completed today`;
}
loadHabits();
loadStats();