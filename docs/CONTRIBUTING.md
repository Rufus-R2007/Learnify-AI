# Contributing to Learnify AI

Thank you for your interest in contributing to Learnify AI! This document provides guidelines for contributing to the project.

---

## 🎯 Project Goals

Learnify AI aims to:
1. Demonstrate practical AI concepts from college curriculum
2. Provide a functional educational chatbot
3. Serve as a learning resource for AI students
4. Implement 25+ AI concepts across 5 units

---

## 🤝 How to Contribute

### Types of Contributions

We welcome:

- 🐛 **Bug fixes** - Fix issues or errors
- ✨ **New features** - Implement AI concepts from the roadmap
- 📚 **Documentation** - Improve guides and comments
- 🎨 **UI improvements** - Enhance user interface
- ⚡ **Performance** - Optimize code and algorithms
- 🧪 **Tests** - Add test coverage
- 💡 **Ideas** - Suggest new features or improvements

---

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button on GitHub to create your copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/AI-Micro-Project.git
cd AI-Micro-Project
```

### 3. Set Up Development Environment

Follow the [Setup Guide](../SETUP_GUIDE.md) to install dependencies.

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding tests

---

## 💻 Development Workflow

### 1. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation if needed

### 2. Test Your Changes

#### Backend Testing
```bash
cd backend
pytest
```

#### Frontend Testing
```bash
cd frontend
npm run lint
npm run build  # Ensure it builds
```

#### Manual Testing
1. Start both backend and frontend
2. Test the feature in the browser
3. Check for console errors
4. Test edge cases

### 3. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add BFS algorithm implementation"
```

Good commit message format:
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

Examples:
```
feat: Add semantic network knowledge representation

Implements semantic network data structure with nodes and edges.
Includes methods for adding concepts and relationships.

Relates to #12
```

```
fix: Correct CORS configuration for production

Updates allowed origins to include production domain.
Fixes issue where frontend couldn't connect to API.

Fixes #45
```

Commit types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting (no code change)
- `refactor` - Code refactoring
- `test` - Adding tests
- `chore` - Maintenance

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template
5. Submit the PR

---

## 📝 Pull Request Guidelines

### PR Title Format

```
[Type] Brief description
```

Examples:
- `[Feature] Add A* search algorithm`
- `[Fix] Correct message timestamp display`
- `[Docs] Update API documentation`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## AI Concepts Implemented (if applicable)
- [ ] Concept 1: Description
- [ ] Concept 2: Description

## Testing
Describe how you tested the changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows project style
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No console errors or warnings
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, PR will be merged
4. Your contribution will be credited

---

## 🎨 Code Style Guidelines

### Python (Backend)

```python
# Use type hints
def process_query(query: str, context: List[Dict]) -> Tuple[str, List[str], float]:
    """
    Process user query and generate response
    
    Args:
        query: User's question
        context: Conversation history
        
    Returns:
        Tuple of (response, concepts_used, confidence)
    """
    pass

# Follow PEP 8
# Use descriptive variable names
# Add docstrings to functions and classes
# Keep functions focused and small
```

### TypeScript (Frontend)

```typescript
// Use explicit types
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

// Use descriptive names
const handleSendMessage = async (content: string): Promise<void> => {
  // Implementation
};

// Add comments for complex logic
// Use functional components with hooks
// Keep components small and focused
```

### General Guidelines

- **Naming:** Use camelCase for variables/functions, PascalCase for classes/components
- **Comments:** Explain why, not what (code should be self-explanatory)
- **Imports:** Organize imports logically
- **Error Handling:** Always handle errors appropriately
- **Console Logs:** Remove debug logs before committing

---

## 🧠 Implementing AI Concepts

When implementing AI concepts from the roadmap:

### 1. Plan Your Implementation

- Review the concept in the README roadmap
- Understand the theory behind the concept
- Design the data structures needed
- Plan the algorithm implementation

### 2. Create Files

