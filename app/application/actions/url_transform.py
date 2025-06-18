import re

from domain.entity.config import CDNConfig
from application.exceptions.action import InvalidUrlError

URL_PATTERN = r"^http://(?P<cluster_id>s\d+)\.[^/]+/(?P<location>.+)$"


def create_target_url(origin_url: str, cdn_config: CDNConfig) -> str:
    parsed_regex = re.match(URL_PATTERN, str(origin_url))
    if parsed_regex:
        cluster_id = parsed_regex.group("cluster_id")
        location = parsed_regex.group("location")
        return f"http://{cdn_config.cdn_host}/{cluster_id}/{location}"
    raise InvalidUrlError("Неверный формат URL")
