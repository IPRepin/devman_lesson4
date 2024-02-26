import logging
import os

import vk_api as vk
from dotenv import load_dotenv
from vk_api.exceptions import VkApiError
from vk_api.longpoll import VkLongPoll

logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    vk_session = vk.VkApi(token=os.getenv("VK_TOKEN"))
    try:
        vk_session.get_api()
        VkLongPoll(vk_session)
        logger.info("VK bot started")
    except VkApiError as vk_err:
        logger.error(vk_err)


if __name__ == "__main__":
    main()
