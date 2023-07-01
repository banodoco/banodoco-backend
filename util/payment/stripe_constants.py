# LIVE DATA
from util.extended_enum import ExtendedEnum


USD_20_BANODOCO_CREDITS = "price_1NOhc2DZUd93qmea1x3C4782"
USD_10_BANODOCO_CREDITS = "price_1NOhc2DZUd93qmeaJIBlJNhL"

# TEST DATA
TEST_USD_20_BANODOCO_CREDITS = "price_1NOiytDZUd93qmeaDFefJYYo"
TEST_USD_10_BANODOCO_CREDITS = "price_1NOiytDZUd93qmeaHCMayL0o"

class StripeEvent(ExtendedEnum):
    INVOICE_PAYMENT_SUCCESS = 'invoice.payment_succeeded'
    INVOICE_PAYMENT_FAILED = 'invoice.payment_failed'