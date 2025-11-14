#!/usr/bin/env python3
"""
Setup script for feature flags in AI Resume Enhancement Platform.
Creates initial feature flags for gradual rollout of new features.
"""

import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.framework.infrastructure.feature_flags.feature_flag_service import (
    FeatureFlagService, FeatureFlag, FeatureFlagType, TargetingRule
)


async def setup_initial_feature_flags():
    """Setup initial feature flags for the platform"""
    
    feature_flag_service = FeatureFlagService()
    await feature_flag_service.initialize()
    
    # Define initial feature flags
    initial_flags = [
        # AI Resume Enhancement Features
        FeatureFlag(
            name="ai_resume_enhancement",
            description="Enable AI-powered resume enhancement features",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=True,
            rollout_percentage=100.0
        ),
        
        FeatureFlag(
            name="ai_interview_v2",
            description="New conversational AI interview system",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=25.0  # Start with 25% rollout
        ),
        
        FeatureFlag(
            name="job_application_customization",
            description="AI-powered job application customization",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=50.0,
            targeting_rules={
                TargetingRule.SUBSCRIPTION_TIER.value: ["PREMIUM", "STANDARD"]
            }
        ),
        
        # Premium Features
        FeatureFlag(
            name="unlimited_downloads",
            description="Unlimited resume downloads for premium users",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=100.0,
            targeting_rules={
                TargetingRule.SUBSCRIPTION_TIER.value: ["PREMIUM"]
            }
        ),
        
        FeatureFlag(
            name="advanced_analytics",
            description="Advanced analytics dashboard",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=10.0,  # Beta feature
            targeting_rules={
                TargetingRule.SUBSCRIPTION_TIER.value: ["PREMIUM"]
            }
        ),
        
        # UI/UX Experiments
        FeatureFlag(
            name="new_dashboard_layout",
            description="New dashboard layout experiment",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=20.0
        ),
        
        FeatureFlag(
            name="mobile_app_promotion",
            description="Show mobile app promotion banner",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=30.0
        ),
        
        # Performance Features
        FeatureFlag(
            name="redis_caching",
            description="Enable Redis caching for improved performance",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=True,
            rollout_percentage=100.0
        ),
        
        FeatureFlag(
            name="async_pdf_processing",
            description="Process PDF uploads asynchronously",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=75.0
        ),
        
        # AI Service Configuration
        FeatureFlag(
            name="ai_service_timeout",
            description="Timeout for AI service requests in seconds",
            flag_type=FeatureFlagType.JSON,
            enabled=True,
            default_value={"timeout": 30, "retry_count": 3},
            rollout_percentage=100.0
        ),
        
        FeatureFlag(
            name="ai_model_version",
            description="AI model version to use",
            flag_type=FeatureFlagType.STRING,
            enabled=True,
            default_value="grok-beta",
            rollout_percentage=100.0
        ),
        
        # Security Features
        FeatureFlag(
            name="enhanced_security_validation",
            description="Enhanced security validation for uploads",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=50.0
        ),
        
        FeatureFlag(
            name="rate_limiting_strict",
            description="Strict rate limiting for API endpoints",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=25.0
        ),
        
        # Internationalization
        FeatureFlag(
            name="multi_language_support",
            description="Enable multi-language support",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=40.0
        ),
        
        FeatureFlag(
            name="rtl_language_support",
            description="Right-to-left language support",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=20.0
        ),
        
        # Experimental Features
        FeatureFlag(
            name="ai_cover_letter_generation",
            description="AI-powered cover letter generation",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=15.0,
            targeting_rules={
                TargetingRule.SUBSCRIPTION_TIER.value: ["PREMIUM"]
            }
        ),
        
        FeatureFlag(
            name="video_interview_practice",
            description="Video interview practice feature",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=False,  # Not ready yet
            default_value=False,
            rollout_percentage=0.0
        ),
        
        # A/B Testing Experiments
        FeatureFlag(
            name="experiment_onboarding_flow",
            description="A/B test for onboarding flow",
            flag_type=FeatureFlagType.JSON,
            enabled=True,
            default_value={
                "variants": {
                    "control": 50,
                    "simplified": 30,
                    "guided": 20
                }
            },
            rollout_percentage=100.0
        ),
        
        FeatureFlag(
            name="experiment_pricing_display",
            description="A/B test for pricing page display",
            flag_type=FeatureFlagType.JSON,
            enabled=True,
            default_value={
                "variants": {
                    "control": 60,
                    "annual_focus": 40
                }
            },
            rollout_percentage=100.0
        ),
        
        # Maintenance and Operations
        FeatureFlag(
            name="maintenance_mode",
            description="Enable maintenance mode",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=False,
            default_value=False,
            rollout_percentage=0.0
        ),
        
        FeatureFlag(
            name="debug_logging",
            description="Enable debug logging",
            flag_type=FeatureFlagType.BOOLEAN,
            enabled=True,
            default_value=False,
            rollout_percentage=5.0,  # Only for small percentage of users
            targeting_rules={
                TargetingRule.EMAIL_DOMAIN.value: ["company.com", "test.com"]
            }
        )
    ]
    
    # Create all feature flags
    created_count = 0
    for flag in initial_flags:
        try:
            success = await feature_flag_service.create_flag(flag)
            if success:
                created_count += 1
                print(f"✅ Created feature flag: {flag.name}")
            else:
                print(f"❌ Failed to create feature flag: {flag.name}")
        except Exception as e:
            print(f"❌ Error creating feature flag {flag.name}: {e}")
    
    print(f"\n🎉 Successfully created {created_count}/{len(initial_flags)} feature flags")
    
    await feature_flag_service.close()


