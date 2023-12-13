from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def create_navbar():
    # navbar = dbc.Nav(
    #     children= [
    #         dbc.NavItem(
    #             dbc.NavLink(
    #                 [
    #                     dbc.Stack(
    #                         [
    #                             html.I(
    #                                 className="fa-solid fa-house-chimney", 
    #                                 style= specs.APP.NAV.BRAND.LOGO.STYLE,
    #                             ),
    #                             dbc.NavbarBrand(
    #                                 "Amort", 
    #                                 className="ms-1",
    #                                 style= specs.APP.NAV.BRAND.NAME.STYLE
    #                             ),
    #                         ],
    #                         direction= 'horizontal',   
    #                     )
    #                 ],
    #                 href= ids.APP.URL.HOME,
    #                 style= specs.APP.NAV.BRAND.STYLE
    #             ),
    #         ),
    #         dbc.Stack(
    #             [
    #                 dbc.NavItem(
    #                     dbc.NavLink(
    #                         [
    #                             html.I(className="fa-brands fa-github",
    #                                    style= specs.APP.NAV.LINKS.GITHUB.LOGO.STYLE
    #                             ), 
    #                         ],
    #                         href= specs.APP.NAV.LINKS.GITHUB.LINK,
    #                         target="_blank",
    #                         style= specs.APP.NAV.LINKS.GITHUB.STYLE
    #                     ),
    #                 ),
    #                 dbc.NavItem(
    #                     dbc.NavLink(
    #                         [
    #                             html.I(
    #                                 className="fa-brands fa-medium",
    #                                 style= specs.APP.NAV.LINKS.MEDIUM.LOGO.STYLE
    #                                 ),  # Font Awesome Icon
    #                             " "  # Text beside icon
    #                         ],
    #                         href=specs.APP.NAV.LINKS.MEDIUM.LINK,
    #                         target="_blank",
    #                         style= specs.APP.NAV.LINKS.MEDIUM.STYLE,
    #                     ),
    #                 ),
    #                 dbc.NavItem(
    #                     dbc.NavLink(
    #                         [
    #                             html.I(
    #                                 className="fa-brands fa-linkedin",
    #                                 style= specs.APP.NAV.LINKS.LINKEDIN.LOGO.STYLE                                   
    #                                 ),  # Font Awesome Icon
    #                             " "  # Text beside icon
    #                         ],
    #                         href= specs.APP.NAV.LINKS.LINKEDIN.LINK,
    #                         target="_blank",
    #                         style= specs.APP.NAV.LINKS.LINKEDIN.STYLE,
    #                     ),
    #                 ),
    #             ],
    #             direction= 'horizontal',
    #             className= 'g-0',
    #             style= specs.APP.NAV.LINKS.STYLE,
    #         ),
    #         dmc.Menu(
    #             [
    #                 dmc.MenuTarget(
    #                     dmc.Button(
    #                         'Menu', 
    #                         size= 'sm', 
    #                         variant= 'gradient',
    #                         gradient= {"from": "grape", "to": "pink", "deg": 35},
    #                     )
    #                 ),
    #                 dmc.MenuDropdown(
    #                     [
    #                         dmc.MenuItem('Home', href= ids.APP.URL.HOME),
    #                         dmc.MenuDivider(),
    #                         dmc.MenuLabel('More'),
    #                         dmc.MenuItem('Page 2', href= '/page2'),
    #                         dmc.MenuItem('Data', href= ids.APP.URL.DATA),
    #                     ],
    #                 ),
                    
    #             ],
    #             transition= 'pop-top-right',
    #             transitionDuration= 100,
    #             style= specs.APP.NAV.DROPDOWN.STYLE,
    #         ),
    #     ],
    #         style= specs.APP.NAV.STYLE,
    #         fill= "True",
    #         justified= True,
    # )

    # build the same object as above with dmc
    # https://abhinavk910.medium.com/building-dashboard-using-dash-responsive-navbar-part-1-455c68eb04ae
    
    Navbar = dmc.Navbar(
        p="md",                  #providing medium padding all side
        fixed= False,             #Setting fixed to false
        width= {"base": 300},     #Initial size of navbar ie. 300px
        hidden= True,             #we want to hide for smaller screen
        hiddenBreakpoint= 'md',   #after past medium size navbar will be hidden.
        height= '100vh',          #providing height of navbar
        id= 'sidebar',
        children= [
          html.Div(
              [
                  dmc.NavLink(
                      label="With icon",
                      icon=DashIconify(icon="bi:house-door-fill", height=16, color="#c2c7d0")
                  ),
                  dmc.NavLink(
                      opened=False,
                      label="With right section",
                      icon=DashIconify(icon="tabler:gauge", height=16, color="#c2c7d0"),
                      rightSection=DashIconify(icon="tabler-chevron-right", height=16, color="#c2c7d0")
                  ),
                  dmc.NavLink(
                      label="Disabled",
                      icon=DashIconify(icon="tabler:circle-off", height=16, color="#c2c7d0"),
                      disabled=True,
                  ),
                  dmc.NavLink(
                      label="With description",
                      description="Additional information",
                      icon=dmc.Badge(
                          "3", size="xs", variant="filled", color="red", w=16, h=16, p=0
                      ),
                  ),
                  dmc.NavLink(
                      label="Active subtle",
                      icon=DashIconify(icon="tabler:activity", height=16, color="#c2c7d0"),
                      rightSection=DashIconify(icon="tabler-chevron-right", height=16, color="#c2c7d0"),
                      variant="subtle",
                      active=True,
                  ),
              ])
        ]
    )

    return Navbar
