# gar-cron
github activity reminder cron - a script to send you reminders about your github commit activity. By default, it shoots a mail when there is no commit activity for 3 or more days. [Read this DEV.to article to understand more about this tool](https://dev.to/prahladyeri/gar-cron-a-python-script-to-remind-you-about-your-github-activity-22ad).

# Installation

	pip install gar-cron

# Usage

	gar-cron

# Configuration

When you run gar-cron for the first time, it will prompt you to set values in `config.json` along with its path. The values you need to set should be as follows (You need an smtp mail account to shoot emails, popular ones like GMail/Hotmail don't support this without oAuth, so register one at [gmx.com](https://gmx.com) or something):

	{
		"github_username": "<your github username>",
		"alert_email": "<your email address>",
		"smtp_server":"<smtp server>",
		"smtp_email": "<smtp sending email>",
		"smtp_username": "<smtp username>",
		"smtp_password": "<smtp password>",
		"smtp_port": "<smtp port>"
	}

Once you do this, run `gar-cron` again to ensure that it works. You may then configure it as a user cron job on linux by running `crontab -e` or on windows by scheduling it through the control panel.

For testing of email reminder, you may temporarily configure someone else's `github_username` in config.json who hasn't committed since a long time before running it.