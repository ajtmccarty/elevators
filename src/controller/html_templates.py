# Taken from websocket Python package browser example
CONTROLLER_STATUS_HTML = """<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket demo</title>
    </head>
    <body>
        <script>
            var ws = new WebSocket("{uri}"),
                messages = document.createElement('ul');
            ws.onmessage = function (event) {{
                var messages = document.getElementsByTagName('ul')[0],
                    message = document.createElement('li'),
                    content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            }};
            document.body.appendChild(messages);
        </script>
    </body>
</html>
"""
