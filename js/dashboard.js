document.addEventListener('DOMContentLoaded', () => {
    const subjectsList = document.getElementById('subjectsList');
    const addSubjectBtn = document.getElementById('addSubject');
    const subjectTemplate = document.querySelector('.subject-template');
    const subjectError = document.getElementById('subjectError');

    // Add Subject
    addSubjectBtn.addEventListener('click', () => {
        const newSubject = subjectTemplate.cloneNode(true);
        newSubject.style.display = 'block';
        newSubject.querySelector('.remove-subject').addEventListener('click', () => {
            newSubject.remove();
            validateSubjects();
        });
        subjectsList.appendChild(newSubject);
    });

    // Validation
    function validateSubjects() {
        const subjects = Array.from(document.querySelectorAll('.subject-name'));
        const uniqueSubjects = new Set();
        
        subjectError.textContent = '';
        
        subjects.forEach(input => {
            const value = input.value.trim();
            if(value) {
                if(uniqueSubjects.has(value.toLowerCase())) {
                    input.classList.add('error');
                    subjectError.textContent = 'Duplicate subjects found!';
                } else {
                    uniqueSubjects.add(value.toLowerCase());
                    input.classList.remove('error');
                }
            }
        });
        
        return uniqueSubjects.size > 0 && subjectError.textContent === '';
    }

    // Form Submission
    document.querySelector('.registration-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if(!validateSubjects()) return;

        const formData = {
            bioData: {
                studentName: document.getElementById('studentName').value,
                studentClass: document.getElementById('studentClass').value,
                resumptionDate: document.getElementById('resumptionDate').value,
                term: document.getElementById('term').value,
                circuit: document.getElementById('circuit').value,
                district: document.getElementById('district').value
            },
            subjects: Array.from(document.querySelectorAll('.subject-item')).map(item => ({
                name: item.querySelector('.subject-name').value,
                maxScore: item.querySelector('.max-score').value
            }))
        };

        try {
            const response = await fetch('/api/registrations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(formData)
            });

            if(response.ok) {
                alert('Registration saved successfully!');
                // Reset form or redirect
            } else {
                const error = await response.json();
                alert(`Error: ${error.message}`);
            }
        } catch (error) {
            console.error('Submission error:', error);
            alert('Failed to save registration');
        }
    });
});