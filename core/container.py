"""
DEPRECATED - This file is no longer used.

Container management has been migrated to modular containers in core/containers/:

- shared_container.py: Shared services (Database, EventBus, Email, AI, Storage, Buses)
- auth_container.py: Authentication and user management
- interview_container.py: Interviews and templates
- company_container.py: Companies, users, roles, candidates
- candidate_container.py: Candidates and applications
- job_position_container.py: Job positions
- workflow_container.py: Workflows and phases
- main_container.py: Main container that composes all the above

HOW TO ADD NEW DEPENDENCIES:

1. Identify which bounded context your dependency belongs to
2. Add the import and Factory to the appropriate container in core/containers/
3. If the dependency needs to be shared across BCs, add it to shared_container.py
4. Register handlers following the pattern: {name}_handler = providers.Factory(...)

Example:
    # In auth_container.py
    from src.auth_bc.user_registration.infrastructure.repositories import UserRegistrationRepository

    user_registration_repository = providers.Factory(
        UserRegistrationRepository,
        session=shared.database.provided.session
    )

For more details, see core/containers/main_container.py
"""
