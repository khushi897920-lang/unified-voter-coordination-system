// Base backend URL
// In local demo this runs on localhost
const BASE_URL = "http://127.0.0.1:8000";

// Helper function to display output
function showOutput(data) {
    document.getElementById("output").textContent =
        JSON.stringify(data, null, 2);
}

// Register a new voter
async function registerVoter() {
    const ref = document.getElementById("regRef").value;
    const state = document.getElementById("regState").value;

    // Simple validation to avoid empty calls
    if (!ref || !state) {
        alert("Please enter reference ID and state");
        return;
    }

    try {
        const response = await fetch(
            `${BASE_URL}/register?reference_id=${ref}&state=${state}`,
            { method: "POST" }
        );
        const data = await response.json();
        showOutput(data);
    } catch (error) {
        showOutput({ error: "Backend not reachable" });
    }
}

// Request interstate migration
async function requestMigration() {
    const ref = document.getElementById("migRef").value;
    const newState = document.getElementById("newState").value;

    if (!ref || !newState) {
        alert("Please enter required fields");
        return;
    }

    try {
        const response = await fetch(
            `${BASE_URL}/migration/request?reference_id=${ref}&new_state=${newState}`,
            { method: "POST" }
        );
        const data = await response.json();
        showOutput(data);
    } catch (error) {
        showOutput({ error: "Migration service unavailable" });
    }
}

// Cast vote (one voter, one vote)
async function castVote() {
    const ref = document.getElementById("voteRef").value;

    if (!ref) {
        alert("Reference ID required");
        return;
    }

    try {
        const response = await fetch(
            `${BASE_URL}/vote/cast?reference_id=${ref}`,
            { method: "POST" }
        );
        const data = await response.json();
        showOutput(data);
    } catch (error) {
        showOutput({ error: "Voting service unavailable" });
    }
}
// Check voter status
async function checkStatus() {
    const ref = document.getElementById("statusRef").value;
}