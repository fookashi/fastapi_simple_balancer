import pytest
from application.actions.url_transform import create_target_url
from domain.entity.config import CDNConfig


@pytest.mark.parametrize(
    "origin_url,cdn_host,distribution_rate,expected",
    [
        (
            "http://s1.origin-cluster/video/1488/abc.m3u8",
            "cdn1.example.com",
            10,
            "http://cdn1.example.com/s1/video/1488/abc.m3u8",
        ),
        (
            "http://s42.origin-cluster/video/999/xyz.m3u8",
            "cdn42.example.com",
            5,
            "http://cdn42.example.com/s42/video/999/xyz.m3u8",
        ),
    ],
)
def test_create_target_url(origin_url, cdn_host, distribution_rate, expected):
    config = CDNConfig(id=1, cdn_host=cdn_host, distribution_rate=distribution_rate)
    result = create_target_url(origin_url, config)
    assert result == expected


def test_create_target_url_invalid():
    config = CDNConfig(id=1, cdn_host="cdn.example.com", distribution_rate=1)
    with pytest.raises(ValueError):
        create_target_url("not_a_url", config)
