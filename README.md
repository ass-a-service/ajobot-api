# ajo-bot API

![https://www.ajobot.com/](https://www.ajobot.com/assets/images/ajologo.png)

Farm ajos by spamming :garlic: in your discord guild. **Beware of the Vampire**.

## Invite the bot
[Play for free](https://discord.com/api/oauth2/authorize?client_id=967138080375046214&permissions=265280&scope=bot%20applications.commands).

## Running the bot
To run the API you need to point to the same Redis of [ajobot](https://github.com/ass-a-service/ajobot).

```sh
pip install --upgrade -r requirements.txt
uvicorn app.main:app
```

