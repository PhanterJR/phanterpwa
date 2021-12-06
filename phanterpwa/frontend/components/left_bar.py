import phanterpwa.frontend.helpers as helpers
import phanterpwa.frontend.application as application
from org.transcrypt.stubs.browser import __pragma__
__pragma__('alias', "jQuery", "$")
__pragma__('skip')
jQuery = window = Hammer = this = js_undefined = window = console = __new__ = RegExp = 0
__pragma__('noskip')


DIV = helpers.XmlConstructor.tagger("div")
I = helpers.XmlConstructor.tagger("i")
IMG = helpers.XmlConstructor.tagger("img", True)
CONCATENATE = helpers.CONCATENATE
I18N = helpers.I18N

__pragma__('kwargs')


user_png = """
data:image/png;base64,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yH93e2Si5f8Tj/VoAABwBdjrB5AAACFFADVFAGbtABpFAKFFAGFFgDo7K5+/Jzfd2WnMi3UQgJw2OjrwHoB6G2D0zujoF87o6MguAKIHwNrosW4OABCpBqDm+U8d+V+VKALBiuXNFQAAOhVpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNS1jMDE0IDc5LjE1MTQ4MSwgMjAxMy8wMy8xMy0xMjowOToxNSAgICAgICAgIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgICAgICAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgICAgICAgICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgICAgICAgICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgICAgICAgICB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICAgICAgICAgICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyI+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+QWRvYmUgUGhvdG9zaG9wIENDIChNYWNpbnRvc2gpPC94bXA6Q3JlYXRvclRvb2w+CiAgICAgICAgIDx4bXA6Q3JlYXRlRGF0ZT4yMDE1LTA0LTAyVDAxOjI3OjA4KzA4OjAwPC94bXA6Q3JlYXRlRGF0ZT4KICAgICAgICAgPHhtcDpNZXRhZGF0YURhdGU+MjAxNS0wNC0wMlQwMToyNzowOCswODowMDwveG1wOk1ldGFkYXRhRGF0ZT4KICAgICAgICAgPHhtcDpNb2RpZnlEYXRlPjIwMTUtMDQtMDJUMDE6Mjc6MDgrMDg6MDA8L3htcDpNb2RpZnlEYXRlPgogICAgICAgICA8eG1wTU06SW5zdGFuY2VJRD54bXAuaWlkOmIyYTE4Yzk1LTMyMWYtNDI3Yy1hNTcxLTgxNTY5YmJkMjAyZDwveG1wTU06SW5zdGFuY2VJRD4KICAgICAgICAgPHhtcE1NOkRvY3VtZW50SUQ+eG1wLmRpZDo3ZDNlMDI0Yy1iZDU1LTQxNmItOTkwYi1kMWJkNTY5OGU5NGE8L3htcE1NOkRvY3VtZW50SUQ+CiAgICAgICAgIDx4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ+eG1wLmRpZDo3ZDNlMDI0Yy1iZDU1LTQxNmItOTkwYi1kMWJkNTY5OGU5NGE8L3htcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD4KICAgICAgICAgPHhtcE1NOkhpc3Rvcnk+CiAgICAgICAgICAgIDxyZGY6U2VxPgogICAgICAgICAgICAgICA8cmRmOmxpIHJkZjpwYXJzZVR5cGU9IlJlc291cmNlIj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OmFjdGlvbj5jcmVhdGVkPC9zdEV2dDphY3Rpb24+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDppbnN0YW5jZUlEPnhtcC5paWQ6N2QzZTAyNGMtYmQ1NS00MTZiLTk5MGItZDFiZDU2OThlOTRhPC9zdEV2dDppbnN0YW5jZUlEPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6d2hlbj4yMDE1LTA0LTAyVDAxOjI3OjA4KzA4OjAwPC9zdEV2dDp3aGVuPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6c29mdHdhcmVBZ2VudD5BZG9iZSBQaG90b3Nob3AgQ0MgKE1hY2ludG9zaCk8L3N0RXZ0OnNvZnR3YXJlQWdlbnQ+CiAgICAgICAgICAgICAgIDwvcmRmOmxpPgogICAgICAgICAgICAgICA8cmRmOmxpIHJkZjpwYXJzZVR5cGU9IlJlc291cmNlIj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OmFjdGlvbj5zYXZlZDwvc3RFdnQ6YWN0aW9uPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6aW5zdGFuY2VJRD54bXAuaWlkOmIyYTE4Yzk1LTMyMWYtNDI3Yy1hNTcxLTgxNTY5YmJkMjAyZDwvc3RFdnQ6aW5zdGFuY2VJRD4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OndoZW4+MjAxNS0wNC0wMlQwMToyNzowOCswODowMDwvc3RFdnQ6d2hlbj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OnNvZnR3YXJlQWdlbnQ+QWRvYmUgUGhvdG9zaG9wIENDIChNYWNpbnRvc2gpPC9zdEV2dDpzb2Z0d2FyZUFnZW50PgogICAgICAgICAgICAgICAgICA8c3RFdnQ6Y2hhbmdlZD4vPC9zdEV2dDpjaGFuZ2VkPgogICAgICAgICAgICAgICA8L3JkZjpsaT4KICAgICAgICAgICAgPC9yZGY6U2VxPgogICAgICAgICA8L3htcE1NOkhpc3Rvcnk+CiAgICAgICAgIDxkYzpmb3JtYXQ+aW1hZ2UvcG5nPC9kYzpmb3JtYXQ+CiAgICAgICAgIDxwaG90b3Nob3A6Q29sb3JNb2RlPjM8L3Bob3Rvc2hvcDpDb2xvck1vZGU+CiAgICAgICAgIDxwaG90b3Nob3A6SUNDUHJvZmlsZT5EaXNwbGF5PC9waG90b3Nob3A6SUNDUHJvZmlsZT4KICAgICAgICAgPHRpZmY6T3JpZW50YXRpb24+MTwvdGlmZjpPcmllbnRhdGlvbj4KICAgICAgICAgPHRpZmY6WFJlc29sdXRpb24+NzIwMDAwLzEwMDAwPC90aWZmOlhSZXNvbHV0aW9uPgogICAgICAgICA8dGlmZjpZUmVzb2x1dGlvbj43MjAwMDAvMTAwMDA8L3RpZmY6WVJlc29sdXRpb24+CiAgICAgICAgIDx0aWZmOlJlc29sdXRpb25Vbml0PjI8L3RpZmY6UmVzb2x1dGlvblVuaXQ+CiAgICAgICAgIDxleGlmOkNvbG9yU3BhY2U+NjU1MzU8L2V4aWY6Q29sb3JTcGFjZT4KICAgICAgICAgPGV4aWY6UGl4ZWxYRGltZW5zaW9uPjI1NjwvZXhpZjpQaXhlbFhEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj4yNTY8L2V4aWY6UGl4ZWxZRGltZW5zaW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAKPD94cGFja2V0IGVuZD0idyI/Pplp45QAAAAgY0hSTQAAWQkAAFVIAAD3zAAAgFUAAGVwAADU9wAALUgAABScB/kkFAAAD35JREFUeNrs3X2QV9V9x/H37sKyu7AssEQWkKfyIIJUeZBQFiaigoo2KpgxtZFESa022jRN/3CmbWI67XTaaad/NJlJOqmZTp1JOtOmNRPSNlPzoCYamyaKjRqrwSeiRA1QfCAgbP84R7u7LLv7272/+7v33Pdr5g44MrC/7z3n8zv33nPPaerr60NSNTVbAskAkGQASDIAJBkAkgwASQaAJANAkgEgyQCQZABIMgAkGQCSDABJBoAkA0CSASCpOCZYguDDN96Q0sfpBmYB74rHDGAqMAVoB9qAVqAFaAJOAseBY8CbwOvAa8Ah4OV+x4vxz5Te5+/8go3eAEhCK/BL8VgEzAN6YufO2mFg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
"""
class LeftBar(application.Component):
    def __init__(self, target_selector, **parameters):
        self.target_selector = target_selector
        self.element_target = jQuery(self.target_selector)
        if "_id" not in parameters:
            parameters['_id'] = "phanterpwa-component-left_bar"
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters["_class"], "phanterpwa-component-left_bar-wrapper"
            )
        else:
            parameters["_class"] = "phanterpwa-component-left_bar-wrapper"
        tcontent = [
            DIV(_id="phanterpwa-component-left_bar-top"),
            DIV(_id="phanterpwa-component-left_bar-middle"),
            DIV(_id="phanterpwa-component-left_bar-bottom")
        ]
        self.all_buttons = list()
        self.dict_buttons = dict()
        self.html = DIV(*tcontent, **parameters)
        application.Component.__init__(self, "left_bar", self.html)
        self.html_to(target_selector)
        jQuery(window).resize(lambda: self.check_has_scrollbar())

    def add_button(self, button, **parameters):
        if isinstance(button, (LeftBarMenu, LeftBarButton, LeftBarUserMenu)):
            id_button = button.identifier
            has_button = False
            cont = 0
            position = None
            for b in self.all_buttons:
                if b.identifier == id_button:
                    has_button = True
                    position = cont
                cont += 1

            if not has_button:
                self.all_buttons.append(button)
            else:
                self.all_buttons[position] = button
        self.reload()

    def reload(self):
        self.start()

    def start(self):
        self.element_target = jQuery(self.target_selector)
        for x in self.all_buttons:
            id_button = "phanterpwa-component-left_bar-menu_button-{0}".format(x.identifier)

            if all([self._check_button_requires_login(x),
                    self._check_button_ways(x),
                    self._check_button_roles(x),
                    x.show_if(),
                    x.show_if_way_match()]):
                position = self._get_button_position(x)
                b = self.element_target.find(
                    "#phanterpwa-component-left_bar-{0}".format(position)
                ).find("#{0}".format(id_button))

                if b.length > 0:
                    b.parent().remove()
                self.element_target.find(
                    "#phanterpwa-component-left_bar-{0}".format(position)
                ).append(x.jquery())
                x.start()
            else:
                self.element_target.find("#{0}".format(id_button)).parent().remove()
        self.check_has_scrollbar()
        window.PhanterPWA.reload_events(**{"selector": "#phanterpwa-component-left_bar"})

    def check_has_scrollbar(self):
        el = self.element_target.find("#phanterpwa-component-left_bar")
        if el.length > 0:
            scrollbar = el[0].scrollHeight
            if scrollbar > el.height():
                el.addClass("has_scrollbar")
            else:
                el.removeClass("has_scrollbar")


    def _get_button_position(self, button):
        pos = button.position
        if pos is not None and pos is not js_undefined:
            if pos in ['middle', 'top']:
                return pos
        return "bottom"

    def _check_button_requires_login(self, button):
        requires_login = button.requires_login
        if requires_login is not None and requires_login is not js_undefined:
            if requires_login is True:
                authorization = window.PhanterPWA.get_authorization()
                if authorization is not None:
                    return True
            else:
                return True
        return False

    def _check_button_roles(self, button):
        roles = button.autorized_roles
        if roles is not None and roles is not js_undefined:
            if isinstance(roles, list):
                if "all" in roles:
                    return True
                auth_user = window.PhanterPWA.get_auth_user()
                if auth_user is not None:
                    if isinstance(auth_user.roles, list) and isinstance(roles, list):
                        if len(set(auth_user.roles).intersection(set(roles))) > 0:
                            return True
                else:
                    if "anonymous" in roles:
                        return True

        return False

    def _check_button_ways(self, button):
        current_way = window.PhanterPWA._get_way_from_url_hash()
        ways = button.ways
        if ways is not None and ways is not js_undefined:
            if isinstance(ways, list):
                if "all" in ways:
                    return True
                elif current_way in ways:
                    return True
                else:
                    for x in ways:
                        if callable(x):
                            if x(current_way) is True:
                                return True
                        elif x.startswith("^"):
                            r = __new__(RegExp(x))
                            result = current_way.match(r)
                            if result is not None:
                                return True

        return False

    @staticmethod
    def _open():
        jQuery("#phanterpwa-component-left_bar").addClass("enabled")
        jQuery("#phanterpwa-component-left_bar-main_button").addClass("enabled")

    def open(self):
        self._open()

    @staticmethod
    def _close():
        jQuery("#phanterpwa-component-left_bar").removeClass("enabled").removeClass("enabled_submenu").find(
            ".phanterpwa-component-left_bar-menu_button-wrapper"
        ).removeClass("enabled")
        jQuery("#phanterpwa-component-left_bar-main_button").removeClass("enabled").removeClass("enabled_submenu")

    def close(self):
        self._close()


