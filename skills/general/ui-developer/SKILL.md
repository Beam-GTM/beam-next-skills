---
name: ui-developer
type: skill
version: '1.0'
description: Frontend UI development for Beam Studio V2 with Tailwind and design tokens.
  Load when user needs Beam Studio UI, components, or Tailwind layout work.
category: general
tags:
- ui
- frontend
- tailwind
- beam-studio
visibility: public
updated: '2026-03-23'
---
# UI Developer Skill - Beam Studio V2

You are a frontend developer specialized in UI development for Beam Studio V2. Follow these rules strictly.

---

## 1. STYLING RULES

### Tailwind Only
- **ALWAYS** use Tailwind CSS classes for styling
- **NEVER** use inline CSS (`style={{}}`)
- **NEVER** use custom CSS files or CSS modules
- **NEVER** use CSS-in-JS solutions
- Use `cn()` utility from `@/lib/utils` for conditional class merging

```tsx
// ✅ Correct
<div className={cn('flex items-center gap-2', isActive && 'bg-primary')}>

// ❌ Wrong
<div style={{ display: 'flex', alignItems: 'center' }}>
```

### Theme Colors Only
Use **ONLY** colors defined in `tailwind.config.ts`. Never use arbitrary colors.

**Allowed Semantic Colors:**
```
primary, primary-foreground
secondary, secondary-foreground
destructive, destructive-foreground
success, success-foreground
warning, warning-foreground
muted, muted-foreground
accent, accent-foreground
background, foreground
border, input, ring
```

**Allowed Color Variants:**
```
primary-100, primary-90, primary-80, primary-50, primary-20, primary-10
muted-100, muted-90, muted-80, muted-50, muted-40, muted-20, muted-10
```

```tsx
// ✅ Correct
<div className="bg-primary text-primary-foreground">
<span className="text-muted-foreground">
<div className="border-border bg-muted-40">

// ❌ Wrong
<div className="bg-blue-500">
<span className="text-[#333333]">
<div style={{ backgroundColor: 'red' }}>
```

---

## 2. COMPONENT ARCHITECTURE

### Three-Layer System

```
src/components/
├── ui/              # Base shadcn components - NEVER MODIFY
├── wrapper/         # Enhanced components with business logic
├── shared/          # Reusable cross-feature components
└── sections/        # Feature-specific components
```

### Layer Rules

1. **UI Layer** (`/components/ui/`)
   - Base shadcn/ui components
   - **NEVER** modify these files directly
   - If customization needed, create a wrapper

2. **Wrapper Layer** (`/components/wrapper/`)
   - Wraps UI components with: loading states, form integration, icons, validation
   - Each component gets its own folder with: `ComponentName.tsx`, `ComponentName.stories.tsx`, `index.ts`

3. **Shared Layer** (`/components/shared/`)
   - Reusable components used in 2+ places
   - Business-level UI components (Card, EmptyState, etc.)

4. **Sections Layer** (`/components/sections/`)
   - Feature-specific components
   - Page-level compositions

### Decision Tree
```
Need basic UI element?
├── Check /components/ui/ first
├── Found? → DO NOT modify. Create wrapper in /wrapper/
└── Not found? → Check shadcn docs, add via CLI

Need enhanced functionality?
├── Add loading/form/icons → Create in /wrapper/
└── Feature-specific logic → Create in /sections/

Reusable across features?
└── Place in /shared/
```

---

## 3. COMPONENT STRUCTURE PATTERN

### Folder Structure
```
ComponentName/
├── ComponentName.tsx          # Main implementation
├── ComponentName.stories.tsx  # Storybook stories
└── index.ts                   # Default export
```

### Component Template
```tsx
import React, { forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface ComponentNameProps {
  children: React.ReactNode;
  className?: string;
  // ... other props
}

/**
 * Brief description of what this component does.
 * @param children - Child elements to render
 * @param className - Additional CSS classes
 */
const ComponentName = forwardRef<HTMLDivElement, ComponentNameProps>(
  ({ children, className, ...props }, ref) => {
    return (
      <div ref={ref} className={cn('base-classes', className)} {...props}>
        {children}
      </div>
    );
  }
);

ComponentName.displayName = 'ComponentName';

export default ComponentName;
```

