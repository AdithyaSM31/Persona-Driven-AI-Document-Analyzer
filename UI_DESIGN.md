# 🎨 UI Design Overview

## Color Palette

### Primary Colors
- **Primary**: `#6366f1` (Indigo)
- **Primary Dark**: `#4f46e5`
- **Primary Light**: `#818cf8`

### Background
- **Main Gradient**: Purple gradient (from `#667eea` to `#764ba2`)
- **Card Background**: `#ffffff` (White)
- **Secondary Background**: `#f8fafc` (Light gray)

### Text Colors
- **Primary Text**: `#0f172a` (Dark slate)
- **Secondary Text**: `#475569` (Slate)
- **Tertiary Text**: `#94a3b8` (Light slate)

## Typography

- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700

## Layout Sections

### 1. Header
- White card with subtle shadow
- Logo icon with floating animation
- Title and subtitle
- Centered alignment

### 2. Input Section (Main Form)
- **Persona Input**: Text field with user icon
- **Task Description**: Textarea with task icon
- **File Upload**: 
  - Drag & drop zone with dashed border
  - Upload icon (48x48px)
  - File list with remove buttons
  - PDF icon for each file
- **Analyze Button**: Full-width primary button with lightning icon

### 3. Loading Section
- Centered spinner animation
- Loading message
- Clean, minimal design

### 4. Results Section
- **Metadata Grid**: 
  - Documents count
  - Persona description
  - Processing time
  - Timestamp
- **Top Sections**:
  - Ranked cards (1-5)
  - Section title and document name
  - Page number
  - Relevance score badge (green)
  - Left border accent (primary color)
  - Hover effect with translation
- **Detailed Analysis**:
  - Text excerpts in cards
  - Document name and page number headers
  - Border separating header from content

### 5. Error Section
- Error icon (red)
- Error message
- Retry button

## Interactive Elements

### Buttons
- **Primary Button**: Purple background, white text, hover lift effect
- **Secondary Button**: White background, border, hover border color change
- **Icon Buttons**: SVG icons (20x20px) with text

### Form Inputs
- 2px border, rounded corners (8px)
- Focus state: Blue border with glow effect
- Transitions: 0.3s cubic-bezier easing

### Cards
- Border radius: 16px for main cards, 12px for nested cards
- Box shadows: Multi-layer for depth
- Hover states on interactive cards

## Animations

1. **Fade In Down**: Header entrance
2. **Fade In Up**: Cards and results entrance
3. **Slide In Right**: File list items
4. **Spin**: Loading spinner
5. **Float**: Logo icon subtle movement

## Responsive Breakpoints

### Desktop (> 768px)
- Max width: 900px container
- Side-by-side metadata grid
- Full padding and spacing

### Tablet (≤ 768px)
- Stacked metadata grid
- Reduced padding
- Smaller title font
- Vertical results header

### Mobile (≤ 480px)
- Single column layout
- Compact spacing
- Smaller logo and fonts
- Vertical stacking for all elements

## Key UI Components

### File Upload Area
```
┌─────────────────────────────────┐
│         [Upload Icon]          │
│  Choose PDF files or drag &    │
│           drop                  │
└─────────────────────────────────┘
```

### Section Card
```
┌───────────────────────────────┐
│ [1] Section Title            │
│     📄 document.pdf          │
│     📖 Page 5                │
│     [85% Match]              │
└───────────────────────────────┘
```

### Metadata Grid
```
┌──────────┬──────────┬──────────┬──────────┐
│Documents │ Persona  │   Time   │Timestamp │
│    3     │Health... │  2.45s   │Oct 20... │
└──────────┴──────────┴──────────┴──────────┘
```

## Accessibility Features

- Semantic HTML structure
- High contrast text
- Clear focus states
- Icon + text labels
- Responsive design
- Keyboard navigation support

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Android)

## Performance Optimizations

- Inline SVG icons (no external requests)
- Single CSS and JS files
- Minimal dependencies
- Optimized animations (GPU accelerated)
- Lazy loading of results
