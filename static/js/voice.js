document.addEventListener("DOMContentLoaded", function () {
    const voiceSearchBtn = document.getElementById('voice-search-btn');
    const languageSelect = document.getElementById('language-select');
    const positionInput = document.getElementById('profession');
    const locationInput = document.getElementById('location');

    // Check for browser support of SpeechRecognition API
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Your browser does not support the Speech Recognition API.');
        return;
    }

    // Initialize SpeechRecognition API
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';  // Default to English

    // Handle language change based on dropdown selection
    languageSelect.addEventListener('change', function () {
        recognition.lang = this.value;  // Change recognition language when the user selects a new language
    });

    // Handle the result from voice recognition
    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript.toLowerCase();
        console.log('Transcript:', transcript);

        // Split transcript based on language
        if (recognition.lang === 'hi-IN') {
            // For Hindi, split by "में" (which means "in")
            if (transcript.includes("में")) {
                const splitTranscript = transcript.split(" में ");
                positionInput.value = splitTranscript[0].trim();  // Job position
                locationInput.value = splitTranscript[1].trim();  // Location
            } else {
                positionInput.value = transcript;
            }
        } else if (recognition.lang === 'en-US') {
            // For English, split by "in"
            if (transcript.includes("in")) {
                const splitTranscript = transcript.split(" in ");
                positionInput.value = splitTranscript[0].trim();
                locationInput.value = splitTranscript[1].trim();
            } else {
                positionInput.value = transcript;
            }
        }

        // Optionally submit the form automatically
        
        document.getElementById('job-main-form').submit();
    };
    // Handle errors
    recognition.onerror = function (event) {
        console.error("Speech recognition error", event.error);
    };

    // Start speech recognition when voice search button is clicked
    voiceSearchBtn.addEventListener('click', function () {
        recognition.lang = languageSelect.value;  // Set the recognition language before starting
        recognition.start();
    });
});