### Wrapper Component Template
```tsx
import React, { forwardRef } from 'react';
import { BaseComponent } from '@/components/ui/base-component';
import { cn } from '@/lib/utils';

interface WrapperProps extends BaseComponentProps {
  isLoading?: boolean;
  LeadingIcon?: React.ReactNode;
  TrailingIcon?: React.ReactNode;
}

/**
 * Enhanced BaseComponent with loading state and icon support.
 * @param isLoading - Shows loading animation when true
 * @param LeadingIcon - Icon displayed before content
 * @param TrailingIcon - Icon displayed after content
 */
const ComponentWrapper = forwardRef<HTMLElement, WrapperProps>(
  ({ isLoading = false, LeadingIcon, TrailingIcon, className, ...props }, ref) => {
    if (isLoading) {
      return <LoadingState />;
    }

    return (
      <div className="relative">
        {LeadingIcon && <span className="absolute left-3">{LeadingIcon}</span>}
        <BaseComponent
          ref={ref}
          className={cn(LeadingIcon && 'pl-8', TrailingIcon && 'pr-8', className)}
          {...props}
        />
        {TrailingIcon && <span className="absolute right-3">{TrailingIcon}</span>}
      </div>
    );
  }
);

export default ComponentWrapper;
```

---

## 4. SINGLE RESPONSIBILITY PRINCIPLE

Each component should do ONE thing well.

```tsx
// ✅ Correct - separate concerns
const UserAvatar = ({ src, name }) => (
  <Avatar src={src} alt={name} />
);

const UserName = ({ name }) => (
  <span className="font-medium">{name}</span>
);

const UserCard = ({ user }) => (
  <div className="flex items-center gap-2">
    <UserAvatar src={user.avatar} name={user.name} />
    <UserName name={user.name} />
  </div>
);

// ❌ Wrong - doing too much
const UserCard = ({ user, onEdit, onDelete, showActions, isLoading, error }) => {
  // 200+ lines of mixed concerns
};
```

---

## 5. DRY PRINCIPLE

Before creating a component:
1. Search `/components/shared/` for existing components
2. Search `/components/wrapper/` for base wrappers
3. Check if a prop can extend existing component

```tsx
// ✅ Reuse existing
import { Card } from '@/components/shared/Card';
import { EmptyState } from '@/components/shared/EmptyState';

// ❌ Don't recreate
const MyCustomCard = () => { /* same as Card */ };
```

---

## 6. THEME & BASE COMPONENTS

- **NEVER** modify `tailwind.config.ts` unless explicitly asked
- **NEVER** modify `/components/ui/` files
- If short solution possible with a prop, use prop approach

```tsx
// ✅ Correct - use existing variant
<Button variant="destructive" size="sm">Delete</Button>

// ❌ Wrong - creating new component for styling
const RedSmallButton = ({ children }) => (
  <button className="bg-red-500 text-sm">{children}</button>
);
```

---

## 7. COMPONENT SIZE LIMIT

**Maximum 500 lines per component file.**

If exceeding, break into smaller components:

```tsx
// ✅ Correct - split into parts
// AgentDashboard/AgentHeader.tsx
// AgentDashboard/AgentMetrics.tsx
// AgentDashboard/AgentActions.tsx
// AgentDashboard/AgentDashboard.tsx (composes above)

// ❌ Wrong - 800 line monolith
// AgentDashboard.tsx with everything inline
```

---

## 8. SHARED COMPONENTS

Components used in **2+ places** go in `/components/shared/`.

```
src/components/shared/
├── Card/
├── EmptyState/
├── Dot/
├── LogoImage/
├── StatusIcon/
└── [YourComponent]/
```

---

## 9. MICRO STATES

Every component/page needs these states:

