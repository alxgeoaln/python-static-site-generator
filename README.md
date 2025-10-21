# Static Site Generator

A custom-built static site generator written in Python that converts Markdown files into a website.

## 🚀 Features

- **Markdown to HTML Conversion** - Write content in Markdown, get beautiful HTML
- **Multiple Page Support** - Automatically generates pages from directory structure
- **Configurable Base Path** - Deploy to GitHub Pages or any subdirectory
- **Responsive Design** - Clean, simple styling that works on all devices
- **Dark Mode Support** - Automatically adapts to system preferences
- **Static Asset Management** - Copies and manages CSS, images, and other assets
- **Blog/Portfolio Structure** - Organized content structure for professional portfolios

## 📋 Prerequisites

- Python 3.x
- Git (for version control and deployment)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/alxgeoaln/python-static-site-generator.git
cd python-static-site-generator
```

2. The project uses only Python standard library, no additional dependencies required!

## 📁 Project Structure

```
static-site-generator/
├── content/              # Markdown content files
│   ├── index.md         # Homepage
│   ├── contact/         # Contact page
│   └── blog/            # Blog posts/sections
│       ├── experience/
│       ├── skills/
│       └── projects/
├── static/              # Static assets (CSS, images)
│   ├── index.css
│   └── images/
├── src/                 # Python source code
│   ├── main.py         # Entry point
│   ├── html.py         # Page generation logic
│   ├── block_parser.py # Markdown block parsing
│   ├── text_parsers.py # Inline text parsing
│   ├── htmlnode.py     # HTML node classes
│   ├── textnode.py     # Text node classes
│   └── blocknode.py    # Block node classes
├── docs/               # Generated site (GitHub Pages)
├── template.html       # HTML template
├── build.sh           # Production build script
└── main.sh            # Development build script
```

## 🎯 Usage

### Local Development

Build the site for local testing (uses `/` as base path):

```bash
python3 -m src.main
```

Or use the shell script:

```bash
./main.sh
```

The site will be generated in the `./docs` directory. You can open `docs/index.html` in your browser to view it.

### Production Build

Build the site for GitHub Pages deployment:

```bash
./build.sh
```

This builds with the correct base path (`/python-static-site-generator/`) for GitHub Pages.

### Custom Base Path

You can specify a custom base path as a command-line argument:

```bash
python3 -m src.main "/my-custom-path/"
```

## 📝 Creating Content

### Adding a New Page

1. Create a new Markdown file in the `content/` directory:
```markdown
# Page Title

Your content here...
```

2. Run the build command:
```bash
python3 -m src.main
```

### Organizing Content

- **Homepage**: Edit `content/index.md`
- **Blog Posts**: Create subdirectories in `content/blog/`
- **Nested Pages**: Create subdirectories with their own `index.md` files

### Markdown Features Supported

- **Headings**: `#`, `##`, `###`, etc.
- **Bold**: `**text**`
- **Italic**: `_text_`
- **Code**: `` `code` `` and ` ```code blocks``` `
- **Links**: `[text](url)`
- **Images**: `![alt](url)`
- **Lists**: Ordered (`1.`) and unordered (`-`, `*`)
- **Blockquotes**: `> quote`
- **Horizontal Rules**: `---`

## 🏗️ Architecture

### Core Components

- **`main.py`**: Entry point, handles CLI arguments and orchestrates the build
- **`html.py`**: Manages page generation, template rendering, and static file copying
- **`block_parser.py`**: Parses Markdown blocks (headings, paragraphs, lists, code blocks)
- **`text_parsers.py`**: Parses inline text formatting (bold, italic, links, images, code)
- **`htmlnode.py`**: HTML node representation and rendering
- **`textnode.py`**: Text node types and transformations
- **`blocknode.py`**: Block-level node types

## 🧪 Testing

Run the test suite:

```bash
./test.sh
```

Or run individual test files:

```bash
python3 -m pytest src/tests/test_htmlnode.py
python3 -m pytest src/tests/test_textnode.py
python3 -m pytest src/tests/test_block_parser.py
```

## 👤 Author

**Alin Alexandru**
- GitHub: [@alxgeoaln](https://github.com/alxgeoaln)
- LinkedIn: [linkedin.com/in/alin-alexandru-312347245](https://linkedin.com/in/alin-alexandru-312347245)
- Email: georgianalinalexandru@gmail.com
---

**Live Site**: [https://alxgeoaln.github.io/python-static-site-generator/](https://alxgeoaln.github.io/python-static-site-generator/)

