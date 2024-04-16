document.addEventListener("DOMContentLoaded", function() {
    let transcription = ''; // Variable to store the transcribed text

    // Event listener for the Record button
    document.getElementById('recordBtn').addEventListener('click', function() {
        fetch('/record_audio', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.partial_text) {
                    transcription += data.partial_text + ' '; // Append partial text to transcription
                    document.getElementById('status').innerText = transcription;
                }
            })
            .catch(error => console.error('Error:', error));
    });

    // Event listener for the Finish button
    document.getElementById('finishBtn').addEventListener('click', function() {
        fetch('/translate_and_speak', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'  // Set the content type to JSON
            },
            body: JSON.stringify({ 'transcribed_text': transcription })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);  // Check the response data in the console
            if (data.message) {
                document.getElementById('status').innerText = data.message;
            } else if (data.error) {
                document.getElementById('status').innerText = data.error;
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
