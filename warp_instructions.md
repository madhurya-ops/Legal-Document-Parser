## WARP COMMAND USAGE EXAMPLES

### Basic Commands with Context
```bash
# Create new feature following these instructions
warp create feature --name "user-authentication" --type "full-stack"

# Edit existing file with strict modification rules
warp edit src/components/UserProfile.tsx --instruction "Add email validation following existing patterns"

# Ask for analysis before implementation
warp ask "How should I implement caching for the user data API endpoint?"

# Review and optimize existing code
warp review src/api/users.js --focus "performance,security,integration"
```

### Project-Specific Integration
```bash
# Analyze entire codebase for integration points
warp analyze --scope "full-project" --focus "architecture,dependencies,dead-code"

# Generate implementation plan
warp plan --feature "payment-processing" --include "frontend,backend,database"

# Implement with testing
warp implement --feature "payment-processing" --include-tests --follow-instructions
```

## USAGE INSTRUCTIONS

To use these instructions effectively with Warp:

1. **Place in Project Root**: Save this file as `.warp/instructions.md` in your project root directory

2. **Automatic Context**: Warp will automatically load these instructions for all AI interactions in this project

3. **Reference SRS**: Keep your SRS document accessible and reference it in Warp commands

4. **Use Specific Commands**: Leverage Warp's specific commands (`/edit`, `/create`, `/ask`) with these instructions as context

5. **Validate Integration**: Always use the quality assurance checklist before finalizing implementations

6. **Iterate with Feedback**: Use Warp's feedback mechanisms to refine implementations

Remember: These instructions ensure production-ready, scalable, and maintainable code that integrates seamlessly with existing systems while following industry best practices and standards.# .warp/instructions.md - Comprehensive AI Web Application Development Instructions

## CORE BEHAVIORAL RULES

### Primary Directives
1. **Modification Protocol**: Only modify existing files when functionally necessary. Never create new files if existing ones can be enhanced or extended.
2. **Functionality Preservation**: Never alter working code unless the modification directly addresses a specific functional requirement or bug fix.
3. **No Assumptions**: Build only what is explicitly requested. Do not add features, styling, or functionality beyond the specified requirements.
4. **File Management**: Automatically identify and remove unused files, dependencies, and code blocks that are no longer referenced in the active codebase.
5. **Integration First**: Every code change must be tested for compatibility with existing systems before implementation.

### Code Quality Standards
1. **Production-Ready Code**: All code must be production-level quality with proper error handling, input validation, and security measures.
2. **Modular Architecture**: Implement clean separation of concerns with reusable components and functions.
3. **Efficient Implementation**: Optimize for performance, memory usage, and scalability in every code decision.
4. **Security First**: Implement proper authentication, authorization, input sanitization, and data protection measures.
5. **Comprehensive Testing**: Include unit tests, integration tests, and error handling for all new functionality.

## DEVELOPMENT WORKFLOW PROTOCOL

### Pre-Development Analysis
Before writing any code, perform the following analysis:
1. **Codebase Audit**: Scan existing files to understand current architecture, patterns, and dependencies.
2. **Integration Point Identification**: Determine exactly where new code will integrate with existing systems.
3. **Dependency Mapping**: Identify all required dependencies and ensure they align with existing package versions.
4. **File Structure Analysis**: Understand the current project structure and maintain consistency.
5. **Database Schema Review**: Analyze existing database structure and relationships before making changes.

### Code Implementation Rules
1. **Single Responsibility**: Each function, component, and module must have a single, well-defined purpose.
2. **DRY Principle**: Eliminate code duplication by creating reusable utilities and components.
3. **Consistent Naming**: Use descriptive, consistent naming conventions throughout the codebase.
4. **Error Handling**: Implement comprehensive error handling with meaningful error messages and appropriate fallback mechanisms.
5. **Type Safety**: Use proper typing (TypeScript) or equivalent validation for all data structures and function parameters.

