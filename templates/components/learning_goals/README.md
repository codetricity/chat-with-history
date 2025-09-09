# Learning Goals Components

This folder contains reusable learning goals components for different pages in the application.

## Structure

- `chat_learning_goals.html` - Learning objectives for the AI chat page
- `README.md` - This documentation file

## Usage

Each learning goals component should be included in the appropriate page template:

```html
{% include "components/learning_goals/chat_learning_goals.html" %}
```

## Requirements

Each learning goals component should:

1. Use Alpine.js for interactivity with `showLearningGoals` variable
2. Follow the established design pattern with:
   - Dropdown header with icon and title
   - Collapsible content with smooth transitions
   - Color-coded sections for different topics
   - Technical implementation details in code blocks
   - Visual icons for each learning objective

## Design Pattern

The learning goals components follow a consistent design pattern:

- **Header**: Clickable area with icon, title, and description
- **Content**: Collapsible sections with smooth transitions
- **Sections**: Each learning objective has:
  - Colored icon in a rounded container
  - Clear title and description
  - Technical implementation details
  - Code examples in monospace font

## Adding New Learning Goals

To add learning goals for a new page:

1. Create a new file: `{page_name}_learning_goals.html`
2. Follow the established pattern from `chat_learning_goals.html`
3. Update the parent page to include the component
4. Add the `showLearningGoals: false` variable to the page's Alpine.js data function
