
from dash import html, dcc
import dash_bootstrap_components as dbc
from app.Dashboard.pages.components.ids import APP


def create_navbar():
    navbar = dbc.Nav(
            children= [
                # html.A(
                    dbc.NavItem(
                        dbc.NavLink(
                            [
                                dbc.Stack(
                                    [
                                        html.I(
                                            className="fa-solid fa-house-chimney", 
                                            style= {
                                                "width": "18%",
                                                "color": "white",
                                                # "margin-top": "8px"
                                            },
                                        ),
                                        dbc.NavbarBrand(
                                            "Amort", 
                                            className="ms-1",
                                            style= {
                                                'width': '40%',
                                                'font-size': '22px',
                                                'text-align': 'left',
                                                'margin-top': '2%',
                                            },
                                        ),
                                    ],
                                    direction= 'horizontal',   
                                )
                            ],
                            href= APP.URL.HOME,
                            style={
                                "color": "white",
                                "fontWeight": "bold",
                                "font-size": "20px",
                                # "padding": "10px",
                                "margin-left": "5%",
                                # 'border': "1px solid",
                                'width': "150px",
                            },
                        ),
                        # align="center",
                        # className="g-0",
                    # ),
                ),
                dbc.Stack(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(className="fa-brands fa-github",
                                           style= {
                                                 "color": "white",
                                                 'font-size': '20px',
                                                 }
                                           ), 
                                    " " 
                                ],
                                href="[YOUR GITHUB PROFILE URL]",
                                target="_blank",
                                style= {
                                    "color": "white",
                                    'size': '100px',
                                }
                            ),
                            style= {
                                # "margin-top": "18px",
                                # 'position': 'absolute',
                                # "left": "70%",
                            }
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(
                                        className="fa-brands fa-medium",
                                        style= {
                                            'color': 'white',
                                            'font-size': '20px',
                                        }
                                        ),  # Font Awesome Icon
                                    " "  # Text beside icon
                                ],
                                href="[YOUR MEDIUM PROFILE URL]",
                                target="_blank"
                            ),
                            style= {
                                # "margin-top": "18px",
                                # "position": 'absolute',
                                # "left": "74%",
                            }
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(
                                        className="fa-brands fa-linkedin",
                                        style= {
                                            'color': 'white',
                                            'font-size': '20px',
                                        }
                                        ),  # Font Awesome Icon
                                    " "  # Text beside icon
                                ],
                                href="[YOUR LINKEDIN PROFILE URL]",
                                target="_blank",
                            ),
                            style= {
                                # "margin-top": "18px",
                                # "position": 'absolute',
                                # "left": "78%",
                            }
                        ),
                    ],
                    direction= 'horizontal',
                    className= 'g-0',
                    style= {
                        'width': '100px',
                        'margin-top': '15px',
                        'position': 'absolute',
                        'left': '75%',
                    }
                ),
                dbc.DropdownMenu(
                    label="Menu",
                    align_end= True,
                    # nav= True,
                    color= "primary",
                    children=[  # Add as many menu items as you need
                        dbc.DropdownMenuItem("Home", href= APP.URL.HOME),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Page 2", href='/page2'),
                        dbc.DropdownMenuItem("Data", href= APP.URL.DATA),
                    ],
                    style= {
                        'color': 'white',
                        'font-size': '18px',
                        'font-weight': 'bold',
                        "border-bottom": "1px solid #0C82DF",
                        "margin-top": "15px",
                        "position": 'absolute',
                        "left": "86%",
                    }
                ),
            ],
            style= {
                'background-color': '#0C82DF',
            },
            fill= "True",
            # pills= True,
            justified= True,
    )

    return navbar