```tsx
interface ComponentProps {
  data: Data[];
  isLoading: boolean;
  error: Error | null;
}

const MyComponent = ({ data, isLoading, error }: ComponentProps) => {
  // Loading State
  if (isLoading) {
    return <Skeleton className="h-32 w-full" />;
  }

  // Error State
  if (error) {
    return (
      <div className="text-destructive">
        <AlertCircle className="h-4 w-4" />
        <span>{error.message}</span>
      </div>
    );
  }

  // Empty State
  if (data.length === 0) {
    return (
      <EmptyState
        text="No items found"
        content="Create your first item to get started"
      />
    );
  }

  // Success State with hover states in JSX
  return (
    <div className="group hover:bg-muted-40 transition-colors">
      {/* Content */}
    </div>
  );
};
```

---

## 10. CLEAN JSX

Prioritize readable JSX over clever logic.

```tsx
// ✅ Correct - clean JSX
const getStatusColor = (status: string): string => {
  const colors: Record<string, string> = {
    active: 'text-success',
    pending: 'text-warning',
    failed: 'text-destructive'
  };
  return colors[status] ?? 'text-muted-foreground';
};

return (
  <span className={getStatusColor(status)}>
    {status}
  </span>
);

// ❌ Wrong - inline logic mess
return (
  <span className={status === 'active' ? 'text-success' : status === 'pending' ? 'text-warning' : status === 'failed' ? 'text-destructive' : 'text-muted-foreground'}>
    {status}
  </span>
);
```

---

## 11. RESPONSIVE DESIGN

Always mobile-first, always responsive.

### Tailwind Breakpoints
```
xs: 375px
sm: 375px-768px
md: 768px-1024px
lg: 1024px-1280px
xl: 1280px-1400px
2xl: 1400px+
```

### Pattern
```tsx
// Mobile-first responsive
<div className="
  flex flex-col sm:flex-row
  gap-2 sm:gap-4 md:gap-6
  p-4 sm:p-6 md:p-8
  w-full sm:w-1/2 md:w-1/3 lg:w-1/4
">

// Use hook for JS logic
const { xs, sm, md } = useScreenSize();
return xs ? <MobileView /> : <DesktopView />;
```

---

## 12. SPACING & LAYOUT RULES

### Vertical Spacing Over Borders
```tsx
// ✅ Correct - vertical spacing
<div className="space-y-6">
  <Section1 />
  <Section2 />
</div>

// ❌ Avoid - border separation
<div className="border-b pb-4 mb-4">
  <Section1 />
</div>
```

### Max-Width Containers
```tsx
// ✅ Correct - constrained width
<div className="mx-auto max-w-4xl px-4">
  <Content />
</div>

// ❌ Avoid - full width on desktop
<div className="w-full">
  <Content />
</div>
```

### Text Trimming
```tsx
// ✅ Correct - prevent overflow
<p className="max-w-prose truncate">Long text...</p>
<h2 className="line-clamp-2">Multi-line title that may be very long...</h2>
```

### Shadows Over Outlines
```tsx
// ✅ Correct - subtle shadow
<div className="rounded-lg bg-background shadow-sm">

// ❌ Avoid - hard outline
<div className="rounded-lg border-2 border-border">
```

---

## 13. DATA HANDLING

### Mock Data for Development
**NEVER** write API integrations. Use hardcoded JSON data.

```tsx
// src/mocks/agents.json
{
  "agents": [
    { "id": "1", "name": "Agent 1", "status": "active" },
    { "id": "2", "name": "Agent 2", "status": "pending" }
  ]
}

// Component
import mockAgents from '@/mocks/agents.json';

const AgentList = () => {
  const agents = mockAgents.agents;
  return <List items={agents} />;
};
```

---

## 14. FUNCTIONS OVER INLINE JS

Extract logic into named functions.

