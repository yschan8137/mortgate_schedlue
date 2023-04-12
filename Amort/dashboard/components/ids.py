class LOAN:
    # PAYMENT_OPTIONS = 'payment-options'
    AMOUNT = 'total-amount'
    DOWNPAYMENT = 'down-payment-rate'
    PERIOD = 'period'
    GRACE = 'grace-period'

    class PREPAY:
        ARR = 'prepay-multi-arr'

    class SUBSIDY:
        ADJUSTABLE = 'determine whether the subsidy interest is adjustable rate'
        ARR = 'subsidy-multi-arr'
        AMOUNT = 'subsidy-amount'
        INTEREST = 'subsidy-interest'
        START = 'subsidy-applying-time'
        TERM = 'subsidy-term'
        GRACE = 'subsidy-grace-period'


class ADVANCED:
    class TOGGLE:
        BUTTON = 'toggle button for multistages interest rate option'
        ITEMS = 'items being toggled'

    class DROPDOWN:
        OPTIONS = 'payment options for loan in dropdown'
        BUTTON = 'refreshable-dropdown-button'


class ADDON:
    NEW = 'new-items'
    ADD = 'addon-function'
    DELETE = 'delete-function'
    MEMORY = 'memory'
    INPUT = 'input'
    OUTPUT = 'output'
    DISABLED = 'disabled'

    class DROPDOWN:
        MENU = 'dropdown-menu'
        MENUITEMS = 'items in  the dropdown menu'
        ITEMS = 'dropdown-items'
        LIST = 'dropdown-list'


class DATATABLE:
    TABLE = 'data-table'

    class PAGE:
        SIZE = 'table-page-size'
        COUNT = 'table-page-count'
