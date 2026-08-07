"""
Scheduler service for SmartReco.
"""

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def refresh_recommendations():
    """
    Refresh recommendations for all users.
    """

    print("Refreshing recommendations...")


scheduler.add_job(
    refresh_recommendations,
    "interval",
    hours=24,
    id="refresh_recommendations",
)


def start_scheduler():
    """
    Start the background scheduler.
    """

    scheduler.start()