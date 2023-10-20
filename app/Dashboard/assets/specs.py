class APP:
    class TAB:
        STYLE= {
            'overflowY': 'auto',
            'position': 'absolute',
            'margin-top': 80,
            'margin-left': 420,
            'background-color': 'rgba(255, 255, 255, 0)',
            'width': '60%',
            'z-index': 2,
        }
        
    class PANEL:
        STYLE= {
            'position': 'relative',
            'left': 10,
            'top': 20,
        }
        
class CONTROLS:
    class MORTGAGEOPTIONS:
        WIDTH= 290
        class TENURE:
            class TEXT:
                SIZE= 'lg'
                WEIGHT= 500
            class SLIDER:
                SIZE= 'md'
        class INTEREST:
            class TEXT:
                SIZE= 'lg'
                WEIGHT= 500
            class SEGMENT:
                VALUE= 'fixed'
                COLOR= 'purple'
                SIZE= 'sm'
                STYLE= {
                    'margin-bottom': '5px',
                    'position': 'left',
                }
            class SINGLE_STAGE:
                SIZE= 'md'
                STYLE= {'display': 'flex'}
            class MULTI_STAGES:
                STYLE= {
                    'display': 'none',
                    "maxWidth": "100%",
                    'position': 'left',
                },
    class ADVANCEDOPTIONS:
        STYLE= {
            'width': '100%',
            'display': 'flex',
            'flex-direction': 'column',
            'background-color': 'transparent',
            'align-items': 'left',
        },
        class ACCORDION:
            STYLE= {
                'width': '100%',
                'justify-content': 'center',
                'align-items': 'center',
            }
        class PREPAY:
            STYLE= {'maxWidth': '100%'}
            class LABEL:
                SIZE= 'md'
        class SUBSIDY:
            VARIANT= "gradient"
            GRADIENT={"from": "teal", "to": "lime", "deg": 105}

                

class DATAFRAME:
    pass

class GRAPHICS:
    pass