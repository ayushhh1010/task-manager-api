import logging
import resend
from app.celery_app import celery
from app.core.config import settings

logger = logging.getLogger(__name__)

resend.api_key = settings.RESEND_API_KEY

@celery.task(name="send_task_created_notification")
def send_task_created_notification(task_id: str, task_title: str, user_email: str):
    try:
        params = {
            "from": "Task Manager<onboarding@resend.dev>",
            "to": [user_email],
            "subject": f"Task Created: {task_title}",
            "html" : f"""
                <h2>Task Created Successfully</h2>
                <p>Your task <strong>{task_title}</strong> has been created.</p>
                <p>Task ID: {task_id}</p>
                <p>You can now track your task in the Task Manager</p>
            """
        }
        response = resend.Emails.send(params)
        logger.info(f"Email sent successfully to {user_email}, ID: {response['id']}")
        return {"status": "email_sent", "task_id": task_id, "email_id": response["id"]}
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return {"status": "email_failed", "error": str(e)}
    