try:
    from .web3_client import YondemBlockchainClient
    __all__ = ["YondemBlockchainClient"]
except ImportError:
    # web3 not installed – blockchain features unavailable
    __all__ = []
