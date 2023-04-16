class LOAN:
    AMOUNT = 'the amount of the loan'
    DOWNPAYMENT = 'downpayment rate of the loan'
    TERM = 'the term of the loan'
    GRACE = 'the grace period of the loan'
    INTEREST = 'the interest rate of the loan'

    class PREPAY:
        ARR = 'multi arrangement of the prepayment'

    class SUBSIDY:
        ARR = 'multi arrangement of the subsidy interest'
        # tricks: addition 'of the subsidy' to enable interoperability between loan and subsidy
        AMOUNT = 'the amount of the loan of the subsidy'
        INTEREST = 'the interest rate of the loan of the subsidy'
        START = 'subsidy-applying-time'
        TERM = 'the term of the loan of the subsidy'
        GRACE = 'the grace period of the loan of the subsidy'


class ADVANCED:
    class TOGGLE:
        BUTTON = 'toggle button for multistages interest rate option'
        ITEMS = 'items being toggled'
        MEMORY = 'record regarding whether the toggle is on or off'

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
