# Header Component

A standardized, reusable header component for the Marketing Firm Admin application.

## Features

- **Consistent Design**: Uses Tailwind CSS for consistent styling across all pages
- **Flexible Configuration**: Customizable through template variables and blocks
- **Responsive Layout**: Works on desktop and mobile devices
- **Icon Support**: Font Awesome icons for better visual hierarchy
- **Action Buttons**: Pre-configured action buttons for common operations
- **Navigation Links**: Standard navigation with conditional display

## Usage

### Basic Usage

```html
{% include "components/header.html" %}
```

### With Custom Title and Badge

```html
{% set page_title="My Page" %}
{% set page_badge="Beta" %}
{% include "components/header.html" %}
```

### With Action Buttons

```html
{% set page_title="Conversations" %}
{% set show_search_button=True %}
{% set show_new_client_button=True %}
{% set show_new_project_button=True %}
{% set show_new_folder_button=True %}
{% include "components/header.html" %}
```

### With Navigation Links

```html
{% set show_conversations_link=True %}
{% set show_admin_link=True %}
{% set show_logout_link=True %}
{% include "components/header.html" %}
```

## Configuration Options

### Template Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `page_title` | String | "Content Management Hub" | Main page title |
| `page_badge` | String | None | Optional badge text |
| `show_search_button` | Boolean | False | Show search action button |
| `show_new_client_button` | Boolean | False | Show new client button |
| `show_new_project_button` | Boolean | False | Show new project button |
| `show_new_folder_button` | Boolean | False | Show new folder button |
| `show_conversations_link` | Boolean | False | Show conversations nav link |
| `show_admin_link` | Boolean | False | Show admin nav link |
| `show_login_link` | Boolean | False | Show login nav link |
| `show_logout_link` | Boolean | False | Show logout nav link |

### Template Blocks

#### `page_title`
Override the page title block for dynamic content:

```html
{% block page_title %}{{ user.name }}'s Dashboard{% endblock %}
```

#### `action_buttons`
Add custom action buttons:

```html
{% block action_buttons %}
<button class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium">
    <i class="fas fa-trash mr-1"></i>
    Delete All
</button>
{% endblock %}
```

#### `nav_links`
Add custom navigation links:

```html
{% block nav_links %}
<a href="/custom-page" class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium">
    <i class="fas fa-star mr-1"></i>
    Custom Link
</a>
{% endblock %}
```

## Examples

See `header_example.html` for comprehensive usage examples.

## Styling

The header component uses Tailwind CSS classes and follows the design system:

- **Background**: White with subtle shadow
- **Typography**: Bold title with gray text for navigation
- **Colors**: Blue for primary actions, purple/indigo/green for secondary actions
- **Spacing**: Consistent padding and margins
- **Icons**: Font Awesome icons with proper spacing

## Dependencies

- Tailwind CSS
- Font Awesome (for icons)
- Alpine.js (for interactive elements like modals)

## Browser Support

- Modern browsers with CSS Grid and Flexbox support
- Mobile responsive design
- Touch-friendly button sizes
