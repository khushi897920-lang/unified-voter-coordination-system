const BASE_URL = "http://127.0.0.1:8000";

function getRefId() {
  return document.getElementById("refId").value.trim();
}

function setOutput(message) {
  document.getElementById("output").innerText = message;
}

async function checkStatus() {
  const refId = getRefId();

  if (!refId) {
    setOutput("Please enter Reference ID");
    return;
  }

  setOutput("Checking status...");

  try {
    const response = await fetch(`${BASE_URL}/reference/status/${refId}`);

    if (!response.ok) {
      throw new Error("Server error");
    }

    const data = await response.json();
    setOutput(`Status: ${JSON.stringify(data)}`);

  } catch (error) {
    setOutput("Error connecting to backend");
    console.error(error);
  }
}

async function castVote() {
  const refId = getRefId();

  if (!refId) {
    setOutput("Please enter Reference ID");
    return;
  }

  setOutput("Casting vote...");

  try {
    const response = await fetch(
      `${BASE_URL}/vote/cast/${refId}`,
      { method: "POST" }
    );

    if (!response.ok) {
      throw new Error("Vote failed");
    }

    const data = await response.json();
    setOutput(data.status || "Vote casted successfully");

  } catch (error) {
    setOutput("Vote failed");
    console.error(error);
  }
}
document.getElementById("checkStatusBtn").addEventListener("click", checkStatus);
document.getElementById("castVoteBtn").addEventListener("click", castVote);