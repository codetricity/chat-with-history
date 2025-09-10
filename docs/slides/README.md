# AI-Powered Business Applications Course Slides

This directory contains Marp-formatted slides for the AI-Powered Business Applications course. The slides are based on the learning materials in the `docs/learning/` directory and cover the core concepts of building AI applications with FastAPI and FastOpp.

## 📚 Course Modules

### 1. Course Overview (`01_course_overview.md`)
- Course introduction and learning objectives
- Technology stack overview
- Business use cases and cost-effective deployment
- Learning path and prerequisites

### 2. AI Chat UI (`02_ai_chat_ui.md`)
- Streaming responses for real-time interactivity
- Context management with conversation history
- Internet search integration with smart triggering
- Database connectivity for business context
- Advanced features for production applications

### 3. Conversation Organization (`03_conversation_organization.md`)
- Hierarchical folder structure with project-based organization
- Drag-and-drop interface using Sortable.js
- Business context integration (clients, projects, content status)
- Advanced filtering by multiple criteria
- Real-time collaboration potential

### 4. Vector Databases & Hybrid Search (`04_vector_databases_hybrid_search.md`)
- Hybrid search concepts (semantic + keyword)
- Embeddings and vector databases (FAISS)
- FTS5 full-text search capabilities
- Weight modification and tuning
- Real-world applications (customer analysis)

## 🚀 Getting Started

### Prerequisites

- [Marp CLI](https://github.com/marp-team/marp-cli) installed globally
- Basic understanding of Markdown
- Familiarity with the FastOpp project

### Installation

```bash
# Install Marp CLI globally
npm install -g @marp-team/marp-cli

# Or use npx (no installation required)
npx @marp-team/marp-cli --help
```

### Viewing Slides

#### Option 1: HTML Output
```bash
# Generate HTML from Markdown
marp docs/slides/01_course_overview.md -o docs/slides/01_course_overview.html

# Open in browser
open docs/slides/01_course_overview.html
```

#### Option 2: PDF Output
```bash
# Generate PDF
marp docs/slides/01_course_overview.md -o docs/slides/01_course_overview.pdf
```

#### Option 3: Live Preview
```bash
# Start live preview server
marp docs/slides/01_course_overview.md --preview

# Or watch for changes
marp docs/slides/01_course_overview.md --watch
```

### Batch Processing

```bash
# Convert all slides to HTML
for file in docs/slides/*.md; do
  marp "$file" -o "${file%.md}.html"
done

# Convert all slides to PDF
for file in docs/slides/*.md; do
  marp "$file" -o "${file%.md}.pdf"
done
```

## 🎨 Customization

### Themes

The slides use the `gaia` theme by default. You can change this by modifying the frontmatter:

```yaml
---
theme: gaia  # or 'default', 'uncover'
_class: lead
paginate: true
backgroundColor: #fff
---
```

### Styling

You can customize the appearance by:

1. **Modifying the frontmatter** in each slide file
2. **Adding custom CSS** using the `style` directive
3. **Using Marp directives** for advanced formatting

### Example Customization

```yaml
---
theme: gaia
_class: lead
paginate: true
backgroundColor: #f0f0f0
backgroundImage: url('path/to/background.jpg')
style: |
  section {
    font-family: 'Arial', sans-serif;
  }
  h1 {
    color: #2c3e50;
  }
---
```

## 📖 Course Structure

### Learning Flow

1. **Start with Course Overview** - Understand the big picture
2. **AI Chat UI** - Learn about streaming and context management
3. **Conversation Organization** - Master business-focused organization
4. **Vector Databases & Hybrid Search** - Implement intelligent search

### Assessment Flow

1. **Test features** on live site with learning objectives
2. **Review code** and documentation
3. **Watch video tutorials** (coming soon)
4. **Subscribe** for video notifications as we complete them

## 🔧 Development

### Adding New Slides

1. Create a new Markdown file in the `docs/slides/` directory
2. Use the Marp frontmatter format
3. Follow the existing slide structure and naming convention
4. Update this README with the new slide information

### Slide Structure

Each slide file should follow this structure:

```yaml
---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
---

# Slide Title

## Subtitle

Content here...

---

# Next Slide

More content...
```

### Best Practices

- **Keep slides focused** - One concept per slide
- **Use clear headings** - Make the structure obvious
- **Include code examples** - Show, don't just tell
- **Add visual breaks** - Use `---` to separate sections
- **Test regularly** - Preview slides as you create them

## 🌐 Integration with FastOpp

These slides are designed to work alongside the FastOpp project:

- **Live site** - Test features as you learn
- **Code examples** - All examples are from the actual codebase
- **Real-world context** - Business use cases and practical applications
- **Hands-on learning** - Build while you learn

## 📚 Additional Resources

- [Marp Documentation](https://marp.app/)
- [Marp CLI GitHub](https://github.com/marp-team/marp-cli)
- [FastOpp Repository](https://github.com/Oppkey/fastopp)
- [Course Learning Materials](../learning/)

## 🤝 Contributing

We welcome contributions to improve these slides:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test the slides**
5. **Submit a pull request**

## 📄 License

This course and all materials are open source and available under the MIT License. We believe in learning together and sharing knowledge freely.

---

**Happy Learning! 🚀**

The best way to learn is by building. Start with small modifications and gradually add more sophisticated features.


