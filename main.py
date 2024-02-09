import re
import json
import hashlib
import requests
from requests.structures import CaseInsensitiveDict
import PySimpleGUI as sg # pylint: disable=import-error


sg.theme("DarkAmber")
arr = ["", "", "", ""]
CREDITS = "produce by norouzy - 29/12/2021 | updated by difhel - 2023"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/96.0.4664.110 Safari/537.36"
)
layout = [
    [sg.T("")],
    [
        sg.Text("Game link    : ", text_color="white", key="-link-"),
        sg.InputText(key="-IN1-", change_submits=True, size=(50, 50)),
    ],
    [
        sg.Text("Score :          ", text_color="white", key="-score-"),
        sg.InputText(key="-IN2-", change_submits=True, size=(10, 10)),
    ],
    [
        sg.Text("Time  :          ", text_color="white", key="-time-"),
        sg.InputText(key="-IN3-", change_submits=True, size=(10, 10)),
    ],
    [
        sg.Text(
            "Results :                   ",
            text_color="white",
            key="-result-",
            visible=False,
        ),
        sg.Multiline(
            " ",
            key="-run-",
            visible=False,
            auto_size_text=True,
            text_color="white",
            size=(50, 20),
        ),
    ],
    [sg.T("")],
    [sg.T("")],
    [
        sg.T(""),
        sg.T(""),
        sg.T(""),
        sg.T(""),
        sg.T(""),
        sg.T(""),
        sg.T(""),
        sg.T(""),
        sg.T(""),
        sg.T(""),
        sg.T(""),
        sg.Button("Submit", button_color=("white", "green"), border_width=5),
        sg.Button("Cancel", button_color=("white", "red"), border_width=5),
    ],
    [sg.T("")],
    [sg.T("")],
    [sg.Text(CREDITS, text_color="white", font="Courier 8")],
]
window = sg.Window(
    "Gamee cheat",
    layout,
    icon="backup_icon-icons.com_72047.ico",
    resizable=True,
    finalize=True,
)


def get_checksum(score, play_time, url):
    game_state_data = ""
    str2hash = (
        f"{score}:{play_time}:{url}:{game_state_data}:"
        "crmjbjm3lczhlgnek9uaxz2l9svlfjw14npauhen"
	)
    result = hashlib.md5(str2hash.encode())
    checksum = result.hexdigest()
    return checksum


def get_token(game_url):
    url = "http://api.service.gameeapp.com"
    headers = CaseInsensitiveDict()
    headers["Host"] = "api.service.gameeapp.com"
    headers["Connection"] = "keep-alive"
    headers["Content-Length"] = "224"
    headers["client-language"] = "en"
    headers["x-install-uuid"] = "0c1cd354-302a-4e76-9745-6d2d3dcf2c56"
    headers["sec-ch-ua-mobile"] = "?0"
    headers[
        "User-Agent"
    ] = USER_AGENT
    headers["sec-ch-ua-platform"] = "Windows"
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "*/*"
    headers["Origin"] = "https://prizes.gamee.com"
    headers["Sec-Fetch-Site"] = "cross-site"
    headers["Sec-Fetch-Mode"] = "cors"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Referer"] = "https://prizes.gamee.com/"
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Accept-Language"] = "en-US,en;q=0.9"
    data = {
		"jsonrpc": "2.0",
		"id": "user.authentication.botLogin",
		"method": "user.authentication.botLogin",
		"params": {
			"botName": "telegram",
			"botGameUrl": game_url,
			"botUserIdentifier": None
		}
	}

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
    except Exception as _: # pylint: disable=broad-exception-caught
        return False

    print(resp.status_code)
    if resp.status_code == 200:
        result_data = resp.json()
        print("result_data")
        print(result_data)
        token = result_data["result"]["tokens"]["authenticate"]
        return token
    return False


