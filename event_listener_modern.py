import asyncio
import logging
import os

from panoramisk import Manager, Message

manager = Manager(
    host=os.getenv('AMI_HOST', '192.168.88.229'),
    port=os.getenv('AMI_PORT', 5038),
    username=os.getenv('AMI_USERNAME', 'testvoip'),
    secret=os.getenv('AMI_SECRET', 'testvoip'),
    ping_delay=10,  # Delay after start
    ping_interval=10,  # Periodically ping AMI (dead or alive)
    reconnect_timeout=2,  # Timeout reconnect if connection lost
)


def on_connect(mngr: Manager):
    logging.info(
        'Connected to %s:%s AMI socket successfully' %
        (mngr.config['host'], mngr.config['port'])
    )


def on_login(mngr: Manager):
    logging.info(
        'Connected user:%s to AMI %s:%s successfully' %
        (mngr.config['username'], mngr.config['host'], mngr.config['port'])
    )


def on_disconnect(mngr: Manager, exc: Exception):
    logging.info(
        'Disconnect user:%s from AMI %s:%s' %
        (mngr.config['username'], mngr.config['host'], mngr.config['port'])
    )
    logging.debug(str(exc))


async def on_startup(
        mngr: Manager):
    await asyncio.sleep(0.1)
    logging.info('Something action...')


async def on_shutdown(mngr: Manager):
    await asyncio.sleep(0.1)
    logging.info(
        'Shutdown AMI connection on %s:%s' % (mngr.config['host'], mngr.config['port'])
    )


@manager.register_event('*')  # Register all events
async def ami_callback(mngr: Manager, msg: Message):
#    if msg.Event == 'FullyBooted':
#    print(f"Event received: {msg.Event}")
    if msg.Event == 'Hangup':
        print(f"Call ended: {msg.Uniqueid}")
        print(f"Cause: {msg.Cause}")
        print(f"Cause-txt: {msg['Cause-txt']}")
    if msg.Event == 'FullyBooted':
        print(f"Device {msg.Uniqueid} is online")
    elif msg.Event == 'DeviceStateChange' and msg.State == 'NOT_INUSE':
        print(f"Device {msg.Device} is offline")
    elif msg.Event == 'DeviceStateChange' and msg.State == 'INUSE':
        print(f"Device {msg.Device} is online")
    elif msg.Event == 'Dial':
        print(f"Dial event: {msg.Uniqueid}")
        print(f"Caller: {msg.CallerIDNum}")
        print(f"Destination: {msg.Destination}")
    elif msg.Event == 'DeviceStateChange':
        print(f"Device {msg.Device} state changed to {msg.State}")
    #print(msg)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    manager.on_connect = on_connect
    manager.on_login = on_login
    manager.on_disconnect = on_disconnect
    manager.connect(run_forever=True, on_startup=on_startup, on_shutdown=on_shutdown)
