from pprint import pprint
import asyncio
import os
from panoramisk import Manager


async def extension_status():
    manager = Manager(
        host=os.getenv('AMI_HOST', '192.168.88.229'),
        port=os.getenv('AMI_PORT', 5038),
        username=os.getenv('AMI_USERNAME', 'testvoip'),
        secret=os.getenv('AMI_SECRET', 'testvoip'),
        ping_delay=10,  # Delay after start
        ping_interval=10,  # Periodically ping AMI (dead or alive)
        reconnect_timeout=2,  # Timeout reconnect if connection lost
       )
    await manager.connect()
    action = {
        'Action': 'ExtensionState',
        'Exten': '222',
        'Context': 'from-internal',
    }
    extension = await manager.send_action(action)
    pprint(extension)
    manager.close()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(extension_status())
    loop.close()


if __name__ == '__main__':
    main()
