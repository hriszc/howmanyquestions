/**
 * Script to automatically add sharing functionality to existing HowManyQ calculator pages
 * This script can be run manually or integrated into the build process
 */

class SharingIntegrator {
    constructor() {
        this.shareScriptPath = 'share-utils.js';
        this.defaultShareText = 'Check out this amazing calculator!';

        // Calculator-specific share text generators
        this.calculatorShareTexts = {
            'calories': (result, input) => `I just calculated my daily calorie needs: ${result} calories per day! 🍎`,
            'steps': (result, input) => `I just converted ${input} steps to ${result} miles! 🚶‍♂️`,
            'christmas': (result, input) => `Only ${result} days until Christmas! 🎄`,
            'halloween': (result, input) => `Only ${result} days until Halloween! 🎃`,
            'miles': (result, input) => `I just calculated: ${input} steps = ${result} miles! 🏃‍♂️`,
            'conversion': (result, input, unit) => `I just calculated: ${result} ${unit}! 📊`
        };
    }

    /**
     * Analyze a calculator page and determine what type it is
     */
    detectCalculatorType(content) {
        const keywords = {
            'calories': ['calories', 'calorie', 'daily calories', 'calorie calculator'],
            'steps': ['steps', 'steps to miles', '10000 steps', 'walking'],
            'christmas': ['christmas', 'xmas', 'december 25'],
            'halloween': ['halloween', 'october 31', 'pumpkin'],
            'miles': ['miles', 'distance', 'walking distance'],
            'volume': ['ounces', 'cups', 'gallons', 'liters', 'quarts', 'pints'],
            'weight': ['pounds', 'grams', 'kilograms', 'ounces'],
            'time': ['days', 'hours', 'weeks', 'years'],
            'temperature': ['celsius', 'fahrenheit', 'temperature'],
            'length': ['feet', 'inches', 'meters', 'centimeters']
        };

        const lowerContent = content.toLowerCase();

        for (const [type, words] of Object.entries(keywords)) {
            if (words.some(word => lowerContent.includes(word))) {
                return type;
            }
        }

        return 'conversion'; // Default type
    }

    /**
     * Find result elements in the page
     */
    findResultElements(content) {
        const patterns = [
            /id=["']([^"']*result[^"']*)["']/gi,
            /class=["']([^"']*result[^"']*)["']/gi,
            /id=["']([^"']*value[^"']*)["']/gi,
            /class=["']([^"']*value[^"']*)["']/gi
        ];

        const elements = [];
        patterns.forEach(pattern => {
            let match;
            while ((match = pattern.exec(content)) !== null) {
                elements.push(match[1]);
            }
        });

        return [...new Set(elements)]; // Remove duplicates
    }

    /**
     * Generate sharing integration code for a calculator page
     */
    generateSharingCode(calculatorType, resultElementId = 'resultValue') {
        const type = calculatorType || 'conversion';

        return `
<!-- Sharing Integration -->
<script src="${this.shareScriptPath}"></script>

<script>
(function() {
    // Wait for page to load
    function initSharing() {
        // Configuration for sharing
        const shareConfig = {
            title: document.title,
            text: '', // Will be populated dynamically
            url: window.location.href,
            platforms: ['native', 'twitter', 'facebook', 'copy'],
            hashtags: ['HowManyQ', 'Calculator'],
            showToast: true,
            onShare: function(platform, options) {
                console.log('Shared on', platform);
            }
        };

        // Function to get calculator result
        function getCalculatorResult() {
            const resultElement = document.getElementById('${resultElementId}');
            const inputElements = [
                document.querySelector('input[type="number"]'),
                document.querySelector('input[type="text"]'),
                document.querySelector('input')
            ].filter(el => el && el.value);

            const result = resultElement ? resultElement.textContent || resultElement.value : '';
            const input = inputElements.length > 0 ? inputElements[0].value : '';

            return { result, input };
        }

        // Function to generate share text based on calculator type
        function generateShareText() {
            const { result, input } = getCalculatorResult();

            if (!result) return 'Check out this calculator!';

            const shareTexts = ${JSON.stringify(this.calculatorShareTexts, null, 12)};
            const generator = shareTexts['${type}'] || shareTexts['conversion'];

            return generator(result, input, '');
        }

        // Create share section HTML
        function createShareSection() {
            const shareSection = document.createElement('div');
            shareSection.className = 'share-section';
            shareSection.innerHTML = \`
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
                    <h3 style="margin-bottom: 16px; color: #333;">Share Your Result</h3>
                    <div id="shareButtonsContainer"></div>
                </div>
            \`;

            // Find a good place to insert the share section
            const calculatorCard = document.querySelector('.calculator-card, .container, main, body > div');
            if (calculatorCard) {
                calculatorCard.appendChild(shareSection);
            } else {
                document.body.appendChild(shareSection);
            }
        }

        // Initialize sharing buttons
        function initializeShareButtons() {
            const shareText = generateShareText();
            shareConfig.text = shareText;

            const sharer = new HowManyQShare(shareConfig);
            sharer.createShareButtons('shareButtonsContainer', shareConfig);
        }

        // Auto-initialize when calculator updates
        function watchForResultUpdates() {
            const resultElement = document.getElementById('${resultElementId}');
            if (resultElement) {
                // Watch for changes in result element
                const observer = new MutationObserver(function() {
                    setTimeout(initializeShareButtons, 100);
                });

                observer.observe(resultElement, {
                    childList: true,
                    characterData: true,
                    subtree: true
                });
            }
        }

        // Initialize everything
        function setupSharing() {
            createShareSection();
            initializeShareButtons();
            watchForResultUpdates();
        }

        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setupSharing);
        } else {
            setupSharing();
        }
    }

    // Initialize sharing
    initSharing();
})();
</script>
`;
    }

