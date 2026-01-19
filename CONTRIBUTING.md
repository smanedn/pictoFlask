# Contributing to PictoFlask

First off, thank you for considering contributing to PictoFlask! 🎮💬

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Guidelines](#development-guidelines)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project and everyone participating in it is governed by a simple principle: **Be respectful, be constructive, be helpful.**

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/smanedn/PictoFlask.git
   cd PictoFlask
   ```
3. **Set up the development environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🤝 How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check existing issues to avoid duplicates.

When creating a bug report, include:

- **Clear descriptive title**
- **Detailed description** of the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs **actual behavior**
- **Screenshots** if applicable
- **Environment details**:
  - OS (Windows/macOS/Linux)
  - Browser and version
  - Python version
  - Flask version

**Example:**
```markdown
**Bug**: Music button doesn't toggle

**Steps to Reproduce**:
1. Open app in Firefox 120
2. Click music button (🔊)
3. Nothing happens

**Expected**: Music should start playing
**Actual**: No sound, button doesn't change state

**Environment**: Windows 11, Firefox 120.0, Python 3.10
```

### Suggesting Enhancements 💡

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any alternative solutions** you've considered
- **Include mockups or examples** if applicable

### Pull Requests 🔄

- Fill in the pull request template
- Follow the [style guidelines](#style-guidelines)
- Include screenshots for UI changes
- Update documentation as needed
- Add tests if applicable

## 🛠️ Development Guidelines

### Project Structure

Understand the project structure before making changes:

```
app/
├── __init__.py      # Application factory
├── config.py        # Configuration
├── extensions.py    # Flask extensions
├── models.py        # Database models
├── sockets.py       # WebSocket handlers
├── utils.py         # Utility functions
└── routes/          # Route blueprints
    ├── admin.py     # Admin panel routes
    ├── auth.py      # Authentication routes
    └── main.py      # Main routes
```

### Running Tests

Currently, this project doesn't have automated tests. **This is a great area to contribute!**

If you add tests:
```bash
# Run tests (once implemented)
pytest tests/
```

### Database Migrations

If you modify database models:
```bash
# Generate migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

## 🎨 Style Guidelines

### Python Code Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines:

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters (flexible for readability)
- Use descriptive variable names
- Add docstrings to functions and classes
- Add comments for complex logic

**Example:**
```python
def calculate_message_count(user_id: int) -> int:
    """
    Calculate the total number of messages sent by a user.
    
    Args:
        user_id: The ID of the user
        
    Returns:
        The total count of messages
    """
    return Message.query.filter_by(user_id=user_id).count()
```

### JavaScript Style

- Use ES6+ features where supported
- Use `const` and `let` (avoid `var`)
- Use camelCase for variable names
- Add comments for complex logic
- Keep functions focused and small

**Example:**
```javascript
// Good
const playSound = (soundType) => {
    if (soundEnabled && sounds[soundType]) {
        sounds[soundType].currentTime = 0;
        sounds[soundType].play().catch(() => {});
    }
};

// Avoid
var x = function(t) { /* ... */ };
```

### CSS Style

- Follow existing DS theme patterns
- Use CSS variables for colors
- Keep selectors specific to avoid conflicts
- Comment major sections
- Maintain responsive design

**Example:**
```css
/* DS Button Component */
.ds-btn {
    font-family: 'Press Start 2P', monospace;
    background: var(--ds-input-bg);
    color: var(--ds-text);
    border: 2px solid var(--ds-border);
    /* ... */
}
```

### HTML/Templates

- Use semantic HTML5 elements
- Maintain accessibility (alt text, ARIA labels)
- Follow Jinja2 template conventions
- Keep templates DRY (extend base.html)

## 📝 Commit Messages

Write clear, descriptive commit messages:

### Format
```
type: Short description (50 chars or less)

Longer explanation if needed (wrap at 72 characters).
Explain what changed and why, not how.

- Bullet points are okay
- Use present tense ("Add feature" not "Added feature")
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples
```bash
# Good
feat: Add volume slider for background music
fix: Resolve typing indicator not clearing
docs: Update music setup instructions

# Avoid
Update stuff
Fixed things
WIP
```

## 🔄 Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Update CHANGELOG.md** with your changes
3. **Ensure your code follows style guidelines**
4. **Test thoroughly** before submitting
5. **Write a clear PR description**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [x] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   How did you test your changes?
   
   ## Screenshots (if applicable)
   Add screenshots here
   ```

6. **Request review** from maintainers
7. **Address feedback** promptly and respectfully
8. **Squash commits** if requested before merge

## 🎯 Good First Issues

New to the project? Look for issues labeled:
- `good first issue`
- `help wanted`
- `documentation`
- `beginner-friendly`

## 💡 Feature Suggestions

Want to add a big feature? **Please open an issue first** to discuss:
- Is this feature aligned with project goals?
- How should it be implemented?
- Are there any concerns?

This prevents wasted effort on pull requests that may not be accepted.

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Socket.IO Documentation](https://socket.io/docs/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

## 🙏 Thank You!

Your contributions make PictoFlask better for everyone. Whether you're:
- Reporting bugs
- Suggesting features
- Writing code
- Improving documentation
- Helping other users

**You're awesome!** 🎮💬

---

**Questions?** Feel free to open an issue or start a discussion on GitHub!

Made with ❤️ and nostalgia for the Nintendo DS era.
