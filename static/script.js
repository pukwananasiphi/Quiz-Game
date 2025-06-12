document.addEventListener('DOMContentLoaded', () => {
    const quizForm = document.getElementById('quiz-form');
    const submitButton = document.getElementById('submit-answer');
    const feedbackDiv = document.getElementById('feedback');
    const explanationDiv = document.getElementById('explanation');
    const explanationText = document.getElementById('explanation-text');
    const nextQuestionButton = document.getElementById('next-question');
    const scoreSpan = document.getElementById('current-score');
    const radioOptions = document.querySelectorAll('input[name="option"]');

    
    const disableOptions = () => {
        radioOptions.forEach(option => option.disabled = true);
        submitButton.style.display = 'none';
        nextQuestionButton.style.display = 'block';
    };

   
    const initialAnsweredCorrectly = submitButton.style.display === 'none'; // Check if submit button is hidden by Jinja
    if (initialAnsweredCorrectly) {
        // If the submit button is hidden, it means the question was already answered correctly
        disableOptions();
        feedbackDiv.style.display = 'block';
        explanationDiv.style.display = 'block';
    }


    quizForm.addEventListener('submit', async (event) => {
        event.preventDefault(); 

        const formData = new FormData(quizForm);
        const selectedOption = formData.get('option');

        if (!selectedOption) {
            feedbackDiv.textContent = "Please select an option.";
            feedbackDiv.className = 'feedback incorrect';
            feedbackDiv.style.display = 'block';
            return;
        }

        try {
            const response = await fetch('/answer', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

           
            scoreSpan.textContent = result.current_score;

            feedbackDiv.style.display = 'block';
            if (result.is_correct) {
                feedbackDiv.textContent = 'Correct!';
                feedbackDiv.className = 'feedback correct';
                disableOptions(); // Disable options and show next question button
            } else {
                feedbackDiv.textContent = 'Incorrect, try again!';
                feedbackDiv.className = 'feedback incorrect';
                // Keep options enabled for retries
                // Keep submit button visible
            }

            
            explanationText.textContent = result.explanation;
            explanationDiv.style.display = 'block';

            // If the question was just answered correctly or already was, show next question button
            if (result.Youtubeed_correctly_now) {
                disableOptions();
            }

        } catch (error) {
            console.error('Error submitting answer:', error);
            feedbackDiv.textContent = 'An error occurred. Please try again.';
            feedbackDiv.className = 'feedback incorrect';
            feedbackDiv.style.display = 'block';
        }
    });

    nextQuestionButton.addEventListener('click', async () => {
        // This will trigger the backend to advance the question and redirect
        window.location.href = '/next_question';
    });
});