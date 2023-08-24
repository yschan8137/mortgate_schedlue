
from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    navbar = dbc.Nav(
            [ 
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.I(
                                className="fa-solid fa-house-chimney", 
                                style= {
                                    "color": "white",
                                    # "margin-top": "8px"
                                    }
                                    )
                            ),
                            dbc.Col(dbc.NavbarBrand(
                                "Amort", 
                                className="ms-1",
                                style= {
                                    'font-size': '22px',
                                    # "margin-top": "15px"
                                }
                                )),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={
                        "textDecoration": "none",
                        "color": "white",
                        "fontWeight": "bold",
                        "font-size": "20px",
                        "padding": "10px",
                        "margin-left": "9%",
                    },
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        [
                            html.I(className="fa-brands fa-github",
                                   style= {
                                         "color": "white",
                                         'font-size': '20px',
                                         }
                                   ),  # Font Awesome Icon
                            " "  # Text beside icon
                        ],
                        href="[YOUR GITHUB PROFILE URL]",
                        target="_blank",
                        style= {
                            "color": "white",
                            'size': '100px',
                        }
                    ),
                    style= {
                        "margin-top": "8px",
                        'position': 'absolute',
                        # "margin-left": "35%",
                        # "margin-right": "5%",
                        "left": "72%",
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
                        "margin-top": "8px",
                        "position": 'absolute',
                        "left": "76%",
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
                        "margin-top": "8px",
                        "position": 'absolute',
                        "left": "80%",
                    }

                ),
                dbc.DropdownMenu(
                    label="Menu",
                    align_end= True,
                    # nav= True,
                    color= "primary",
                    children=[  # Add as many menu items as you need
                        dbc.DropdownMenuItem("Home", href='/'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Page 2", href='/page2'),
                        dbc.DropdownMenuItem("Data", href='/data'),
                    ],
                    style= {
                        'color': 'white',
                        'font-size': '18px',
                        # 'padding': '10px',
                        # 'border-radius': '2px',
                        'font-weight': 'bold',
                        # 'border': "1px solid #0",
                        # "box-shadow": "0 2px 4px rgba(0, 0, 0)",
                        # "margin-left": "40%",
                        "border-bottom": "1px solid #0C82DF",
                        "margin-top": "6px",
                        # "margin-right": "8%",
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
