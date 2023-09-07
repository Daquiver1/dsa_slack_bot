"""Strings used in app."""

# Hello
HELLO = """Welcome to Daquiver's DSA Bot. This bot helps monitor your DSA journey. The following features are supported.
* /hello - Get a welcome message from the bot.
* /create - Create your account.
* /update - Add your leetcode update for the day.
* /weekly - Get your weekly leetcode update.
* /create-reminder - Create a reminder to send in your leetcode update.
* /delete-reminder - Delete your reminder.
* /history - View your entire leetcode update history.
"""

# Leetcode updates
LEETCODE_UPDATE_CONFIRMATION_MESSAGE = """Thanks for the update. Your leetcode update has been stored successfully. \n\nWe go again tomorrow."""
NO_UPDATE = """You haven't given an update so far."""
ALREADY_SENT_UPDATE = """You've already sent your update for today. We'll go again tomorrow."""
REMINDER_TEXT = """Don't forget to send in your leetcode update for today. We've got a goal to meet."""
REMINDER_CREATED = """A reminder has been created. Every day I'll send you two reminders to send in your leetcode update. You can delete the reminder with the /delete-reminder command."""
REMINDER_DELETED = """Reminder has been deleted successfully."""

# Account
ACCOUNT_CREATED = """Your account has been created successfully. You can now add leetcode updates with the /update command. All the best in your journey."""
ALREADY_HAVE_AN_ACCOUNT = """You already have an account. """
DONT_HAVE_AN_ACCOUNT = """You don't have an account with us, please create your account with the /create command."""
INVALID_NUMBER = """Please enter a valid number. Input should ONLY be a number and be between the range of 0-50. You can't solve 50 questions in a day. Go out and see the sun. 😑"""