```
backend/app/ai/
├── knowledge/           # Unit 1: Knowledge Representation
│   ├── semantic_network.py
│   └── frames.py
├── search/             # Unit 2: Search Algorithms
│   ├── uninformed.py
│   └── informed.py
├── logic/              # Unit 3: Logic and Reasoning
│   ├── propositional.py
│   └── first_order.py
├── rules/              # Unit 4: Rule-Based Systems
│   └── production_rules.py
└── expert/             # Unit 5: Expert Systems
    └── inference_engine.py
```

### 3. Write Tests

```python
# backend/tests/test_search_algorithms.py
def test_bfs_finds_shortest_path():
    """Test that BFS finds the shortest path"""
    graph = create_test_graph()
    result = bfs(graph, start='A', goal='D')
    assert result.path == ['A', 'B', 'D']
    assert result.cost == 2
```

### 4. Integrate with Chat Service

Update `backend/app/services/ai_service.py` to use your implementation.

### 5. Update Documentation

- Mark concept as implemented in README
- Add usage examples
- Update API documentation if needed

---

## 🧪 Testing Guidelines

### Writing Tests

```python
# Backend test example
import pytest
from app.services.ai_service import AIService

@pytest.fixture
def ai_service():
    return AIService()

def test_greeting_detection(ai_service):
    """Test that greetings are detected correctly"""
    response, concepts, confidence = ai_service.process_query("hello")
    assert "hello" in response.lower()
    assert "Rule-Based System" in concepts
    assert confidence > 0.9
```

```typescript
// Frontend test example (future)
import { render, screen } from '@testing-library/react';
import MessageBubble from './MessageBubble';

test('renders user message correctly', () => {
  const message = {
    id: '1',
    role: 'user',
    content: 'Test message',
    timestamp: new Date()
  };
  
  render(<MessageBubble message={message} />);
  expect(screen.getByText('Test message')).toBeInTheDocument();
});
```

### Test Coverage

Aim for:
- **Backend:** 80%+ coverage
- **Frontend:** 70%+ coverage
- 100% coverage for critical algorithms

---

## 📚 Documentation Standards

### Code Comments

```python
def a_star_search(graph: Graph, start: Node, goal: Node, heuristic: Callable) -> Path:
    """
    Implement A* search algorithm
    
    A* uses f(n) = g(n) + h(n) where:
    - g(n) is the cost from start to n
    - h(n) is the heuristic estimate from n to goal
    
    Args:
        graph: The search space
        start: Starting node
        goal: Goal node
        heuristic: Heuristic function h(n)
        
    Returns:
        Path object containing the solution path and cost
        
    Raises:
        NoPathFoundError: If no path exists from start to goal
        
    Example:
        >>> graph = create_graph()
        >>> path = a_star_search(graph, 'A', 'Z', euclidean_distance)
        >>> print(path.nodes)
        ['A', 'B', 'D', 'Z']
    """
```

### README Updates

When implementing a concept, update the README:

```markdown
| # | Concept | Description | Status |
|---|---------|-------------|--------|
| 6 | Uninformed Search | BFS, DFS, DLS, IDS, UCS | ✅ Implemented |
```

Change status from ⏳ Planned to ✅ Implemented.

---

## 🐛 Reporting Bugs

### Before Reporting

1. Check existing issues
2. Verify it's reproducible
3. Test on latest version

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Windows 11]
- Browser: [e.g., Chrome 120]
- Python version: [e.g., 3.11]
- Node version: [e.g., 18.16]

**Additional Context**
Any other relevant information
```

---

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why this feature would be useful

**AI Concept Alignment**
Which AI concept(s) does this relate to?

**Proposed Implementation**
Your ideas on how to implement it (optional)

**Alternatives Considered**
Other approaches you've thought about
```

---

## 🏆 Recognition

Contributors will be:
- Listed in the project README
- Credited in release notes
- Acknowledged in documentation

---

## ❓ Questions?

- Open an issue with the `question` label
- Check existing documentation
- Ask in project discussions

---

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a friendly, safe, and welcoming environment for all contributors.

### Expected Behavior

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Thank you for contributing to Learnify AI! 🎉**

Together, we're making AI education more accessible.
