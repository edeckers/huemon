from huemon.api.api import Api
from huemon.api.cached_api import CachedApi
from huemon.const import DEFAULT_MAX_CACHE_AGE_SECONDS


def create_hue_hub_url(config: dict):
    return f"http://{config['ip']}/api/{config['key']}"


def create_api(config: dict):
    enable_cache = (
        "cache" in config
        and "enable" in config["cache"]
        and bool(config["cache"]["enable"])
    )

    is_cache_age_configured = "cache" in config and "max_age_seconds" in config["cache"]

    max_cache_age_seconds = (
        int(config["cache"]["max_age_seconds"])
        if is_cache_age_configured
        else DEFAULT_MAX_CACHE_AGE_SECONDS
    )

    api = Api(create_hue_hub_url(config))

    return CachedApi(api, max_cache_age_seconds) if enable_cache else api
