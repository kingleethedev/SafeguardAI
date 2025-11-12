// Dashboard specific JavaScript functionality

class DashboardManager {
    constructor() {
        this.autoRefreshInterval = 30000; // 30 seconds
        this.init();
    }

    init() {
        this.setupAutoRefresh();
        this.setupEventListeners();
        this.loadRealTimeData();
    }

    setupAutoRefresh() {
        setInterval(() => {
            this.refreshDashboard();
        }, this.autoRefreshInterval);
    }

    setupEventListeners() {
        // Refresh button
        document.getElementById('refreshBtn')?.addEventListener('click', () => {
            this.refreshDashboard();
        });

        // Alert click handlers
        document.addEventListener('click', (e) => {
            if (e.target.closest('.alert-item')) {
                this.showAlertDetails(e.target.closest('.alert-item'));
            }
        });
    }

    async refreshDashboard() {
        try {
            // Show loading state
            this.showLoading();

            // Reload the page for simplicity
            // In a real app, you'd use AJAX to update specific components
            window.location.reload();
            
        } catch (error) {
            console.error('Error refreshing dashboard:', error);
            this.showError('Failed to refresh data');
        }
    }

    async loadRealTimeData() {
        // Simulate real-time data updates
        setInterval(() => {
            this.updateLiveCounters();
        }, 5000);
    }

    updateLiveCounters() {
        // Update counter animations
        const counters = document.querySelectorAll('.counter');
        counters.forEach(counter => {
            const target = parseInt(counter.textContent);
            this.animateCounter(counter, target);
        });
    }

    animateCounter(element, target) {
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 20);
    }

    showAlertDetails(alertElement) {
        const alertId = alertElement.dataset.alertId;
        // Implement alert details modal
        console.log('Showing details for alert:', alertId);
    }

    showLoading() {
        // Implement loading indicator
        const loadingEl = document.createElement('div');
        loadingEl.className = 'loading-overlay';
        loadingEl.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        `;
        document.body.appendChild(loadingEl);
    }

    showError(message) {
        // Implement error notification
        const errorEl = document.createElement('div');
        errorEl.className = 'alert alert-danger alert-dismissible fade show';
        errorEl.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.container-fluid').prepend(errorEl);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DashboardManager();
});

// Utility functions
const DashboardUtils = {
    formatTimeAgo(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diff = now - time;
        
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);
        
        if (days > 0) return `${days}d ago`;
        if (hours > 0) return `${hours}h ago`;
        if (minutes > 0) return `${minutes}m ago`;
        return 'Just now';
    },

    getThreatLevelColor(level) {
        const colors = {
            'high': '#dc3545',
            'medium': '#ffc107',
            'low': '#17a2b8'
        };
        return colors[level] || '#6c757d';
    },

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};