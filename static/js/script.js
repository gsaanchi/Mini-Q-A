async function fetchAnswer() {
    const query = document.getElementById("query").value;
    
    if (!query.trim()) {
        alert("Please enter a question!");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/generate_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch answer');
        }

        const data = await response.json();

        const answerElement = document.getElementById("answer");
        const sourcesList = document.getElementById("sourcesList");

        answerElement.innerText = data.answer; 
        sourcesList.innerHTML = ''; 

        // Append each source link to the sources list
        data.sources.forEach((source, index) => {
            const listItem = document.createElement("li");
            const link = document.createElement("a");
            link.href = source.link;
            link.target = "_blank"; // Open links in a new tab
            link.innerText = `${index + 1}. ${source.title}`;
            listItem.appendChild(link);
            sourcesList.appendChild(listItem);
        });

    } catch (error) {
        console.error('Error:', error);
        alert("There was an error retrieving the answer. Please try again.");
    }
}