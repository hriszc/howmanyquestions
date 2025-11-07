# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HowManyQ is a static web application that hosts a collection of "How Many" calculator and converter tools. The project uses pure HTML5, CSS3, and vanilla JavaScript for the frontend, with Python automation for navigation management.

## Key Commands

### Navigation Management
```bash
# Generate navigation data (run after adding new tools)
python3 navigation_generator.py

# Create new tool folders from keywords
python3 create_folders.py

# Manual navigation update with logging
./navigation_updater.sh

# Check cron job status
./check_cron_status.sh
```

### Development Workflow
```bash
# Test navigation generation
python3 navigation_generator.py && cat navigation_data.json | jq '.tools | length'

# View recent navigation updates
git log --oneline -n 10 -- navigation_data.json

# Check for uncommitted navigation changes
git diff navigation_data.json
```

## Architecture & Structure

### Monorepo Organization
- **Tool Directories**: Each `how_many_*` folder contains a self-contained calculator tool
- **Central Navigation**: `index.html` serves as the main navigation hub using `navigation_data.json`
- **Auto-Discovery**: `navigation_generator.py` automatically finds and catalogs tools
- **GitHub Actions**: Automated updates trigger on tool additions/modifications

### Key Files
- `navigation_generator.py`: Scans for tools and generates navigation metadata
- `navigation_data.json`: Auto-generated catalog of all tools with categories and metadata
- `index.html`: Main navigation page consuming the JSON data
- `.github/workflows/update-navigation.yml`: CI/CD automation

### Category System
Tools are automatically categorized based on keywords:
- **time**: christmas, days, weeks, hours (icon: ⏰)
- **volume**: ounces, cups, gallons, liters (icon: 🧪)
- **weight**: pounds, grams, kilograms (icon: ⚖️)
- **length**: feet, inches, meters, miles (icon: 📏)
- **measurement**: steps, bmi, temperature (icon: 📊)

### Automation Flow
1. New tool folder created with `index.html`
2. GitHub Actions detects change via path monitoring
3. `navigation_generator.py` runs and updates `navigation_data.json`
4. Changes are auto-committed with descriptive messages
5. Pull request created for review (if configured)

## Development Guidelines

### Adding New Tools
1. Create folder named `how_many_[description]`
2. Add `index.html` with calculator functionality
3. Navigation will auto-update within minutes via GitHub Actions
4. Manual update: `python3 navigation_generator.py`

### Navigation Updates
- Always run `python3 navigation_generator.py` after structural changes
- Check `navigation_data.json` for proper categorization
- Monitor GitHub Actions for automated update failures
- View logs in `cron.log` for manual script execution

### Testing Considerations
- No formal test suite exists - testing is manual
- Verify navigation updates by checking generated JSON
- Test mobile responsiveness for new calculator tools
- Validate SEO meta tags in individual tool pages

## Important Notes

- **Static Hosting**: Site is deployed on GitHub Pages - no server-side processing
- **No Build Process**: Pure static files, no npm/webpack/build steps
- **Bilingual Support**: Tools should support both English and Chinese
- **SEO Focus**: Each tool page needs proper meta tags and structured data
- **Automation Dependency**: Navigation system relies on GitHub Actions for updates