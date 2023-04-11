# MangaDigestionBot-Pyrogram

## Introduction

MangaDigestion was a telegram channel which was created to provide Manga/Manhwa/Manhua to it's readers. The repository contains the bot that was made to provide Manga/Manhwa/Manhua to it's users, without any manual work, directly from a Telegram Bot.

The Bot will fetch the images from the website and it'll convert the images to pdf, as we can't send images directly in telegram, and send it to user. Which user can download and read it. In addition, it contains a request feature which allows the user to send manga requests.

**The bot is no longer on Telegram as Heroku has started monthly subscription. But the APIs are still working.**

## Commands

```
/start - Start the Bot
/help - Usage info
/about - More info
/kalot - To fetch manga by manga name
/request - Request Mangas by manga name
```

### /kalot

/kalot command is used with a string, for example, /kalot Grand Blue. Where Grand Blue is a manga name. This command will fetch every manga which contain 'Grand Blue' in it and show it to the user.

```
/kalot Grand Blue
```

### /request

Like /kalot, /request command is also used with a string. It is used to take request manga from the user and send the information to Google Sheets.

```
/request Black Clover
```

### /start

/start command is used to start the bot and give greetings to the user.

```
/start
```

### /help

/help command is used to send help text to the user, which he/she/they can follow to get help using the bot.

```
/help
```

### /about

/about command is used to show more information about the bot.

```
/about
```

## Env Variables

`API_ID` - Get the value from [my.telegram.org](https://my.telegram.org/apps) here.

`API_HASH` - Get the value from [my.telegram.org](https://my.telegram.org/apps) here.

`BOT_TOKEN` - Make a bot from [@BotFather](https://t.me/BotFather) and enter token here.

`GSPREAD_JSON` - A link of google sheets API JSON file hosted in the cloud, configure it in https://console.cloud.google.com. For more help [watch this video.](https://www.youtube.com/watch?v=bu5wXjz2KvU)

## Deploy
You can deploy your own project on [Heroku](https://www.heroku.com/)

## Help
We are always here to help, visit our Telegram Group [MangaDigestionCommunity](https://t.me/MangaDigestionCommunity) to ask any questions.
