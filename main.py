# Copyright (C) 2017-2018 Jaysinh Shukla (jaysinhp@gmail.com)
# Please find copy of license at "LICENSE"
# at the root of the project.


import argparse
import asyncio
import logging

from yamq import server


if __name__ == '__main__':
    description = """
    Yet Another Messaging Queue (YAMQ) is messaging broker.

    Copyright (C) 2017-2018 Jaysinh Shukla (jaysinh@gmail.com)
    Please find copy of license at "LICENSE" at the root of the project.
    """

    parser = argparse.ArgumentParser(description)
    parser.add_argument(
        "-d", "--host",
        type=str,
        nargs="?",
        default="localhost",
        help="Host name on which the server will bind to."
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        nargs='?',
        default=8000,
        help=(
            "Port number on which the server will listen for incoming requests."
        )
    )
    parser.add_argument(
        "-l", "--log-level",
        type=str,
        nargs='?',
        default="DEBUG",
        choices= ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        help="Decide the level of log the application should throw."
    )
    args = parser.parse_args()
    event_loop = asyncio.get_event_loop()
    coro = event_loop.create_server(server.STOMP_Server, args.host, args.port)
    server = event_loop.run_until_complete(coro)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(args.log_level)
    streamHandler.setFormatter(formatter)


    logger = logging.getLogger(__name__)
    logger.setLevel(args.log_level)

    logger.addHandler(streamHandler)

    logger.info("Started server at {}:{}".format(args.host, args.port))

    try:
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    event_loop.run_until_complete(server.wait_closed())
    event_loop.close()
