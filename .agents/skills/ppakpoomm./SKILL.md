```markdown
# ppakpoomm. Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill introduces the core development patterns and conventions used in the `ppakpoomm.` TypeScript codebase. It covers file organization, code style, commit practices, and testing patterns to ensure consistency and maintainability. Whether you're contributing new features or reviewing code, following these guidelines will help keep the project clean and efficient.

## Coding Conventions

### File Naming
- Use **camelCase** for all filenames.
  - Example: `userProfile.ts`, `dataFetcher.test.ts`

### Import Style
- Use **relative imports** for referencing modules within the project.
  ```typescript
  import { fetchData } from './dataFetcher';
  ```

### Export Style
- Use **named exports** exclusively.
  ```typescript
  // dataFetcher.ts
  export function fetchData() { ... }
  ```

### Commit Messages
- Follow the **Conventional Commits** standard.
- Use the `feat` prefix for new features.
- Keep commit messages concise (average ~67 characters).
  - Example: `feat: add user authentication middleware`

## Workflows

### Feature Development
**Trigger:** When adding a new feature  
**Command:** `/feature-development`

1. Create a new file using camelCase naming.
2. Write your TypeScript code using named exports.
3. Use relative imports for any dependencies.
4. Write or update corresponding test files (`*.test.ts`).
5. Commit changes with a message starting with `feat:` and a concise description.
6. Open a pull request for review.

### Testing
**Trigger:** When validating code changes  
**Command:** `/run-tests`

1. Identify or create test files matching the `*.test.*` pattern.
2. Use the project's preferred (unknown) testing framework to run tests.
3. Ensure all tests pass before merging or deploying changes.

## Testing Patterns

- Test files follow the `*.test.*` naming convention (e.g., `userProfile.test.ts`).
- The specific testing framework is not defined; check project documentation or existing tests for details.
- Place test files alongside the modules they test or in a dedicated test directory.

  ```typescript
  // userProfile.test.ts
  import { getUserProfile } from './userProfile';

  describe('getUserProfile', () => {
    it('should return user data', () => {
      // test implementation
    });
  });
  ```

## Commands
| Command              | Purpose                                   |
|----------------------|-------------------------------------------|
| /feature-development | Start a new feature using project patterns|
| /run-tests           | Run all tests in the codebase             |
```
