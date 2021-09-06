from phanterpwa.helpers import (
    CONCATENATE
)

text = CONCATENATE(
    "A new password was requested on {{app_name}}:",
    "\n\n",
    "{{password}}",
    "\n\n",
    "If you have not made this request, you do not have to do anything.",
)
