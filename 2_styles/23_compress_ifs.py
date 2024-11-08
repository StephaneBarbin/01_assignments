# STYLE ***************************************************************************
# content = Assignment: (Python Advanced)
#
# date    = 2024-10-28
#**********************************************************************************


# COMMENT --------------------------------------------------
# More optimal
def set_color(ctrlList=None, color=None):
    color_mapping = {1: 4,
                     2: 13,
                     3: 25,
                     4: 17,
                     5: 17,
                     6: 15,
                     7: 6,
                     8: 16}

    for ctrlName in ctrlList:
        try:
            mc.setAttr(ctrlName + 'Shape.overrideEnabled', 1)

            if color in color_mapping:
                mc.setAttr(ctrlName + 'Shape.overrideColor', color_mapping[color])
        except:
            pass


# EXAMPLE
# set_color(['circle','circle1'], 8)
