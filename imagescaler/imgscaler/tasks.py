from celery.task.schedules import crontab
from celery.decorators import periodic_task
from imgscaler.services import ImageService
from celery.utils.log import get_task_logger
from datetime import datetime
 
logger = get_task_logger(__name__)
 
# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scale_task_regular():
    logger.info("Start task")
    now = datetime.now()
    result = ImageService.scale_task()
    logger.info("Task finished: "+str(result))