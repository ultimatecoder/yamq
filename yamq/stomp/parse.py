from .frame import Frame


def loads(raw_frame):
    """Parses raw data into STOMP Frame."""
    null_octed = raw_frame.index("\x00")
    lines = raw_frame[:null_octed].splitlines()

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
    return Frame(
        command=lines[0],
        headers=headers,
        body=lines[body_start:]
    )


def dumps(frame):
    """Serialises standard STOMP response."""
    if not isinstance(frame, Frame):
        raise ValueError("Error: Expecting stomp.Frame object.")
    response = [frame.command]

    for key, value in frame.headers.items():
        response.append("{}:{}".format(key, value))
    response.append("")

    response.append(frame.body)
    response.append("\x00")
    return '\r\n'.join(response)
