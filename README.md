Spotify Lyric
===
> An command line tool to show lyric of current playing song on Spotify.
> Use 千千音樂 Search to optimize Chinese song searching result.

![](https://i.imgur.com/7SN1nmG.jpg)

## Usage

### 1. Get Spotipy Client Token 

* Go to https://developer.spotify.com/dashboard/login, use your Spotify Account to sign in.
* click on **CREATE CLIENT ID**, follow all the instructions to create your application.

![](https://i.imgur.com/vQ1YTOS.png)

* You can find your Client ID on the Dashboard, click **SHOW CLIENT SECRET** to get the secret token.

![](https://i.imgur.com/JeQcDxM.png)


* Go to **Edit Settings** and add the following uri to **Redirect URIs**: http://localhost:8888/callback/. Make sure you save it.

![](https://i.imgur.com/S1kJfbe.png)

### 2. Create `const.py`
You can either create a `const.py` file in the root directory  **or just rename** `const_example.py` to `const.py`. Paste the **CLIENT_ID** and **CLIENT_SECRET** you got from app dashboard here. (Also make sure the **redirect_uri** match the value you set in the dashboard setting.)
```python
USERNAME = 'Anton'
CLIENT_ID = 'PASTE YOUR CLIENT IT HERE'
CLIENT_SECRET = 'PASTE YOUR CLIENT SECRET HERE'
REDIRECT_URI = 'http://localhost:8888/callback/'
```

### 3. Run it for the first time

Run the following command to start the tool:
```console
python3 start_live_lyric.py
```
If this is your first time running with the `USERNAME` you set, you will be ask to login to Spotify on your web browser, **copy the whole uri you were redirected to** and paste it to the terminal:

Example URI:

```
http://localhost:8888/callback/?code=AQBIrqzUgg21VHOB8g4u-mzGvKv_IG7d39PirD3iWr5bM6awaeAOrQiweCdOMWOO03EI9hoae51oEuqNVzpJC1xxJXT6LcdI53aGjJTtGRMyRW52bPsXU58gTpn96lzp-mNOpPeDWaJVAKQ53ZNxD3-ebnHAEhlb48il3QlqO5r8bTYdXmlItgyA9wPXTENp8xZoOyepZHWAs6aZRtbmmWVnEiFSTLGwLD7e_QBVr1loGKnr
```

![](https://i.imgur.com/Az2xJSc.png)

Press `Enter` to start the tool.

![](https://i.imgur.com/4TxAwSt.jpg)
