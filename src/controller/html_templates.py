# Taken from websocket Python package browser example
CONTROLLER_STATUS_HTML = """<!DOCTYPE html>
<html>
    <head>
        <title>Elevator Controller Status</title>
    </head>
    <body>
        <p id="messages"></p>
        <script>
            var ws = new WebSocket("{uri}"),
                messages = document.getElementById('messages');
            ws.onmessage = function (event) {{
                var messages = document.getElementById('messages');
                    //console.log(JSON.parse(event.data));
                    messages.innerHTML = JSON.stringify(event.data);
            }};
        </script>
    </body>
</html>
"""
