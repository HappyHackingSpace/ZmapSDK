from zmapsdk.schemas import ScanRequest


def test_minimal_valid_request():
    """Test that minimal valid request works"""
    request = ScanRequest()
    assert request.target_port is None
    assert request.return_results is False


def test_full_valid_request():
    """Test all fields with valid values"""
    request = ScanRequest(
        target_port=80,
        subnets=["192.168.1.0/24", "10.0.0.0/8"],
        output_file="/path/to/output.json",
        blocklist_file="/path/to/blocklist.txt",
        allowlist_file="/path/to/allowlist.txt",
        bandwidth="10Mbps",
        probe_module="tcp_syn",
        rate=1000,
        seed=42,
        verbosity=2,
        return_results=True,
    )
    assert request.target_port == 80
    assert request.subnets == ["192.168.1.0/24", "10.0.0.0/8"]
    assert request.return_results is True
