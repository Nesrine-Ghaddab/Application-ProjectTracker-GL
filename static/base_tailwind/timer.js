async function startSession() {
  const title = document.querySelector("#title").value;
  const study = document.querySelector("#study_minutes").value;
  const rest = document.querySelector("#break_minutes").value;

  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const res = await fetch("/api/sessions/start/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      title: title,
      planned_minutes: study,
      break_minutes: rest,
    }),
  });
  if (res.ok) {
    const data = await res.json();
    console.log("Session démarrée:", data);
    localStorage.setItem("session_id", data.session_id);
  } else {
    alert("Erreur au démarrage de la session");
  }
}

async function stopSession() {
  const id = localStorage.getItem("session_id");
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const res = await fetch("/api/sessions/stop/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ session_id: id }),
  });
  if (res.ok) {
    const data = await res.json();
    console.log("Session stoppée:", data);
  }
}
