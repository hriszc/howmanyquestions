/**
 * Universal Sharing Component for HowManyQ Tools
 * Provides consistent sharing functionality across all calculator tools
 */

class HowManyQShare {
    constructor(options = {}) {
        this.options = {
            // Default configuration
            title: options.title || document.title,
            text: options.text || '',
            url: options.url || window.location.href,

            // Social media specific options
            hashtags: options.hashtags || ['HowManyQ', 'Calculator'],
            via: options.via || 'HowManyQ',
            related: options.related || 'HowManyQ',

            // UI options
            buttonClass: options.buttonClass || 'share-btn',
            showToast: options.showToast !== false,
            toastDuration: options.toastDuration || 2000,

            // Platform specific options
            platforms: options.platforms || ['twitter', 'facebook', 'copy', 'native'],

            // Callbacks
            onShare: options.onShare || null,
            onCopy: options.onCopy || null,
            onError: options.onError || null
        };

        // Platform configurations
        this.platforms = {
            twitter: {
                name: 'Twitter',
                icon: '🐦',
                color: '#1DA1F2',
                action: this.shareOnTwitter.bind(this)
            },
            facebook: {
                name: 'Facebook',
                icon: '📘',
                color: '#4267B2',
                action: this.shareOnFacebook.bind(this)
            },
            linkedin: {
                name: 'LinkedIn',
                icon: '💼',
                color: '#0077B5',
                action: this.shareOnLinkedIn.bind(this)
            },
            whatsapp: {
                name: 'WhatsApp',
                icon: '💬',
                color: '#25D366',
                action: this.shareOnWhatsApp.bind(this)
            },
            telegram: {
                name: 'Telegram',
                icon: '✈️',
                color: '#0088cc',
                action: this.shareOnTelegram.bind(this)
            },
            copy: {
                name: 'Copy Link',
                icon: '📋',
                color: '#6C757D',
                action: this.copyToClipboard.bind(this)
            },
            native: {
                name: 'Share',
                icon: '🔗',
                color: '#007AFF',
                action: this.nativeShare.bind(this)
            }
        };

        // Initialize
        this.init();
    }

    init() {
        // Check for Web Share API support
        this.hasNativeShare = 'share' in navigator;

        // Create toast container if needed
        if (this.options.showToast) {
            this.createToastContainer();
        }
    }

    /**
     * Create sharing buttons for a specific container
     */
    createShareButtons(containerId, customOptions = {}) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with ID '${containerId}' not found`);
            return;
        }

        // Merge custom options
        const options = { ...this.options, ...customOptions };

        // Create share buttons HTML
        const buttonsHTML = this.generateShareButtonsHTML(options);

        // Insert into container
        container.innerHTML = buttonsHTML;

        // Add event listeners
        this.attachEventListeners(container, options);
    }

    /**
     * Generate HTML for share buttons
     */
    generateShareButtonsHTML(options) {
        const platforms = options.platforms;
        let html = '<div class="share-buttons-container">';

        platforms.forEach(platform => {
            if (platform === 'native' && !this.hasNativeShare) {
                // Fallback to copy if native share not available
                platform = 'copy';
            }

            const config = this.platforms[platform];
            if (config) {
                html += `
                    <button class="${options.buttonClass} share-${platform}"
                            data-platform="${platform}"
                            style="background-color: ${config.color}"
                            title="Share on ${config.name}">
                        <span class="share-icon">${config.icon}</span>
                        <span class="share-text">${config.name}</span>
                    </button>
                `;
            }
        });

        html += '</div>';
        return html;
    }

    /**
     * Attach event listeners to share buttons
     */
    attachEventListeners(container, options) {
        const buttons = container.querySelectorAll('.share-btn');

        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const platform = button.dataset.platform;
                this.handleShare(platform, options);
            });
        });
    }

    /**
     * Handle sharing for a specific platform
     */
    handleShare(platform, options) {
        const config = this.platforms[platform];
        if (config && config.action) {
            try {
                config.action(options);

                // Call success callback
                if (options.onShare) {
                    options.onShare(platform, options);
                }
            } catch (error) {
                console.error(`Error sharing on ${platform}:`, error);

                // Call error callback
                if (options.onError) {
                    options.onError(platform, error);
                }

                this.showToast('❌ Sharing failed. Please try again.', 'error');
            }
        }
    }

    /**
     * Native Web Share API
     */
    nativeShare(options) {
        const shareData = {
            title: options.title,
            text: options.text,
            url: options.url
        };

        if (navigator.share) {
            navigator.share(shareData)
                .then(() => {
                    this.showToast('✅ Shared successfully!', 'success');
                })
                .catch((error) => {
                    if (error.name !== 'AbortError') {
                        console.error('Native share failed:', error);
                        // Fallback to copy
                        this.copyToClipboard(options);
                    }
                });
        } else {
            // Fallback to copy
            this.copyToClipboard(options);
        }
    }

    /**
     * Twitter sharing
     */
    shareOnTwitter(options) {
        const text = encodeURIComponent(options.text);
        const url = encodeURIComponent(options.url);
        const hashtags = options.hashtags.join(',');
        const via = options.via;

        const twitterUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}&hashtags=${hashtags}&via=${via}`;