### File Management Protocol
1. **Existing File Priority**: Always check if functionality can be added to existing files before creating new ones.
2. **Import Optimization**: Remove unused imports and optimize import statements for better performance.
3. **Dead Code Elimination**: Identify and remove functions, components, or variables that are no longer used.
4. **Dependency Cleanup**: Remove unused dependencies from package.json and requirements files.
5. **Asset Optimization**: Compress and optimize images, fonts, and other static assets.

## FRONTEND DEVELOPMENT INSTRUCTIONS

### Component Architecture
1. **Atomic Design**: Structure components using atomic design principles (atoms, molecules, organisms, templates, pages).
2. **State Management**: Implement centralized state management (Redux, Zustand, Context API) for complex applications.
3. **Performance Optimization**: Use lazy loading, code splitting, and memoization techniques to optimize rendering performance.
4. **Responsive Design**: Implement mobile-first responsive design with proper breakpoints and fluid layouts.
5. **Accessibility**: Ensure WCAG 2.1 AA compliance with proper ARIA labels, keyboard navigation, and screen reader support.

### UI/UX Implementation Rules
1. **Design System Consistency**: Maintain consistent spacing, typography, colors, and component behavior across the application.
2. **User Flow Optimization**: Design intuitive user flows with minimal cognitive load and clear navigation paths.
3. **Loading States**: Implement proper loading states, skeleton screens, and progress indicators for all async operations.
4. **Error States**: Design clear error states with actionable error messages and recovery options.
5. **Feedback Mechanisms**: Provide immediate feedback for user actions through animations, notifications, and state changes.

### Frontend Technology Stack Rules
1. **Framework Selection**: Choose appropriate frameworks (React, Vue, Angular) based on project requirements and team expertise.
2. **Build Tools**: Configure efficient build tools (Vite, Webpack) with proper optimization settings.
3. **CSS Architecture**: Use CSS methodologies (BEM, CSS Modules, Styled Components) for maintainable styling.
4. **Testing Framework**: Implement comprehensive testing with Jest, React Testing Library, or equivalent testing frameworks.
5. **Performance Monitoring**: Integrate performance monitoring tools (Lighthouse, Web Vitals) for continuous optimization.

## BACKEND DEVELOPMENT INSTRUCTIONS

### API Design Principles
1. **RESTful Architecture**: Design clean, RESTful APIs with proper HTTP methods and status codes.
2. **API Versioning**: Implement proper API versioning strategy to maintain backward compatibility.
3. **Authentication & Authorization**: Implement secure authentication (JWT, OAuth) and role-based authorization systems.
4. **Rate Limiting**: Implement rate limiting and request throttling to prevent abuse and ensure system stability.
5. **API Documentation**: Generate comprehensive API documentation using OpenAPI/Swagger specifications.

### Server Architecture
1. **Layered Architecture**: Implement clean architecture with separate layers for controllers, services, and data access.
2. **Dependency Injection**: Use dependency injection patterns for better testability and maintainability.
3. **Error Handling**: Implement centralized error handling with proper logging and monitoring.
4. **Input Validation**: Validate all input data with proper sanitization and type checking.
5. **Security Middleware**: Implement security middleware for CORS, helmet, input validation, and SQL injection prevention.

### Database Integration
1. **ORM/ODM Usage**: Use appropriate ORM/ODM tools (Prisma, TypeORM, Mongoose) for database operations.
2. **Migration Management**: Implement proper database migration strategies with version control.
3. **Connection Pooling**: Configure database connection pooling for optimal performance.
4. **Transaction Management**: Implement proper transaction handling for data consistency.
5. **Query Optimization**: Optimize database queries with proper indexing and query analysis.

## DATABASE DESIGN INSTRUCTIONS

### Schema Design
1. **Normalization**: Design normalized database schemas to eliminate redundancy and maintain data integrity.
2. **Indexing Strategy**: Implement appropriate indexes for frequently queried columns and foreign keys.
3. **Constraint Management**: Use database constraints (foreign keys, unique constraints, check constraints) to enforce data integrity.
4. **Data Types**: Choose appropriate data types for optimal storage and performance.
5. **Audit Trails**: Implement audit trails for sensitive data changes with proper timestamping.

