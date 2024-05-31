import json
import requests

# Fetch JSON data from the URL
url = "https://universe-playlist.deno.dev"
response = requests.get(url)
data = response.json()

# Iterate over each channel in the JSON data
for channel in data:
    channel_name = channel['name']
    mpd_file = channel['url']
    key_id = channel['kid']
    key = channel['k']

    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{channel_name}</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            margin: 0px;
        }}

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
    <div id="jwplayerDiv"></div>
    <script src="//content.jwplatform.com/libraries/SAHhwvZq.js"></script>
    <script type="text/javascript">
        // Use the PHP configuration directly within the JavaScript
        var config = {{"file":"{mpd_file}?begin=20240525T010000&end=20240531T160000","drm":{{"clearkey":{{"keyId":"{key_id}","key":"{key}"}}}}};

        jwplayer("jwplayerDiv").setup({{
            file: config.file,
            position: 'bottom',
            autostart: true,
            stretching: "",
            width: "100%",
            type: "dash",
            drm: {{
                clearkey: {{
                    keyId: config.drm.clearkey.keyId,
                    key: config.drm.clearkey.key
                }}
            }}
        }});
    </script>
</body>
</html>"""

    # Write HTML content to a file
    with open(f"{channel_name}.html", "w") as html_file:
        html_file.write(html_content)

    print(f"HTML file '{channel_name}.html' created successfully.")
