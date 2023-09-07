# Daquiver's DSA Slack Bot

This is a Python-based Slack bot designed for any slack channel. It enables users to view their previous history, add today's update to their history, and view weekly reports. The bot integrates several powerful libraries, including SlackClient, FastAPI, and SQLAlchemy, to provide seamless functionality.

## Prerequisites

Before running the script, please make sure you have the following:

- A Slack bot token
- A Slack bot ID

## Getting Started

1. Clone the repository:

   ```python
   git clone https://github.com/Daquiver1/dsa_slack_bot.git
   ```

2. Change to the project directory:

   ```python
   cd dsa_slack_bot
   ```

3. Install the required dependencies:

   ```python
    pip install -r requirements.txt
   ```

4. Rename the `.env.template` file to `.env` and update the environment variables with your own values.

5. Run the python file with the following command:

   ```python
   uvicorn src.main.api:app --reload
   ```

6. `The app is now running.`

## TODO

- [ ] Integrate Celery for background tasks(weekly report and daily reminders.)
- [ ] Add test cases.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please create an issue or submit a pull request.

## Contact

[![Gmail](https://img.shields.io/badge/Gmail-Mail-red.svg?logo=gmail&logoColor=white)](mailto:cabrokwa11@gmail.com)
[![Linkedin](https://img.shields.io/badge/Linkedin-follow-blue.svg?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/daquiver/)
[![Twitter](https://img.shields.io/badge/Twitter-follow-blue.svg?logo=twitter&logoColor=white)](https://twitter.com/daquiver1)
[![Medium](https://img.shields.io/badge/Medium-follow-black.svg?logo=medium&logoColor=white)](https://daquiver.medium.com)

---

```python

if youEnjoyed:
    starThisRepository()

```