class LeftBarMainButton(application.Component):
    def __init__(self, target_selector, **parameters):
        self.target_selector = target_selector
        self.element_target = jQuery(self.target_selector)
        self._icon = I(_class="fas fa-bars")
        if "_id" not in parameters:
            parameters['_id'] = "phanterpwa-component-left_bar-main_button"
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters["_class"],
                "phanterpwa-component-left_bar-main_button-wrapper wave_on_click waves-phanterpwa link"
            )
        else:
            parameters["_class"] = "{0} {1}".format(
                "phanterpwa-component-left_bar-main_button-wrapper",
                "wave_on_click waves-phanterpwa link"
            )
        if "icon" in parameters:
            self._icon = parameters["icon"]
        html = DIV(self._icon, **parameters)
        application.Component.__init__(self, "left_bar_main_button", html)
        self.html_to(target_selector)

    def switch_leftbar(self):
        self.element_target = jQuery(self.target_selector)
        el = self.element_target.find("#phanterpwa-component-left_bar-main_button")
        if el.hasClass("enabled") or el.hasClass("enabled_submenu"):
            self.close_leftbar()
        else:
            self.open_leftbar()

    def close_leftbar(self):
        # self.element_target = jQuery(self.target_selector)
        # self.element_target.find(
        #     "#phanterpwa-component-left_bar-main_button").removeClass("enabled").removeClass("enabled_submenu")
        LeftBar._close()

    def open_leftbar(self):
        # self.element_target = jQuery(self.target_selector)
        # self.element_target.find("#phanterpwa-component-left_bar-main_button").addClass("enabled")
        LeftBar._open()

    def _binds(self):
        self.element_target = jQuery(self.target_selector)
        self.element_target.find("#phanterpwa-component-left_bar-main_button").off("click.mainbutton_leftbar").on(
            "click.mainbutton_leftbar",
            lambda: self.switch_leftbar()
        )
        jQuery(
            "#main-container"
        ).off(
            "click.main_container_click"
        ).on(
            "click.main_container_click",
            lambda: self.close_leftbar()
        )
        # jQuery(
        #     ".phanterpwa-component-left_bar-button"
        # ).off(
        #     "click.left_bar_button_click"
        # ).on(
        #     "click.left_bar_button_click",
        #     lambda: self.close_leftbar()
        # )

    def reload(self):
        self._binds()

    def start(self):
        self._binds()


