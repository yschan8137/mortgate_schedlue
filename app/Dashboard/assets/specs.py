class APP:
    class NAV:
        STYLE= {
                'background-color': '#0C82DF',
                'width': '100%',
                'height': '100%',
        }
        class BRAND:
            STYLE= {
            "color": "white",
            "fontWeight": "bold",
            "font-size": "20px",
            "margin-left": "5%",
            'width': "150px",
        }
            class LOGO:
                STYLE= {
                    "width": "18%",
                    "color": "white",
                    # "margin-top": "8px"
                }
            class NAME:
                STYLE= {
                    'width': '40%',
                    'font-size': '22px',
                    'text-align': 'left',
                    'margin-top': '2%',
                }
        class LINKS:
            STYLE= {
                'width': '100px',
                'margin-top': '10px',
                'margin-bottom': '5px',
                'margin-right': '5%',
            }
            class GITHUB:
                LINK= "[YOUR GITHUB PROFILE URL]"
                STYLE= {
                    "color": "white",
                    'size': '100px',
                }
                class LOGO:
                    STYLE= {
                         "color": "white",
                         'font-size': '20px',
                    }
            class MEDIUM:
                STYLE= {}
                LINK= "[YOUR MEDIUM PROFILE URL]"
                class LOGO:
                    STYLE= {
                        'color': 'white',
                        'font-size': '20px',
                    }
            class LINKEDIN:
                STYLE= {}
                LINK= "[YOUR LINKEDIN PROFILE URL]"
                class LOGO:
                    STYLE= {
                        'color': 'white',
                        'font-size': '20px',
                    }
        class DROPDOWN:
            COLOR= "primary"
            STYLE= {
                'font-size': '18px',
                'font-weight': 'bold',
                "border-bottom": "1px solid #0C82DF",
                "margin-top": "10px",
                'margin-bottom': '5px',
                # "position": 'absolute',
                # "left": "86%",
                "margin-right": "10%",
                # "margin-bottom": "3%",
            }
            
    class TAB:
        STYLE= {
            'width': '100%',
            'height': '92vh',
            'overflowY': 'auto',
            'position': 'absolute',
            'margin-top': 10,
            'margin-left': 50,
            'background-color': 'rgba(255, 255, 255, 0)',
            'width': '60%',
            'overflow-y': 'auto',
        }
        
    class PANEL:
        STYLE= {
            'width': 'auto',
            'height': '92vh',
            'margin-top': 10,
            'margin-left': 15,
            'overflow-y': 'auto',
            'scrollbar-color': '#0C82DF #E2E2E2',
        }
        
class COMPONENTS:
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
                }
    class ADVANCEDOPTIONS:
        STYLE= {
            'width': '100%',
            'display': 'flex',
            'flex-direction': 'column',
            'background-color': 'transparent',
            'align-items': 'left',
        }
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

class PANEL:
    class FRONT:
        STYLE= {
            'width': 365,
            'height': 'auto',
            'border': '1px solid #ccc',
            'border-radius': '5px',
            'font-size': '20px',
            'font-weight': 'bold',
            'padding': '20px',
            'color': '#333',
            'item-align': 'center',
            'background-color': '#E2E2E2',
            'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
        }
    class ADVANCEDOPTIONS:
        STYLE= {
            'width': 365,
            'height': 'auto',
            'border': '1px solid #ccc',
            'border-radius': '5px',
            'font-size': '20px',
            'font-weight': 'bold',
            'padding': '20px',
            'color': '#333',
            'background-color': '#E2E2E2',
            'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
        }         

class DATAFRAME:

    class ROWS:
        SIZE= 24
        STYLE= {
            'display': 'inline-block',
            'verticalAlign': 'right',
            'align': 'right',
        }
    class COLUMN_CHECKBOX:
            STYLE= {
                # 'display': 'inline-block',
                'align': 'left',
            }
    class SUM:
        class STYLE:
            HEADER= {
                'textAlign': 'center',
                'border': '1px solid black'
            }
            
            TABLE= {
                "overflow": "auto",
                'scrollX': True
            }
            CELL= {
                'border': '1px solid lightblue',
            }
    class CONTENT:
        STYLE= {
            'width': '100vh',
        }
        class STYLES:
            HEADER= {
                 'textAlign': 'center',
                'border': '1px solid black'
            }
            TABLE= {
                 'overflow': 'auto', 
                 'border': 'medium',
             }
            CELL= {
                 'border': '1px solid pink',
             } 

class GRAPHICS:
    pass