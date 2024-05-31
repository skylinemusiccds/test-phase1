import json
import requests

# Provided playlist URL (assuming it's legitimate)
url = "https://universe-playlist.deno.dev"

try:
    # Fetch JSON data from the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP request errors
    data = response.json()

    # Iterate over each channel in the JSON data
    for channel in data:
        try:
            channel_name = channel['name']
            mpd_file = channel['url']  # Assuming 'url' key contains the MPD file URL

            # Create a dictionary for the config object (assuming key and keyId are present)
            config_dict = {
                "file": f"{mpd_file}?begin=20240525T010000&end=20240531T160000",
                "drm": {
                    "clearkey": {
                        "keyId": channel.get('kid', ""),  # Use .get() for optional key
                        "key": channel.get('k', ""),     # Use .get() for optional key
                    }
                }
            }

            # Generate HTML content using f-strings for clarity
            html_content = f"""
            <!DOCTYPE html>
            <html lang='en'>
              <head>
                <meta charset='UTF-8'>
                <title>{channel_name}</title>
                <meta http-equiv='X-UA-Compatible' content='IE=edge'>
                <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                <style>
                  body {{ margin: 0px; }}
                  .jwplayer {{
                    position: absolute !important;
                  }}
                  .jwplayer.jw-flag-aspect-mode {{
                    min-height: 100%;
                    max-height: 100%;
                  }}
                </style>
              </head>
              <body>
                <div id='jwplayerDiv'></div>
                <script src='//content.jwplatform.com/libraries/SAHhwvZq.js'></script>
                <script type='text/javascript'>
                  var config = {json.dumps(config_dict)};
                  jwplayer("jwplayerDiv").setup({{
                    file: config.file,
                    position: 'bottom',
                    autostart: true,
                    stretching: "",
                    width: "100%",
                    type: "dash",
                    drm: config.drm
                  }});
                </script>
              </body>
            </html>
            """

            # Write HTML content to a file
            with open(f"{channel_name}.html", "w") as html_file:
                html_file.write(html_content)

            print(f"HTML file '{channel_name}.html' created successfully.")
        except Exception as e:
            print(f"\n\n\nAn error occurred while processing channel '{channel_name}': {e}\n\n\n\n")

except requests.RequestException as e:
    print(f"HTTP request failed: {e}")
except json.JSONDecodeError:
    print("Failed to decode JSON from the response")
except Exception as e:
    print(f"An error occurred: {e}")