### Performance Optimization
1. **Query Analysis**: Analyze and optimize slow queries using database profiling tools.
2. **Caching Strategy**: Implement appropriate caching layers (Redis, Memcached) for frequently accessed data.
3. **Connection Management**: Configure proper connection pooling and connection limits.
4. **Backup Strategy**: Implement automated backup strategies with proper recovery procedures.
5. **Monitoring**: Set up database monitoring and alerting for performance and availability issues.

## TESTING AND QUALITY ASSURANCE

### Testing Strategy
1. **Unit Testing**: Write comprehensive unit tests for all business logic and utility functions.
2. **Integration Testing**: Test API endpoints and database interactions with proper test data.
3. **End-to-End Testing**: Implement E2E tests for critical user flows using tools like Cypress or Playwright.
4. **Performance Testing**: Conduct load testing and stress testing to ensure application scalability.
5. **Security Testing**: Perform security testing including penetration testing and vulnerability assessments.

### Code Review and Quality
1. **Static Analysis**: Use ESLint, Prettier, and similar tools for code quality and formatting.
2. **Code Coverage**: Maintain minimum code coverage thresholds (80%+) for all critical functionality.
3. **Documentation**: Write clear, comprehensive documentation for all APIs, components, and business logic.
4. **Version Control**: Use proper Git branching strategies with meaningful commit messages.
5. **Continuous Integration**: Implement CI/CD pipelines with automated testing and deployment.

## DEPLOYMENT AND DEVOPS

### Environment Management
1. **Environment Configuration**: Use environment-specific configuration files and variables.
2. **Container Strategy**: Implement Docker containerization for consistent deployment across environments.
3. **Cloud Architecture**: Design cloud-native architecture with proper scaling and monitoring.
4. **Security Configuration**: Implement proper security configurations for production environments.
5. **Monitoring and Logging**: Set up comprehensive monitoring and logging systems for application health.

### Scalability Planning
1. **Horizontal Scaling**: Design applications for horizontal scaling with load balancers and distributed systems.
2. **Caching Strategy**: Implement multi-level caching strategies for improved performance.
3. **Database Scaling**: Plan for database scaling with read replicas and sharding strategies.
4. **CDN Integration**: Use Content Delivery Networks for static asset optimization.
5. **Performance Monitoring**: Implement APM tools for continuous performance monitoring.

## PROMPT TEMPLATES FOR SPECIFIC TASKS

### Frontend Development Prompt
```
Context: [SRS Document] + [Current Codebase] + [These Instructions]

Task: Develop [specific frontend feature] following these requirements:
- Integrate with existing [specify existing components/systems]
- Maintain current design system and patterns
- Implement proper error handling and loading states
- Ensure mobile responsiveness and accessibility
- Add appropriate unit tests
- Optimize for performance and user experience
- Remove any unused code or dependencies

Requirements:
[List specific functional requirements]

Constraints:
- Do not modify working functionality
- Use existing state management patterns
- Maintain current code structure and naming conventions
- Implement only specified features without additions
```

### Backend Development Prompt
```
Context: [SRS Document] + [Current Codebase] + [These Instructions]

Task: Develop [specific backend feature] with these specifications:
- Integrate with existing API structure and patterns
- Implement proper authentication and authorization
- Add comprehensive input validation and error handling
- Ensure database transaction integrity
- Include unit and integration tests
- Optimize for performance and scalability
- Remove unused endpoints or middleware

Requirements:
[List specific functional requirements]

Database Changes:
[Specify any required database modifications]

Constraints:
- Maintain existing API contracts
- Use established error handling patterns
- Follow current authentication mechanisms
- Implement only specified functionality
```

