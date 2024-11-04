# STYLE ***************************************************************************
# content = Assignment: applying style knowledge
#
# date    = 2024-10-28
#************************************************************************************


def find_caller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """

    current_frame = currentframe()

    #On some versions of IronPython, currentframe() returns None if
    #IronPython isn't run with -X:Frames.
    if current_frame is not None:
        current_frame = current_frame.f_back

    while hasattr(current_frame, "f_code"):
        current_frame_code = current_frame.f_code
        filename = os.path.normcase(current_frame_code.co_filename)

        if filename == _srcfile:
            current_frame = current_frame.f_back
            continue
        else:
            return (current_frame_code.co_filename, current_frame.f_lineno, current_frame_code.co_name)

    return "(unknown file)", 0, "(unknown function)"

