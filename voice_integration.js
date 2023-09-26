document.getElementById("submit-button").addEventListener("click", async () => {
    const userInput = document.getElementById("user-input").value;
    const responseContainer = document.getElementById("response");
    
    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `user_input=${userInput}`
    });
    
    const data = await response.json();
    responseContainer.innerText = `ChatBot: ${data.response}`;
});

document.getElementById("voice-button").addEventListener("click", async () => {
    const responseContainer = document.getElementById("response");
    
    const response = await fetch("/voice-interaction", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    
    const data = await response.json();
    responseContainer.innerText = `ChatBot: ${data.response}`;
});
