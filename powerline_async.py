import aiohttp
import xml.etree.ElementTree as ET
import hashlib

# Replace these with your Fritz Powerline login details
USERNAME = '' # If you don't know the user, try with an empty string
PASSWORD = '' # The password, with wich you login in the userinterface
IP_ADDRESS = '' # IP-Adress of your Powerline device
SWITCH_URL = f"http://{IP_ADDRESS}/net/home_auto_overview.lua"

async def get_sid():
    login_url = f'http://{IP_ADDRESS}/login_sid.lua'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(login_url) as response:
                response_text = response.text()
        except Exception as e:
            print(f"Error during initial request: {e}")
            raise
        
        root = ET.fromstring(response_text)
        challenge = root.find('Challenge').text

        challenge_response = f"{challenge}-{PASSWORD}".encode('utf-16le')
        response_text = challenge + '-' + hashlib.md5(challenge_response).hexdigest()

        try:
            async with session.get(login_url, params={'username': USERNAME, 'response': response_text}) as sid_response:
                sid_response_text = sid_response.text()
        except Exception as e:
            print(f"Error during SID request: {e}")
            raise

        sid_root = ET.fromstring(sid_response_text)
        sid = sid_root.find('SID').text

        if sid == '0000000000000000':
            raise Exception("Failed to get SID. Check your username and password.")

        return sid

async def switch_on(session, sid):
    print('switching on')
    switch_on_payload = {
        "sid": sid,
        "device": "1000",
        "switch": "1",
        "xhr": "1",
        "useajax": "1"
    }
    try:
        await session.post(SWITCH_URL, data=switch_on_payload)
    except Exception as e:
        print(f"Error during switch on: {e}")
        raise

async def switch_off(session, sid):
    print('switching off')
    switch_off_payload = {
        "sid": sid,
        "device": "1000",
        "switch": "0",
        "xhr": "1",
        "useajax": "1"
    }
    try:
        await session.post(SWITCH_URL, data=switch_off_payload)
    except Exception as e:
        print(f"Error during switch off: {e}")
        raise

@service
async def async_switch_powerline(switchaction):
    print(f"switchaction: {switchaction}")
    if switchaction.lower() in ['on', 'off']:
        try:
            sid = get_sid()
        except Exception as e:
            print(f"Error getting SID: {e}")
            raise
        
        async with aiohttp.ClientSession() as session:
            if switchaction.lower() == "on":
                await switch_on(session, sid)
            else:
                await switch_off(session, sid)
    else:
        raise Exception(f"Wrong argument for switchaction: {switchaction}")
