---
name: Brand Design System
description: Ensures all UI code matches brand identity with consistent design tokens
---

# Brand Design System Skill

## Purpose

This skill ensures **visual consistency** across all UI components by enforcing brand design tokens (colors, typography, spacing) and preventing ad-hoc styling that breaks brand identity.

## Triggers

- Creating new UI components
- Styling HTML/CSS/React/Vue components
- User mentions "design", "UI", "interface", "styling"
- Generating images or visual assets
- Creating landing pages or dashboards

## Brand Design Tokens

### Color Palette

```javascript
// Primary Colors
const colors = {
  // Brand Identity
  primary: '#6366F1',      // Indigo - Main brand color
  primaryDark: '#4F46E5',  // Darker variant for hover
  primaryLight: '#818CF8', // Lighter variant for backgrounds
  
  // Accent Colors
  accent: '#EC4899',       // Pink - Call-to-action
  accentDark: '#DB2777',
  accentLight: '#F472B6',
  
  // Neutrals
  dark: '#0F172A',         // Slate 900 - Text
  darkAlt: '#1E293B',      // Slate 800 - Backgrounds
  gray: '#64748B',         // Slate 500 - Secondary text
  grayLight: '#CBD5E1',    // Slate 300 - Borders
  light: '#F1F5F9',        // Slate 100 - Backgrounds
  white: '#FFFFFF',
  
  // Semantic Colors
  success: '#10B981',      // Green
  warning: '#F59E0B',      // Amber
  error: '#EF4444',        // Red
  info: '#3B82F6',         // Blue
};
```

### Typography

```css
/* Font Family */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-display: 'Outfit', 'Inter', sans-serif;
--font-code: 'JetBrains Mono', 'Fira Code', monospace;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Spacing

```css
/* Spacing Scale (rem-based) */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-24: 6rem;     /* 96px */
```

### Effects

```css
/* Shadows */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

/* Border Radius */
--radius-sm: 0.375rem;  /* 6px */
--radius-md: 0.5rem;    /* 8px */
--radius-lg: 0.75rem;   /* 12px */
--radius-xl: 1rem;      /* 16px */
--radius-2xl: 1.5rem;   /* 24px */
--radius-full: 9999px;

/* Transitions */
--transition-fast: 150ms ease;
--transition-base: 200ms ease;
--transition-slow: 300ms ease;
```

## Execution Checklist

When creating UI components:

- [ ] **Load Design Tokens**: Import or reference brand colors, fonts, spacing
- [ ] **Use CSS Variables**: Prefer `var(--primary)` over hardcoded `#6366F1`
- [ ] **Semantic Naming**: Use color purposes (primary, accent) not values (blue, pink)
- [ ] **Consistent Spacing**: Use spacing scale, not arbitrary values
- [ ] **Typography Hierarchy**: Use defined font sizes and weights
- [ ] **Shadows & Effects**: Use predefined shadow tokens
- [ ] **Responsive Design**: Mobile-first with consistent breakpoints
- [ ] **Accessibility**: WCAG AA contrast ratios (4.5:1 for text)
- [ ] **Dark Mode Support**: Define dark mode variants if needed
- [ ] **Component Library**: Check if component already exists before creating

## Patterns & Examples

### Pattern 1: CSS Variables Setup

```css
:root {
  /* Colors */
  --color-primary: #6366F1;
  --color-primary-dark: #4F46E5;
  --color-accent: #EC4899;
  --color-dark: #0F172A;
  --color-gray: #64748B;
  --color-light: #F1F5F9;
  
  /* Typography */
  --font-primary: 'Inter', sans-serif;
  --text-base: 1rem;
  --text-lg: 1.25rem;
  
  /* Spacing */
  --space-4: 1rem;
  --space-6: 1.5rem;
  
  /* Effects */
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --radius-md: 0.5rem;
}
```

### Pattern 2: React Component with Design Tokens

```jsx
// Button.jsx
const Button = ({ variant = 'primary', children, ...props }) => {
  const styles = {
    primary: {
      backgroundColor: 'var(--color-primary)',
      color: 'var(--color-light)',
      padding: 'var(--space-3) var(--space-6)',
      borderRadius: 'var(--radius-md)',
      fontFamily: 'var(--font-primary)',
      fontSize: 'var(--text-base)',
      fontWeight: 'var(--font-semibold)',
      boxShadow: 'var(--shadow-md)',
      transition: 'var(--transition-base)',
    },
    accent: {
      backgroundColor: 'var(--color-accent)',
      // ... similar structure
    }
  };
  
  return <button style={styles[variant]} {...props}>{children}</button>;
};
```

### Pattern 3: Tailwind Config (if using Tailwind)

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    colors: {
      primary: '#6366F1',
      accent: '#EC4899',
      dark: '#0F172A',
      gray: '#64748B',
      light: '#F1F5F9',
    },
    fontFamily: {
      sans: ['Inter', 'sans-serif'],
      display: ['Outfit', 'sans-serif'],
    },
    extend: {
      spacing: {
        '18': '4.5rem',
        '112': '28rem',
      }
    }
  }
};
```

### Pattern 4: Image Generation with Brand Colors

When using `generate_image` tool:

```python
prompt = f"""
A modern dashboard interface with:
- Primary color: Indigo (#6366F1)
- Accent color: Pink (#EC4899)
- Dark backgrounds: Slate (#0F172A)
- Clean, minimal design
- Inter font family aesthetic
- Subtle shadows and rounded corners
"""
```

## Anti-Patterns

❌ **DON'T** use random colors
```css
/* BAD */
.button { background: #FF5733; }

/* GOOD */
.button { background: var(--color-primary); }
```

❌ **DON'T** use arbitrary spacing
```css
/* BAD */
.card { padding: 23px 17px; }

/* GOOD */
.card { padding: var(--space-6) var(--space-4); }
```

❌ **DON'T** mix font families randomly
```css
/* BAD */
h1 { font-family: 'Comic Sans'; }

/* GOOD */
h1 { font-family: var(--font-display); }
```

❌ **DON'T** create design tokens on the fly
```javascript
// BAD
const randomBlue = '#3A7BD5';

// GOOD
const primaryColor = 'var(--color-primary)';
```

## Integration

### With Odyssey ML
When generating UI images, always include brand colors in prompts:
```python
await generate_image(
    prompt="Modern dashboard with indigo primary, pink accents, dark slate background",
    ...
)
```

### With Workflows
- Use `/generate-video` with brand-consistent visuals
- Reference design tokens in all UI generation tasks

### With Other Skills
- **Troubleshooting Skill**: Check for color contrast issues
- **Planning Skill**: Include design token setup in architecture plans
- **NotebookLM Skill**: Query for design inspiration that matches brand

## Design Token Updates

When brand evolves:

1. Update tokens in this skill file
2. Re-export CSS variables
3. Run global find/replace for hardcoded values
4. Test all UI components
5. Update documentation
6. Commit with clear message: `[design] Update brand colors`

## Resources

- Google Fonts: https://fonts.google.com/specimen/Inter
- Color Contrast Checker: https://webaim.org/resources/contrastchecker/
- Design System Examples: https://www.designsystems.com/

---

**Remember**: Consistency > Creativity when it comes to brand identity.
