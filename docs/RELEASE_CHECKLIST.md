# Release Checklist

This checklist ensures all releases meet quality and documentation standards.

## Pre-Release

### Code Quality

- [ ] All tests passing (`poetry run pytest` and `npm run test:run`)
- [ ] Test coverage maintained (70%+ overall, 85%+ per file)
- [ ] Linters passing:
  - [ ] Backend: `poetry run ruff check backend`
  - [ ] Backend: `poetry run black --check backend`
  - [ ] Backend: `poetry run mypy backend`
  - [ ] Frontend: `npm run lint`
- [ ] Type checking passing:
  - [ ] Backend: MyPy passes
  - [ ] Frontend: `npm run build` (TypeScript compilation)

### Documentation

- [ ] CHANGELOG.md updated with new version
- [ ] README.md updated if needed (features, setup, etc.)
- [ ] API documentation updated (OpenAPI/Swagger)
- [ ] User guide updated if features changed
- [ ] Deployment guide updated if deployment changed

### Version Management

- [ ] Version numbers updated consistently:
  - [ ] `pyproject.toml` (backend version)
  - [ ] `frontend/package.json` (frontend version)
  - [ ] Version numbers match between files
- [ ] Git tag created: `v0.1.0` (or appropriate version)

### Security

- [ ] No secrets or credentials in code
- [ ] Environment variables documented in `.env.example`
- [ ] Dependencies audited for vulnerabilities:
  - [ ] Python: `pip-audit` or `safety check`
  - [ ] Node.js: `npm audit`
- [ ] Security considerations documented in SECURITY.md if needed

### Testing

- [ ] Unit tests cover new functionality
- [ ] Integration tests cover new endpoints/workflows
- [ ] E2E tests cover critical user flows
- [ ] Manual testing completed:
  - [ ] Flipping calculator works
  - [ ] Gear calculator works
  - [ ] Slayer tracker works
  - [ ] All major features functional

### Backward Compatibility

- [ ] No breaking API changes (or documented if necessary)
- [ ] No removed endpoints or fields
- [ ] Database migrations are backward compatible
- [ ] Frontend types updated if API changed

## Release Process

### 1. Create Release Branch

```bash
git checkout -b release/v0.1.0
```

### 2. Final Verification

- [ ] Run full test suite
- [ ] Build frontend: `cd frontend && npm run build`
- [ ] Verify production build works
- [ ] Check health endpoint: `/api/v1/health`

### 3. Update Version Numbers

Update versions in:
- `pyproject.toml`
- `frontend/package.json`
- `CHANGELOG.md` (add release date)

### 4. Create Release Commit

```bash
git add .
git commit -m "chore: release v0.1.0"
git tag v0.1.0
```

### 5. Create GitHub Release

- [ ] Create release on GitHub
- [ ] Use CHANGELOG.md content for release notes
- [ ] Attach release artifacts if needed
- [ ] Mark as latest release

### 6. Merge and Deploy

- [ ] Merge release branch to `main`
- [ ] Push tags: `git push --tags`
- [ ] Deploy to production (if applicable)
- [ ] Verify production deployment

## Post-Release

### Monitoring

- [ ] Monitor error logs for 24-48 hours
- [ ] Check health endpoint status
- [ ] Monitor API usage and rate limits
- [ ] Check database performance

### Documentation

- [ ] Update deployment documentation if needed
- [ ] Update user guide if features changed
- [ ] Archive old documentation if needed

### Communication

- [ ] Announce release (if applicable)
- [ ] Update project status
- [ ] Respond to issues/questions

## Emergency Hotfix Process

For critical bugs discovered after release:

1. **Create hotfix branch** from release tag:
   ```bash
   git checkout -b hotfix/v0.1.1 v0.1.0
   ```

2. **Fix the issue**:
   - [ ] Write test for the bug
   - [ ] Fix the bug
   - [ ] Verify fix works

3. **Release hotfix**:
   - [ ] Update version to patch version (0.1.0 → 0.1.1)
   - [ ] Update CHANGELOG.md
   - [ ] Create release tag
   - [ ] Merge to main and release branch

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.2.0): New features, backward compatible
- **PATCH** (0.1.1): Bug fixes, backward compatible

### Examples

- `0.1.0` → `0.1.1`: Bug fix
- `0.1.1` → `0.2.0`: New feature (backward compatible)
- `0.2.0` → `1.0.0`: Breaking change

## Checklist for Different Release Types

### Major Release (Breaking Changes)

- [ ] Migration guide created
- [ ] Breaking changes documented in CHANGELOG.md
- [ ] Deprecation warnings added (if applicable)
- [ ] Communication plan for breaking changes

### Minor Release (New Features)

- [ ] New features documented
- [ ] User guide updated
- [ ] API documentation updated
- [ ] Examples/tutorials updated

### Patch Release (Bug Fixes)

- [ ] Bug fixes documented
- [ ] Tests added to prevent regression
- [ ] Impact assessment completed

## Quality Gates

All items must be checked before release. If any item cannot be checked, document why and get approval before proceeding.

## Release Notes Template

```markdown
## [Version] - YYYY-MM-DD

### Added
- New feature 1
- New feature 2

### Changed
- Changed behavior 1
- Changed behavior 2

### Fixed
- Bug fix 1
- Bug fix 2

### Security
- Security fix 1 (if applicable)

### Deprecated
- Deprecated feature 1 (if applicable)

### Removed
- Removed feature 1 (if applicable)
```

---

*Last Updated: 2026-01-28*
