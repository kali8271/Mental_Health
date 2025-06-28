// Enhanced Mental Health Platform JavaScript

// Theme Management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme();
        this.setupThemeToggle();
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        localStorage.setItem('theme', this.currentTheme);
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme();
    }

    setupThemeToggle() {
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }
}

// Dashboard Analytics
class DashboardAnalytics {
    constructor() {
        this.init();
    }

    init() {
        this.loadMoodChart();
        this.loadActivityChart();
        this.updateStats();
        this.setupRealTimeUpdates();
    }

    loadMoodChart() {
        const moodCtx = document.getElementById('moodChart');
        if (!moodCtx) return;

        const moodData = this.getMoodData();
        new Chart(moodCtx, {
            type: 'line',
            data: {
                labels: moodData.labels,
                datasets: [{
                    label: 'Mood Trend',
                    data: moodData.values,
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 5,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    loadActivityChart() {
        const activityCtx = document.getElementById('activityChart');
        if (!activityCtx) return;

        const activityData = this.getActivityData();
        new Chart(activityCtx, {
            type: 'doughnut',
            data: {
                labels: activityData.labels,
                datasets: [{
                    data: activityData.values,
                    backgroundColor: [
                        '#4f46e5',
                        '#06b6d4',
                        '#10b981',
                        '#f59e0b',
                        '#ef4444'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    getMoodData() {
        // Mock data - replace with real API call
        return {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            values: [3, 4, 2, 5, 4, 3, 4]
        };
    }

    getActivityData() {
        // Mock data - replace with real API call
        return {
            labels: ['Exercise', 'Meditation', 'Social', 'Work', 'Sleep'],
            values: [30, 20, 15, 25, 10]
        };
    }

    updateStats() {
        const stats = this.getStats();
        Object.keys(stats).forEach(key => {
            const element = document.getElementById(`stat-${key}`);
            if (element) {
                element.textContent = stats[key];
            }
        });
    }

    getStats() {
        // Mock data - replace with real API call
        return {
            'mood-average': '3.8',
            'streak-days': '7',
            'sessions-completed': '12',
            'goals-achieved': '5'
        };
    }

    setupRealTimeUpdates() {
        // Update stats every 30 seconds
        setInterval(() => this.updateStats(), 30000);
    }
}

// Mood Tracker
class MoodTracker {
    constructor() {
        this.currentMood = null;
        this.init();
    }

    init() {
        this.setupMoodOptions();
        this.loadMoodHistory();
    }

    setupMoodOptions() {
        const moodOptions = document.querySelectorAll('.mood-option');
        moodOptions.forEach(option => {
            option.addEventListener('click', () => {
                this.selectMood(option);
            });
        });
    }

    selectMood(option) {
        // Remove previous selection
        document.querySelectorAll('.mood-option').forEach(opt => {
            opt.classList.remove('selected');
        });

        // Add selection to clicked option
        option.classList.add('selected');
        this.currentMood = option.dataset.mood;

        // Show mood details
        this.showMoodDetails();
    }

    showMoodDetails() {
        const detailsContainer = document.getElementById('mood-details');
        if (!detailsContainer) return;

        const moodData = this.getMoodData(this.currentMood);
        detailsContainer.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h3>${moodData.label}</h3>
                </div>
                <div class="card-body">
                    <p>${moodData.description}</p>
                    <div class="mt-4">
                        <h4>Suggested Activities:</h4>
                        <ul>
                            ${moodData.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    getMoodData(mood) {
        const moodData = {
            'very-sad': {
                label: 'Very Sad',
                description: 'It\'s okay to feel this way. Remember that difficult emotions are temporary.',
                suggestions: [
                    'Practice self-compassion',
                    'Reach out to a trusted friend',
                    'Try gentle physical activity',
                    'Consider talking to a professional'
                ]
            },
            'sad': {
                label: 'Sad',
                description: 'Acknowledge your feelings and be kind to yourself.',
                suggestions: [
                    'Listen to uplifting music',
                    'Take a warm bath or shower',
                    'Write in your journal',
                    'Do something creative'
                ]
            },
            'neutral': {
                label: 'Neutral',
                description: 'A balanced state. Consider what might help you feel more positive.',
                suggestions: [
                    'Try a new hobby',
                    'Connect with friends',
                    'Go for a walk',
                    'Practice gratitude'
                ]
            },
            'happy': {
                label: 'Happy',
                description: 'Great! Enjoy this positive energy and share it with others.',
                suggestions: [
                    'Celebrate your achievements',
                    'Help someone else',
                    'Plan something fun',
                    'Document this feeling'
                ]
            },
            'very-happy': {
                label: 'Very Happy',
                description: 'Wonderful! You\'re radiating positive energy.',
                suggestions: [
                    'Share your joy with others',
                    'Set new goals',
                    'Express gratitude',
                    'Create positive memories'
                ]
            }
        };
        return moodData[mood] || moodData['neutral'];
    }

    loadMoodHistory() {
        const historyContainer = document.getElementById('mood-history');
        if (!historyContainer) return;

        const history = this.getMoodHistory();
        historyContainer.innerHTML = history.map(entry => `
            <div class="card mb-4">
                <div class="flex justify-between items-center">
                    <div>
                        <h4>${entry.date}</h4>
                        <p class="text-muted">${entry.mood}</p>
                    </div>
                    <div class="text-right">
                        <span class="badge badge-primary">${entry.activities}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }

    getMoodHistory() {
        // Mock data - replace with real API call
        return [
            { date: 'Today', mood: 'Happy', activities: 'Exercise, Meditation' },
            { date: 'Yesterday', mood: 'Neutral', activities: 'Work, Social' },
            { date: '2 days ago', mood: 'Sad', activities: 'Rest, Self-care' }
        ];
    }
}

// Meditation Timer
class MeditationTimer {
    constructor() {
        this.isRunning = false;
        this.timeLeft = 0;
        this.timer = null;
        this.init();
    }

    init() {
        this.setupTimerControls();
        this.setupPresetButtons();
    }

    setupTimerControls() {
        const startBtn = document.getElementById('timer-start');
        const pauseBtn = document.getElementById('timer-pause');
        const resetBtn = document.getElementById('timer-reset');

        if (startBtn) startBtn.addEventListener('click', () => this.startTimer());
        if (pauseBtn) pauseBtn.addEventListener('click', () => this.pauseTimer());
        if (resetBtn) resetBtn.addEventListener('click', () => this.resetTimer());
    }

    setupPresetButtons() {
        const presets = document.querySelectorAll('.timer-preset');
        presets.forEach(preset => {
            preset.addEventListener('click', () => {
                const minutes = parseInt(preset.dataset.minutes);
                this.setTime(minutes * 60);
            });
        });
    }

    setTime(seconds) {
        this.timeLeft = seconds;
        this.updateDisplay();
    }

    startTimer() {
        if (this.timeLeft <= 0) return;
        
        this.isRunning = true;
        this.timer = setInterval(() => {
            this.timeLeft--;
            this.updateDisplay();
            
            if (this.timeLeft <= 0) {
                this.completeTimer();
            }
        }, 1000);

        this.updateButtonStates();
    }

    pauseTimer() {
        this.isRunning = false;
        clearInterval(this.timer);
        this.updateButtonStates();
    }

    resetTimer() {
        this.pauseTimer();
        this.timeLeft = 0;
        this.updateDisplay();
        this.updateButtonStates();
    }

    completeTimer() {
        this.pauseTimer();
        this.showCompletionMessage();
        this.playCompletionSound();
    }

    updateDisplay() {
        const display = document.getElementById('timer-display');
        if (!display) return;

        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        display.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    updateButtonStates() {
        const startBtn = document.getElementById('timer-start');
        const pauseBtn = document.getElementById('timer-pause');
        const resetBtn = document.getElementById('timer-reset');

        if (startBtn) startBtn.style.display = this.isRunning ? 'none' : 'inline-block';
        if (pauseBtn) pauseBtn.style.display = this.isRunning ? 'inline-block' : 'none';
        if (resetBtn) resetBtn.disabled = this.timeLeft === 0;
    }

    showCompletionMessage() {
        const message = document.createElement('div');
        message.className = 'alert alert-success';
        message.innerHTML = `
            <h4>Meditation Complete! 🧘‍♀️</h4>
            <p>Great job! You've completed your meditation session. Take a moment to notice how you feel.</p>
        `;
        
        const container = document.querySelector('.meditation-timer');
        if (container) {
            container.appendChild(message);
            setTimeout(() => message.remove(), 5000);
        }
    }

    playCompletionSound() {
        // Play a gentle completion sound
        const audio = new Audio('/static/sounds/meditation-complete.mp3');
        audio.volume = 0.3;
        audio.play().catch(() => {
            // Fallback if audio fails
            console.log('Meditation session completed!');
        });
    }
}

// Breathing Exercise
class BreathingExercise {
    constructor() {
        this.isActive = false;
        this.cycle = 0;
        this.breathingTimer = null;
        this.init();
    }

    init() {
        this.setupBreathingControls();
    }

    setupBreathingControls() {
        const startBtn = document.getElementById('breathing-start');
        const stopBtn = document.getElementById('breathing-stop');

        if (startBtn) startBtn.addEventListener('click', () => this.startBreathing());
        if (stopBtn) stopBtn.addEventListener('click', () => this.stopBreathing());
    }

    startBreathing() {
        this.isActive = true;
        this.cycle = 0;
        this.breathingTimer = setInterval(() => {
            this.cycle++;
            this.updateBreathingState();
        }, 4000); // 4 seconds per breath cycle

        this.updateButtonStates();
        this.updateBreathingState();
    }

    stopBreathing() {
        this.isActive = false;
        clearInterval(this.breathingTimer);
        this.resetBreathingState();
        this.updateButtonStates();
    }

    updateBreathingState() {
        const circle = document.querySelector('.breathing-circle');
        const instruction = document.getElementById('breathing-instruction');
        const cycleCount = document.getElementById('breathing-cycle');

        if (!circle || !instruction) return;

        const isInhale = this.cycle % 2 === 0;
        
        if (isInhale) {
            circle.classList.add('inhale');
            circle.classList.remove('exhale');
            instruction.textContent = 'Inhale...';
        } else {
            circle.classList.add('exhale');
            circle.classList.remove('inhale');
            instruction.textContent = 'Exhale...';
        }

        if (cycleCount) {
            cycleCount.textContent = Math.floor(this.cycle / 2) + 1;
        }
    }

    resetBreathingState() {
        const circle = document.querySelector('.breathing-circle');
        const instruction = document.getElementById('breathing-instruction');
        const cycleCount = document.getElementById('breathing-cycle');

        if (circle) {
            circle.classList.remove('inhale', 'exhale');
        }
        if (instruction) {
            instruction.textContent = 'Ready to begin...';
        }
        if (cycleCount) {
            cycleCount.textContent = '0';
        }
    }

    updateButtonStates() {
        const startBtn = document.getElementById('breathing-start');
        const stopBtn = document.getElementById('breathing-stop');

        if (startBtn) startBtn.style.display = this.isActive ? 'none' : 'inline-block';
        if (stopBtn) stopBtn.style.display = this.isActive ? 'inline-block' : 'none';
    }
}

// Wellness Goals Tracker
class WellnessGoalsTracker {
    constructor() {
        this.goals = [];
        this.init();
    }

    init() {
        this.loadGoals();
        this.setupGoalForm();
    }

    loadGoals() {
        const goalsContainer = document.getElementById('wellness-goals');
        if (!goalsContainer) return;

        this.goals = this.getGoals();
        goalsContainer.innerHTML = this.goals.map(goal => this.renderGoal(goal)).join('');
    }

    renderGoal(goal) {
        const progressPercent = (goal.current / goal.target) * 100;
        return `
            <div class="card mb-4">
                <div class="card-header">
                    <h4>${goal.title}</h4>
                    <span class="badge badge-${goal.status}">${goal.status}</span>
                </div>
                <div class="card-body">
                    <p>${goal.description}</p>
                    <div class="mt-4">
                        <div class="flex justify-between mb-2">
                            <span>Progress</span>
                            <span>${goal.current}/${goal.target} ${goal.unit}</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar" style="width: ${progressPercent}%"></div>
                        </div>
                    </div>
                    <div class="mt-4">
                        <button class="btn btn-sm btn-primary" onclick="wellnessGoals.updateProgress(${goal.id})">
                            Update Progress
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    getGoals() {
        // Mock data - replace with real API call
        return [
            {
                id: 1,
                title: 'Daily Meditation',
                description: 'Practice meditation for 10 minutes every day',
                current: 7,
                target: 10,
                unit: 'minutes',
                status: 'active'
            },
            {
                id: 2,
                title: 'Exercise',
                description: 'Complete 30 minutes of physical activity',
                current: 25,
                target: 30,
                unit: 'minutes',
                status: 'active'
            },
            {
                id: 3,
                title: 'Water Intake',
                description: 'Drink 8 glasses of water daily',
                current: 6,
                target: 8,
                unit: 'glasses',
                status: 'active'
            }
        ];
    }

    setupGoalForm() {
        const form = document.getElementById('goal-form');
        if (!form) return;

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.addGoal(form);
        });
    }

    addGoal(form) {
        const formData = new FormData(form);
        const goal = {
            title: formData.get('title'),
            description: formData.get('description'),
            target: parseInt(formData.get('target')),
            unit: formData.get('unit'),
            current: 0,
            status: 'active'
        };

        this.goals.push(goal);
        this.loadGoals();
        form.reset();
    }

    updateProgress(goalId) {
        const goal = this.goals.find(g => g.id === goalId);
        if (!goal) return;

        const newProgress = prompt(`Update progress for "${goal.title}" (current: ${goal.current}/${goal.target} ${goal.unit}):`);
        if (newProgress !== null) {
            goal.current = Math.min(parseInt(newProgress) || 0, goal.target);
            if (goal.current >= goal.target) {
                goal.status = 'completed';
            }
            this.loadGoals();
        }
    }
}

// Notification System
class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.init();
    }

    init() {
        this.setupNotificationContainer();
        this.loadNotifications();
    }

    setupNotificationContainer() {
        if (!document.getElementById('notification-container')) {
            const container = document.createElement('div');
            container.id = 'notification-container';
            container.className = 'fixed top-4 right-4 z-50';
            document.body.appendChild(container);
        }
    }

    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} mb-2 animate-fade-in`;
        notification.innerHTML = `
            <div class="flex justify-between items-center">
                <span>${message}</span>
                <button class="btn btn-sm" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        const container = document.getElementById('notification-container');
        container.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, duration);
    }

    loadNotifications() {
        const container = document.getElementById('notifications-list');
        if (!container) return;

        this.notifications = this.getNotifications();
        container.innerHTML = this.notifications.map(notification => `
            <div class="card mb-4 ${notification.read ? 'opacity-75' : ''}">
                <div class="flex justify-between items-start">
                    <div>
                        <h4>${notification.title}</h4>
                        <p class="text-muted">${notification.message}</p>
                        <small class="text-muted">${notification.time}</small>
                    </div>
                    ${!notification.read ? '<span class="badge badge-primary">New</span>' : ''}
                </div>
            </div>
        `).join('');
    }

    getNotifications() {
        // Mock data - replace with real API call
        return [
            {
                title: 'Meditation Reminder',
                message: 'Time for your daily meditation session!',
                time: '2 hours ago',
                read: false
            },
            {
                title: 'Goal Achievement',
                message: 'Congratulations! You\'ve completed your exercise goal.',
                time: '1 day ago',
                read: true
            }
        ];
    }
}

// Initialize all components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme manager
    window.themeManager = new ThemeManager();
    
    // Initialize dashboard analytics
    window.dashboardAnalytics = new DashboardAnalytics();
    
    // Initialize mood tracker
    window.moodTracker = new MoodTracker();
    
    // Initialize meditation timer
    window.meditationTimer = new MeditationTimer();
    
    // Initialize breathing exercise
    window.breathingExercise = new BreathingExercise();
    
    // Initialize wellness goals tracker
    window.wellnessGoals = new WellnessGoalsTracker();
    
    // Initialize notification system
    window.notifications = new NotificationSystem();
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.card, .stat-card').forEach(el => {
        observer.observe(el);
    });
});

// Utility functions
window.utils = {
    formatDate: (date) => {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    formatTime: (seconds) => {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    },
    
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    throttle: (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}; 