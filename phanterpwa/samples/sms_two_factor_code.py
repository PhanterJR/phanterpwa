from phanterpwa.helpers import (
    CONCATENATE
)

text = CONCATENATE(
    "You have created an account on {{app_name}}. Confirm your mobile number, use the activation code:",
    "\n\n",
    "{{code}}",
    "\n\n",
    "Thank you! Bye!"
)
