# Pteroller
Pteroller is a Discord Bot to control Pterodactyl Panel using Discord Slash Command.

# Requirements:
The system must have python3 or python install. You also need to install these packages for it to work.
```
python3 -m pip install -U discord.py
python3 -m pip install -U watchdog
python3 -m pip install -U requests
```
After you install these dependencies, You need to open config.json and change your ``API_URL``, ``API_KEY`` and ``token``.
## Example Config:
```json
{
    "token": "Discord Bot Token",

    "activity_type": "playing",
    "activity_name": "Pteroller",

    "pingserver": "1.1.1.1",
    "API_URL": "https://pteroller.xyz/api/client",
    "API_KEY": "Pterodactyl API_KEY"
}
```
After changing the config, You can do ``python3 Bot.py`` to start it up.

# Features:
- Lists all available servers.
> ![image](https://github.com/user-attachments/assets/934e91a8-8467-47d9-ad92-ad51c492a02f)

- Check Connectivity with Cloudflare DNS Server.
> ![image](https://github.com/user-attachments/assets/e07ef76e-a306-4a69-a9d1-d3e273c535c2)

- Abilties to Restart, Start, Stop and Kill The Server.
> ![image](https://github.com/user-attachments/assets/ea96ca16-e1df-4246-8292-cfaf2d7c7add)