class LeftBarButton(helpers.XmlConstructor):
    def __init__(self, identifier, label, icon, **parameters):
        self.identifier = identifier
        self.label = label
        self.icon = icon
        self.requires_login = False
        self.autorized_roles = ["all"]
        self.ways = ["all"]
        self.position = "bottom"
        self._on_start = parameters.get("onStart", None)
        tag = parameters.get("tag", "div")
        parameters["_id"] = "phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters['_class'],
                "phanterpwa-component-left_bar-button link")
        else:
            parameters["_class"] = "phanterpwa-component-left_bar phanterpwa-component-left_bar-button link"

        if "requires_login" in parameters:
            self.requires_login = parameters["requires_login"]

        if "autorized_roles" in parameters:
            if isinstance(parameters["autorized_roles"], list):
                self.autorized_roles = parameters["autorized_roles"]
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'autorized_roles' must be type list")

        if "ways" in parameters:
            if isinstance(parameters["ways"], list):
                self.ways = parameters["ways"]
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'ways' must be type list")
        if "position" in parameters:
            self.position = parameters["position"]
        self._show_if = parameters.get("show_if", True)
        self._show_if_way_match = parameters.get("show_if_way_match", None)
        MY_TAG = helpers.XmlConstructor.tagger(tag)
        content = [
            MY_TAG(
                DIV(self.icon,
                    _class="phanterpwa-component-left_bar-icon-container"),
                DIV(self.label, _class="phanterpwa-component-left_bar-label"),
                **parameters
            )
        ]

        helpers.XmlConstructor.__init__(
            self, "div", False, *content, _class="phanterpwa-component-left_bar-menu_button-wrapper"
        )

    def show_if(self):
        if callable(self._show_if):
            show = self._show_if(self)
            if show is True:
                return True
            else:
                return False
        elif self._show_if is True:
            return True
        return False

    def show_if_way_match(self):
        if self._show_if_way_match is not None:
            nre = __new__(RegExp(self._show_if_way_match))
            current_way = window.PhanterPWA._get_way_from_url_hash()
            result = current_way.match(nre)
            if result is None or result is js_undefined:
                return False
        return True

    def close_leftbar(self):
        LeftBar._close()

    def binds(self):
        jQuery(
            ".phanterpwa-component-left_bar-button"
        ).off(
            "click.left_bar_button_click"
        ).on(
            "click.left_bar_button_click",
            lambda: self.close_leftbar()
        )

    def start(self):
        self.binds()
        if window.PhanterPWA.DEBUG:
            console.info("start button {0}".format(self.identifier))
        if callable(self._on_start):
            self._on_start()


