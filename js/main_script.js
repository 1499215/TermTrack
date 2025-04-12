
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