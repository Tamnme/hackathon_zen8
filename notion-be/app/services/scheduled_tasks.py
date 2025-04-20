from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import requests
from flask import current_app
from app.models import db
from app.models.app_setting import AppSetting
import re

scheduler = BackgroundScheduler()

def get_cron_expression(schedule_period):
    """Convert schedule period to cron expression"""
    if schedule_period == "daily":
        return "0 0 * * *"  # Run at midnight every day
    elif schedule_period == "weekly":
        return "0 0 * * 0"  # Run at midnight on Sunday
    elif schedule_period == "monthly":
        return "0 0 1 * *"  # Run at midnight on the first day of each month
    else:
        # Check for hourly interval pattern (e.g., "2h" or "3h")
        match = re.match(r'^(\d+)h$', schedule_period)
        if match:
            hours = int(match.group(1))
            if hours > 0:
                return f"0 */{hours} * * *"  # Run every X hours
        return None

def trigger_summary_for_user(email):
    """Trigger summary for a specific user"""
    try:
        # Get app settings for the user
        app_setting = AppSetting.query.get(email)
        if not app_setting:
            current_app.logger.error(f"No app settings found for email: {email}")
            return

        # Get the latest summary's start time
        latest_response = requests.get(
            f"{current_app.config['BASE_URL']}/api/summary/latest",
            params={"email": email}
        )
        
        start_time = None
        if latest_response.status_code == 200:
            latest_data = latest_response.json()
            start_time = latest_data.get('start_time')
            current_app.logger.info(f"Found latest summary start time for {email}: {start_time}")
        else:
            current_app.logger.warning(f"No previous summary found for {email}")

        # Make request to trigger summary API with start_time
        trigger_data = {"email": email}
        if start_time:
            trigger_data["start_time"] = start_time

        response = requests.post(
            f"{current_app.config['BASE_URL']}/summary/trigger",
            json=trigger_data
        )
        
        if response.status_code != 202:
            current_app.logger.error(f"Failed to trigger summary for {email}: {response.text}")
    except Exception as e:
        current_app.logger.error(f"Error triggering summary for {email}: {str(e)}")

def schedule_summary_tasks():
    """Schedule summary tasks for all users based on their schedule period"""
    # Clear existing jobs
    scheduler.remove_all_jobs()
    
    # Get all app settings
    app_settings = AppSetting.query.all()
    
    for setting in app_settings:
        if not setting.schedule_period:
            continue
            
        cron_expression = get_cron_expression(setting.schedule_period)
        if not cron_expression:
            current_app.logger.warning(f"Invalid schedule period for {setting.email}: {setting.schedule_period}")
            continue
            
        # Add job to scheduler
        scheduler.add_job(
            trigger_summary_for_user,
            CronTrigger.from_crontab(cron_expression),
            args=[setting.email],
            id=f"summary_{setting.email}",
            replace_existing=True
        )
    
    if not scheduler.running:
        scheduler.start()

def init_scheduler(app):
    """Initialize the scheduler with the Flask app"""
    scheduler.init_app(app)
    schedule_summary_tasks() 