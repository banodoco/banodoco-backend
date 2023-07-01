from util.extended_enum import ExtendedEnum


class PaymentOrderStatus(ExtendedEnum):
    COMPLETED = 'completed'
    PENDING = 'pending'
    FAILED = 'failed'
    TIMEOUT = 'timeout'

PAYMENT_ORDER_IDENTIFIER_LENGTH  = 6