# frontend/styles.py
STYLES = """
<style>
.main { 
    padding: 2rem; 
    max-width: 1200px; 
    margin: 0 auto; 
}
/* Button Styling */
.stButton button {
    width: 100%;
    border-radius: 30px;  /* Softer roundness for modern look */
    padding: 0.75rem 1.5rem;  /* Slightly increased for better touch interaction */
    background-color: #90D4B7;  /* Softer red-orange for a fresh and vibrant look */
    color: white;
    font-weight: bold;  /* Added bold text for better readability */
    border: none;
    margin-top: 1rem;
    transition: all 0.3s ease-in-out;  /* Smooth transition for hover effect */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  /* Subtle shadow for a floating effect */
}

.stButton button:hover {
    background-color: #78C4A5;  /* Slightly darker tone for hover */
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);  /* Enhanced shadow on hover */
    transform: translateY(-3px);  /* Slight upward shift on hover for interactivity */
    color: white;  /* White text on hover */

}

/* Message Box Styling */
.message {
    padding: 1.5rem;  /* Increased padding for better readability */
    border-radius: 12px;  /* Softer roundness for a modern touch */
    margin: 1rem 0;
    background-color: #f9f9f9;  /* Light background for contrast */
    color: #333;  /* Dark text for readability */
    border: 1px solid #ddd;  /* Subtle border for definition */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
}

/* Add an animation for messages */
@keyframes fadeIn {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.message {
    animation: fadeIn 0.5s ease-in-out;
}

.success-message {
    background-color: #E8F5E9;
    border: 1px solid #4CAF50;
}
.error-message {
    background-color: #FFEBEE;
    border: 1px solid #EF5350;
}
</style>


"""

