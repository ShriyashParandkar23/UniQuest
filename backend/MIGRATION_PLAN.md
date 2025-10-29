# Migration Plan: Multiple Apps → Single Core App

## Overview
Consolidating 7 separate Django apps into 1 unified `core` app for simpler architecture.

## Current Structure (7 Apps)
```
backend/apps/
├── users/          # User authentication
├── students/       # Student profiles  
├── preferences/    # User preferences
├── recommendations/# Recommendations
├── feedback/       # Feedback
├── dataset/        # Dataset management
└── llm/           # LLM services
```

## New Structure (1 App)
```
backend/apps/
└── core/          # Everything consolidated
    ├── models.py          # All models
    ├── serializers.py     # All serializers
    ├── views.py           # All views
    ├── urls.py            # All URLs
    ├── services.py        # All services
    ├── admin.py           # All admin
    ├── management/        # Management commands
    │   └── commands/
    └── migrations/
```

## Migration Steps

### Phase 1: Create Core App ✅
- [x] Create `apps/core/` directory
- [x] Create `apps/core/__init__.py`
- [x] Create `apps/core/apps.py`
- [x] Create `apps/core/models.py` (consolidated)

### Phase 2: Consolidate Code
- [ ] Create `apps/core/services.py` (DatasetService, RecommendationService, LLMService)
- [ ] Create `apps/core/serializers.py` (all serializers)
- [ ] Create `apps/core/views.py` (all views)
- [ ] Create `apps/core/urls.py` (all URL patterns)
- [ ] Create `apps/core/admin.py` (all admin configs)
- [ ] Copy `apps/dataset/management/` to `apps/core/management/`

### Phase 3: Update Settings
- [ ] Update `settings/base.py` INSTALLED_APPS
- [ ] Update AUTH_USER_MODEL to 'core.User'
- [ ] Remove old app references

### Phase 4: Update URLs
- [ ] Update `urls.py` to use `core.urls`
- [ ] Remove old app URL includes

### Phase 5: Create Initial Migration
- [ ] Run `python manage.py makemigrations core`
- [ ] Review migration file
- [ ] **IMPORTANT**: This will recreate all tables

### Phase 6: Data Migration (if needed)
- [ ] Backup existing database
- [ ] Export data: `python manage.py dumpdata > backup.json`
- [ ] Drop old tables (or start fresh)
- [ ] Run migrations: `python manage.py migrate`
- [ ] Import data if needed

### Phase 7: Testing
- [ ] Test user authentication
- [ ] Test profile creation
- [ ] Test recommendations generation
- [ ] Test feedback submission
- [ ] Test dataset commands
- [ ] Run full test suite

### Phase 8: Cleanup
- [ ] Delete old app directories
- [ ] Update documentation
- [ ] Update diagrams

## Database Impact

### ⚠️ IMPORTANT: Database Tables
The table names will remain the same (using `db_table` in Meta):
- `users`
- `student_profiles`
- `preferences`
- `recommendations`
- `feedback`
- `ingestion_runs`

This means existing data can be preserved if migrations are handled correctly.

## Rollback Plan
If issues arise:
1. Keep old apps directory as backup
2. Revert settings changes
3. Restore from database backup
4. Re-run old migrations

## Benefits of Single App
✅ Simpler project structure
✅ Easier imports (no circular dependencies)
✅ Single migrations directory
✅ Clearer code organization
✅ Easier for new developers to understand

## Risks
⚠️ Large migration file
⚠️ Potential data loss if not careful
⚠️ Need to update all imports
⚠️ Testing required for all features

## Timeline
- Phase 1-2: 2 hours (code consolidation)
- Phase 3-4: 30 minutes (settings/URLs)
- Phase 5-6: 1 hour (migrations)
- Phase 7: 2 hours (testing)
- Phase 8: 30 minutes (cleanup)
**Total: ~6 hours**

## Next Steps
1. Complete Phase 2 (consolidate remaining code)
2. Backup database
3. Update settings
4. Create migrations
5. Test thoroughly

