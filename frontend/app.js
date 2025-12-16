async function rank() {
  const risk = parseFloat(document.getElementById("risk").value);
  const life = parseFloat(document.getElementById("life").value);

  const response = await fetch("/api/defects/rank", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      risk: risk,
      remaining_life: life
    })
  });

  const data = await response.json();
  document.getElementById("result").innerText =
    "Приоритет ремонта: " + data.priority_score;
}
