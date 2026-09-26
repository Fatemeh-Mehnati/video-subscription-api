from django.conf import settings


class MockGateway:
    """Fake payment gateway for development."""

    def request_payment(self, payment):
        return f"{settings.MOCK_GATEWAY_URL}?authority={payment.authority}"

    def verify_payment(self, payment):
        return True, f"REF-{payment.authority[:8]}"


def get_gateway():
    return MockGateway()