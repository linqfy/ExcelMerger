from plyer import notification

class GlobalNotificationHandler:
    def push(title, content):
        try:
            notification.notify(
            title=title,
            message=content,
            timeout=2  # Notification will be visible for 10 seconds
            )
            return True
        except Exception as e:
            print("Error sending notification, exception: %s" % e)