async def update_rollout_percentages():
    """Update rollout percentages for gradual feature rollout"""
    
    feature_flag_service = FeatureFlagService()
    await feature_flag_service.initialize()
    
    # Define rollout schedule (this could be automated based on metrics)
    rollout_updates = {
        "ai_interview_v2": 50.0,  # Increase from 25% to 50%
        "job_application_customization": 75.0,  # Increase from 50% to 75%
        "new_dashboard_layout": 40.0,  # Increase from 20% to 40%
        "async_pdf_processing": 90.0,  # Increase from 75% to 90%
    }
    
    for flag_name, new_percentage in rollout_updates.items():
        try:
            success = await feature_flag_service.update_flag(
                flag_name,
                {"rollout_percentage": new_percentage}
            )
            if success:
                print(f"✅ Updated {flag_name} rollout to {new_percentage}%")
            else:
                print(f"❌ Failed to update {flag_name}")
        except Exception as e:
            print(f"❌ Error updating {flag_name}: {e}")
    
    await feature_flag_service.close()


async def emergency_disable_feature(flag_name: str):
    """Emergency disable a feature flag"""
    
    feature_flag_service = FeatureFlagService()
    await feature_flag_service.initialize()
    
    try:
        success = await feature_flag_service.update_flag(
            flag_name,
            {"enabled": False, "rollout_percentage": 0.0}
        )
        if success:
            print(f"🚨 Emergency disabled feature flag: {flag_name}")
        else:
            print(f"❌ Failed to disable feature flag: {flag_name}")
    except Exception as e:
        print(f"❌ Error disabling feature flag {flag_name}: {e}")
    
    await feature_flag_service.close()


async def list_all_flags():
    """List all feature flags and their current status"""
    
    feature_flag_service = FeatureFlagService()
    await feature_flag_service.initialize()
    
    try:
        flags = await feature_flag_service.get_all_flags()
        
        print("\n📋 Current Feature Flags:")
        print("-" * 80)
        
        for flag in sorted(flags, key=lambda f: f.name):
            status = "🟢 ENABLED" if flag.enabled else "🔴 DISABLED"
            rollout = f"{flag.rollout_percentage}%" if flag.rollout_percentage > 0 else "0%"
            
            print(f"{flag.name:<30} {status:<12} {rollout:<8} {flag.description}")
        
        print(f"\nTotal flags: {len(flags)}")
        
    except Exception as e:
        print(f"❌ Error listing feature flags: {e}")
    
    await feature_flag_service.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Feature Flag Management")
    parser.add_argument("action", choices=["setup", "update", "disable", "list"], 
                       help="Action to perform")
    parser.add_argument("--flag", help="Flag name for disable action")
    
    args = parser.parse_args()
    
    if args.action == "setup":
        asyncio.run(setup_initial_feature_flags())
    elif args.action == "update":
        asyncio.run(update_rollout_percentages())
    elif args.action == "disable":
        if not args.flag:
            print("❌ --flag parameter required for disable action")
            sys.exit(1)
        asyncio.run(emergency_disable_feature(args.flag))
    elif args.action == "list":
        asyncio.run(list_all_flags())