def game_id(game_url):
    url = "https://api.service.gameeapp.com/"

    headers = CaseInsensitiveDict()
    headers["accept"] = "*/*"
    headers["accept-encoding"] = "gzip, deflate, br"
    headers["accept-language"] = "en-US,en;q=0.9"
    headers["cache-control"] = "no-cache"
    headers["client-language"] = "en"
    headers["content-length"] = "173"
    headers["Content-Type"] = "application/json"
    headers["origin"] = "https://prizes.gamee.com"
    headers["pragma"] = "no-cache"
    headers["referer"] = "https://prizes.gamee.com/"
    headers["sec-ch-ua-mobile"] = "?0"
    headers["sec-ch-ua-platform"] = "Windows"
    headers["sec-fetch-dest"] = "empty"
    headers["sec-fetch-mode"] = "cors"
    headers["sec-fetch-site"] = "cross-site"
    headers["User-Agent"] = USER_AGENT
    data = {
		"jsonrpc": "2.0",
		"id": "game.getWebGameplayDetails",
  		"method": "game.getWebGameplayDetails",
		"params": {
			"gameUrl": game_url
		}
	}

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
    except Exception as _: # pylint: disable=broad-exception-caught
        return False
    if resp.status_code == 200:
        result_data = resp.json()
        return result_data["result"]["game"]["id"]
    return False

# pylint: disable-next=too-many-arguments, too-many-locals
def send_score(score, time_play, checksum, token, game_url, game_id_):
    url = "http://api.service.gameeapp.com"
    headers = CaseInsensitiveDict()
    headers["Host"] = "api.service.gameeapp.com"
    headers["User-Agent"] = USER_AGENT
    headers["Accept"] = "*/*"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    headers["Accept-Encoding"] = "gzip, deflate"
    headers["X-Install-Uuid"] = "128942b2-e6e9-41b7-b754-5c7ba3373f8e"
    headers["Client-Language"] = "en"
    headers["Content-Type"] = "application/json"
    headers["Origin"] = "https://prizes.gamee.com"
    headers["Referer"] = "https://prizes.gamee.com/"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "cors"
    headers["Sec-Fetch-Site"] = "cross-site"
    headers["Te"] = "trailers"
    headers["Authorization"] = f"Bearer {token}"
    data = {
		"jsonrpc": "2.0",
		"id": "game.saveWebGameplay",
		"method": "game.saveWebGameplay",
		"params": {
			"gameplayData": {
				"gameId": game_id_,
				"score": int(score),
				"playTime": int(time_play),
				"gameUrl": game_url,
				"metadata": {
					"gameplayId": 30
				},
				"releaseNumber": 8,
				"gameStateData": None,
				"createdTime": "2021-12-28T03:20:24+03:30",
				"checksum": checksum,
				"replayVariant": None,
				"replayData": None,
				"replayDataChecksum": None,
				"isSaveState": False,
				"gameplayOrigin": "game"
			}
		}
	}

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
    except Exception as _: # pylint: disable=broad-exception-caught
        return False

    if resp.status_code == 200:
        result_text = ""
        status = 0
        my_json = resp.json()
        keys_list = list(my_json)
        for i in keys_list:
            if i == "error":
                print(my_json)
                result_text = (
                    my_json["error"]["message"]
                    + "\n"
                    + my_json["error"]["data"]["reason"]
                    + "\n"
                    + "try after "
                    + my_json["user"]["cheater"]["banStatus"]
                )
                status = 1
                break

        if status == 0:
            user_posin_rank = my_json["result"]["surroundingRankings"][0]["ranking"]
            for user in user_posin_rank:
                result_text = (
                    str(user["rank"])
                    + " - "
                    + user["user"]["firstname"]
                    + " "
                    + user["user"]["lastname"]
                    + " score : "
                    + str(user["score"])
                    + "\n"
                    + result_text
                )
        return result_text
    return False


def game_link(url):
    match = re.search(r'game-bot/([\w-]+)', url)
    if match:
        game_code = match.group(1)
        print("/game-bot/" + game_code)
        return "/game-bot/" + game_code
    else:
        return False


def check_is_digit(num):
    return num.strip().isdigit()

def start_polling():
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit', 'Cancel'):
            window.close()
            break
        if event == "Submit":
            window["-run-"].update(visible=True)
            score = values["-IN2-"]
            time = values["-IN3-"]
            if values["-IN1-"] == "" or score == "" or time == "":
                result = "fill empty field !"
            else:
                if not check_is_digit(score) or not check_is_digit(time):
                    result = "score and time fields should be number!"
                else:
                    game_url = game_link(values["-IN1-"])
                    if game_url is False:
                        result = "someting went wrong !" + "\n" + "Not valid link"
                    else:
                        token = get_token(game_url)
                        checksum = get_checksum(score, time, game_url)
                        game_id_ = game_id(game_url)
                        result = send_score(
							score, time, checksum, token, game_url, game_id_
						)
            if result is False:
                window["-run-"].update("Check your internet connection")
            else:
                window["-run-"].update(result)

start_polling()
