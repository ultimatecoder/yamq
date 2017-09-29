from .frame import Frame


def loads(raw_frame):
    """Parses raw data into STOMP Frame."""
    lines = raw_frame.splitlines()

    if not lines:
        raise ValueError("Error: Empty frame")

    headers = {}
    # Parsing header
    header_start = 1
    header_end = lines.index("")
    for line in lines[header_start:header_end]:
        key, value = line.split(':')
        headers[key] = value

    # Parsing Body
    body_start = header_end + 1
    body_end = lines.index("\x00")
    return Frame(
        command=lines[0],
        headers=headers,
        body=lines[body_start:body_end]
    )


def dumps(frame):
    """Serialises standard STOMP response."""
    if not type(frame) is Frame:
        raise ValueError("Error: Expecting stomp.Frame object.")
    response = [frame.command]

    for key, value in frame.headers.items():
        response.append("{}:{}".format(key, value))
    response.append("")

    response.append(frame.body)
    response.append("\x00")
    return '\r\n'.join(response)