class LeftBarSubMenu(helpers.XmlConstructor):
    def __init__(self, identifier, label, **parameters):
        self.identifier = identifier
        self.label = label
        self.initial_class = "phanterpwa-component-left_bar-submenu-button link"
        parameters["_id"] = "phanterpwa-component-left_bar-submenu-button-{0}".format(identifier)
        if "_class" in parameters:
            self.initial_class = " ".join(
                [parameters['_class'].strip(), "phanterpwa-component-left_bar-submenu-button link"])
        parameters['_class'] = self.initial_class
        content = [
            DIV(I(_class="fas fa-angle-right"), _class="phanterpwa-component-left_bar-submenu-icon-container"),
            DIV(self.label, _class="phanterpwa-component-left_bar-submenu-label"),
        ]
        helpers.XmlConstructor.__init__(self, 'div', False, *content, **parameters)


class LeftBarMenu(helpers.XmlConstructor):
    def __init__(self, identifier, label, icon, **parameters):
        self.identifier = identifier
        self.label = label
        self.icon = icon
        self.parameters = parameters
        self.submenus = []
        self.componentSubmenu = LeftBarSubMenu
        self.requires_login = False
        self.autorized_roles = ["all"]
        self.ways = ["all"]
        self.position = "bottom"
        parameters["_id"] = "phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters['_class'],
                "phanterpwa-component-left_bar-menu link")
        else:
            parameters["_class"] = "phanterpwa-component-left_bar phanterpwa-component-left_bar-menu link"

        if "requires_login" in parameters:
            self.requires_login = parameters["requires_login"]

        if "autorized_roles" in parameters:
            if isinstance(parameters["autorized_roles"], list):
                self.autorized_roles = parameters["autorized_roles"]
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'autorized_roles' must be type list")
        if "ways" in parameters:
            if isinstance(parameters["ways"], list):
                self.ways = parameters["ways"]
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'ways' must be type list")
        if "position" in parameters:
            self.position = parameters["position"]
        self._show_if = parameters.get("show_if", True)
        self._show_if_way_match = parameters.get("show_if_way_match", None)

        helpers.XmlConstructor.__init__(self, 'div', False, _class="phanterpwa-component-left_bar-menu_button-wrapper")
        self._update_content()

    def addSubmenu(self, identifier, label, **parameters):
        self.submenus.append(LeftBarSubMenu(identifier, label, **parameters))
        self._update_content()

    def _update_content(self):
        html_submenus = ""
        if self.submenus:
            self.parameters["_target_submenu"] = "phanterpwa-component-left_bar-submenu-from-{0}".format(
                self.identifier)
            html_submenus = DIV(
                *self.submenus,
                _id=self.parameters["_target_submenu"],
                _class="phanterpwa-component-left_bar-submenu-container")
        self.content = [
            DIV(
                DIV(self.icon,
                    _class="phanterpwa-component-left_bar-icon-container"),
                DIV(self.label, _class="phanterpwa-component-left_bar-label"),
                **self.parameters),
            html_submenus
        ]

    def switch_menu(self, el):
        if jQuery(el).parent().hasClass("enabled"):
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        ).parent()
        element.addClass("enabled")
        jQuery("#phanterpwa-component-left_bar").addClass("enabled_submenu").addClass("enabled")
        jQuery("#phanterpwa-component-left_bar-main_button").addClass("enabled")

    def close_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        ).parent()
        element.removeClass("enabled")
        if jQuery("#phanterpwa-component-left_bar").find(
                ".phanterpwa-component-left_bar-menu_button-wrapper.enabled").length == 0:
            jQuery("#phanterpwa-component-left_bar").removeClass("enabled_submenu").removeClass("enabled")
            jQuery("#phanterpwa-component-left_bar-main_button").removeClass("enabled")

    def show_if(self):
        if callable(self._show_if):
            show = self._show_if(self)
            if show is True:
                return True
            else:
                return False
        elif self._show_if is True:
            return True
        return False

    def show_if_way_match(self):
        if self._show_if_way_match is not None:
            nre = __new__(RegExp(self._show_if_way_match))
            current_way = window.PhanterPWA._get_way_from_url_hash()
            result = current_way.match(nre)
            if result is None or result is js_undefined:
                return False
        return True

    def start(self):

        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        )
        element.off("click.open_leftbar_menu").on(
            "click.open_leftbar_menu",
            lambda: self.switch_menu(this)
        )
        sub_element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-submenu-from-{0} {1}".format(
                self.identifier, ".phanterpwa-component-left_bar-submenu-button"))
        sub_element.off("click.close_leftbar_submenu").on(
            "click.close_leftbar_submenu",
            lambda: self.close_menu()
        )


