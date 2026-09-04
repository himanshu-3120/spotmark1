/**
 * Athena - Tech Empowerment Interactivity
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // ==========================================
    // 1. Header Scroll Effect
    // ==========================================
    const header = document.getElementById('main-header');
    
    const handleScroll = () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };
    
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Trigger once on load

    // ==========================================
    // 2. Mobile Menu Navigation
    // ==========================================
    const mobileNavToggle = document.getElementById('mobile-nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    if (mobileNavToggle && navMenu) {
        mobileNavToggle.addEventListener('click', () => {
            mobileNavToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close mobile menu when a link is clicked
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileNavToggle.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }

    // ==========================================
    // 3. Program Tab Switcher
    // ==========================================
    const tabButtons = document.querySelectorAll('.menu-tab-btn');
    const tabContents = document.querySelectorAll('.menu-tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            // Deactivate all buttons
            tabButtons.forEach(b => b.classList.remove('active'));
            // Hide all tab contents
            tabContents.forEach(content => content.classList.remove('active'));

            // Activate current button and tab content
            btn.classList.add('active');
            const targetContent = document.getElementById(`tab-content-${targetTab}`);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });

    // ==========================================
    // 4. Testimonials Slider
    // ==========================================
    const slides = document.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.getElementById('prev-testimonial');
    const nextBtn = document.getElementById('next-testimonial');
    
    let currentSlide = 0;
    let slideInterval;

    const showSlide = (index) => {
        if (slides.length === 0) return;

        // Handle wrap around
        if (index >= slides.length) currentSlide = 0;
        else if (index < 0) currentSlide = slides.length - 1;
        else currentSlide = index;

        // Hide all slides
        slides.forEach(slide => slide.classList.remove('active'));
        // Deactivate all dots
        dots.forEach(dot => dot.classList.remove('active'));

        // Show current slide & dot
        slides[currentSlide].classList.add('active');
        if (dots[currentSlide]) {
            dots[currentSlide].classList.add('active');
        }
    };

    const nextSlide = () => {
        showSlide(currentSlide + 1);
    };

    const prevSlide = () => {
        showSlide(currentSlide - 1);
    };

    // Auto-slide setup
    const startSlideShow = () => {
        if (slides.length > 0) {
            slideInterval = setInterval(nextSlide, 8000);
        }
    };

    const resetSlideShow = () => {
        clearInterval(slideInterval);
        startSlideShow();
    };

    if (prevBtn && nextBtn) {
        prevBtn.addEventListener('click', () => {
            prevSlide();
            resetSlideShow();
        });

        nextBtn.addEventListener('click', () => {
            nextSlide();
            resetSlideShow();
        });

        dots.forEach(dot => {
            dot.addEventListener('click', () => {
                const index = parseInt(dot.getAttribute('data-index'));
                showSlide(index);
                resetSlideShow();
            });
        });

        startSlideShow();
    }

    // ==========================================
    // 5. Application Form & Success Feedback
    // ==========================================
    const resForm = document.getElementById('reservation-form');
    const successScreen = document.getElementById('reservation-success');
    
    const summaryName = document.getElementById('summary-name');
    const summaryEmail = document.getElementById('summary-email');
    const summaryRole = document.getElementById('summary-role');
    const summaryTrack = document.getElementById('summary-track');
    const summaryRef = document.getElementById('summary-ref');
    const resetResBtn = document.getElementById('btn-reset-res');

    if (resForm && successScreen) {
        resForm.addEventListener('submit', (e) => {
            e.preventDefault();

            // Gather inputs
            const name = document.getElementById('res-name').value;
            const email = document.getElementById('res-email').value;
            const role = document.getElementById('res-role').value;
            const track = document.getElementById('res-track').value;

            // Generate mock registration code
            const randomCode = 'ATH-' + Math.floor(1000 + Math.random() * 9000);

            // Set confirmation details
            if (summaryName) summaryName.textContent = name;
            if (summaryEmail) summaryEmail.textContent = email;
            if (summaryRole) summaryRole.textContent = role;
            if (summaryTrack) summaryTrack.textContent = track;
            if (summaryRef) summaryRef.textContent = randomCode;

            // Animate transition (hide form, show confirmation)
            resForm.classList.add('hide');
            successScreen.classList.remove('hide');
            
            // Scroll to the application section nicely
            document.getElementById('join').scrollIntoView({ behavior: 'smooth' });
        });

        if (resetResBtn) {
            resetResBtn.addEventListener('click', () => {
                resForm.reset();
                successScreen.classList.add('hide');
                resForm.classList.remove('hide');
            });
        }
    }

    // ==========================================
    // 6. Interactive Bar Chart Animation
    // ==========================================
    const barChart = document.getElementById('placement-bar-chart');
    const bars = document.querySelectorAll('.bar');

    if (barChart && bars.length > 0) {
        const animateBars = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    bars.forEach(bar => {
                        const targetHeight = bar.getAttribute('data-height');
                        bar.style.height = `${targetHeight}%`;
                    });
                    observer.unobserve(entry.target); // Trigger once
                }
            });
        }, {
            threshold: 0.15
        });

        animateBars.observe(barChart);
    }

    // ==========================================
    // 7. Interactive Donut Chart Segment & Legend
    // ==========================================
    const segments = document.querySelectorAll('.donut-segment');
    const legendItems = document.querySelectorAll('.legend-item');
    const donutPercent = document.getElementById('donut-percent');
    const donutLabel = document.getElementById('donut-label');

    const updateDonutCenter = (value, label, index) => {
        if (donutPercent && donutLabel) {
            donutPercent.textContent = value;
            donutLabel.textContent = label;
        }

        // Highlight active legend item
        legendItems.forEach(item => {
            if (parseInt(item.getAttribute('data-index')) === index) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        // Add visual scale / highlight to active segment
        segments.forEach(seg => {
            if (parseInt(seg.getAttribute('data-index')) === index) {
                seg.style.strokeWidth = '18';
                seg.style.filter = 'drop-shadow(0 0 8px rgba(139, 92, 246, 0.5))';
            } else {
                seg.style.strokeWidth = '14';
                seg.style.filter = 'none';
            }
        });
    };

    if (segments.length > 0 && legendItems.length > 0) {
        // Initialize default view to first slice (Software Engineering, 40%)
        updateDonutCenter('40%', 'Software Eng.', 0);

        segments.forEach(seg => {
            seg.addEventListener('mouseenter', () => {
                const value = seg.getAttribute('data-value');
                const label = seg.getAttribute('data-label');
                const index = parseInt(seg.getAttribute('data-index'));
                updateDonutCenter(value, label, index);
            });
        });

        legendItems.forEach(item => {
            item.addEventListener('mouseenter', () => {
                const index = parseInt(item.getAttribute('data-index'));
                const matchingSeg = document.querySelector(`.donut-segment[data-index="${index}"]`);
                if (matchingSeg) {
                    const value = matchingSeg.getAttribute('data-value');
                    const label = matchingSeg.getAttribute('data-label');
                    updateDonutCenter(value, label, index);
                }
            });
        });
    }

    // ==========================================
    // 8. 3D Card Tilt Effect
    // ==========================================
    const cards3d = document.querySelectorAll('.card-3d');

    cards3d.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; // x position within the element
            const y = e.clientY - rect.top;  // y position within the element
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Calculate rotation angle (max 12 degrees)
            const rotateX = -((y - centerY) / centerY) * 12;
            const rotateY = ((x - centerX) / centerX) * 12;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
    });

    // ==========================================
    // 9. Scroll Reveal Intersection Observer
    // ==========================================
    const revealElements = document.querySelectorAll('.reveal');

    const revealOnScroll = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Stop observing after it reveals
            }
        });
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(el => {
        revealOnScroll.observe(el);
    });
});
