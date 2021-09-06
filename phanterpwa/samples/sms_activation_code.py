from phanterpwa.helpers import (
    CONCATENATE
)

text = CONCATENATE(
    "To complete authentication in the {{app_name}} application it is necessary to add this code.",
    "\n\n",
    "{{code}}",
    "\n\n",
    "Thank you! Bye!"
)
