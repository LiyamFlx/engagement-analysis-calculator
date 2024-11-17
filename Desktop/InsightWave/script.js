const API_URL = 'https://engagement-analysis-calculator.onrender.com/analyze';

async function analyzeAudio(formData) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Failed to analyze audio');
        }

        const data = await response.json();
        console.log('Analysis results:', data);

        // Display results on the frontend
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to analyze the audio file. Please try again.');
    }
}
