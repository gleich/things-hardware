import requests
import time
import microdotphat


def main():
    microdotphat.set_rotate180(True)
    token = get_api_token()
    animation_sleep_time = 0.005
    while True:
        todos = get_todos(token)
        (count_done_text, percent_done) = gen_count_done_text(todos["today_todos"])
        if percent_done == 100:
            microdotphat.write_string("DONE!", kerning=False)
            microdotphat.show()
            time.sleep(10)
            continue
        create_progress_bar(percent_done)
        microdotphat.write_string(count_done_text, offset_y=9, kerning=False)
        microdotphat.show()
        todos = get_todos(token)
        time.sleep(4)
        for _ in range(9):
            microdotphat.scroll_vertical()
            microdotphat.show()
            time.sleep(animation_sleep_time)
        time.sleep(4)
        for _ in range(9):
            microdotphat.scroll_vertical(-1)
            microdotphat.show()
            time.sleep(animation_sleep_time)
        microdotphat.clear()


def get_api_token():
    with open("/home/matt/things-hardware/token.txt") as token_file:
        token = token_file.read().removesuffix("\n")
        return token


def get_todos(token):
    try:
        response = requests.get(
            url="https://api.mattglei.ch/things/cache",
            headers={
                "Authorization": "Bearer " + token,
            },
        )
        return response.json()
    except requests.exceptions.RequestException:
        print("HTTP Request failed")


def gen_count_done_text(today_todos):
    num_done = 0
    for todo in today_todos:
        if todo["status"] == "completed":
            num_done += 1
    return (
        f"{num_done}/{len(today_todos)}",
        round((num_done / len(today_todos)) * 100),
    )


def create_progress_bar(percent_done):
    pixels_total = microdotphat.WIDTH * microdotphat.HEIGHT
    set_pixels = 0
    for x in range(microdotphat.WIDTH):
        for y in range(microdotphat.HEIGHT):
            if set_pixels > pixels_total * (percent_done / 100):
                return
            microdotphat.set_pixel(x, y, 1)
            set_pixels += 1


if __name__ == "__main__":
    main()
