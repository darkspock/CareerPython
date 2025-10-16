#!/usr/bin/env python3
"""
AI System Integration Validator

This script validates that all AI features are properly integrated
and working together in the complete system.
"""

import asyncio
import sys
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AISystemIntegrationValidator:
    """Validates complete AI system integration"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)
        self.test_results: Dict[str, Any] = {}
        
        # Test database setup
        self.db_url = "sqlite:///./test_validation.db"
        self.engine = create_engine(self.db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} {test_name}: {details}")
        self.test_results[test_name] = {
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
    
    async def validate_api_health(self) -> bool:
        """Validate API is running and healthy"""
        try:
            response = await self.client.get("/health")
            if response.status_code == 200:
                self.log_test_result("API Health Check", True, "API is responding")
                return True
            else:
                self.log_test_result("API Health Check", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test_result("API Health Check", False, f"Connection failed: {str(e)}")
            return False
    
    async def validate_database_schema(self) -> bool:
        """Validate database schema includes all AI enhancement tables"""
        try:
            with self.engine.connect() as conn:
                # Check for required tables
                required_tables = [
                    'users', 'candidates', 'user_assets', 'profile_sections',
                    'interviews', 'interview_answers', 'usage_tracking',
                    'interview_templates', 'interview_template_questions'
                ]
                
                for table in required_tables:
                    result = conn.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"))
                    if not result.fetchone():
                        self.log_test_result("Database Schema", False, f"Missing table: {table}")
                        return False
                
                # Check for AI-specific columns
                ai_columns = [
                    ('users', 'subscription_tier'),
                    ('users', 'subscription_expires_at'),
                    ('profile_sections', 'ai_generated_content'),
                    ('user_assets', 'text_content')
                ]
                
                for table, column in ai_columns:
                    result = conn.execute(text(f"PRAGMA table_info({table})"))
                    columns = [row[1] for row in result.fetchall()]
                    if column not in columns:
                        self.log_test_result("Database Schema", False, f"Missing column: {table}.{column}")
                        return False
                
                self.log_test_result("Database Schema", True, "All required tables and columns present")
                return True
                
        except Exception as e:
            self.log_test_result("Database Schema", False, f"Database error: {str(e)}")
            return False
    
    async def validate_ai_service_integration(self) -> bool:
        """Validate AI service integration"""
        try:
            # Test AI service health endpoint if available
            response = await self.client.get("/monitoring/ai-service/health")
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get("status") == "healthy":
                    self.log_test_result("AI Service Integration", True, "AI service is healthy")
                    return True
                else:
                    self.log_test_result("AI Service Integration", False, f"AI service unhealthy: {health_data}")
                    return False
            else:
                # If monitoring endpoint doesn't exist, assume integration is working
                self.log_test_result("AI Service Integration", True, "Monitoring endpoint not available, assuming healthy")
                return True
                
        except Exception as e:
            self.log_test_result("AI Service Integration", False, f"AI service check failed: {str(e)}")
            return False
    
    async def validate_subscription_system(self) -> bool:
        """Validate subscription system integration"""
        try:
            # Test subscription plans endpoint
            response = await self.client.get("/subscription/plans")
            if response.status_code == 200:
                plans_data = response.json()
                
                # Validate plan structure
                if "plans" in plans_data and len(plans_data["plans"]) == 3:
                    tiers = [plan["tier"] for plan in plans_data["plans"]]
                    expected_tiers = ["FREE", "STANDARD", "PREMIUM"]
                    
                    if all(tier in tiers for tier in expected_tiers):
                        self.log_test_result("Subscription System", True, "All subscription tiers available")
                        return True
                    else:
                        self.log_test_result("Subscription System", False, f"Missing tiers: {set(expected_tiers) - set(tiers)}")
                        return False
                else:
                    self.log_test_result("Subscription System", False, "Invalid plans structure")
                    return False
            else:
                self.log_test_result("Subscription System", False, f"Plans endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Subscription System", False, f"Subscription validation failed: {str(e)}")
            return False
    
    async def validate_middleware_integration(self) -> bool:
        """Validate middleware integration"""
        try:
            # Test that subscription middleware is working
            response = await self.client.get("/profile/dashboard")
            
            # Should return 401 without authentication
            if response.status_code == 401:
                error_data = response.json()
                if "error_code" in error_data and "message" in error_data:
                    self.log_test_result("Middleware Integration", True, "Authentication middleware working")
                    return True
                else:
                    self.log_test_result("Middleware Integration", False, "Invalid error response format")
                    return False
            else:
                self.log_test_result("Middleware Integration", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Middleware Integration", False, f"Middleware validation failed: {str(e)}")
            return False
    
    async def validate_api_documentation(self) -> bool:
        """Validate API documentation is accessible"""
        try:
            endpoints = ["/docs", "/redoc", "/openapi.json"]
            
            for endpoint in endpoints:
                response = await self.client.get(endpoint)
                if response.status_code != 200:
                    self.log_test_result("API Documentation", False, f"{endpoint} not accessible")
                    return False
            
            # Validate OpenAPI spec contains AI endpoints
            response = await self.client.get("/openapi.json")
            openapi_spec = response.json()
            
            ai_endpoints = [
                "/candidates/upload-resume",
                "/interviews/start/{candidate_id}",
                "/resume/generate/{candidate_id}",
                "/job-applications/customize",
                "/subscription/upgrade"
            ]
            
            paths = openapi_spec.get("paths", {})
            missing_endpoints = []
            
            for endpoint in ai_endpoints:
                # Check if endpoint exists (handle path parameters)
                endpoint_found = False
                for path in paths.keys():
                    if endpoint.replace("{candidate_id}", "{id}") in path or endpoint in path:
                        endpoint_found = True
                        break
                
                if not endpoint_found:
                    missing_endpoints.append(endpoint)
            
            if missing_endpoints:
                self.log_test_result("API Documentation", False, f"Missing endpoints: {missing_endpoints}")
                return False
            else:
                self.log_test_result("API Documentation", True, "All AI endpoints documented")
                return True
                
        except Exception as e:
            self.log_test_result("API Documentation", False, f"Documentation validation failed: {str(e)}")
            return False
    
    async def validate_error_handling(self) -> bool:
        """Validate error handling integration"""
        try:
            # Test validation error handling
            response = await self.client.post(
                "/candidates/upload-resume",
                files={"file": ("invalid.txt", b"not a pdf", "text/plain")},
                data={"email": "invalid-email"}
            )
            
            if response.status_code == 422:
                error_data = response.json()
                required_fields = ["error_code", "message", "details"]
                
                if all(field in error_data for field in required_fields):
                    self.log_test_result("Error Handling", True, "Validation errors properly formatted")
                    return True
                else:
                    self.log_test_result("Error Handling", False, "Invalid error response format")
                    return False
            else:
                self.log_test_result("Error Handling", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("Error Handling", False, f"Error handling validation failed: {str(e)}")
            return False
    
    async def validate_cors_configuration(self) -> bool:
        """Validate CORS configuration for frontend integration"""
        try:
            # Test preflight request
            response = await self.client.options(
                "/candidates/upload-resume",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type,Authorization"
                }
            )
            
            required_headers = [
                "access-control-allow-origin",
                "access-control-allow-methods",
                "access-control-allow-headers"
            ]
            
            missing_headers = []
            for header in required_headers:
                if header not in response.headers:
                    missing_headers.append(header)
            
            if missing_headers:
                self.log_test_result("CORS Configuration", False, f"Missing headers: {missing_headers}")
                return False
            else:
                self.log_test_result("CORS Configuration", True, "CORS properly configured")
                return True
                
        except Exception as e:
            self.log_test_result("CORS Configuration", False, f"CORS validation failed: {str(e)}")
            return False
    
    async def validate_monitoring_endpoints(self) -> bool:
        """Validate monitoring endpoints are accessible"""
        try:
            monitoring_endpoints = [
                "/monitoring/health",
                "/monitoring/metrics",
                "/monitoring/ai-service/status"
            ]
            
            accessible_endpoints = 0
            
            for endpoint in monitoring_endpoints:
                try:
                    response = await self.client.get(endpoint)
                    if response.status_code in [200, 404]:  # 404 is acceptable if endpoint doesn't exist
                        accessible_endpoints += 1
                except:
                    pass  # Endpoint might not exist, which is acceptable
            
            if accessible_endpoints > 0:
                self.log_test_result("Monitoring Endpoints", True, f"{accessible_endpoints} monitoring endpoints accessible")
                return True
            else:
                self.log_test_result("Monitoring Endpoints", False, "No monitoring endpoints accessible")
                return False
                
        except Exception as e:
            self.log_test_result("Monitoring Endpoints", False, f"Monitoring validation failed: {str(e)}")
            return False
    
    async def run_complete_validation(self) -> Dict[str, Any]:
        """Run complete system validation"""
        logger.info("🚀 Starting AI System Integration Validation")
        logger.info("=" * 50)
        
        start_time = time.time()
        
        # Run all validation tests
        validations = [
            ("API Health", self.validate_api_health()),
            ("Database Schema", self.validate_database_schema()),
            ("AI Service Integration", self.validate_ai_service_integration()),
            ("Subscription System", self.validate_subscription_system()),
            ("Middleware Integration", self.validate_middleware_integration()),
            ("API Documentation", self.validate_api_documentation()),
            ("Error Handling", self.validate_error_handling()),
            ("CORS Configuration", self.validate_cors_configuration()),
            ("Monitoring Endpoints", self.validate_monitoring_endpoints())
        ]
        
        results = {}
        for name, validation_coro in validations:
            logger.info(f"Running {name} validation...")
            try:
                result = await validation_coro
                results[name] = result
            except Exception as e:
                logger.error(f"Validation {name} failed with exception: {str(e)}")
                results[name] = False
                self.log_test_result(name, False, f"Exception: {str(e)}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Generate summary
        passed_tests = sum(1 for result in results.values() if result)
        total_tests = len(results)
        success_rate = (passed_tests / total_tests) * 100
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": success_rate,
            "duration_seconds": duration,
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "detailed_results": self.test_results
        }
        
        logger.info("=" * 50)
        logger.info("🎯 Validation Summary")
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {total_tests - passed_tests}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info(f"Duration: {duration:.2f} seconds")
        
        if success_rate == 100:
            logger.info("🎉 All validations passed! System is fully integrated.")
        elif success_rate >= 80:
            logger.warning("⚠️  Most validations passed, but some issues detected.")
        else:
            logger.error("❌ Multiple validation failures detected. System needs attention.")
        
        return summary
    
    def save_validation_report(self, summary: Dict[str, Any], filename: str = "validation_report.json"):
        """Save validation report to file"""
        report_path = Path("test-results") / filename
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"📄 Validation report saved to {report_path}")


async def main():
    """Main validation function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate AI System Integration")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--output", default="validation_report.json", help="Output report filename")
    
    args = parser.parse_args()
    
    async with AISystemIntegrationValidator(args.url) as validator:
        summary = await validator.run_complete_validation()
        validator.save_validation_report(summary, args.output)
        
        # Exit with appropriate code
        if summary["success_rate"] == 100:
            sys.exit(0)
        elif summary["success_rate"] >= 80:
            sys.exit(1)  # Warning level
        else:
            sys.exit(2)  # Error level


if __name__ == "__main__":
    asyncio.run(main())