### Database Development Prompt
```
Context: [SRS Document] + [Current Database Schema] + [These Instructions]

Task: Modify database schema for [specific requirement]:
- Analyze current schema for integration points
- Design normalized schema changes
- Create appropriate indexes and constraints
- Generate safe migration scripts
- Ensure data integrity and consistency
- Remove unused tables or columns
- Optimize queries for performance

Requirements:
[List specific data requirements]

Migration Strategy:
[Specify migration approach - zero-downtime, maintenance window, etc.]

Constraints:
- Maintain existing data relationships
- Ensure backward compatibility where possible
- Implement proper rollback procedures
- Test migration on staging environment first
```

### Full-Stack Integration Prompt
```
Context: [SRS Document] + [Complete Codebase] + [These Instructions]

Task: Implement end-to-end feature [feature name]:
- Frontend: [specific UI/UX requirements]
- Backend: [specific API requirements]
- Database: [specific data requirements]
- Integration: [specific integration requirements]

Implementation Requirements:
- Maintain existing architecture patterns
- Implement comprehensive error handling
- Add proper testing at all layers
- Ensure security best practices
- Optimize for performance and scalability
- Remove any unused code or dependencies

Testing Requirements:
- Unit tests for all new functionality
- Integration tests for API endpoints
- E2E tests for critical user flows
- Performance testing for scalability

Constraints:
- Do not modify existing working features
- Use established patterns and conventions
- Implement only specified functionality
- Maintain current security and authentication mechanisms
```

## QUALITY ASSURANCE CHECKLIST

### Pre-Implementation Verification
- [ ] Analyzed existing codebase for integration points
- [ ] Identified all dependencies and compatibility requirements
- [ ] Reviewed current architecture and design patterns
- [ ] Confirmed functional requirements align with SRS document
- [ ] Planned testing strategy for new functionality

### Post-Implementation Verification
- [ ] All new code follows established patterns and conventions
- [ ] Comprehensive error handling implemented
- [ ] Unit and integration tests added and passing
- [ ] Performance optimization implemented
- [ ] Security measures properly configured
- [ ] Documentation updated for new functionality
- [ ] Dead code and unused dependencies removed
- [ ] Integration with existing systems verified
- [ ] User experience flows tested and optimized

### Code Quality Metrics
- [ ] Code coverage above 80% for critical functionality
- [ ] No security vulnerabilities detected
- [ ] Performance benchmarks met
- [ ] Accessibility standards (WCAG 2.1 AA) complied
- [ ] Mobile responsiveness verified
- [ ] Cross-browser compatibility tested
- [ ] Error handling covers all edge cases
- [ ] Input validation implemented for all user inputs

## MAINTENANCE AND MONITORING

### Continuous Improvement
1. **Performance Monitoring**: Regularly monitor application performance and optimize bottlenecks.
2. **Security Updates**: Keep all dependencies and frameworks updated with security patches.
3. **Code Refactoring**: Regularly refactor code to improve maintainability and performance.
4. **Documentation Updates**: Keep documentation current with code changes and new features.
5. **User Feedback Integration**: Incorporate user feedback to improve user experience and functionality.

### Troubleshooting Protocol
1. **Error Logging**: Implement comprehensive error logging with proper context and stack traces.
2. **Debugging Tools**: Use appropriate debugging tools and techniques for efficient problem resolution.
3. **Performance Profiling**: Regular performance profiling to identify and resolve bottlenecks.
4. **Health Checks**: Implement health check endpoints for monitoring system status.
5. **Rollback Procedures**: Maintain proper rollback procedures for quick recovery from issues.

---

---

## WARP CONFIGURATION

This file should be placed at `.warp/instructions.md` in your project root. Warp will automatically load these instructions as context for all AI interactions within this project.

### File Structure
```
your-project/
├── .warp/
│   ├── instructions.md (this file)
│   └── .warpignore (optional - specify files to ignore)
├── src/
├── docs/
└── ...
```

### Warp-Specific Usage
1. **Automatic Context Loading**: Warp will automatically include this file as context
2. **Project-Specific Rules**: These rules apply to all AI interactions in this project
3. **Command Integration**: Use with Warp's `/edit`, `/create`, and `/ask` commands
4. **Multi-file Operations**: Warp will consider these rules when working across multiple files

---