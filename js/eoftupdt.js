// Student ID Generator
let studentCounter = 1;
function generateStudentID(classLevel) {
    const paddedCounter = studentCounter.toString().padStart(5, '0');
    return `B${classLevel}-${paddedCounter}`;
}

// Proficiency Calculator
function calculateProficiency(score) {
    if (score >= 80) return 'A';
    if (score >= 75) return 'P';
    if (score >= 70) return 'AP';
    if (score >= 65) return 'D';
    return 'B';
}

// School Days Calculator
function calculateSchoolDays() {
    const start = new Date(document.getElementById('termResumption').value);
    const end = new Date(document.getElementById('termVacation').value);
    const holidays = parseInt(document.getElementById('holidays').value) || 0;

    if (!start || !end || isNaN(start.getTime()) || isNaN(end.getTime())) {
        return 0; // Return 0 if dates are invalid
    }

    // Calculate total days including both resumption and vacation days
    const totalDays = Math.ceil((end - start) / (1000 * 3600 * 24)) + 1;

    // Count Saturdays and Sundays
    let weekendCount = 0;
    for (let date = new Date(start); date <= end; date.setDate(date.getDate() + 1)) {
        const day = date.getDay();
        if (day === 0 || day === 6) { // Sunday (0) or Saturday (6)
            weekendCount++;
        }
    }

    // Subtract weekends from total days
    const schoolDaysWithoutWeekends = totalDays - weekendCount;

    // Validate holidays
    if (holidays > schoolDaysWithoutWeekends) {
        alert('Error: Number of public holidays exceeds total school days.');
        return 0;
    }

    // Subtract public holidays
    const finalSchoolDays = schoolDaysWithoutWeekends - holidays;

    return finalSchoolDays;
}

// Real-time Calculations
document.getElementById('etaScore').addEventListener('input', function(e) {
    if (this.value < 1 || this.value > 100) {
        this.setCustomValidity('ETA must be between 1-100');
    } else {
        this.setCustomValidity('');
    }
});

document.querySelectorAll('.calculation-grid input').forEach(input => {
    input.addEventListener('input', updateCalculations);
});

function updateCalculations() {
    // SBA Calculation
    const sba = parseFloat(document.getElementById('sbaScore').value) || 0;
    const sbaFinal = (sba / 30 * 30).toFixed(2);
    document.getElementById('sbaCalculation').textContent = sbaFinal;

    // ETA Calculation
    const eta = parseFloat(document.getElementById('etaScore').value) || 0;
    const etaFinal = (eta * 0.7).toFixed(2);
    document.getElementById('etaCalculation').textContent = etaFinal;

    // Final Score
    const totalScore = parseFloat(sbaFinal) + parseFloat(etaFinal);
    document.getElementById('finalScore').textContent = `${totalScore.toFixed(2)}%`;
    document.getElementById('proficiencyLevel').textContent = calculateProficiency(totalScore);

    // School Days
    document.getElementById('totalSchoolDays').textContent = calculateSchoolDays();
}

// Student Records Table
function populateStudentTable(students) {
    const tbody = document.querySelector('#studentsTable tbody');
    tbody.innerHTML = '';
    
    students.forEach(student => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${generateStudentID(student.classLevel)}</td>
            <td>${student.name}</td>
            <td>B${student.classLevel}</td>
            <td>
                <button class="edit-btn" data-id="${student.id}">Update</button>
            </td>
        `;
        tbody.appendChild(row);
    });
    
    studentCounter = students.length + 1;
}

// Modal Handling
document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const studentId = this.dataset.id;
        // Fetch student data and populate modal
        openEditModal(studentId);
    });
});

function openEditModal(studentId) {
    // Add logic to fetch student data and populate form
    document.getElementById('editModal').style.display = 'block';
}