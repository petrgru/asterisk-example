"""
Example script to originate a call through Asterisk Manager Interface.

Usage: python originate.py config.ini

"""
import sys
import asyncio
from panoramisk.call_manager import CallManager

async def originate():
#    callmanager = CallManager.from_config(sys.argv[1])
    callmanager = CallManager(
        host='192.168.88.229',  # AMI host
        port=5038,  # AMI port
        username='testvoip',  # AMI username
        secret='testvoip',  # AMI secret    
        ping_delay=10,  # Delay after start
        ping_interval=10,  # Periodically ping AMI (dead or alive)
        reconnect_timeout=2,  # Timeout reconnect if connection lost    
    )
    await callmanager.connect()
    call = await callmanager.send_originate({
        'Action': 'Originate',
        'Channel': 'PJSIP/222',
        'WaitTime': 20,
        'CallerID': 'testik',
        'Exten': '500',
        'Context': 'from-internal',
        'Priority': 1})
    print(call)
    while not call.queue.empty():
        event = call.queue.get_nowait()
        print(event)
    while True:
        event = await call.queue.get()
        print(event)
        if event.event.lower() == 'hangup' and event.cause in ('0', '17'):
            break
    callmanager.clean_originate(call)
    callmanager.close()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(originate())
    loop.close()


if __name__ == '__main__':
    main()
