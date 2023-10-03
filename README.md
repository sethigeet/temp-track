# Temp-Track

A simple application that fetches the current temperature in the location specified and notifies the user when the temperature in that location goes outside the range specified by the user.

# Running the program

- Create a free account on [weatherapi.com](weatherapi.com) and create an API key.
- Copy the `.env.example` to `.env` and paste your API key from [weatherapi.com](weatherapi.com).
- Install the required dependencies using `poetry install`.
- Run the program using `poetry run python main.py` and follow on screen instructions!

:warning: **NOTE**: The text displayed on the terminal refreshes automatically every 10 mins so don't think that the text is not updating! It is a change right in the place of the old text and no new line is printed!

:warning: **NOTE**: This project uses the latest version of `poetry` and there are some breaking changes in how poetry stores its config files so older versions might not work. So, please use the latest version.

# Notifiers

Currently, there is only the console notifier which prints to the console from which the program is running but this can be extended to many other things such as sending an email, a push notification or even a text message. The options are limitless!
