DATA_TABLE = 'data-table'
PAGE_SIZE = 'page-size'
PAGE_COUNT = 'page-count'


class LOAN:
    PAYMENT_OPTIONS = 'payment-options'
    TOTAL_AMOUNT = 'total-amount'
    DOWN_PAYMENT_RATE = 'down-payment-rate'
    PERIOD = 'period'
    GRACE = 'grace-period'

    class DROPDOWN:
        REFRESHABLE = 'refreshable-dropdown'
        BUTTON = 'refreshable-dropdown-button'

    class ARR:
        ADD = 'add-a-interest-or-payment-to-the-arrangement'
        DROPDOWN = 'dropdown-for-arrange-options'

    class PREPAY:
        # OPTION = 'prepay-plan'  # 選擇提前付款
        # AMOUNT = 'prepay-amount'
        ARR = 'prepay-multi-arr'

    class SUBSIDY:
        # OPTION = 'subsidy-plan'  # 選擇申請補貼貸款
        INTEREST_OPTION = 'determine whether the subsidy interest is adjustable rate'
        ARR = 'subsidy-multi-arr'
        AMOUNT = 'subsidy-amount'
        INTEREST = 'subsidy-interest'
        START = 'subsidy_START_time'
        TERM = 'subsidy-term'
        GRACE = 'subsidy-grace-period'
        METHOD = 'subsidy-pay-method'


class ADDON:
    NEW_ITEMS = 'new-items'
    ADD = 'addon function'
    DELETE = 'delete function'
    MEMORY = 'memory'
    INPUT = 'input'
    OUTPUT = 'output'
    DISABLED = 'disabled'

    class DROPDOWN:
        MENU = 'dropdown-menu'
        ITEMS = 'dropdown-items'
        LIST = 'dropdown-list'