        this.openShareWindow(twitterUrl, 'Twitter Share');
        this.showToast('🐦 Opening Twitter...', 'info');
    }

    /**
     * Facebook sharing
     */
    shareOnFacebook(options) {
        const url = encodeURIComponent(options.url);
        const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;

        this.openShareWindow(facebookUrl, 'Facebook Share');
        this.showToast('📘 Opening Facebook...', 'info');
    }

    /**
     * LinkedIn sharing
     */
    shareOnLinkedIn(options) {
        const url = encodeURIComponent(options.url);
        const title = encodeURIComponent(options.title);
        const summary = encodeURIComponent(options.text);

        const linkedinUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}&title=${title}&summary=${summary}`;

        this.openShareWindow(linkedinUrl, 'LinkedIn Share');
        this.showToast('💼 Opening LinkedIn...', 'info');
    }

    /**
     * WhatsApp sharing
     */
    shareOnWhatsApp(options) {
        const text = encodeURIComponent(`${options.text} ${options.url}`);
        const whatsappUrl = `https://wa.me/?text=${text}`;

        this.openShareWindow(whatsappUrl, 'WhatsApp Share');
        this.showToast('💬 Opening WhatsApp...', 'info');
    }

    /**
     * Telegram sharing
     */
    shareOnTelegram(options) {
        const text = encodeURIComponent(`${options.text} ${options.url}`);
        const telegramUrl = `https://t.me/share/url?url=${encodeURIComponent(options.url)}&text=${text}`;

        this.openShareWindow(telegramUrl, 'Telegram Share');
        this.showToast('✈️ Opening Telegram...', 'info');
    }

    /**
     * Copy to clipboard
     */
    copyToClipboard(options) {
        const text = `${options.text}\n${options.url}`;

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text)
                .then(() => {
                    this.showToast('📋 Copied to clipboard!', 'success');
                    if (options.onCopy) {
                        options.onCopy(text);
                    }
                })
                .catch(() => {
                    this.fallbackCopyToClipboard(text);
                });
        } else {
            this.fallbackCopyToClipboard(text);
        }
    }

    /**
     * Fallback copy method for older browsers
     */
    fallbackCopyToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            document.execCommand('copy');
            this.showToast('📋 Copied to clipboard!', 'success');
        } catch (error) {
            console.error('Fallback copy failed:', error);
            this.showToast('❌ Copy failed. Please copy manually.', 'error');
        } finally {
            document.body.removeChild(textArea);
        }
    }

    /**
     * Open sharing window
     */
    openShareWindow(url, title) {
        const width = 600;
        const height = 400;
        const left = (window.screen.width - width) / 2;
        const top = (window.screen.height - height) / 2;

        window.open(
            url,
            title,
            `width=${width},height=${height},left=${left},top=${top},resizable=yes,scrollbars=yes`
        );
    }

    /**
     * Create toast container
     */
    createToastContainer() {
        if (document.getElementById('share-toast-container')) return;

        const container = document.createElement('div');
        container.id = 'share-toast-container';
        container.className = 'share-toast-container';
        document.body.appendChild(container);
    }

    /**
     * Show toast notification
     */
    showToast(message, type = 'info') {
        if (!this.options.showToast) return;

        const container = document.getElementById('share-toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `share-toast share-toast-${type}`;
        toast.textContent = message;

        container.appendChild(toast);

        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);

        // Remove after duration
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (container.contains(toast)) {
                    container.removeChild(toast);
                }
            }, 300);
        }, this.options.toastDuration);
    }

    /**
     * Generate share text based on calculator type and result
     */
    static generateShareText(calculatorType, result, unit = '') {
        const texts = {
            'calories': `I just calculated my daily calorie needs: ${result} calories per day! 🍎`,
            'steps': `I just converted ${result} steps to miles! 🚶‍♂️`,
            'christmas': `Only ${result} days until Christmas! 🎄`,
            'halloween': `Only ${result} days until Halloween! 🎃`,
            'conversion': `I just calculated: ${result} ${unit}! 📊`,
            'default': `I just used this calculator and got: ${result} ${unit}! 🎯`
        };

        return texts[calculatorType] || texts['default'];
    }

    /**
     * Quick share method for calculators
     */
    static quickShare(calculatorType, result, unit = '', customText = '') {
        const text = customText || this.generateShareText(calculatorType, result, unit);
        const url = window.location.href;

        const sharer = new HowManyQShare({
            text: text,
            platforms: ['native', 'twitter', 'facebook', 'copy']
        });

        // Try native share first, fallback to Twitter
        if (sharer.hasNativeShare) {
            sharer.nativeShare({ text, url });
        } else {
            sharer.shareOnTwitter({ text, url });
        }
    }
}

// CSS styles for the share component
const shareStyles = `
    .share-buttons-container {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        justify-content: center;
        margin: 16px 0;
    }

    .share-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 20px;
        border: none;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        color: white;
        text-decoration: none;
        min-height: 40px;
    }

    .share-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        opacity: 0.9;
    }

    .share-btn:active {
        transform: translateY(0);
    }

    .share-icon {
        font-size: 16px;
    }

    .share-text {
        font-weight: 500;
    }

    /* Toast notifications */
    .share-toast-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .share-toast {
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
        word-wrap: break-word;
    }

    .share-toast.show {
        transform: translateX(0);
    }

    .share-toast-success {
        background-color: #34C759;
    }

    .share-toast-error {
        background-color: #FF3B30;
    }

    .share-toast-info {
        background-color: #007AFF;
    }

    /* Responsive design */
    @media (max-width: 480px) {
        .share-buttons-container {
            flex-direction: column;
            align-items: stretch;
        }

        .share-btn {
            justify-content: center;
        }

        .share-toast-container {
            left: 20px;
            right: 20px;
            max-width: none;
        }
    }
`;

// Auto-inject styles if not already present
if (!document.getElementById('howmanyq-share-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'howmanyq-share-styles';
    styleSheet.textContent = shareStyles;
    document.head.appendChild(styleSheet);
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HowManyQShare;
} else if (typeof window !== 'undefined') {
    window.HowManyQShare = HowManyQShare;
}