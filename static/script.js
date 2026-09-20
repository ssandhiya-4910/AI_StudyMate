async function generateResponse() {
    const task = document.getElementById("task").value;
    const userInput = document.getElementById("userInput").value.trim();

    const generateBtn = document.getElementById("generateBtn");
    const loading = document.getElementById("loading");
    const resultBox = document.getElementById("resultBox");
    const result = document.getElementById("result");
    const errorBox = document.getElementById("errorBox");

    // Clear previous messages
    errorBox.classList.add("hidden");
    resultBox.classList.add("hidden");
    result.textContent = "";

    // Basic validation
    if (!userInput) {
        errorBox.textContent = "Please enter some text before generating a response.";
        errorBox.classList.remove("hidden");
        return;
    }

    // Show loading
    generateBtn.disabled = true;
    generateBtn.textContent = "Generating...";
    loading.classList.remove("hidden");

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                task: task,
                text: userInput
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        result.textContent = data.result;
        resultBox.classList.remove("hidden");

    } catch (error) {
        errorBox.textContent =
            error.message || "Unable to connect to the AI service.";
        errorBox.classList.remove("hidden");

    } finally {
        loading.classList.add("hidden");
        generateBtn.disabled = false;
        generateBtn.textContent = "✨ Generate AI Response";
    }
}
