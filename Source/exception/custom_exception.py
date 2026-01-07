import sys
import traceback
import os

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # If running in Jupyter/IPython, try to get a more readable name
    if 'ipykernel' in file_name or 'IPython' in file_name:
        # Check if we can get the notebook name from IPython
        try:
            from IPython import get_ipython
            ipython = get_ipython()
            if ipython and hasattr(ipython, 'user_ns'):
                # Try to get notebook name from the session
                if '__vsc_ipynb_file__' in ipython.user_ns:
                    file_name = ipython.user_ns['__vsc_ipynb_file__']
                else:
                    file_name = "Jupyter Notebook"
        except:
            file_name = "Jupyter Notebook"
    
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))
    
    return error_message

class DocumentPortalException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
        
        # Store full traceback for logging
        _, _, exc_tb = error_detail.exc_info()
        if exc_tb:
            exc_type, exc_value, _ = error_detail.exc_info()
            self.traceback_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        else:
            self.traceback_str = ""
    
    def __str__(self):
        return self.error_message
