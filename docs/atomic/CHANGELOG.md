# Atomic Documentation Changelog

All notable changes to atomic documentation are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-11-05

### Added
- Initial release of AI Generator for Async Microservices framework
- 135+ atomic documentation modules covering architecture, services, infrastructure, observability, testing, security
- Complete service templates structure (Business API, Bots, Workers, PostgreSQL/MongoDB Data APIs)
- Production-ready infrastructure configurations (Docker, Nginx, CI/CD, Prometheus, Grafana, Jaeger)
- 7-stage AI workflow (Validation → Requirements → Planning → Generation → Verification → Handoff)
- Improved Hybrid Architecture with strict HTTP-only data access
- Maturity levels system (PoC to Production)
- Comprehensive testing strategies and quality standards

---

## Versioning Guidelines

### Version Number Format
- **Major version** (X.0.0): Breaking changes to documentation structure or significant reorganization
- **Minor version** (0.X.0): New atomic documents added, sections reorganized
- **Patch version** (0.1.X): Link fixes, typos, clarifications, minor updates

### What Constitutes Breaking Changes?
- Renaming or moving atomic files without redirects
- Removing atomic files that are referenced by multiple documents
- Changing fundamental architecture principles
- Restructuring INDEX.md navigation significantly

### Update Workflow
1. Make changes to atomic documentation
2. Update this CHANGELOG.md under [Unreleased]
3. When ready for release:
   - Decide version number based on changes
   - Move [Unreleased] content to new version section
   - Update version date
   - Tag Git repository with version

### Git Tagging
```bash
# Tag the release
git tag -a v0.1.0 -m "Release v0.1.0: Initial framework release"

# Push tags to remote
git push origin v0.1.0
```

## Contributing

When adding new atomic documentation:
1. Create the atomic file in appropriate domain directory
2. Add entry to this CHANGELOG under [Unreleased]
3. Update `INDEX.md` with new file reference
4. Run link validation: `./scripts/check_links.sh`
5. Update version in pull request based on change type

## Support

For questions about atomic documentation versions:
- Check this CHANGELOG for recent changes
- Review `INDEX.md` for current structure
- See `agent-context-summary.md` for quick orientation
