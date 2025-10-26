# Workflow System - Complete Implementation Plan

**Version**: 1.0
**Date**: 2025-10-26
**Status**: Ready for Implementation

---

## Table of Contents

1. [Overview](#overview)
2. [Phase 1: Custom Fields System](#phase-1-custom-fields-system)
3. [Phase 2: Field Validation System](#phase-2-field-validation-system)
4. [Phase 3: Position-Workflow Integration](#phase-3-position-workflow-integration)
5. [Phase 4: Stage Assignments](#phase-4-stage-assignments)
6. [Phase 5: Application Processing with Validations](#phase-5-application-processing-with-validations)
7. [Phase 6: Task Management System](#phase-6-task-management-system)
8. [Phase 7: Email Integration](#phase-7-email-integration)
9. [Phase 8: Talent Pool](#phase-8-talent-pool)
10. [Phase 9: Analytics and Reporting](#phase-9-analytics-and-reporting)

---

## Overview

This document outlines all the tasks required to implement the complete workflow system for CareerPython ATS. The implementation is divided into 9 phases, each building upon the previous one.

**Estimated Total Time**: 10-12 weeks
**Priority**: High

---

## Phase 1: Custom Fields System

**Goal**: Implement custom fields that can be added to workflows to capture specific information per stage.

**Estimated Time**: 2 weeks
**Dependencies**: None
**Priority**: HIGH

### Backend Tasks

#### 1.1 Database Schema

- [ ] **Task**: Create migration `create_workflow_custom_fields.sql`
  - **Details**: Create `workflow_custom_fields` table with all columns
  - **File**: `migrations/versions/XXX_create_workflow_custom_fields.sql`
  - **Time**: 2 hours

- [ ] **Task**: Create migration `create_stage_field_configurations.sql`
  - **Details**: Create `stage_field_configurations` table
  - **File**: `migrations/versions/XXX_create_stage_field_configurations.sql`
  - **Time**: 2 hours

- [ ] **Task**: Run migrations and verify tables created
  - **Command**: `make migrate`
  - **Time**: 30 minutes

#### 1.2 Domain Layer

- [ ] **Task**: Create `CustomField` entity
  - **File**: `src/workflow_custom_field/domain/entities/custom_field.py`
  - **Details**:
    - Add all properties (id, workflow_id, field_key, field_name, field_type, field_config, order)
    - Create factory method `create()`
    - Create update method `update()`
    - Add validation for field_key (must be snake_case)
    - Add `_validate_config()` method for type-specific validation
  - **Time**: 4 hours

- [ ] **Task**: Create `FieldConfiguration` entity
  - **File**: `src/workflow_custom_field/domain/entities/field_configuration.py`
  - **Details**:
    - Add all properties (id, stage_id, custom_field_id, visibility)
    - Create factory method `create()`
  - **Time**: 2 hours

- [ ] **Task**: Create `FieldType` enum
  - **File**: `src/workflow_custom_field/domain/enums/field_type.py`
  - **Values**: text_short, text_long, dropdown, checkbox, radio, date, datetime, time, file, currency, integer, float, percentage
  - **Time**: 1 hour

- [ ] **Task**: Create `FieldVisibility` enum
  - **File**: `src/workflow_custom_field/domain/enums/field_visibility.py`
  - **Values**: hidden, mandatory, recommended, optional
  - **Time**: 1 hour

- [ ] **Task**: Create value objects
  - **Files**:
    - `src/workflow_custom_field/domain/value_objects/custom_field_id.py`
    - `src/workflow_custom_field/domain/value_objects/field_configuration_id.py`
  - **Time**: 2 hours

- [ ] **Task**: Create repository interface
  - **File**: `src/workflow_custom_field/domain/infrastructure/custom_field_repository_interface.py`
  - **Methods**: get_by_id, get_by_workflow, save, delete, get_by_field_key
  - **Time**: 2 hours

#### 1.3 Infrastructure Layer

- [ ] **Task**: Create `CustomFieldModel` SQLAlchemy model
  - **File**: `src/workflow_custom_field/infrastructure/models/custom_field_model.py`
  - **Details**: Map all columns, add relationships to workflow
  - **Time**: 3 hours

- [ ] **Task**: Create `FieldConfigurationModel` SQLAlchemy model
  - **File**: `src/workflow_custom_field/infrastructure/models/field_configuration_model.py`
  - **Details**: Map all columns, add relationships to stage and field
  - **Time**: 2 hours

- [ ] **Task**: Create `CustomFieldRepository` implementation
  - **File**: `src/workflow_custom_field/infrastructure/repositories/custom_field_repository.py`
  - **Details**:
    - Implement all interface methods
    - Add `_to_domain()` mapper
    - Add `_to_model()` mapper
  - **Time**: 4 hours

#### 1.4 Application Layer

- [ ] **Task**: Create `CustomFieldDto`
  - **File**: `src/workflow_custom_field/application/dtos/custom_field_dto.py`
  - **Details**: Include all fields, add `from_entity()` method
  - **Time**: 2 hours

- [ ] **Task**: Create `CreateCustomFieldCommand`
  - **File**: `src/workflow_custom_field/application/commands/create_custom_field_command.py`
  - **Time**: 2 hours

- [ ] **Task**: Create `CreateCustomFieldCommandHandler`
  - **File**: `src/workflow_custom_field/application/commands/create_custom_field_command_handler.py`
  - **Details**: Validate and create custom field
  - **Time**: 3 hours

- [ ] **Task**: Create `UpdateCustomFieldCommand` and handler
  - **File**: `src/workflow_custom_field/application/commands/update_custom_field_command.py`
  - **Time**: 3 hours

- [ ] **Task**: Create `DeleteCustomFieldCommand` and handler
  - **File**: `src/workflow_custom_field/application/commands/delete_custom_field_command.py`
  - **Time**: 2 hours

- [ ] **Task**: Create `ListCustomFieldsQuery`
  - **File**: `src/workflow_custom_field/application/queries/list_custom_fields_query.py`
  - **Details**: Filter by workflow_id
  - **Time**: 2 hours

- [ ] **Task**: Create `GetCustomFieldByIdQuery`
  - **File**: `src/workflow_custom_field/application/queries/get_custom_field_by_id_query.py`
  - **Time**: 2 hours

- [ ] **Task**: Create `UpdateFieldVisibilityCommand` and handler
  - **File**: `src/workflow_custom_field/application/commands/update_field_visibility_command.py`
  - **Details**: Update visibility for a field in a specific stage
  - **Time**: 3 hours

#### 1.5 Presentation Layer

- [ ] **Task**: Create request/response schemas
  - **Files**:
    - `src/workflow_custom_field/presentation/schemas/create_custom_field_request.py`
    - `src/workflow_custom_field/presentation/schemas/update_custom_field_request.py`
    - `src/workflow_custom_field/presentation/schemas/custom_field_response.py`
  - **Time**: 3 hours

- [ ] **Task**: Create `CustomFieldMapper`
  - **File**: `src/workflow_custom_field/presentation/mappers/custom_field_mapper.py`
  - **Methods**: dto_to_response, dtos_to_responses
  - **Time**: 2 hours

- [ ] **Task**: Create `CustomFieldController`
  - **File**: `src/workflow_custom_field/presentation/controllers/custom_field_controller.py`
  - **Methods**:
    - create_custom_field
    - update_custom_field
    - delete_custom_field
    - list_custom_fields
    - get_custom_field
    - update_field_visibility
  - **Time**: 4 hours

- [ ] **Task**: Create router
  - **File**: `src/workflow_custom_field/presentation/routers/custom_field_router.py`
  - **Endpoints**:
    - GET /api/workflows/{workflow_id}/custom-fields
    - POST /api/workflows/{workflow_id}/custom-fields
    - PUT /api/custom-fields/{field_id}
    - DELETE /api/custom-fields/{field_id}
    - GET /api/stages/{stage_id}/field-configurations
    - PUT /api/stages/{stage_id}/fields/{field_id}/visibility
  - **Time**: 3 hours

- [ ] **Task**: Register router in main application
  - **File**: `src/main.py` or appropriate initialization file
  - **Time**: 30 minutes

#### 1.6 Dependency Injection

- [ ] **Task**: Register repositories in container
  - **File**: `src/core/container.py`
  - **Time**: 1 hour

- [ ] **Task**: Register command/query handlers in container
  - **File**: `src/core/container.py`
  - **Time**: 1 hour

#### 1.7 Testing

- [ ] **Task**: Write unit tests for `CustomField` entity
  - **File**: `tests/unit/workflow_custom_field/test_custom_field.py`
  - **Tests**:
    - test_create_custom_field_with_valid_data
    - test_create_custom_field_with_invalid_key_fails
    - test_validate_config_for_dropdown_requires_options
    - test_validate_config_for_currency_requires_currency
  - **Time**: 4 hours

- [ ] **Task**: Write integration tests for custom field APIs
  - **File**: `tests/integration/workflow_custom_field/test_custom_field_api.py`
  - **Tests**:
    - test_create_custom_field
    - test_list_custom_fields_by_workflow
    - test_update_field_visibility
    - test_delete_custom_field
  - **Time**: 4 hours

### Frontend Tasks

#### 1.8 Types and Services

- [ ] **Task**: Create TypeScript types
  - **File**: `client-vite/src/types/customField.ts`
  - **Types**: CustomField, FieldType, FieldVisibility, CreateCustomFieldRequest, UpdateCustomFieldRequest
  - **Time**: 2 hours

- [ ] **Task**: Create API service
  - **File**: `client-vite/src/services/customFieldService.ts`
  - **Methods**: listCustomFields, createCustomField, updateCustomField, deleteCustomField, updateFieldVisibility
  - **Time**: 3 hours

#### 1.9 Components

- [ ] **Task**: Create `CustomFieldEditor` component
  - **File**: `client-vite/src/components/company/workflow/CustomFieldEditor.tsx`
  - **Features**:
    - Add new field button
    - List of existing fields
    - Field type selector
    - Field configuration form (dynamic based on type)
    - Reorder fields (drag & drop or up/down buttons)
    - Delete field
  - **Time**: 8 hours

- [ ] **Task**: Create `FieldConfigEditor` component
  - **File**: `client-vite/src/components/company/workflow/FieldConfigEditor.tsx`
  - **Features**:
    - Dropdown field with options editor
    - Currency field with min/max
    - File field with allowed extensions
    - Range inputs
  - **Time**: 6 hours

- [ ] **Task**: Create `FieldVisibilityMatrix` component
  - **File**: `client-vite/src/components/company/workflow/FieldVisibilityMatrix.tsx`
  - **Features**:
    - Table showing fields (rows) vs stages (columns)
    - Dropdown in each cell: Hidden, Mandatory, Recommended, Optional
    - Bulk actions (set all fields in stage to same visibility)
  - **Time**: 6 hours

#### 1.10 Integration with Workflow Pages

- [ ] **Task**: Add custom fields tab to `EditWorkflowPage`
  - **File**: `client-vite/src/pages/company/EditWorkflowPage.tsx`
  - **Details**: Add new tab for custom fields after stages tab
  - **Time**: 3 hours

- [ ] **Task**: Add custom fields section to `CreateWorkflowPage`
  - **File**: `client-vite/src/pages/company/CreateWorkflowPage.tsx`
  - **Details**: Add step for custom fields in wizard
  - **Time**: 3 hours

#### 1.11 Testing

- [ ] **Task**: Write component tests for CustomFieldEditor
  - **File**: `client-vite/src/components/company/workflow/__tests__/CustomFieldEditor.test.tsx`
  - **Time**: 3 hours

---

## Phase 2: Field Validation System

**Goal**: Implement validation rules for custom fields that check values during stage transitions.

**Estimated Time**: 2 weeks
**Dependencies**: Phase 1
**Priority**: HIGH

### Backend Tasks

#### 2.1 Database Schema

- [ ] **Task**: Create migration `create_field_validation_rules.sql`
  - **Details**: Create `field_validation_rules` table with all columns
  - **File**: `migrations/versions/XXX_create_field_validation_rules.sql`
  - **Columns**: id, custom_field_id, stage_id, rule_type, comparison_operator, position_field_path, comparison_value, severity, validation_message, auto_reject, rejection_reason, is_active
  - **Time**: 3 hours

- [ ] **Task**: Add validation-related fields to `job_positions` table if needed
  - **Details**: Ensure position has fields like max_salary, minimum_experience, location, desired_start_date
  - **File**: New migration or verify existing schema
  - **Time**: 2 hours

#### 2.2 Domain Layer

- [ ] **Task**: Create `ValidationRule` entity
  - **File**: `src/workflow_custom_field/domain/entities/validation_rule.py`
  - **Details**:
    - Add all properties
    - Create factory method `create()`
    - Add `evaluate()` method with full comparison logic
    - Add `_get_position_field_value()` helper
    - Add `_perform_comparison()` helper
    - Add `_build_message()` helper with variable substitution
  - **Time**: 6 hours

- [ ] **Task**: Create `ValidationResult` value object
  - **File**: `src/workflow_custom_field/domain/value_objects/validation_result.py`
  - **Methods**: passed(), failed()
  - **Time**: 2 hours

- [ ] **Task**: Create enums
  - **Files**:
    - `src/workflow_custom_field/domain/enums/validation_rule_type.py` (compare_position_field, range, pattern, custom)
    - `src/workflow_custom_field/domain/enums/comparison_operator.py` (gt, gte, lt, lte, eq, neq, in_range, out_range)
    - `src/workflow_custom_field/domain/enums/validation_severity.py` (warning, error)
  - **Time**: 2 hours

- [ ] **Task**: Create repository interface
  - **File**: `src/workflow_custom_field/domain/infrastructure/validation_rule_repository_interface.py`
  - **Methods**: get_by_id, get_by_stage, get_by_field, save, delete, activate, deactivate
  - **Time**: 2 hours

#### 2.3 Infrastructure Layer

- [ ] **Task**: Create `ValidationRuleModel` SQLAlchemy model
  - **File**: `src/workflow_custom_field/infrastructure/models/validation_rule_model.py`
  - **Time**: 3 hours

- [ ] **Task**: Create `ValidationRuleRepository` implementation
  - **File**: `src/workflow_custom_field/infrastructure/repositories/validation_rule_repository.py`
  - **Details**: Implement all interface methods with mappers
  - **Time**: 4 hours

#### 2.4 Application Layer - Services

- [ ] **Task**: Create `FieldValidationService`
  - **File**: `src/workflow_custom_field/application/services/field_validation_service.py`
  - **Methods**:
    - `validate_stage_transition()` - main validation method
    - Returns `StageTransitionValidationResult`
  - **Time**: 6 hours

- [ ] **Task**: Create `StageTransitionValidationResult` DTO
  - **File**: `src/workflow_custom_field/application/dtos/stage_transition_validation_result.py`
  - **Methods**: allow(), warn(), block()
  - **Time**: 2 hours

#### 2.5 Application Layer - Commands and Queries

- [ ] **Task**: Create `CreateValidationRuleCommand` and handler
  - **File**: `src/workflow_custom_field/application/commands/create_validation_rule_command.py`
  - **Time**: 3 hours

- [ ] **Task**: Create `UpdateValidationRuleCommand` and handler
  - **File**: `src/workflow_custom_field/application/commands/update_validation_rule_command.py`
  - **Time**: 3 hours

- [ ] **Task**: Create `DeleteValidationRuleCommand` and handler
  - **File**: `src/workflow_custom_field/application/commands/delete_validation_rule_command.py`
  - **Time**: 2 hours

- [ ] **Task**: Create `ActivateValidationRuleCommand` and handler
  - **File**: `src/workflow_custom_field/application/commands/activate_validation_rule_command.py`
  - **Time**: 2 hours

- [ ] **Task**: Create `ListValidationRulesQuery`
  - **File**: `src/workflow_custom_field/application/queries/list_validation_rules_query.py`
  - **Details**: Filter by field_id or stage_id
  - **Time**: 2 hours

- [ ] **Task**: Create `ValidateStageTransitionQuery`
  - **File**: `src/workflow_custom_field/application/queries/validate_stage_transition_query.py`
  - **Details**: Preview validation without actually moving stage
  - **Time**: 3 hours

#### 2.6 Presentation Layer

- [ ] **Task**: Create request/response schemas
  - **Files**:
    - `src/workflow_custom_field/presentation/schemas/create_validation_rule_request.py`
    - `src/workflow_custom_field/presentation/schemas/validation_rule_response.py`
    - `src/workflow_custom_field/presentation/schemas/validation_result_response.py`
  - **Time**: 3 hours

- [ ] **Task**: Create `ValidationRuleController`
  - **File**: `src/workflow_custom_field/presentation/controllers/validation_rule_controller.py`
  - **Methods**: create, update, delete, list, activate, deactivate, validate_preview
  - **Time**: 4 hours

- [ ] **Task**: Create router
  - **File**: `src/workflow_custom_field/presentation/routers/validation_rule_router.py`
  - **Endpoints**:
    - GET /api/custom-fields/{field_id}/validation-rules
    - POST /api/custom-fields/{field_id}/validation-rules
    - GET /api/validation-rules/{rule_id}
    - PUT /api/validation-rules/{rule_id}
    - DELETE /api/validation-rules/{rule_id}
    - POST /api/validation-rules/{rule_id}/activate
    - POST /api/validation-rules/{rule_id}/deactivate
    - GET /api/stages/{stage_id}/validation-rules
    - POST /api/applications/{app_id}/validate-stage-transition
  - **Time**: 4 hours

#### 2.7 Update Application Processing

- [ ] **Task**: Update `ChangeStageCommandHandler` to use validation service
  - **File**: `src/candidate_application/application/commands/change_stage_command_handler.py`
  - **Details**:
    - Inject `FieldValidationService`
    - Inject `PositionRepository`
    - Call validation before stage change
    - Handle validation results (block, warn, auto-reject)
    - Return `ChangeStageResult` with validation info
  - **Time**: 4 hours

- [ ] **Task**: Update `ChangeStageCommand` to add `force_with_warnings` flag
  - **File**: `src/candidate_application/application/commands/change_stage_command.py`
  - **Time**: 1 hour

- [ ] **Task**: Create `ChangeStageResult` DTO
  - **File**: `src/candidate_application/application/dtos/change_stage_result.py`
  - **Properties**: success, status, errors, warnings, rejection_reason
  - **Methods**: success(), validation_failed(), needs_confirmation(), rejected()
  - **Time**: 2 hours

- [ ] **Task**: Update `CandidateApplication` entity with `reject()` method
  - **File**: `src/candidate_application/domain/entities/candidate_application.py`
  - **Details**: Add method to reject application with reason
  - **Time**: 2 hours

#### 2.8 Dependency Injection

- [ ] **Task**: Register validation rule repository in container
  - **File**: `src/core/container.py`
  - **Time**: 1 hour

- [ ] **Task**: Register `FieldValidationService` in container
  - **File**: `src/core/container.py`
  - **Time**: 1 hour

- [ ] **Task**: Register command/query handlers in container
  - **File**: `src/core/container.py`
  - **Time**: 1 hour

#### 2.9 Testing

- [ ] **Task**: Write unit tests for `ValidationRule` entity
  - **File**: `tests/unit/workflow_custom_field/test_validation_rule.py`
  - **Tests**:
    - test_create_validation_rule_with_position_comparison
    - test_validation_rule_evaluate_salary_exceeds_max
    - test_validation_rule_evaluate_salary_within_range
    - test_validation_rule_with_range_operator
    - test_validation_rule_message_substitution
    - test_auto_reject_only_for_errors
  - **Time**: 6 hours

- [ ] **Task**: Write unit tests for `FieldValidationService`
  - **File**: `tests/unit/workflow_custom_field/test_field_validation_service.py`
  - **Tests**:
    - test_validate_stage_transition_blocks_on_errors
    - test_validate_stage_transition_warns_but_allows
    - test_validate_stage_transition_multiple_rules
    - test_validate_stage_transition_auto_reject
  - **Time**: 4 hours

- [ ] **Task**: Write integration tests for validation APIs
  - **File**: `tests/integration/workflow_custom_field/test_validation_rule_api.py`
  - **Tests**:
    - test_create_validation_rule
    - test_list_validation_rules_by_stage
    - test_validate_stage_transition_preview
  - **Time**: 4 hours

- [ ] **Task**: Write integration tests for stage change with validation
  - **File**: `tests/integration/candidate_application/test_change_stage_with_validation.py`
  - **Tests**:
    - test_change_stage_blocked_by_validation_error
    - test_change_stage_with_warnings_requires_confirmation
    - test_change_stage_with_force_flag
    - test_change_stage_auto_rejects_candidate
  - **Time**: 5 hours

### Frontend Tasks

#### 2.10 Types and Services

- [ ] **Task**: Create TypeScript types
  - **File**: `client-vite/src/types/validationRule.ts`
  - **Types**: ValidationRule, ComparisonOperator, ValidationSeverity, ValidationResult, StageTransitionValidationResult, ChangeStageResult
  - **Time**: 2 hours

- [ ] **Task**: Create API service
  - **File**: `client-vite/src/services/validationRuleService.ts`
  - **Methods**: createValidationRule, updateValidationRule, deleteValidationRule, listValidationRules, activateRule, deactivateRule, validateStageTransition
  - **Time**: 3 hours

- [ ] **Task**: Update application service
  - **File**: `client-vite/src/services/applicationService.ts`
  - **Update**: `changeStage()` method to handle new response format with validation results
  - **Time**: 2 hours

#### 2.11 Components

- [ ] **Task**: Create `ValidationRuleEditor` component
  - **File**: `client-vite/src/components/company/workflow/ValidationRuleEditor.tsx`
  - **Features**:
    - Field selector
    - Rule type selector
    - Comparison operator selector
    - Position field path input (autocomplete with available fields)
    - Severity selector (Warning/Error)
    - Message input with variable helper
    - Auto-reject checkbox
    - Rejection reason input (conditional)
  - **Time**: 8 hours

- [ ] **Task**: Create `ValidationRuleList` component
  - **File**: `client-vite/src/components/company/workflow/ValidationRuleList.tsx`
  - **Features**:
    - List all rules for a field or stage
    - Show rule details (comparison, severity, message)
    - Edit/Delete actions
    - Activate/Deactivate toggle
  - **Time**: 4 hours

- [ ] **Task**: Create `ValidationResultModal` component
  - **File**: `client-vite/src/components/company/application/ValidationResultModal.tsx`
  - **Features**:
    - Show validation errors (block with message)
    - Show validation warnings (with "Proceed Anyway" button)
    - Handle auto-reject case
    - Cancel action
  - **Time**: 6 hours

- [ ] **Task**: Update `StageTransitionButton` component
  - **File**: `client-vite/src/components/company/application/StageTransitionButton.tsx`
  - **Details**:
    - Call validation preview before moving
    - Show ValidationResultModal if validation fails
    - Handle force_with_warnings flag on retry
  - **Time**: 4 hours

#### 2.12 Integration

- [ ] **Task**: Add validation rules to custom field editor
  - **File**: `client-vite/src/components/company/workflow/CustomFieldEditor.tsx`
  - **Details**: Add "Validation Rules" button/section for each field
  - **Time**: 3 hours

- [ ] **Task**: Add validation rules tab to `EditWorkflowPage`
  - **File**: `client-vite/src/pages/company/EditWorkflowPage.tsx`
  - **Details**: Add tab to view/manage all validation rules for workflow
  - **Time**: 3 hours

#### 2.13 Testing

- [ ] **Task**: Write component tests for ValidationRuleEditor
  - **File**: `client-vite/src/components/company/workflow/__tests__/ValidationRuleEditor.test.tsx`
  - **Time**: 3 hours

- [ ] **Task**: Write E2E test for validation flow
  - **File**: `client-vite/e2e/workflow-validation.spec.ts`
  - **Scenario**: Create validation rule, try to move candidate with invalid data, verify blocked
  - **Time**: 4 hours

---

## Phase 3: Position-Workflow Integration

**Goal**: Connect workflows to job positions so each position uses a specific workflow.

**Estimated Time**: 1 week
**Dependencies**: Phase 1, Phase 2
**Priority**: HIGH

### Backend Tasks

#### 3.1 Database Schema

- [ ] **Task**: Create migration `add_workflow_id_to_positions.sql`
  - **Details**: Add `workflow_id` column to `job_positions` table
  - **File**: `migrations/versions/XXX_add_workflow_id_to_positions.sql`
  - **Time**: 1 hour

- [ ] **Task**: Add default workflow to company
  - **Details**: Add `default_workflow_id` column to `companies` table (if not exists)
  - **File**: New migration or verify existing
  - **Time**: 1 hour

#### 3.2 Domain Layer

- [ ] **Task**: Update `Position` entity to include workflow_id
  - **File**: `src/position/domain/entities/position.py`
  - **Details**: Add workflow_id property, update factory method
  - **Time**: 2 hours

- [ ] **Task**: Add business rule: workflow must belong to same company
  - **File**: `src/position/domain/entities/position.py`
  - **Details**: Add validation in factory method
  - **Time**: 1 hour

- [ ] **Task**: Update `Company` entity to include default_workflow_id
  - **File**: `src/company/domain/entities/company.py`
  - **Time**: 2 hours

#### 3.3 Infrastructure Layer

- [ ] **Task**: Update `PositionModel` to include workflow_id
  - **File**: `src/position/infrastructure/models/position_model.py`
  - **Details**: Add column, add relationship to workflow
  - **Time**: 2 hours

- [ ] **Task**: Update `PositionRepository` mappers
  - **File**: `src/position/infrastructure/repositories/position_repository.py`
  - **Details**: Include workflow_id in _to_domain() and _to_model()
  - **Time**: 2 hours

#### 3.4 Application Layer

- [ ] **Task**: Update `CreatePositionCommand` to include workflow_id
  - **File**: `src/position/application/commands/create_position_command.py`
  - **Time**: 1 hour

- [ ] **Task**: Update `CreatePositionCommandHandler`
  - **File**: `src/position/application/commands/create_position_command_handler.py`
  - **Details**:
    - If workflow_id not provided, use company's default_workflow_id
    - Validate workflow belongs to company
    - Emit `PositionCreatedEvent` with workflow_id
  - **Time**: 3 hours

- [ ] **Task**: Update `UpdatePositionCommand` to allow changing workflow
  - **File**: `src/position/application/commands/update_position_command.py`
  - **Time**: 2 hours

- [ ] **Task**: Update `PositionDto` to include workflow information
  - **File**: `src/position/application/dtos/position_dto.py`
  - **Details**: Add workflow_id, optionally workflow_name
  - **Time**: 1 hour

#### 3.5 Presentation Layer

- [ ] **Task**: Update `CreatePositionRequest` schema
  - **File**: `src/position/presentation/schemas/create_position_request.py`
  - **Details**: Add workflow_id field (optional)
  - **Time**: 1 hour

- [ ] **Task**: Update `PositionResponse` schema
  - **File**: `src/position/presentation/schemas/position_response.py`
  - **Details**: Include workflow_id and workflow_name
  - **Time**: 1 hour

- [ ] **Task**: Update `PositionController`
  - **File**: `src/position/presentation/controllers/position_controller.py`
  - **Details**: Pass workflow_id in create and update methods
  - **Time**: 2 hours

#### 3.6 Testing

- [ ] **Task**: Write unit tests for position with workflow
  - **File**: `tests/unit/position/test_position_with_workflow.py`
  - **Tests**:
    - test_create_position_with_workflow
    - test_create_position_uses_default_workflow
    - test_create_position_validates_workflow_company
  - **Time**: 3 hours

- [ ] **Task**: Write integration tests
  - **File**: `tests/integration/position/test_position_workflow_integration.py`
  - **Tests**:
    - test_create_position_with_workflow_via_api
    - test_change_position_workflow
  - **Time**: 3 hours

### Frontend Tasks

#### 3.7 Components

- [ ] **Task**: Create `WorkflowSelector` component
  - **File**: `client-vite/src/components/company/position/WorkflowSelector.tsx`
  - **Features**:
    - Dropdown to select workflow
    - Display workflow stages preview
    - Show stage count and estimated timeline
    - Option to use company default
  - **Time**: 6 hours

- [ ] **Task**: Update `CreatePositionPage` to include workflow selection
  - **File**: `client-vite/src/pages/company/CreatePositionPage.tsx`
  - **Details**: Add WorkflowSelector component after basic info
  - **Time**: 3 hours

- [ ] **Task**: Update `EditPositionPage` to allow changing workflow
  - **File**: `client-vite/src/pages/company/EditPositionPage.tsx`
  - **Details**: Add warning about existing applications if changing workflow
  - **Time**: 3 hours

- [ ] **Task**: Update `PositionDetailPage` to display workflow
  - **File**: `client-vite/src/pages/company/PositionDetailPage.tsx`
  - **Details**: Show assigned workflow name and stages
  - **Time**: 2 hours

#### 3.8 Testing

- [ ] **Task**: Write component tests for WorkflowSelector
  - **File**: `client-vite/src/components/company/position/__tests__/WorkflowSelector.test.tsx`
  - **Time**: 2 hours

---

## Phase 4: Stage Assignments

**Goal**: Allow assigning specific users to handle each stage of a position's workflow.

**Estimated Time**: 1.5 weeks
**Dependencies**: Phase 3
**Priority**: HIGH

### Backend Tasks

#### 4.1 Database Schema

- [ ] **Task**: Create migration `create_position_stage_assignments.sql`
  - **Details**: Create `position_stage_assignments` table
  - **File**: `migrations/versions/XXX_create_position_stage_assignments.sql`
  - **Columns**: id, position_id, stage_id, assigned_user_ids (JSONB array)
  - **Time**: 2 hours

#### 4.2 Domain Layer

- [ ] **Task**: Create `PositionStageAssignment` entity
  - **File**: `src/position_stage_assignment/domain/entities/position_stage_assignment.py`
  - **Details**:
    - Properties: id, position_id, stage_id, assigned_user_ids
    - Factory method `create()`
    - Method `add_user(user_id)`
    - Method `remove_user(user_id)`
    - Method `replace_users(user_ids)`
  - **Time**: 4 hours

- [ ] **Task**: Create value objects
  - **Files**:
    - `src/position_stage_assignment/domain/value_objects/position_stage_assignment_id.py`
    - `src/position_stage_assignment/domain/value_objects/assigned_user_ids.py`
  - **Time**: 2 hours

- [ ] **Task**: Create repository interface
  - **File**: `src/position_stage_assignment/domain/infrastructure/position_stage_assignment_repository_interface.py`
  - **Methods**: get_by_id, get_by_position, get_by_position_and_stage, save, delete
  - **Time**: 2 hours

#### 4.3 Infrastructure Layer

- [ ] **Task**: Create `PositionStageAssignmentModel`
  - **File**: `src/position_stage_assignment/infrastructure/models/position_stage_assignment_model.py`
  - **Time**: 3 hours

- [ ] **Task**: Create `PositionStageAssignmentRepository` implementation
  - **File**: `src/position_stage_assignment/infrastructure/repositories/position_stage_assignment_repository.py`
  - **Time**: 4 hours

#### 4.4 Application Layer - Commands

- [ ] **Task**: Create `AssignUsersToStageCommand` and handler
  - **File**: `src/position_stage_assignment/application/commands/assign_users_to_stage_command.py`
  - **Details**: Batch assign users to a stage (create or update)
  - **Time**: 3 hours

- [ ] **Task**: Create `RemoveUserFromStageCommand` and handler
  - **File**: `src/position_stage_assignment/application/commands/remove_user_from_stage_command.py`
  - **Time**: 2 hours

- [ ] **Task**: Create `CopyWorkflowAssignmentsCommand` and handler
  - **File**: `src/position_stage_assignment/application/commands/copy_workflow_assignments_command.py`
  - **Details**: Copy default_assigned_users from workflow stages to position
  - **Time**: 4 hours

#### 4.5 Application Layer - Queries

- [ ] **Task**: Create `ListStageAssignmentsQuery` and handler
  - **File**: `src/position_stage_assignment/application/queries/list_stage_assignments_query.py`
  - **Details**: Get all assignments for a position
  - **Time**: 2 hours

- [ ] **Task**: Create `GetAssignedUsersQuery` and handler
  - **File**: `src/position_stage_assignment/application/queries/get_assigned_users_query.py`
  - **Details**: Get users assigned to specific stage
  - **Time**: 2 hours

#### 4.6 Application Layer - Event Handlers

- [ ] **Task**: Create `CreateDefaultStageAssignmentsHandler`
  - **File**: `src/position_stage_assignment/application/handlers/create_default_stage_assignments_handler.py`
  - **Details**:
    - Listen to `PositionCreatedEvent`
    - If position has workflow, copy default assignments
  - **Time**: 4 hours

- [ ] **Task**: Register event handler
  - **File**: `src/core/event_bus.py` or container
  - **Time**: 1 hour

#### 4.7 Presentation Layer

- [ ] **Task**: Create request/response schemas
  - **Files**:
    - `src/position_stage_assignment/presentation/schemas/assign_users_request.py`
    - `src/position_stage_assignment/presentation/schemas/position_stage_assignment_response.py`
  - **Time**: 2 hours

- [ ] **Task**: Create `PositionStageAssignmentController`
  - **File**: `src/position_stage_assignment/presentation/controllers/position_stage_assignment_controller.py`
  - **Methods**: assign_users, remove_user, list_assignments, copy_workflow_defaults
  - **Time**: 4 hours

- [ ] **Task**: Create router
  - **File**: `src/position_stage_assignment/presentation/routers/position_stage_assignment_router.py`
  - **Endpoints**:
    - GET /api/positions/{position_id}/stage-assignments
    - POST /api/positions/{position_id}/stage-assignments (batch)
    - PUT /api/positions/{position_id}/stages/{stage_id}/users
    - POST /api/positions/{position_id}/stages/{stage_id}/users/{user_id}
    - DELETE /api/positions/{position_id}/stages/{stage_id}/users/{user_id}
    - POST /api/positions/{position_id}/copy-workflow-assignments
  - **Time**: 4 hours

#### 4.8 Dependency Injection

- [ ] **Task**: Register all components in container
  - **File**: `src/core/container.py`
  - **Time**: 1 hour

#### 4.9 Testing

- [ ] **Task**: Write unit tests for `PositionStageAssignment` entity
  - **File**: `tests/unit/position_stage_assignment/test_position_stage_assignment.py`
  - **Tests**:
    - test_create_position_stage_assignment
    - test_add_user_to_assignment
    - test_remove_user_from_assignment
    - test_replace_users
  - **Time**: 3 hours

- [ ] **Task**: Write integration tests
  - **File**: `tests/integration/position_stage_assignment/test_position_stage_assignment_api.py`
  - **Tests**:
    - test_assign_users_to_stage
    - test_list_assignments_for_position
    - test_copy_workflow_defaults
    - test_auto_create_assignments_on_position_creation
  - **Time**: 4 hours

### Frontend Tasks

#### 4.10 Types and Services

- [ ] **Task**: Create TypeScript types
  - **File**: `client-vite/src/types/positionStageAssignment.ts`
  - **Types**: PositionStageAssignment, AssignUsersRequest
  - **Time**: 1 hour

- [ ] **Task**: Create API service
  - **File**: `client-vite/src/services/positionStageAssignmentService.ts`
  - **Methods**: listAssignments, assignUsers, removeUser, copyWorkflowDefaults
  - **Time**: 3 hours

#### 4.11 Components

- [ ] **Task**: Create `StageAssignmentEditor` component
  - **File**: `client-vite/src/components/company/position/StageAssignmentEditor.tsx`
  - **Features**:
    - Table or cards showing each stage
    - Multi-select dropdown for users per stage
    - Show role suggestions from stage.default_roles
    - Save button (batch update)
    - "Copy from workflow" button
  - **Time**: 8 hours

- [ ] **Task**: Create `UserMultiSelect` component
  - **File**: `client-vite/src/components/company/position/UserMultiSelect.tsx`
  - **Features**:
    - Search/filter users
    - Show user avatar and name
    - Show user roles
    - Selected users as chips
  - **Time**: 6 hours

#### 4.12 Integration with Position Pages

- [ ] **Task**: Add stage assignment step to `CreatePositionPage`
  - **File**: `client-vite/src/pages/company/CreatePositionPage.tsx`
  - **Details**: Add step after workflow selection
  - **Time**: 4 hours

- [ ] **Task**: Add "Edit Assignments" button to `PositionDetailPage`
  - **File**: `client-vite/src/pages/company/PositionDetailPage.tsx`
  - **Details**: Open modal with StageAssignmentEditor
  - **Time**: 3 hours

#### 4.13 Testing

- [ ] **Task**: Write component tests
  - **File**: `client-vite/src/components/company/position/__tests__/StageAssignmentEditor.test.tsx`
  - **Time**: 3 hours

---

## Phase 5: Application Processing with Validations

**Goal**: Implement full application processing flow with permission checks and field validations.

**Estimated Time**: 2 weeks
**Dependencies**: Phase 2, Phase 4
**Priority**: HIGH

### Backend Tasks

#### 5.1 Update Application Entity

- [ ] **Task**: Add validation and stage tracking fields to `CandidateApplication`
  - **File**: `src/candidate_application/domain/entities/candidate_application.py`
  - **Details**:
    - Add `stage_entered_at: datetime`
    - Add `stage_deadline: Optional[datetime]`
    - Add `task_status: TaskStatus` enum (pending, in_progress, completed, blocked)
    - Add method `calculate_stage_deadline(stage: WorkflowStage)`
    - Add method `move_to_stage(new_stage_id, changed_by)`
  - **Time**: 4 hours

- [ ] **Task**: Create migration to add new fields
  - **File**: `migrations/versions/XXX_add_stage_tracking_to_applications.sql`
  - **Time**: 2 hours

#### 5.2 Permission Service

- [ ] **Task**: Create `StagePermissionService`
  - **File**: `src/candidate_application/application/services/stage_permission_service.py`
  - **Methods**:
    - `can_user_process_stage(user_id, application)` → bool
    - `get_assigned_users_for_stage(position_id, stage_id)` → List[str]
    - `is_user_company_admin(user_id, company_id)` → bool
  - **Details**: Check if user is assigned to stage or is admin
  - **Time**: 4 hours

#### 5.3 Update Change Stage Command

- [ ] **Task**: Update `ChangeStageCommandHandler` with full validation and permission checks
  - **File**: `src/candidate_application/application/commands/change_stage_command_handler.py`
  - **Details** (already partially covered in Phase 2):
    - Verify permission
    - Validate stage transition (field validations)
    - Update stage_entered_at
    - Calculate stage_deadline
    - Handle auto-reject
    - Emit event
  - **Time**: 2 hours (refinement from Phase 2)

#### 5.4 Presentation Layer

- [ ] **Task**: Update change stage endpoint to return full result
  - **File**: `src/candidate_application/presentation/controllers/candidate_application_controller.py`
  - **Details**: Return ChangeStageResult with all validation info
  - **Time**: 2 hours

- [ ] **Task**: Create permission check endpoint
  - **Endpoint**: GET /api/applications/{app_id}/can-change-stage
  - **Details**: Return boolean if current user can move candidate
  - **Time**: 2 hours

#### 5.5 Testing

- [ ] **Task**: Write integration tests for full flow
  - **File**: `tests/integration/candidate_application/test_application_processing_flow.py`
  - **Tests**:
    - test_create_application_sets_initial_stage
    - test_change_stage_updates_timestamps
    - test_change_stage_calculates_deadline
    - test_change_stage_blocked_by_permission
    - test_change_stage_blocked_by_validation
    - test_change_stage_auto_rejects
  - **Time**: 6 hours

### Frontend Tasks

#### 5.6 Update Application Components

- [ ] **Task**: Update `ApplicationCard` to show deadline and status
  - **File**: `client-vite/src/components/company/application/ApplicationCard.tsx`
  - **Details**: Add deadline badge, task status indicator
  - **Time**: 3 hours

- [ ] **Task**: Update `StageTransitionButton` with permission check
  - **File**: `client-vite/src/components/company/application/StageTransitionButton.tsx`
  - **Details**:
    - Call permission check API on mount
    - Disable if no permission
    - Show tooltip explaining why
  - **Time**: 2 hours (additional work from Phase 2)

- [ ] **Task**: Create `ApplicationHistory` component
  - **File**: `client-vite/src/components/company/application/ApplicationHistory.tsx`
  - **Features**:
    - Timeline showing stage changes
    - Show who moved candidate
    - Show time in each stage
    - Show deadline missed/met
  - **Time**: 6 hours

#### 5.7 Testing

- [ ] **Task**: Write E2E test for complete application flow
  - **File**: `client-vite/e2e/application-processing.spec.ts`
  - **Scenario**: Create position, candidate applies, move through stages with validations
  - **Time**: 4 hours

---

## Phase 6: Task Management System

**Goal**: Implement task dashboard for users to see and manage their assigned applications.

**Estimated Time**: 2 weeks
**Dependencies**: Phase 5
**Priority**: MEDIUM

### Backend Tasks

#### 6.1 User Roles System

- [ ] **Task**: Add roles field to `CompanyUser`
  - **File**: `src/company_user/domain/entities/company_user.py`
  - **Details**: Add `roles: List[str]` property
  - **Time**: 2 hours

- [ ] **Task**: Create migration to add roles column
  - **File**: `migrations/versions/XXX_add_roles_to_company_users.sql`
  - **Details**: Add `roles JSONB DEFAULT '[]'` to company_users table
  - **Time**: 1 hour

- [ ] **Task**: Create `AssignRolesToUserCommand` and handler
  - **File**: `src/company_user/application/commands/assign_roles_to_user_command.py`
  - **Time**: 3 hours

- [ ] **Task**: Create `GetUserRolesQuery` and handler
  - **File**: `src/company_user/application/queries/get_user_roles_query.py`
  - **Time**: 2 hours

#### 6.2 Task Priority System

- [ ] **Task**: Create `TaskPriority` value object
  - **File**: `src/candidate_application/domain/value_objects/task_priority.py`
  - **Details**:
    - Properties: base_priority, deadline_weight, position_weight, candidate_weight
    - Method `calculate(application, current_date)` → TaskPriority
    - Method `total_score()` → int
    - Static method `_calculate_deadline_weight(deadline, now)` → int
  - **Time**: 4 hours

- [ ] **Task**: Add priority calculation to `CandidateApplication`
  - **File**: `src/candidate_application/domain/entities/candidate_application.py`
  - **Details**: Add method `calculate_priority()` that uses TaskPriority
  - **Time**: 2 hours

#### 6.3 Task Queries

- [ ] **Task**: Create `GetMyAssignedTasksQuery` and handler
  - **File**: `src/candidate_application/application/queries/get_my_assigned_tasks_query.py`
  - **Details**:
    - Return applications where user is in assigned_user_ids for current stage
    - Sort by priority desc, stage_entered_at asc
    - Add filters (stage, priority, deadline, position)
  - **Time**: 6 hours

- [ ] **Task**: Create `GetAvailableTasksQuery` and handler
  - **File**: `src/candidate_application/application/queries/get_available_tasks_query.py`
  - **Details**:
    - Return applications where:
      - Current stage's default_roles contains any of user's roles
      - User not in assigned_user_ids (unassigned)
    - Sort by priority desc
  - **Time**: 6 hours

- [ ] **Task**: Create `GetAllMyTasksQuery` and handler
  - **File**: `src/candidate_application/application/queries/get_all_my_tasks_query.py`
  - **Details**: Combine assigned and available, sort by assigned first
  - **Time**: 3 hours

#### 6.4 Task Actions

- [ ] **Task**: Create `ClaimTaskCommand` and handler
  - **File**: `src/candidate_application/application/commands/claim_task_command.py`
  - **Details**: User claims an available task, updates task_status to in_progress
  - **Time**: 3 hours

- [ ] **Task**: Create `UnclaimTaskCommand` and handler
  - **File**: `src/candidate_application/application/commands/unclaim_task_command.py`
  - **Details**: User releases a task back to available pool
  - **Time**: 2 hours

- [ ] **Task**: Create `UpdateTaskStatusCommand` and handler
  - **File**: `src/candidate_application/application/commands/update_task_status_command.py`
  - **Details**: Update task status (pending, in_progress, completed, blocked)
  - **Time**: 2 hours

#### 6.5 Presentation Layer

- [ ] **Task**: Create `TaskDto`
  - **File**: `src/candidate_application/application/dtos/task_dto.py`
  - **Properties**: application, candidate_name, candidate_photo, position_title, current_stage_name, priority_score, deadline, days_in_stage, assignment_type, can_process
  - **Time**: 3 hours

- [ ] **Task**: Create `TaskController`
  - **File**: `src/candidate_application/presentation/controllers/task_controller.py`
  - **Methods**: get_assigned_tasks, get_available_tasks, get_all_tasks, claim_task, unclaim_task, update_task_status
  - **Time**: 4 hours

- [ ] **Task**: Create task router
  - **File**: `src/candidate_application/presentation/routers/task_router.py`
  - **Endpoints**:
    - GET /api/company-users/{user_id}/tasks/assigned
    - GET /api/company-users/{user_id}/tasks/available
    - GET /api/company-users/{user_id}/tasks/all
    - POST /api/applications/{app_id}/claim
    - POST /api/applications/{app_id}/unclaim
    - PUT /api/applications/{app_id}/task-status
  - **Time**: 3 hours

#### 6.6 Testing

- [ ] **Task**: Write unit tests for TaskPriority
  - **File**: `tests/unit/candidate_application/test_task_priority.py`
  - **Tests**:
    - test_calculate_priority_with_overdue_deadline
    - test_calculate_priority_with_position_priority
    - test_calculate_priority_combined_factors
  - **Time**: 3 hours

- [ ] **Task**: Write integration tests for task queries
  - **File**: `tests/integration/candidate_application/test_task_queries.py`
  - **Tests**:
    - test_get_assigned_tasks
    - test_get_available_tasks_by_role
    - test_task_priority_sorting
    - test_claim_and_unclaim_task
  - **Time**: 5 hours

### Frontend Tasks

#### 6.7 Types and Services

- [ ] **Task**: Create TypeScript types
  - **File**: `client-vite/src/types/task.ts`
  - **Types**: Task, TaskFilters, TaskPriority, TaskStatus
  - **Time**: 2 hours

- [ ] **Task**: Create API service
  - **File**: `client-vite/src/services/taskService.ts`
  - **Methods**: getAssignedTasks, getAvailableTasks, getAllTasks, claimTask, unclaimTask, updateTaskStatus
  - **Time**: 3 hours

#### 6.8 Components

- [ ] **Task**: Create `MyTasksPage`
  - **File**: `client-vite/src/pages/company/MyTasksPage.tsx`
  - **Features**:
    - Header with filters and search
    - Two sections: "My Assigned Tasks" and "Available Tasks"
    - Task cards with all info
    - Pagination
  - **Time**: 8 hours

- [ ] **Task**: Create `TaskCard` component
  - **File**: `client-vite/src/components/company/tasks/TaskCard.tsx`
  - **Features**:
    - Candidate name and photo
    - Position title
    - Current stage name
    - Priority badge (color-coded)
    - Deadline with urgency indicator
    - Time in stage
    - Quick actions: View, Claim, Move to Next Stage
  - **Time**: 6 hours

- [ ] **Task**: Create `TaskFilters` component
  - **File**: `client-vite/src/components/company/tasks/TaskFilters.tsx`
  - **Features**:
    - Filter by stage (multi-select)
    - Filter by priority (slider or select)
    - Filter by deadline (overdue, today, this week, all)
    - Filter by position
  - **Time**: 5 hours

- [ ] **Task**: Create `PriorityBadge` component
  - **File**: `client-vite/src/components/company/tasks/PriorityBadge.tsx`
  - **Features**:
    - Color-coded: Red (175+), Orange (150-174), Yellow (125-149), Gray (<125)
    - Show priority number
  - **Time**: 2 hours

- [ ] **Task**: Create `DeadlineIndicator` component
  - **File**: `client-vite/src/components/company/tasks/DeadlineIndicator.tsx`
  - **Features**:
    - Color-coded: Red (overdue), Orange (today), Yellow (1-2 days), Gray (3+ days)
    - Show relative time ("due in 2 hours", "overdue by 1 day")
  - **Time**: 3 hours

#### 6.9 Navigation

- [ ] **Task**: Add "My Tasks" link to navigation
  - **File**: `client-vite/src/components/layout/CompanyNav.tsx`
  - **Details**: Add link with task count badge
  - **Time**: 2 hours

- [ ] **Task**: Implement real-time task count update
  - **Details**: Poll API or use WebSocket for task count
  - **Time**: 4 hours

#### 6.10 Testing

- [ ] **Task**: Write component tests
  - **File**: `client-vite/src/components/company/tasks/__tests__/TaskCard.test.tsx`
  - **Time**: 3 hours

- [ ] **Task**: Write E2E test for task dashboard
  - **File**: `client-vite/e2e/task-dashboard.spec.ts`
  - **Scenario**: User logs in, sees tasks, claims task, completes it
  - **Time**: 4 hours

---

## Phase 7: Email Integration

**Goal**: Implement email templates and automatic emails on stage transitions.

**Estimated Time**: 1.5 weeks
**Dependencies**: Phase 5
**Priority**: MEDIUM

### Backend Tasks

#### 7.1 Database Schema

- [ ] **Task**: Create migration `create_email_templates.sql`
  - **Details**: Create `email_templates` table
  - **File**: `migrations/versions/XXX_create_email_templates.sql`
  - **Time**: 2 hours

#### 7.2 Domain Layer

- [ ] **Task**: Create `EmailTemplate` entity
  - **File**: `src/email_template/domain/entities/email_template.py`
  - **Details**:
    - Properties: id, company_id, name, subject, body, variables
    - Method `render(context, custom_text)` → str
  - **Time**: 4 hours

- [ ] **Task**: Create `EmailVariables` helper class
  - **File**: `src/email_template/domain/services/email_variables.py`
  - **Methods**: build_context(candidate, position, company, stage, custom_text)
  - **Constants**: CANDIDATE_NAME, CANDIDATE_FIRST_NAME, POSITION_TITLE, COMPANY_NAME, STAGE_NAME, CUSTOM_TEXT
  - **Time**: 3 hours

- [ ] **Task**: Create repository interface
  - **File**: `src/email_template/domain/infrastructure/email_template_repository_interface.py`
  - **Time**: 2 hours

#### 7.3 Infrastructure Layer

- [ ] **Task**: Create `EmailTemplateModel`
  - **File**: `src/email_template/infrastructure/models/email_template_model.py`
  - **Time**: 2 hours

- [ ] **Task**: Create `EmailTemplateRepository` implementation
  - **File**: `src/email_template/infrastructure/repositories/email_template_repository.py`
  - **Time**: 3 hours

#### 7.4 Application Layer - CRUD

- [ ] **Task**: Create full CQRS for email templates
  - **Commands**: Create, Update, Delete
  - **Queries**: List, GetById
  - **Time**: 6 hours

#### 7.5 Application Layer - Event Handler

- [ ] **Task**: Create `SendStageTransitionEmailHandler`
  - **File**: `src/email_template/application/handlers/send_stage_transition_email_handler.py`
  - **Details**:
    - Listen to `ApplicationStageChangedEvent`
    - Get new stage
    - If stage has email_template_id, render and send email
    - Log email sent
  - **Time**: 6 hours

- [ ] **Task**: Register event handler
  - **File**: `src/core/event_bus.py`
  - **Time**: 1 hour

#### 7.6 Presentation Layer

- [ ] **Task**: Create email template CRUD endpoints
  - **Controller**: `EmailTemplateController`
  - **Router**: `EmailTemplateRouter`
  - **Endpoints**:
    - GET /api/company/{company_id}/email-templates
    - POST /api/company/{company_id}/email-templates
    - GET /api/email-templates/{template_id}
    - PUT /api/email-templates/{template_id}
    - DELETE /api/email-templates/{template_id}
    - POST /api/email-templates/{template_id}/preview
    - POST /api/email-templates/{template_id}/test-send
  - **Time**: 6 hours

#### 7.7 Seed Data

- [ ] **Task**: Create seed script for default email templates
  - **File**: `seeds/email_templates.py`
  - **Templates**:
    - "Stage Transition - Generic"
    - "Interview Invitation"
    - "Offer Letter"
    - "Rejection Notice"
  - **Time**: 4 hours

#### 7.8 Testing

- [ ] **Task**: Write unit tests for email rendering
  - **File**: `tests/unit/email_template/test_email_template.py`
  - **Tests**:
    - test_render_template_with_variables
    - test_render_template_with_custom_text
    - test_variable_substitution
  - **Time**: 3 hours

- [ ] **Task**: Write integration tests
  - **File**: `tests/integration/email_template/test_send_stage_transition_email.py`
  - **Tests**:
    - test_email_sent_on_stage_change
    - test_no_email_if_template_not_configured
  - **Time**: 4 hours

### Frontend Tasks

#### 7.9 Types and Services

- [ ] **Task**: Create TypeScript types and service
  - **Files**: `client-vite/src/types/emailTemplate.ts`, `client-vite/src/services/emailTemplateService.ts`
  - **Time**: 2 hours

#### 7.10 Components

- [ ] **Task**: Create `EmailTemplatesPage`
  - **File**: `client-vite/src/pages/company/EmailTemplatesPage.tsx`
  - **Features**: List, Create, Edit, Delete templates
  - **Time**: 6 hours

- [ ] **Task**: Create `TemplateEditor` component
  - **File**: `client-vite/src/components/company/email/TemplateEditor.tsx`
  - **Features**:
    - Rich text editor (TipTap or similar)
    - Variable palette (insert placeholders)
    - Preview button
    - Test send button
  - **Time**: 10 hours

- [ ] **Task**: Create `TemplateVariables` helper component
  - **File**: `client-vite/src/components/company/email/TemplateVariables.tsx`
  - **Features**: Show available variables, copy to clipboard
  - **Time**: 3 hours

- [ ] **Task**: Create `EmailPreview` component
  - **File**: `client-vite/src/components/company/email/EmailPreview.tsx`
  - **Features**: Render email with sample data
  - **Time**: 4 hours

#### 7.11 Update Workflow Stage Form

- [ ] **Task**: Add email configuration to stage form
  - **File**: `client-vite/src/components/company/workflow/StageForm.tsx`
  - **Details**:
    - Email template dropdown
    - Preview button
    - Custom email text textarea
    - Preview final email button
  - **Time**: 4 hours

#### 7.12 Testing

- [ ] **Task**: Write component tests
  - **File**: `client-vite/src/components/company/email/__tests__/TemplateEditor.test.tsx`
  - **Time**: 3 hours

---

## Phase 8: Talent Pool

**Goal**: Implement talent pool system for candidates in sourcing workflow.

**Estimated Time**: 1 week
**Dependencies**: None (can be parallel)
**Priority**: LOW

### Backend Tasks

#### 8.1 Database Schema

- [ ] **Task**: Create migration `create_company_talent_pool.sql`
  - **Details**: Create `company_talent_pool` table
  - **File**: `migrations/versions/XXX_create_company_talent_pool.sql`
  - **Time**: 2 hours

#### 8.2 Domain Layer

- [ ] **Task**: Create `CompanyTalentPool` entity
  - **File**: `src/talent_pool/domain/entities/company_talent_pool.py`
  - **Details**:
    - Properties: id, company_id, company_candidate_id, comments, tags, added_at, added_by_user_id
    - Factory method `create()`
    - Method `update_comments()`
    - Method `add_tag()`, `remove_tag()`
  - **Time**: 4 hours

- [ ] **Task**: Create repository interface
  - **File**: `src/talent_pool/domain/infrastructure/company_talent_pool_repository_interface.py`
  - **Time**: 2 hours

#### 8.3 Infrastructure Layer

- [ ] **Task**: Create `CompanyTalentPoolModel`
  - **File**: `src/talent_pool/infrastructure/models/company_talent_pool_model.py`
  - **Time**: 2 hours

- [ ] **Task**: Create `CompanyTalentPoolRepository` implementation
  - **File**: `src/talent_pool/infrastructure/repositories/company_talent_pool_repository.py`
  - **Time**: 3 hours

#### 8.4 Application Layer

- [ ] **Task**: Create CQRS commands and queries
  - **Commands**: AddToTalentPool, RemoveFromTalentPool, UpdateTalentPoolEntry
  - **Queries**: ListTalentPool, GetTalentPoolEntry, SearchTalentPool
  - **Time**: 8 hours

#### 8.5 Presentation Layer

- [ ] **Task**: Create controller and router
  - **Endpoints**:
    - GET /api/company/{company_id}/talent-pool
    - POST /api/company/{company_id}/talent-pool
    - GET /api/talent-pool/{entry_id}
    - PUT /api/talent-pool/{entry_id}
    - DELETE /api/talent-pool/{entry_id}
    - POST /api/talent-pool/search
  - **Time**: 5 hours

#### 8.6 Testing

- [ ] **Task**: Write tests
  - **Unit tests**: Entity tests
  - **Integration tests**: API tests
  - **Time**: 5 hours

### Frontend Tasks

#### 8.7 Components

- [ ] **Task**: Create `TalentPoolPage`
  - **File**: `client-vite/src/pages/company/TalentPoolPage.tsx`
  - **Features**: List, search, filter, add/remove candidates
  - **Time**: 8 hours

- [ ] **Task**: Create `TalentPoolCard` component
  - **File**: `client-vite/src/components/company/talentPool/TalentPoolCard.tsx`
  - **Time**: 4 hours

#### 8.8 Testing

- [ ] **Task**: Write component tests
  - **Time**: 3 hours

---

## Phase 9: Analytics and Reporting

**Goal**: Implement analytics for workflow performance.

**Estimated Time**: 1.5 weeks
**Dependencies**: Phase 5
**Priority**: LOW

### Backend Tasks

#### 9.1 Application Layer - Analytics Queries

- [ ] **Task**: Create `GetWorkflowAnalyticsQuery` and handler
  - **File**: `src/workflow/application/queries/get_workflow_analytics_query.py`
  - **Returns**:
    - Average time in each stage
    - Conversion rate per stage
    - Total applications
    - Active/Completed/Rejected counts
  - **Time**: 8 hours

- [ ] **Task**: Create `GetStageBottlenecksQuery` and handler
  - **File**: `src/workflow/application/queries/get_stage_bottlenecks_query.py`
  - **Details**: Return stages taking longest on average
  - **Time**: 4 hours

- [ ] **Task**: Create `GetCostPerHireQuery` and handler
  - **File**: `src/workflow/application/queries/get_cost_per_hire_query.py`
  - **Details**: Sum estimated_cost of all stages for hired candidates
  - **Time**: 4 hours

#### 9.2 Presentation Layer

- [ ] **Task**: Create `WorkflowAnalyticsController`
  - **File**: `src/workflow/presentation/controllers/workflow_analytics_controller.py`
  - **Methods**: get_workflow_analytics, get_bottlenecks, get_cost_analysis
  - **Time**: 4 hours

- [ ] **Task**: Create analytics router
  - **File**: `src/workflow/presentation/routers/workflow_analytics_router.py`
  - **Endpoints**:
    - GET /api/workflows/{workflow_id}/analytics
    - GET /api/workflows/{workflow_id}/bottlenecks
    - GET /api/workflows/{workflow_id}/cost-analysis
    - GET /api/positions/{position_id}/hiring-metrics
  - **Time**: 3 hours

#### 9.3 Testing

- [ ] **Task**: Write integration tests with real data
  - **File**: `tests/integration/workflow/test_workflow_analytics.py`
  - **Time**: 5 hours

### Frontend Tasks

#### 9.4 Components

- [ ] **Task**: Create `WorkflowAnalyticsPage`
  - **File**: `client-vite/src/pages/company/WorkflowAnalyticsPage.tsx`
  - **Features**:
    - Metrics cards (total applications, avg time, conversion rate)
    - Stage conversion funnel chart
    - Time-in-stage bar chart
    - Cost per hire line chart
    - Bottleneck table
    - Date range picker
    - Export to CSV/PDF button
  - **Time**: 12 hours

- [ ] **Task**: Integrate charting library
  - **Library**: recharts or Chart.js
  - **Time**: 4 hours

#### 9.5 Testing

- [ ] **Task**: Write component tests
  - **Time**: 3 hours

---

## Summary and Timeline

### Phase Summary

| Phase | Name | Time | Priority | Dependencies |
|-------|------|------|----------|--------------|
| 1 | Custom Fields System | 2 weeks | HIGH | None |
| 2 | Field Validation System | 2 weeks | HIGH | Phase 1 |
| 3 | Position-Workflow Integration | 1 week | HIGH | Phase 1, 2 |
| 4 | Stage Assignments | 1.5 weeks | HIGH | Phase 3 |
| 5 | Application Processing | 2 weeks | HIGH | Phase 2, 4 |
| 6 | Task Management | 2 weeks | MEDIUM | Phase 5 |
| 7 | Email Integration | 1.5 weeks | MEDIUM | Phase 5 |
| 8 | Talent Pool | 1 week | LOW | None |
| 9 | Analytics | 1.5 weeks | LOW | Phase 5 |

### Total Estimated Time

- **Sequential (all high priority)**: 8.5 weeks
- **With parallelization**: 10-12 weeks (including medium/low priority phases)

### Recommended Implementation Order

**Sprint 1-2 (2 weeks)**: Phase 1 - Custom Fields System
**Sprint 3-4 (2 weeks)**: Phase 2 - Field Validation System
**Sprint 5 (1 week)**: Phase 3 - Position-Workflow Integration
**Sprint 6-7 (1.5 weeks)**: Phase 4 - Stage Assignments
**Sprint 8-9 (2 weeks)**: Phase 5 - Application Processing
**Sprint 10-11 (2 weeks)**: Phase 6 - Task Management (parallel with Phase 8)
**Sprint 12-13 (1.5 weeks)**: Phase 7 - Email Integration
**Sprint 14 (1 week)**: Phase 8 - Talent Pool
**Sprint 15-16 (1.5 weeks)**: Phase 9 - Analytics

---

## Development Guidelines

### Code Quality Standards

- [ ] All code must follow Clean Architecture principles
- [ ] All public methods must have docstrings
- [ ] All entities must have factory methods
- [ ] All commands must return void
- [ ] All queries must return DTOs
- [ ] All controllers must use mappers
- [ ] No business logic in controllers
- [ ] No database access in domain layer

### Testing Requirements

- [ ] Minimum 80% code coverage
- [ ] All entities must have unit tests
- [ ] All commands/queries must have integration tests
- [ ] Critical user flows must have E2E tests

### Documentation Requirements

- [ ] Update API documentation (OpenAPI/Swagger)
- [ ] Update README with new features
- [ ] Create user guide for new features
- [ ] Update architecture diagrams

### Performance Considerations

- [ ] Add database indexes for new queries
- [ ] Implement caching for frequently accessed data
- [ ] Optimize N+1 query problems
- [ ] Load test critical endpoints

---

## Risk Management

### Technical Risks

1. **Database Performance**: Large number of validation rules may slow down stage transitions
   - **Mitigation**: Implement caching, optimize queries, add indexes

2. **Complex Validation Logic**: Field comparisons with nested position fields
   - **Mitigation**: Extensive testing, clear error messages

3. **Frontend State Management**: Complex forms with dynamic fields
   - **Mitigation**: Use form library (React Hook Form), break into smaller components

### Business Risks

1. **User Adoption**: Complex validation rules may confuse users
   - **Mitigation**: Clear UI, helpful tooltips, examples, documentation

2. **Migration**: Existing workflows need to be migrated
   - **Mitigation**: Provide default workflows, migration scripts, support

---

## Success Criteria

### Phase 1
- [ ] Can create custom fields for workflows
- [ ] Can configure field visibility per stage
- [ ] All field types work correctly

### Phase 2
- [ ] Can create validation rules that compare with position fields
- [ ] Validations block stage transitions correctly
- [ ] Warnings allow proceeding with confirmation
- [ ] Auto-reject works for error validations

### Phase 3
- [ ] Positions can select workflows
- [ ] Default workflow is used if not specified
- [ ] Workflow assignment is saved correctly

### Phase 4
- [ ] Can assign users to stages
- [ ] Default assignments are copied from workflow
- [ ] Multiple users can be assigned to same stage

### Phase 5
- [ ] Permission checks block unauthorized stage changes
- [ ] Validation errors prevent stage transitions
- [ ] Stage deadlines are calculated correctly
- [ ] Application history is tracked

### Phase 6
- [ ] Users see their assigned tasks
- [ ] Task priority calculation works correctly
- [ ] Users can claim/unclaim tasks
- [ ] Task filters work correctly

### Phase 7
- [ ] Email templates can be created/edited
- [ ] Emails are sent on stage transitions
- [ ] Variable substitution works correctly

### Phase 8
- [ ] Candidates can be added to talent pool
- [ ] Talent pool can be searched/filtered

### Phase 9
- [ ] Analytics show correct metrics
- [ ] Charts render correctly
- [ ] Export functionality works

---

## Appendix: Useful Commands

### Backend

```bash
# Create new migration
make revision m="migration_message"

# Run migrations
make migrate

# Run tests
make test

# Run specific test
pytest tests/unit/workflow_custom_field/test_custom_field.py

# Type checking
make mypy

# Linting
make flake8
```

### Frontend

```bash
# Run dev server
npm run dev

# Run tests
npm test

# Run specific test
npm test CustomFieldEditor

# Build
npm run build

# Type checking
npm run type-check
```

---

**Document End**
