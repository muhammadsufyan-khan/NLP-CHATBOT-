async function sendMessage() {
    const input = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    
    // Khali message ko rokne ke liye
    if (input.value.trim() === "") return;

    // 1. User ka message screen par dikhayein
    chatWindow.innerHTML += `<div class="message user">${input.value}</div>`;
    
    const userText = input.value;
    input.value = ""; // Input box ko khali kar dein

    try {
        // 2. Backend se connect karein (URL aur Body ko update kiya gaya hai)
        const response = await fetch('http://localhost:8000/api/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                question: userText,
                user_id: "sufyan_student" // Backend ChatRequest model ke mutabiq
            })
        });
        
        // Agar response sahi nahi aata
        if (!response.ok) {
            throw new Error('Server error');
        }

        const data = await response.json();

        // 3. AI ka jawab screen par dikhayein
        // Backend 'answer' key bhejta hai
        chatWindow.innerHTML += `<div class="message bot">${data.answer}</div>`;
        
    } catch (error) {
        console.error("Error:", error);
        chatWindow.innerHTML += `<div class="message bot" style="color: red;">Error: Backend connect nahi ho saka. Check karein 'python app.py' chal raha hai ya nahi.</div>`;
    }
    
    // Chat ko auto-scroll karein niche ki taraf
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Enter key dabane par message send ho jaye
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
