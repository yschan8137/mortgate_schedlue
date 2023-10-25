
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from app.Dashboard.assets import ids, specs


def create_navbar():
    navbar = dbc.Nav(
        children= [
            dbc.NavItem(
                dbc.NavLink(
                    [
                        dbc.Stack(
                            [
                                html.I(
                                    className="fa-solid fa-house-chimney", 
                                    style= specs.APP.NAV.BRAND.LOGO.STYLE,
                                ),
                                dbc.NavbarBrand(
                                    "Amort", 
                                    className="ms-1",
                                    style= specs.APP.NAV.BRAND.NAME.STYLE
                                ),
                            ],
                            direction= 'horizontal',   
                        )
                    ],
                    href= ids.APP.URL.HOME,
                    style= specs.APP.NAV.BRAND.STYLE
                ),
            ),
            dbc.Stack(
                [
                    dbc.NavItem(
                        dbc.NavLink(
                            [
                                html.I(className="fa-brands fa-github",
                                       style= specs.APP.NAV.LINKS.GITHUB.LOGO.STYLE
                                ), 
                            ],
                            href= specs.APP.NAV.LINKS.GITHUB.LINK,
                            target="_blank",
                            style= specs.APP.NAV.LINKS.GITHUB.STYLE
                        ),
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            [
                                html.I(
                                    className="fa-brands fa-medium",
                                    style= specs.APP.NAV.LINKS.MEDIUM.LOGO.STYLE
                                    ),  # Font Awesome Icon
                                " "  # Text beside icon
                            ],
                            href=specs.APP.NAV.LINKS.MEDIUM.LINK,
                            target="_blank",
                            style= specs.APP.NAV.LINKS.MEDIUM.STYLE,
                        ),
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            [
                                html.I(
                                    className="fa-brands fa-linkedin",
                                    style= specs.APP.NAV.LINKS.LINKEDIN.LOGO.STYLE                                   
                                    ),  # Font Awesome Icon
                                " "  # Text beside icon
                            ],
                            href= specs.APP.NAV.LINKS.LINKEDIN.LINK,
                            target="_blank",
                            style= specs.APP.NAV.LINKS.LINKEDIN.STYLE,
                        ),
                    ),
                ],
                direction= 'horizontal',
                className= 'g-0',
                style= specs.APP.NAV.LINKS.STYLE,
            ),
            dmc.Menu(
                [
                    dmc.MenuTarget(
                        dmc.Button(
                            'Menu', 
                            size= 'sm', 
                            variant= 'gradient',
                            gradient= {"from": "grape", "to": "pink", "deg": 35},
                        )
                    ),
                    dmc.MenuDropdown(
                        [
                            dmc.MenuItem('Home', href= ids.APP.URL.HOME),
                            dmc.MenuDivider(),
                            dmc.MenuLabel('More'),
                            dmc.MenuItem('Page 2', href= '/page2'),
                            dmc.MenuItem('Data', href= ids.APP.URL.DATA),
                        ],
                    ),
                    
                ],
                transition= 'pop-top-right',
                transitionDuration= 100,
                style= specs.APP.NAV.DROPDOWN.STYLE,
            ),
            # dbc.DropdownMenu(
            #     label="Menu",
            #     align_end= True,
            #     # nav= True,
            #     color= specs.APP.NAV.DROPDOWN.COLOR,
            #     children=[  # Add as many menu items as you need
            #         dbc.DropdownMenuItem("Home", href= ids.APP.URL.HOME),
            #         dbc.DropdownMenuItem(divider=True),
            #         dbc.DropdownMenuItem("Page 2", href='/page2'),
            #         dbc.DropdownMenuItem("Data", href= ids.APP.URL.DATA),
            #     ],
            #     style= specs.APP.NAV.DROPDOWN.STYLE,
            # ),
        ],
            style= specs.APP.NAV.STYLE,
            fill= "True",
            justified= True,
    )

    return navbar