    /**
     * Add sharing to a specific HTML file
     */
    addSharingToFile(filePath) {
        try {
            const fs = require('fs');
            let content = fs.readFileSync(filePath, 'utf8');

            // Check if sharing is already implemented
            if (content.includes('share-utils.js') || content.includes('HowManyQShare')) {
                console.log(`⏭️  Skipping ${filePath} - sharing already implemented`);
                return { skipped: true, reason: 'Already has sharing' };
            }

            // Detect calculator type
            const calculatorType = this.detectCalculatorType(content);
            console.log(`🔍 Detected calculator type: ${calculatorType}`);

            // Find result elements
            const resultElements = this.findResultElements(content);
            const resultElementId = resultElements.length > 0 ? resultElements[0] : 'resultValue';
            console.log(`🎯 Using result element: ${resultElementId}`);

            // Generate sharing code
            const sharingCode = this.generateSharingCode(calculatorType, resultElementId);

            // Insert sharing code before closing body tag
            const bodyCloseIndex = content.lastIndexOf('</body>');
            if (bodyCloseIndex === -1) {
                console.log(`⚠️  Warning: Could not find </body> tag in ${filePath}`);
                return { error: 'No body tag found' };
            }

            const newContent = content.slice(0, bodyCloseIndex) + sharingCode + content.slice(bodyCloseIndex);

            // Backup original file
            const backupPath = filePath + '.backup';
            fs.writeFileSync(backupPath, content);
            console.log(`💾 Backup created: ${backupPath}`);

            // Write new content
            fs.writeFileSync(filePath, newContent);
            console.log(`✅ Sharing added to ${filePath}`);

            return {
                success: true,
                calculatorType,
                resultElementId,
                backupPath
            };

        } catch (error) {
            console.error(`❌ Error processing ${filePath}:`, error.message);
            return { error: error.message };
        }
    }

    /**
     * Add sharing to all calculator pages in a directory
     */
    async addSharingToAll(directory) {
        const fs = require('fs');
        const path = require('path');

        console.log(`🚀 Starting sharing integration for directory: ${directory}`);

        // Find all index.html files in how_many_* directories
        const glob = require('glob');
        const pattern = path.join(directory, 'how_many_*', 'index.html');

        return new Promise((resolve, reject) => {
            glob(pattern, (err, files) => {
                if (err) {
                    console.error('❌ Error finding files:', err);
                    reject(err);
                    return;
                }

                console.log(`📁 Found ${files.length} calculator pages`);

                const results = [];
                files.forEach(filePath => {
                    console.log(`\n🔄 Processing: ${filePath}`);
                    const result = this.addSharingToFile(filePath);
                    results.push({ filePath, ...result });
                });

                // Summary
                console.log('\n📊 Integration Summary:');
                const successful = results.filter(r => r.success);
                const skipped = results.filter(r => r.skipped);
                const failed = results.filter(r => r.error && !r.skipped);

                console.log(`✅ Successfully updated: ${successful.length}`);
                console.log(`⏭️  Skipped (already have sharing): ${skipped.length}`);
                console.log(`❌ Failed: ${failed.length}`);

                if (failed.length > 0) {
                    console.log('\nFailed files:');
                    failed.forEach(f => console.log(`  - ${f.filePath}: ${f.error}`));
                }

                resolve({ successful, skipped, failed, total: results.length });
            });
        });
    }

    /**
     * Remove sharing from a file (restore from backup)
     */
    removeSharingFromFile(filePath) {
        try {
            const fs = require('fs');
            const backupPath = filePath + '.backup';

            if (!fs.existsSync(backupPath)) {
                console.log(`⚠️  No backup found for ${filePath}`);
                return { error: 'No backup found' };
            }

            // Restore from backup
            const backupContent = fs.readFileSync(backupPath, 'utf8');
            fs.writeFileSync(filePath, backupContent);

            // Remove backup
            fs.unlinkSync(backupPath);

            console.log(`🔄 Sharing removed from ${filePath} (restored from backup)`);
            return { success: true };

        } catch (error) {
            console.error(`❌ Error removing sharing from ${filePath}:`, error.message);
            return { error: error.message };
        }
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SharingIntegrator;
} else {
    window.SharingIntegrator = SharingIntegrator;
}

// CLI usage
if (require.main === module) {
    const integrator = new SharingIntegrator();
    const directory = process.argv[2] || process.cwd();

    console.log('🎯 HowManyQ Sharing Integration Tool');
    console.log('=====================================');

    integrator.addSharingToAll(directory)
        .then(results => {
            console.log('\n🎉 Integration complete!');
            process.exit(0);
        })
        .catch(error => {
            console.error('💥 Integration failed:', error);
            process.exit(1);
        });
}