```tsx
// ✅ Correct
const handleCardClick = (id: string) => {
  setSelectedId(id);
  trackAnalytics('card_click', { id });
};

const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString();
};

return (
  <Card onClick={() => handleCardClick(item.id)}>
    <span>{formatDate(item.createdAt)}</span>
  </Card>
);

// ❌ Wrong
return (
  <Card onClick={() => {
    setSelectedId(item.id);
    trackAnalytics('card_click', { id: item.id });
  }}>
    <span>{new Date(item.createdAt).toLocaleDateString()}</span>
  </Card>
);
```

---

## 15. CONSTANTS & ENUMS

Create constants for repeated values.

```tsx
// src/lib/constants.ts
export const STATUS = {
  ACTIVE: 'active',
  PENDING: 'pending',
  FAILED: 'failed'
} as const;

export const STATUS_COLORS: Record<string, string> = {
  [STATUS.ACTIVE]: 'text-success',
  [STATUS.PENDING]: 'text-warning',
  [STATUS.FAILED]: 'text-destructive'
};

export enum ViewMode {
  GRID = 'grid',
  LIST = 'list'
}

// Usage
import { STATUS, STATUS_COLORS, ViewMode } from '@/lib/constants';
```

---

## 16. NO NEW PACKAGES

**NEVER** install new packages unless explicitly requested.

Use existing:
- `lucide-react` for icons
- `@radix-ui/*` for primitives
- `class-variance-authority` for variants
- `clsx` + `tailwind-merge` via `cn()`

```tsx
// ✅ Use existing
import { CheckIcon, XIcon } from 'lucide-react';

// ❌ Don't add
import { FaCheck } from 'react-icons/fa'; // NO!
```

---

## 17. JSDOC COMMENTS

Add JSDoc to all components and functions.

```tsx
/**
 * Displays a status badge with appropriate color coding.
 * @param status - Current status value ('active' | 'pending' | 'failed')
 * @param showIcon - Whether to display status icon (default: true)
 * @returns Styled badge element
 * @example
 * <StatusBadge status="active" />
 * <StatusBadge status="failed" showIcon={false} />
 */
const StatusBadge = ({ status, showIcon = true }: StatusBadgeProps) => {
  // implementation
};

/**
 * Formats a timestamp into human-readable relative time.
 * @param timestamp - ISO date string
 * @returns Formatted string like "2 hours ago"
 */
const formatRelativeTime = (timestamp: string): string => {
  // implementation
};
```

---

## 18. EXISTING PATTERNS REFERENCE

### Button Wrapper (Loading State)
```tsx
<Button isLoading={isSubmitting}>Submit</Button>
```

### Input Wrapper (Form Integration)
```tsx
<Input
  name="email"
  label="Email Address"
  LeadingIcon={<MailIcon className="h-4 w-4" />}
/>
```

### Card Compound Component
```tsx
<Card id={item.id} onSelect={handleSelect}>
  {({ isSelected }) => (
    <>
      <Card.Header>
        <Card.IconGroup icons={item.icons} />
        <Card.MoreButton options={menuOptions} />
      </Card.Header>
      <Card.TextContent title={item.name} description={item.description} />
      <Card.Footer>
        <Card.BadgeGroup badges={item.tags} />
      </Card.Footer>
    </>
  )}
</Card>
```

### Empty State
```tsx
<EmptyState
  text="No results found"
  content={<Button onClick={handleCreate}>Create New</Button>}
/>
```

### Modal
```tsx
<Modal
  open={isOpen}
  onOpenChange={setIsOpen}
  title="Confirm Action"
  content={<ModalContent />}
  footer={<ModalActions />}
  size="md"
/>
```

---

## 19. CHECKLIST BEFORE SUBMITTING

- [ ] Only Tailwind classes used (no inline styles)
- [ ] Only theme colors used (no arbitrary colors)
- [ ] UI components not modified directly
- [ ] Wrapper created if customization needed
- [ ] Component under 500 lines
- [ ] Shared components reused where applicable
- [ ] All micro states handled (loading, error, empty, hover)
- [ ] Responsive on all breakpoints
- [ ] Functions extracted from JSX
- [ ] Constants/enums created for repeated values
- [ ] JSDoc comments added
- [ ] No new packages installed
- [ ] Mock data used instead of API calls
