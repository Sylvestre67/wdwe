from celery.decorators import task
from celery.utils.log import get_task_logger

from main.utils import update_yp_op_information,send_pusher_event
import models

logger = get_task_logger(__name__)

@task(name="update_yp_op_information")
def task_update_yp_op_information(location_id):
    """
    Make an API call to Yelp and THEN to OpenTable to retrieve/update location information.
    """
    logger.info("Updating information")
    return update_yp_op_information(location_id)

@task(name="task_send_pusher_event")
def task_send_pusher_event(media):
    """
    Send a PUSHER event.
    """
    logger.info("Send PusherEvent")
    return send_pusher_event(media)