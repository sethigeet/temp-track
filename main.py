from dotenv import load_dotenv

from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.prompt import Prompt

from temp_track.utils import weatherapi

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

loc = Prompt.ask("Enter your [blue bold]location[/]")

# Make sure we have data available for the given location
with Progress(
    SpinnerColumn(),
    TextColumn("{task.description}"),
    TimeElapsedColumn(),
    transient=True,
) as progress:
    loc_check_task = progress.add_task("Checking location")

    try:
        temp = weatherapi.get_temp(loc)
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

print(temp)
