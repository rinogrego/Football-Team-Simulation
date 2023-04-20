from .base import *


DEPLOYMENT = os.getenv("DEPLOYMENT_MODE")

if DEPLOYMENT == "dev":
    from .dev import *
    
elif DEPLOYMENT == "prod":
    from .prod import *
    
# DEBUG = True # because otherwise railway interal server error (500), but somehow API request via script (test_request_api.py) still works
print("DEBUG mode:", DEBUG)