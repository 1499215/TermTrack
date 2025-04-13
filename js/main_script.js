
        // Add card drag effect (basic implementation)
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mousedown', () => {
                card.style.transform = 'rotate(2deg)';
            });
            card.addEventListener('mouseup', () => {
                card.style.transform = 'none';
            });
        });

        // Animate testimonial cards on scroll
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    entry.target.style.opacity = 1;
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        });

        document.querySelectorAll('.testimonial-card').forEach(card => {
            card.style.opacity = 0;
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.5s ease-out';
            observer.observe(card);
        });
   


        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Add animation on scroll
        window.addEventListener('scroll', function() {
            const features = document.querySelectorAll('.feature-card');
            features.forEach(feature => {
                const position = feature.getBoundingClientRect();
                if(position.top < window.innerHeight) {
                    feature.style.opacity = '1';
                }
            });
        });


        // Update existing JavaScript
        // begining of "How It Works" section js
  function initializeTooltips() {
    const steps = document.querySelectorAll('.step');
    
    steps.forEach(step => {
      let tapTimer;
      const tooltip = step.querySelector('.step-tooltip');
      
      // Touch Events
      step.addEventListener('touchstart', (e) => {
        e.preventDefault();
        tapTimer = setTimeout(() => showTooltip(tooltip), 500);
      }, { passive: false });
  
      step.addEventListener('touchend', () => {
        clearTimeout(tapTimer);
        hideTooltip(tooltip);
      });
  
      // Click fallback
      step.addEventListener('click', (e) => {
        if(window.innerWidth > 768) return;
        tooltip.classList.toggle('active');
      });
    });
  
    function showTooltip(tooltip) {
      tooltip.style.opacity = '1';
      tooltip.style.visibility = 'visible';
    }
  
    function hideTooltip(tooltip) {
      tooltip.style.opacity = '0';
      tooltip.style.visibility = 'hidden';
    }

    

    // Update modal function
    function showModal(type) {
      const modal = document.getElementById('previewModal');
      const img = document.getElementById('modalImage');
      const loader = modal.querySelector('.loader');

      img.classList.remove('loaded');
      loader.style.display = 'block';

      img.onload = () => {
        img.classList.add('loaded');
        loader.style.display = 'none';
      };
    }
  }//end of how it works js

  // Signin Signup Authentication JS
        function showForm(formType) {
            document.querySelectorAll('.auth-form').forEach(form => {
                form.classList.remove('active');
            });
            document.querySelectorAll('.auth-switch button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            document.getElementById(`${formType}-form`).classList.add('active');
            event.target.classList.add('active');
        }

        function togglePassword(fieldId) {
            const passwordField = document.getElementById(fieldId);
            const toggleIcon = event.target;
            
            if(passwordField.type === 'password') {
                passwordField.type = 'text';
                toggleIcon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                passwordField.type = 'password';
                toggleIcon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        }

        // Password Strength Checker
        document.getElementById('signup-password').addEventListener('input', function(e) {
            const strengthBar = document.getElementById('strength-bar');
            const password = e.target.value;
            let strength = 0;

            if(password.match(/[A-Z]/)) strength++;
            if(password.match(/[0-9]/)) strength++;
            if(password.match(/[^A-Za-z0-9]/)) strength++;
            if(password.length >= 8) strength++;

            strengthBar.style.width = `${(strength/4)*100}%`;
            strengthBar.style.background = strength < 2 ? '#ff4444' : 
                                         strength < 4 ? '#ffbb33' : 
                                         '#00C851';
        });

        // Form Validation
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                // Add your backend integration here
                console.log('Form submitted:', this.id);
            });
        });




        // Handle Signup
document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        school_name: document.querySelector('#signup-form input[type="text"]').value,
        email: document.querySelector('#signup-form input[type="email"]').value,
        password: document.querySelector('#signup-form input[type="password"]').value
    };

    try {
        const response = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if(response.ok) {
            alert('Registration successful! Please login.');
            showForm('signin');
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert('Failed to connect to server');
    }
});

// Handle Login
document.getElementById('signin-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        email: document.querySelector('#signin-form input[type="email"]').value,
        password: document.querySelector('#signin-form input[type="password"]').value
    };

    try {
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if(response.ok) {
            localStorage.setItem('token', data.access_token);
            window.location.href = '/dashboard.html';
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert('Failed to connect to server');
    }
});
