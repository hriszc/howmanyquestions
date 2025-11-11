#!/bin/bash
# HowManyQ Sitemap Updater
# Automatically updates sitemap.xml when new tools are added

set -e

echo "🔄 Updating HowManyQ Sitemap..."
echo "================================"

# Check if navigation data exists
if [ ! -f "navigation_data.json" ]; then
    echo "❌ Error: navigation_data.json not found!"
    echo "   Run navigation_generator.py first."
    exit 1
fi

# Generate new sitemap
echo "📋 Generating sitemap..."
python3 sitemap_generator.py > /dev/null 2>&1

# Check if sitemap was created
if [ ! -f "sitemap.xml" ]; then
    echo "❌ Error: sitemap.xml generation failed!"
    exit 1
fi

# Count URLs in sitemap
url_count=$(grep -c "</loc>" sitemap.xml)
echo "✅ Sitemap updated successfully!"
echo "📊 Total URLs: $url_count"

# Show git status
echo ""
echo "📦 Git status:"
git status --short | grep -E "(sitemap|robots)" || echo "   No changes to commit"

echo ""
echo "📝 Next steps:"
echo "   - Commit sitemap.xml and robots.txt"
echo "   - Submit to Google Search Console"
echo "   - Deploy to production"
