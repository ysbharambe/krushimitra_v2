# Contributing to KrushiMitra

Thank you for your interest in contributing to KrushiMitra! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python version, Node version)

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Test backend endpoints
   - Test frontend components
   - Ensure no breaking changes

5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe your changes
   - Link related issues
   - Add screenshots for UI changes

## Development Guidelines

### Code Style

**Python (Backend)**
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions focused and small

**JavaScript (Frontend)**
- Use functional components
- Follow React best practices
- Use meaningful variable names
- Add PropTypes or TypeScript

### Commit Messages

Format: `Type: Brief description`

Types:
- `Add:` New feature
- `Fix:` Bug fix
- `Update:` Modification to existing feature
- `Refactor:` Code restructuring
- `Docs:` Documentation changes
- `Style:` Formatting, missing semicolons, etc.
- `Test:` Adding tests

Examples:
```
Add: multilingual support for Hindi
Fix: image upload timeout issue
Update: pesticide recommendations database
Docs: add API endpoint examples
```

### Testing

- Test all new features thoroughly
- Check edge cases
- Verify on multiple browsers (frontend)
- Test API endpoints with different inputs (backend)

## Areas for Contribution

### High Priority
- Add more plant diseases to detection model
- Improve translation accuracy
- Add more regional languages
- Optimize model inference speed
- Add user feedback mechanism

### Medium Priority
- Add disease severity classification
- Implement crop type detection
- Add seasonal disease alerts
- Create mobile app version
- Add offline mode support

### Documentation
- Improve setup instructions
- Add video tutorials
- Translate documentation
- Add API usage examples
- Create troubleshooting guide

### Design
- Improve UI/UX
- Add dark mode
- Create better icons
- Improve mobile responsiveness
- Add accessibility features

## Questions?

Feel free to:
- Open a discussion on GitHub
- Comment on existing issues
- Reach out to maintainers

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Keep discussions on-topic

Thank you for contributing to KrushiMitra! 🌱