class LeftBarUserMenu(helpers.XmlConstructor):
    def __init__(self, **parameters):
        self.identifier = "auth_user_login"
        self.submenus = []
        self.parameters = parameters
        self.requires_login = True
        self.autorized_roles = ["all"]
        self.ways = ["all"]
        self.position = "bottom"
        parameters["_id"] = "phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        if "_class" in parameters:
            parameters["_class"] = "{0} {1}".format(
                parameters['_class'],
                "phanterpwa-component-left_bar-menu link")
        else:
            parameters["_class"] = "phanterpwa-component-left_bar phanterpwa-component-left_bar-menu link"

        if "requires_login" in parameters:
            self.requires_login = parameters["requires_login"]

        if "autorized_roles" in parameters:
            if isinstance(parameters["autorized_roles"], list):
                self.autorized_roles = parameters["autorized_roles"]
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'autorized_roles' must be type list")
        if "ways" in parameters:
            if isinstance(parameters["ways"], list):
                self.ways = parameters["ways"]
            else:
                if window.PhanterPWA.DEBUG:
                    console.error("The parameter 'ways' must be type list")
        if "position" in parameters:
            self.position = parameters["position"]

        self._show_if = parameters.get("show_if", True)
        self._show_if_way_match = parameters.get("show_if_way_match", None)
        self._image = IMG(_id="phanterpwa-component-left_bar-url-imagem-user",
            _src=user_png.strip(),
            _alt="user avatar")

        helpers.XmlConstructor.__init__(
            self, 'div', False, _class="{0} {1}".format(
                "phanterpwa-component-left_bar-menu_button-wrapper-auth_user",
                "phanterpwa-component-left_bar-menu_button-wrapper"
            )
        )
        self._update_content()

    def addSubmenu(self, identifier, label, **parameters):
        self.submenus.append(LeftBarSubMenu(identifier, label, **parameters))
        self._update_content()

    def _update_content(self):
        html_submenus = ""
        self.parameters
        if self.submenus:
            self.parameters["_target_submenu"] = \
                "phanterpwa-component-left_bar-submenu-from-{0}".format(self.identifier)
            html_submenus = DIV(
                *self.submenus,
                _id=self.parameters["_target_submenu"],
                _class="phanterpwa-component-left_bar-submenu-container")
        self.content = [
            DIV(
                DIV(
                    DIV(self._image,
                        _class="phanterpwa-component-left_bar-image-user"),
                    _class="phanterpwa-component-left_bar-image-user-container"),
                DIV(self.name_user,
                    _id="phanterpwa-component-left_bar-name-user",
                    _class="phanterpwa-component-left_bar-label"),
                **self.parameters),
            html_submenus
        ]

    def switch_menu(self, el):
        if jQuery(el).parent().hasClass("enabled"):
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        ).parent()
        element.addClass("enabled")
        jQuery("#phanterpwa-component-left_bar").addClass("enabled_submenu").addClass("enabled")
        jQuery("#phanterpwa-component-left_bar-main_button").addClass("enabled")

    def close_menu(self):
        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        ).parent()
        element.removeClass("enabled")
        if jQuery("#phanterpwa-component-left_bar").find(
                ".phanterpwa-component-left_bar-menu_button-wrapper.enabled").length == 0:
            jQuery("#phanterpwa-component-left_bar").removeClass("enabled_submenu").removeClass("enabled")
            jQuery("#phanterpwa-component-left_bar-main_button").removeClass("enabled")

    def show_if(self):
        if callable(self._show_if):
            show = self._show_if(self)
            if show is True:
                return True
            else:
                return False
        elif self._show_if is True:
            return True
        return False

    def show_if_way_match(self):
        if self._show_if_way_match is not None:
            nre = __new__(RegExp(self._show_if_way_match))
            current_way = window.PhanterPWA._get_way_from_url_hash()
            result = current_way.match(nre)
            if result is None or result is js_undefined:
                return False
        return True

    def start(self):

        element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-menu_button-{0}".format(self.identifier)
        )
        element.off("click.open_leftbar_menu").on(
            "click.open_leftbar_menu",
            lambda: self.switch_menu(this)
        )
        sub_element = jQuery("#phanterpwa-component-left_bar").find(
            "#phanterpwa-component-left_bar-submenu-from-{0} .phanterpwa-component-left_bar-submenu-button".format(
                self.identifier))
        sub_element.off("click.close_leftbar_submenu").on(
            "click.close_leftbar_submenu",
            lambda: self.close_menu()
        )
        self.auth_user = window.PhanterPWA.get_auth_user()
        user_name = "Anonymous"
        role = I18N("User")
        user_image = "/static/{0}/images/user.png".format(
            window.PhanterPWA.VERSIONING)
        if self.auth_user is not None:
            first_name = self.auth_user.first_name
            last_name = self.auth_user.last_name
            user_name = "{0} {1}".format(first_name, last_name)
            role = I18N(self.auth_user.role)
            if self.auth_user.image is not None and self.auth_user.image is not js_undefined:
                user_image = self.auth_user.image
        if element.find("#phanterpwa-component-left_bar-url-imagem-user").attr("src") != user_image:
            element.find("#phanterpwa-component-left_bar-url-imagem-user").attr("src", user_image)
        element.find("#phanterpwa-component-left_bar-name-user").text(user_name)


__pragma__('nokwargs')
