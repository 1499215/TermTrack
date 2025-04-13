// Registration Form Handler
document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("Registration initiated");

    const formData = {
        school_name: document.querySelector('#signup-form input[type="text"]').value,
        email: document.querySelector('#signup-form input[type="email"]').value,
        password: document.querySelector('#signup-form input[type="password"]').value
    };

    console.log("Form data:", formData); // Verify data collection

    try {
        const response = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        console.log("Server response:", data); // Log server response

        if(response.ok) {
            alert('Registration successful! Please login.');
            showForm('signin');
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert('Failed to connect to server');
    }
});