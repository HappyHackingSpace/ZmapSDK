import pytest

from zmapsdk import ZMapScanConfig, ZMapConfigError


def test_config() -> None:
    """Test config."""
    conf = ZMapScanConfig(
        target_port=80,
        bandwidth=None,
        rate=50,
        max_targets=10,
        min_hitrate=10,
        vpn=False
    )
    assert conf.target_port == 80
    assert conf.to_dict().get("rate") == 50

    with pytest.raises(ZMapConfigError) as exc_info:
        conf = ZMapScanConfig(source_port=-9999)
        assert f"Invalid source port range: {conf.source_port}. Must be between 0 and 65535." in str(exc_info.value)
