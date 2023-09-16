from errno import EPIPE


class LOAN:
    AMOUNT = 'the amount of the loan'
    DOWNPAYMENT = 'downpayment rate of the loan'
    GRACE = 'the grace period of the loan'
    TENURE = 'the tenure of the loan'
    INTEREST = 'interest rate applied to total tenure of the loan'
    OPTIONS = 'the repayment options of the loan'
    TYPE = 'Loan'

    class RESULT:
        KWARGS = 'the results of the keyword arguments'
        DATAFRAME = 'the results of the dataframe'

    class PREPAY:
        TYPE = 'Prepayment'

    class SUBSIDY:
        # tricks: addition 'of the subsidy' to enable interoperability between loan and subsidy
        # avoid the duplication against the loan.
        TENURE = 'the tenurere of the loan of the subsidy'
        START = 'subsidy-applying-time'
        TYPE = 'Subsidy'

        class PREPAY:
            OPTION = 'whether to set a prepaymet of the subsidy'
            ARR = 'multi arrangement of the prepayment of the subsidy'
            TYPE = 'prepayment of the subsidy'

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
    COLLAPSE= 'collapses'
    
    class TOGGLE:
        SINGLE= 'toggles for single interest rate option'
        MULTI= 'toggles for multi-stages interest rate option'

    class LABEL:
        TIME= 'Time'

    class DROPDOWN:
        MENU = 'dropdown menu'
        MENUITEMS = 'items in the dropdown menu'
        ITEMS = 'dropdown items'
        LIST = 'dropdown list'
        TRANSITION = 'transition'


class DATATABLE:
    TABLE = 'data-table'
    SUM = 'data-sum'
    COLUMN = 'data-column'

    class PAGE:
        SIZE = 'table-page-size'
        COUNT = 'table-page-count'

class CONTROLS:
    BUTTON = 'controls-button'

class GRAPH:
    LINE= 'line charts'
    CHECKLIST= 'choose repayment for charting'
    DROPDOWNS= 'subitems under repayment payments method for charting'
    RESULTS= 'results of selection for charting'
    ACCUMULATION= 'Accumulative'
    LOADING= 'Loading animations for charting'
    
    class DROPDOWN:
        MENU= 'dropdown menu of charts'
        ITEM= 'dropdown items for charting'
        
    class REPAYMENT:
        EPP= 'equal principle payment method for charting'
        ETP= 'equal total payment method for charting'

class APP:
    LOADING= 'loading page contents'

    class INDEX:
        HOME= 'Homepage'
        DATA= 'Spreadsheet'
        GRAPH= 'Graph'
    
    class URL:
        HOME= '/'
        DATA= '/spreadsheet'
