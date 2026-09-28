async function askAI() {
    const question = document.getElementById("question").value.trim();
    const answerBox = document.getElementById("answer");

    if (!question) {
        answerBox.innerText = "Please enter a question.";
        return;
    }

    answerBox.innerText = "Thinking...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        // Convert simple Markdown to clean HTML
        let answer = data.answer;

        answer = answer
            .replace(/^### (.*)$/gm, "<h3>$1</h3>")
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
            .replace(/```python\n([\s\S]*?)```/g, "<pre><code>$1</code></pre>")
            .replace(/```([\s\S]*?)```/g, "<pre><code>$1</code></pre>")
            .replace(/\n/g, "<br>");

        answerBox.innerHTML = answer;

    } catch (error) {
        answerBox.innerText = "Something went wrong. Please try again.";
        console.error(error);
    }
}