#!/usr/bin/env python3
"""
AI Monitoring CLI Tool

A command-line interface for monitoring AI services, performance, and usage.
"""

import asyncio
import json
import sys
import argparse
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Add project root to path
sys.path.append('.')

from src.shared.infrastructure.monitoring.monitoring_service import MonitoringService
from src.user.infrastructure.repositories.usage_tracking_repository import SQLAlchemyUsageTrackingRepository
from src.user.infrastructure.repositories.user import SQLAlchemyUserRepository
from src.shared.infrastructure.services.comprehensive_email_service import ComprehensiveEmailService
from src.shared.infrastructure.services.smtp_email_service import SMTPEmailService
from core.database import get_db


class MonitoringCLI:
    """Command-line interface for AI monitoring"""
    
    def __init__(self):
        self.monitoring_service = self._get_monitoring_service()
    
    def _get_monitoring_service(self) -> MonitoringService:
        """Get monitoring service instance"""
        db_session = next(get_db())
        usage_tracking_repo = SQLAlchemyUsageTrackingRepository(db_session)
        user_repo = SQLAlchemyUserRepository(db_session)
        smtp_service = SMTPEmailService()
        email_service = ComprehensiveEmailService(smtp_service)
        
        return MonitoringService(
            usage_tracking_repo=usage_tracking_repo,
            user_repo=user_repo,
            email_service=email_service
        )
    
    async def health_check(self, verbose: bool = False) -> Dict[str, Any]:
        """Perform AI service health check"""
        print("🔍 Checking AI service health...")
        
        try:
            result = await self.monitoring_service.perform_health_check()
            
            status = result['status']
            response_time = result.get('response_time_ms', 0)
            
            # Status emoji
            status_emoji = {
                'healthy': '✅',
                'degraded': '⚠️',
                'unhealthy': '❌',
                'error': '💥'
            }.get(status, '❓')
            
            print(f"{status_emoji} AI Service Status: {status.upper()}")
            print(f"⏱️  Response Time: {response_time:.1f}ms")
            
            if result.get('error_message'):
                print(f"❌ Error: {result['error_message']}")
            
            if verbose and result.get('metadata'):
                print("\n📋 Detailed Information:")
                for key, value in result['metadata'].items():
                    print(f"   {key}: {value}")
            
            return result
            
        except Exception as e:
            print(f"💥 Error performing health check: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def performance_metrics(self, hours: int = 24, verbose: bool = False) -> Dict[str, Any]:
        """Get AI service performance metrics"""
        print(f"📊 Getting performance metrics for last {hours} hours...")
        
        try:
            metrics = self.monitoring_service.get_performance_metrics(hours)
            
            total_calls = metrics.get('total_calls', 0)
            success_rate = metrics.get('overall_success_rate', 0)
            total_operations = metrics.get('total_operations', 0)
            
            print(f"📈 Performance Summary:")
            print(f"   Total Operations: {total_operations}")
            print(f"   Total Calls: {total_calls}")
            print(f"   Success Rate: {success_rate:.1f}%")
            
            # Show slowest and fastest operations
            slowest = metrics.get('slowest_operation')
            fastest = metrics.get('fastest_operation')
            
            if slowest:
                print(f"🐌 Slowest Operation: {slowest['name']} ({slowest['avg_duration_ms']:.1f}ms)")
            
            if fastest:
                print(f"🚀 Fastest Operation: {fastest['name']} ({fastest['avg_duration_ms']:.1f}ms)")
            
            # Show problematic operations
            problematic = metrics.get('problematic_operations', [])
            if problematic:
                print(f"\n⚠️  Problematic Operations ({len(problematic)}):")
                for op in problematic:
                    print(f"   - {op['operation']}: {op['success_rate']:.1f}% success")
            
            if verbose:
                print("\n📋 Detailed Operation Stats:")
                operations_stats = metrics.get('operations_stats', {})
                for op_name, stats in operations_stats.items():
                    print(f"\n   {op_name}:")
                    print(f"     Calls: {stats['total_calls']}")
                    print(f"     Success Rate: {stats['success_rate']:.1f}%")
                    print(f"     Avg Duration: {stats['avg_duration_ms']:.1f}ms")
                    print(f"     P95 Duration: {stats['p95_duration_ms']:.1f}ms")
            
            return metrics
            
        except Exception as e:
            print(f"💥 Error getting performance metrics: {e}")
            return {'error': str(e)}
    
    def usage_metrics(self, verbose: bool = False) -> Dict[str, Any]:
        """Get usage and subscription metrics"""
        print("👥 Getting usage metrics...")
        
        try:
            metrics = self.monitoring_service.get_usage_metrics()
            
            total_users = metrics.get('total_users', 0)
            users_exceeding = metrics.get('users_exceeding_limits', 0)
            revenue_impact = metrics.get('total_revenue_impact', 0)
            
            print(f"👥 Usage Summary:")
            print(f"   Total Users: {total_users}")
            print(f"   Users Exceeding Limits: {users_exceeding}")
            print(f"   Revenue Impact: €{revenue_impact:.2f}")
            
            # Show subscription breakdown
            subscription_stats = metrics.get('subscription_stats', {})
            if subscription_stats:
                print(f"\n💳 Subscription Breakdown:")
                for tier, stats in subscription_stats.items():
                    users = stats.get('total_users', 0)
                    active_today = stats.get('active_users_today', 0)
                    print(f"   {tier}: {users} users ({active_today} active today)")
            
            # Show recent alerts
            recent_alerts = metrics.get('recent_alerts_24h', 0)
            if recent_alerts > 0:
                print(f"\n🚨 Recent Alerts (24h): {recent_alerts}")
                
                alert_breakdown = metrics.get('alert_breakdown', {})
                for alert_type, count in alert_breakdown.items():
                    print(f"   {alert_type}: {count}")
            
            if verbose:
                print("\n📋 Detailed Subscription Stats:")
                for tier, stats in subscription_stats.items():
                    print(f"\n   {tier}:")
                    for key, value in stats.items():
                        if key != 'tier':
                            print(f"     {key}: {value}")
            
            return metrics
            
        except Exception as e:
            print(f"💥 Error getting usage metrics: {e}")
            return {'error': str(e)}
    
    def alerts(self, hours: int = 24, severity: Optional[str] = None) -> list:
        """Get system alerts"""
        severity_filter = f" (severity: {severity})" if severity else ""
        print(f"🚨 Getting alerts for last {hours} hours{severity_filter}...")
        
        try:
            alerts = self.monitoring_service.get_alerts(hours, severity)
            
            if not alerts:
                print("✅ No alerts found")
                return []
            
            print(f"🚨 Found {len(alerts)} alerts:")
            
            for alert in alerts:
                severity_emoji = {
                    'info': 'ℹ️',
                    'warning': '⚠️',
                    'critical': '🔥'
                }.get(alert.get('severity', 'info'), '❓')
                
                timestamp = alert.get('timestamp', '')
                if timestamp:
                    # Parse and format timestamp
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        time_str = timestamp
                else:
                    time_str = 'Unknown'
                
                print(f"\n{severity_emoji} {alert.get('title', 'Unknown Alert')}")
                print(f"   Severity: {alert.get('severity', 'unknown').upper()}")
                print(f"   Time: {time_str}")
                print(f"   Message: {alert.get('message', 'No message')}")
                print(f"   Source: {alert.get('source', 'unknown')}")
                
                if alert.get('resolved'):
                    print(f"   ✅ Resolved at: {alert.get('resolved_at', 'Unknown')}")
            
            return alerts
            
        except Exception as e:
            print(f"💥 Error getting alerts: {e}")
            return []
    
    async def comprehensive_status(self, verbose: bool = False) -> Dict[str, Any]:
        """Get comprehensive system status"""
        print("🔍 Getting comprehensive system status...")
        
        try:
            status = await self.monitoring_service.get_comprehensive_health_status()
            
            overall_health = status.get('overall_health', 'unknown')
            monitoring_active = status.get('monitoring_active', False)
            
            # Overall health emoji
            health_emoji = {
                'healthy': '✅',
                'warning': '⚠️',
                'degraded': '⚠️',
                'critical': '🔥',
                'unknown': '❓'
            }.get(overall_health, '❓')
            
            print(f"{health_emoji} Overall System Health: {overall_health.upper()}")
            print(f"🔄 Monitoring Active: {'Yes' if monitoring_active else 'No'}")
            
            components = status.get('components', {})
            
            # AI Service
            ai_service = components.get('ai_service', {})
            ai_status = ai_service.get('status', 'unknown')
            ai_response_time = ai_service.get('response_time_ms', 0)
            
            ai_emoji = {
                'healthy': '✅',
                'degraded': '⚠️',
                'unhealthy': '❌'
            }.get(ai_status, '❓')
            
            print(f"\n🤖 AI Service:")
            print(f"   {ai_emoji} Status: {ai_status.upper()}")
            print(f"   ⏱️  Response Time: {ai_response_time:.1f}ms")
            
            # Performance
            performance = components.get('performance', {})
            perf_summary = performance.get('summary', {})
            
            print(f"\n📊 Performance:")
            print(f"   Success Rate: {perf_summary.get('overall_success_rate', 0):.1f}%")
            print(f"   Total Calls: {perf_summary.get('total_calls', 0)}")
            
            # Usage
            usage = components.get('usage_monitoring', {})
            
            print(f"\n👥 Usage:")
            print(f"   Total Users: {usage.get('total_users', 0)}")
            print(f"   Users Exceeding Limits: {usage.get('users_exceeding_limits', 0)}")
            
            # Alerts
            alerting = components.get('alerting', {})
            
            print(f"\n🚨 Alerts:")
            print(f"   Active Alerts: {alerting.get('total_active_alerts', 0)}")
            
            critical_alerts = alerting.get('critical_alerts', [])
            if critical_alerts:
                print(f"   🔥 Critical Alerts: {len(critical_alerts)}")
                for alert in critical_alerts[:3]:  # Show first 3
                    print(f"      - {alert.get('title', 'Unknown')}")
            
            if verbose:
                print(f"\n📋 Detailed Status:")
                print(json.dumps(status, indent=2, default=str))
            
            return status
            
        except Exception as e:
            print(f"💥 Error getting comprehensive status: {e}")
            return {'error': str(e)}
    
    async def force_check(self) -> Dict[str, Any]:
        """Force immediate monitoring check"""
        print("🔄 Forcing immediate monitoring check...")
        
        try:
            result = await self.monitoring_service.force_monitoring_check()
            
            alerts_generated = result.get('alerts_generated', 0)
            status = result.get('status', 'unknown')
            
            print(f"✅ Monitoring check completed: {status}")
            print(f"🚨 Alerts generated: {alerts_generated}")
            
            if alerts_generated > 0:
                alerts = result.get('alerts', [])
                print(f"\n🚨 New Alerts:")
                for alert in alerts:
                    severity_emoji = {
                        'info': 'ℹ️',
                        'warning': '⚠️',
                        'critical': '🔥'
                    }.get(alert.get('severity', 'info'), '❓')
                    
                    print(f"   {severity_emoji} {alert.get('title', 'Unknown')}")
            
            return result
            
        except Exception as e:
            print(f"💥 Error forcing monitoring check: {e}")
            return {'error': str(e)}
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve a specific alert"""
        print(f"✅ Resolving alert: {alert_id}")
        
        try:
            success = self.monitoring_service.resolve_alert(alert_id)
            
            if success:
                print(f"✅ Alert {alert_id} resolved successfully")
            else:
                print(f"❌ Alert {alert_id} not found or already resolved")
            
            return success
            
        except Exception as e:
            print(f"💥 Error resolving alert: {e}")
            return False


async def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description='AI Monitoring CLI Tool')
    parser.add_argument('command', choices=[
        'health', 'performance', 'usage', 'alerts', 'status', 'check', 'resolve'
    ], help='Command to execute')
    
    parser.add_argument('--hours', type=int, default=24, 
                       help='Hours back to analyze (default: 24)')
    parser.add_argument('--severity', choices=['info', 'warning', 'critical'],
                       help='Filter alerts by severity')
    parser.add_argument('--alert-id', type=str,
                       help='Alert ID to resolve (for resolve command)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    cli = MonitoringCLI()
    
    try:
        if args.command == 'health':
            await cli.health_check(verbose=args.verbose)
        
        elif args.command == 'performance':
            cli.performance_metrics(hours=args.hours, verbose=args.verbose)
        
        elif args.command == 'usage':
            cli.usage_metrics(verbose=args.verbose)
        
        elif args.command == 'alerts':
            cli.alerts(hours=args.hours, severity=args.severity)
        
        elif args.command == 'status':
            await cli.comprehensive_status(verbose=args.verbose)
        
        elif args.command == 'check':
            await cli.force_check()
        
        elif args.command == 'resolve':
            if not args.alert_id:
                print("❌ Error: --alert-id is required for resolve command")
                sys.exit(1)
            cli.resolve_alert(args.alert_id)
        
    except KeyboardInterrupt:
        print("\n👋 Monitoring CLI interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())