import argparse
from rich_argparse import RichHelpFormatter

from dotenv import load_dotenv
import uvicorn

from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.prompt import Prompt

from temp_track.utils import weatherapi, misc
from temp_track.agents import tracker, notifier, bureau
from temp_track.notification_providers.console import ConsoleNotificationProvider

parser = argparse.ArgumentParser(formatter_class=RichHelpFormatter)
parser.add_argument("--cli", action="store_true", help="display output on cli")
parser.add_argument("--web", action="store_true", help="display output on web app")
args = parser.parse_args()

# Load environment variables from `.env` file
load_dotenv()

# Make sure that the API key is set and is valid
with Progress(
    SpinnerColumn(),
    TextColumn("{task.description}"),
    TimeElapsedColumn(),
    transient=True,
) as progress:
    loc_check_task = progress.add_task("Verifying API Key")
    try:
        valid = weatherapi.api_key_is_valid()
        # valid = True
        if not valid:
            print("[red bold]:cross_mark: Verification failed!")
            print("[red italic]The API key is either not set or is invalid!")
            print(
                "Please make sure that the correct API key is set in the environmet variable [red bold]WEATHERAPI_API_KEY"
            )
            exit(1)
    except Exception as e:
        print("[red bold]:cross_mark: Verification failed!")
        print("[red italic]An unknown error occurred!")
        print(f"Error message: [grey54]{e}")
        exit(1)
    finally:
        progress.update(loc_check_task, completed=True)

print("[green bold]:white_heavy_check_mark: Verification succeded!")

if args.cli:
    loc = Prompt.ask("Enter your [blue bold]location[/] (leave empty for auto detect)")

    # Make sure we have data available for the given location
    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        loc_check_task = progress.add_task("Checking location")

        try:
            if loc == "":
                loc = misc.get_ip_addr()
            loc_name = weatherapi.get_loc_name_from_loc(loc)
        except weatherapi.DataUnavailableException:
            print("[red bold]:cross_mark: Invalid location!")
            print(
                "[red italic]Data for the location you entered is not available, please use a different location!"
            )
            exit(1)
        except Exception as e:
            print("[red bold]:cross_mark: Location check failed!")
            print("[red italic]An unknown error occurred!")
            print(f"Error message: [grey54]{e}")
            exit(1)
        finally:
            progress.update(loc_check_task, completed=True)
    print(f"Setting location to [green bold]{loc_name}")
    tracker.add_tracker_location(loc)

    min_temp = Prompt.ask("Enter the [blue bold]minimum temperature[/]")
    try:
        min_temp = float(min_temp)
        min_temp = round(min_temp, ndigits=1)
    except Exception:
        print("[red bold]:cross_mark: Invalid minimum temperature!")
        print("[red italic]Please enter a valid number")
        exit(1)

    max_temp = Prompt.ask("Enter the [blue bold]maximum temperature[/]")
    try:
        max_temp = float(max_temp)
        max_temp = round(max_temp, ndigits=1)
    except Exception:
        print("[red bold]:cross_mark: Invalid maximum temperature!")
        print("[red italic]Please enter a valid number")
        exit(1)
    print(f"Setting temperature range to [green bold]{min_temp}-{max_temp}")
    tracker.set_loc_temp_range(loc, min_temp, max_temp)

    notifier.register_notification_proivder(ConsoleNotificationProvider())

    bureau.run()

    print("\n\n\n")

else:
    uvicorn.run(
        "temp_track.notification_providers.api:api", port=3000, log_level="info"
    )
