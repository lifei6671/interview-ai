import logging
from .config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format=format("%(asctime)s - %(levelname)s [%(name)s] - %(message)s"),
)

logger = logging.getLogger("jd-interview-gen")