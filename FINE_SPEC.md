# Fine Spec: Debasish Mukherjee Personal Website

## Goal
Create a single-page professional website that presents Debasish Mukherjee's profile and enables contact only via email or LinkedIn.

## Inputs
- Debasish_Resume.pdf
- DebasishMukehrjee_LinkedIn.pdf

## Pages
- index.html (main profile page)
- email.html (email compose options page)

## Functional Requirements
- Display name, title, summary, highlights, experience, skills, certifications, education, and languages.
- Provide contact options only via email and LinkedIn.
- Do not display or link to any phone numbers.
- Email actions must open a new window that offers multiple ways to compose an email.

## Design Direction
- Professional, high-tech aesthetic with a dark gradient background and cyan/amber accents.
- Expressive typography: Space Grotesk for headings, JetBrains Mono for labels.
- Motion: subtle hero rise and section reveal animations with reduced-motion support.

## Technical Stack
- HTML5, modern CSS (Grid, custom properties), and ES2023 JavaScript.
- No build step required.

## Accessibility & Performance
- High-contrast text on dark background.
- Responsive layout for mobile and desktop.
- Lightweight assets and no external JS dependencies.

## Tests
- tests/test_site.py verifies contact methods and absence of phone numbers across both pages.

## Acceptance Criteria
- Page renders with all sections and a professional, high-tech look.
- Email and LinkedIn are the only contact methods visible.
- No phone numbers appear anywhere on the site.
- Responsive and accessible across common screen sizes.
