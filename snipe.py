import aiohttp
import logging
from colorama import Fore, init
from datetime import datetime, timedelta
import asyncio
from os import path
import time
from bs4 import BeautifulSoup

#Define color codes
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"

import sys
try:
    import webbrowser
except Exception:
    pass

init()

logging.basicConfig(level=logging.INFO, format='%(message)s')
times = []


def custom_info(message):
    logging.info(f"{Fore.RED}[info] {Fore.RESET}{message}")


def print_title():
    print(f"""

     {Fore.CYAN}
░█████╗░░█████╗░██████╗░███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝
██║░░╚═╝██║░░██║██████╔╝█████╗░░
██║░░██╗██║░░██║██╔══██╗██╔══╝░░
╚█████╔╝╚█████╔╝██║░░██║███████╗
░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝
{Fore.WHITE}""", Fore.RESET)


def menu(options):
    i = 1
    # loop through options and print
    custom_info(f"select a number 1 - {len(options)}")
    for option in options:
        print(f"{i}). {option}")
        i += 1
    # main function loop
    # Doesn't end until a correct answer is given
    while True:
        try:
            # takes an input using readchar's readkey function
            choice = int(input("> "))
            options[choice - 1]
            # returns the option the user selected by list index
            return choice - 1
        except (ValueError, IndexError):
            print("please enter a valid option")


def custom_input(message):
    print(f"{Fore.RED}[input] {Fore.RESET}", end='')
    input_return = input(message)
    return input_return


def check_resp(status):
    if str(status)[0] == str(2):
        return True
    else:
        return False


def resp_error(message):
    print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] {message}")
  
  #proxy here

async def namemc_timing(target, block_snipe):
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    now = datetime.strptime(now, '%Y-%m-%dT%H:%M:%S')
    block_snipe_words = ["snipe", "block"]
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://namemc.com/search?q={target}") as page:
                # page = requests.get(namemc_url)
                soup = BeautifulSoup(await page.text(), 'html.parser')
                snipe_time = soup.find("time", {"id": "availability-time"}).attrs["datetime"]
                snipe_time = datetime.strptime(snipe_time, '%Y-%m-%dT%H:%M:%S.000Z')
        except AttributeError:
            status_bar = soup.find(id="status-bar")
            info = status_bar.find_all("div", class_="col-sm-6 my-1")
            status = info[0].text.split("\n")[2]
            if status.lower().rstrip('*') == 'available':
                custom_info(f"\"{target}\" is {status}. The sniper can turbo {status} names!")
                snipe_time = custom_input("At what time will this name be able to be turboed (month/day/yr, 24hrtime_hour:minute:second) (UTC)\nexample: 03/06/2020 01:06:45\n» ")
                snipe_time = datetime.strptime(snipe_time.strip(), "%m/%d/%Y %H:%M:%S")
                wait_time = snipe_time - now
                wait_time = wait_time.seconds
                if wait_time >= 60:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time / 60)} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                else:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} seconds | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                return snipe_time
            print(f"\"{target}\" is {status}. The sniper cannot claim names that are {status} so go claim it fast through https://my.minecraft.net if possible.")
            quit()

        wait_time = snipe_time - now
        wait_time = wait_time.seconds
        if wait_time >= 60:
            custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time / 60)} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
        elif wait_time >= 3600:
            custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time / 3600)} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
        else:
            custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} seconds | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
        return snipe_time


async def nx_timing(target, block_snipe):
    now = datetime.utcnow()
    block_snipe_words = ["snipe", "block"]
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api-v2.statz.xyz//check/{target}") as r:
            resp_json = await r.json()
            if resp_json["status"] == "soon":
                snipe_time = datetime.strptime(resp_json()["drop_time"], "%Y-%m-%dT%H:%M:%S.000Z")
            elif resp_json["status"] == "taken":
                print(f"\"{target}\" is taken already. The sniper cannot claim names that are taken.")
            if resp_json["status"] == "":
                custom_info(f"{target} is available now. If you would like to turbo the name see below.")
                snipe_time = custom_input("At what time will this name be able to be turboed (month/day/yr, 24hrtime_hour:minute:second) (UTC)\nexample: 03/06/2020 01:06:45\n» ")
                snipe_time = datetime.strptime(snipe_time.strip(), "%m/%d/%Y %H:%M:%S")
                wait_time = snipe_time - now
                wait_time = wait_time.seconds
                if wait_time >= 60:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time / 60)} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                else:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} seconds | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                return snipe_time


async def time_snipe(target, block_snipe):
    try:
        timing = await nx_timing(target, block_snipe)
    except Exception:
        timing = await namemc_timing(target, block_snipe)
    return timing


class Account:
    def __init__(self, email, password, questions=[]):
        self.email = email
        self.password = password
        self.questions = questions
        self.got_name = False
        self.failed_auth = False
        self.authenticate_json = {"agent": {"name": "Minecraft", "version": 1}, "username": self.email, "password": self.password}
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.3", "Content-Type": "application/json"}

    async def authenticate(self, session, sleep_time):
        await asyncio.sleep(sleep_time)
        # custom_info(f"{Fore.WHITE}starting auth for {self.email}")
        debug_mode = False
        async with session.post("https://authserver.mojang.com/authenticate", json=self.authenticate_json, headers=self.headers) as r:
            if check_resp(r.status):
                resp_json = await r.json()
                try:
                    self.uuid = resp_json["selectedProfile"]["id"]
                except KeyError:
                    if debug_mode:
                        print(resp_json)
                    else:
                        custom_info(f"{self.email} is unpaid and cannot snipe names. please make sure you are blocking.")
                self.auth = {"Authorization": "Bearer: " + resp_json["accessToken"]}
                self.access_token = resp_json["accessToken"]
            else:
                resp_error(f"invalid credentials | {self.email}")
                self.failed_auth = True
                return
        async with session.get("https://api.mojang.com/user/security/challenges", headers=self.auth) as r:
            answers = []
            if check_resp(r.status):
                resp_json = await r.json()
                if resp_json == []:
                    logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.GREEN} signed in to {self.email}{Fore.RESET}")
                else:
                    try:
                        for x in range(3):
                            answers.append({"id": resp_json[x]["answer"]["id"], "answer": self.questions[x]})
                    except IndexError:
                        logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} {self.email} has security questions and you did not provide any!")
                        return
                    async with session.post("https://api.mojang.com/user/security/location", json=answers, headers=self.auth) as r:
                        if check_resp(r.status):
                            logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.GREEN} signed in to {self.email}{Fore.RESET}")
                        else:
                            resp_error(f"security questions incorrect | {self.email}")
                            self.failed_auth = True
            else:
                logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} {self.email} something went wrong with authentication for {self.email}!")
                self.failed_auth = True

    async def block_req(self, session, ctarget_username):
        await asyncio.sleep(0)
        async with session.put(f"https://api.mojang.com/user/profile/agent/minecraft/name/{target_username}", headers=self.auth) as response:
            now = datetime.now()
            logging.info(f"{Fore.WHITE}[{f'{Fore.GREEN}SUCCESS' if response.status == 204 else f'{Fore.RED}FAIL'}{Fore.WHITE}]{Fore.RESET}{' ' + target_username + ' ' + Fore.GREEN + self.email if str(response.status)[0] == str(2) else Fore.RED} | {response.status}{Fore.RESET} @ {Fore.CYAN}{now}{Fore.RESET}")
            await response.read()
            if response.status == 204:
                asyncio.get_event_loop().stop()

    async def snipe_req(self, session, target_username):
        await asyncio.sleep(0)
        try:
            async with session.post(f"https://api.mojang.com/user/profile/{self.uuid}/name", headers=self.auth, json={"name": target_username, "password": self.password}) as response:
                now = datetime.now()
                logging.info(f"{Fore.WHITE}[{f'{Fore.GREEN}SUCCESS' if response.status == 204 else f'{Fore.RED}FAIL'}{Fore.WHITE}]{Fore.RESET}{' ' + target_username + ' ' + Fore.GREEN + self.email if str(response.status)[0] == str(2) else Fore.RED} | {response.status}{Fore.RESET} @ {Fore.CYAN}{now}{Fore.RESET}")
                await response.read()
                if response.status == 204:
                    self.got_name = True
                    asyncio.get_event_loop().stop()
        except AttributeError:
            print(f'{Fore.WHITE}[{Fore.RED}error{Fore.WHITE}]{Fore.RESET} {self.email} failed authentication and cannot snipe!')

    async def webhook_skin_write_file(self):
        async with aiohttp.ClientSession() as session:
            with open("success.txt", "a") as f:
                f.write(f"{self.email}:{self.password} - {target_username}\n")
            try:
                files = {"model": "slim", "url": open("skin.txt", "r").read().strip()}
                auth = self.auth
                auth["Content-Type"] = "application/x-www-form-urlencoded"
                async with session.post(f"https://api.mojang.com/user/profile/{self.uuid}/skin", headers=self.auth, data=files) as r:
                    if r.status == 204 or r.status == 200:
                        logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.RESET} changed skin of {self.email}")
                    else:
                        logging.info(f"{Fore.WHITE}[{Fore.RED}FAIL{Fore.WHITE}]{Fore.RESET} Failed to change skin {self.email} | {str(r.status)}")
                        logging.info(await r.json())
            except FileNotFoundError:
                pass
            except Exception:
                logging.info(f"{Fore.WHITE}[{Fore.RED}i have no idea{Fore.WHITE}]{Fore.RESET} i dont know what happend but it failed")
            try:
                webhooks = []
                with open("webhook.txt", "r") as f:
                    unconverted_webhooks = f.readlines()
                for hook in unconverted_webhooks:
                    webhooks.append(hook.strip())
                for hook in webhooks:
                    if hook.split(":")[0] == "custom_announce":
                        async with session.post("https://announcements-api.herokuapp.com/api/v1/announce", json={"name": target_username.strip()}, headers={"Authorization": hook.split(":")[1].strip()}) as r:
                            if r.status == 204:
                                logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.RESET} sent custom announcement of snipe!")
                            else:
                                logging.info(f"{Fore.RED} {r.status} | Failed to send custom announcement!{Fore.RESET}")
                                print(await r.json())
                    else:
                        async with session.post(hook, json={"embeds": [{"title": "New Snipe!", "description": f"Name: `{target_username}`\n Person: <@760100933098274868>", "color": 1583209}]}) as r:
                            if r.status == 200 or r.status == 204:
                                logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.RESET} sent webhook of snipe!")
                            else:
                                logging.info(r.status)
                                logging.info(await r.json())
            except FileNotFoundError:
                pass


async def get_name_of_the_week():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://announcements-api.herokuapp.com/api/v1/nameoftheweek") as r:
            name_json = await r.json()
            name = name_json["name"]
            custom_info(f"Opening {name} in namemc!")
            try:
                webbrowser.open_new_tab(f"https://namemc.com/name/{name}")
                custom_input("press enter to quit: ")
            except Exception:
                print("failed to open name!")
                custom_input("press enter to quit: ")


def gather_info():
    block_snipe = menu(options=["Snipe name", "Block Name", "Open name of the week in namemc"])
    if block_snipe == 2:
        asyncio.get_event_loop().run_until_complete(get_name_of_the_week())
        quit()
    target_username = custom_input(f"What name you would you like to {['snipe', 'block'][block_snipe]}: ")
    try:
        delay = int(custom_input("Custom delay in ms: "))
    except ValueError:
        print('thats not a valid number')
    return block_snipe, target_username, delay


def load_accounts_file():
    accounts = []
    if not path.exists("accounts.txt"):
        print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} accounts.txt not found | creating one")
        open('accounts.txt', 'w+')
        input("Press enter to reload accounts. ")
        load_accounts_file()
    else:
        accounts = open('accounts.txt').readlines()
        if len(accounts) == 0:
            print(f"Accounts not found in accounts.txt file please add accounts with format (email:pass) or (email:pass:q1:q2:q3)")
            input("Press any key to reload accounts.")
            load_accounts_file()
        if len(accounts) < 3:
            for i in range(len(accounts)):
                accounts.append(accounts[i])
            custom_info("You had less than 3 accounts | Using 2 of each account")
        if len(accounts) > 30:
            print(f"{Fore.WHITE}[{Fore.YELLOW}warning{Fore.WHITE}]{Fore.RESET} you inputted too many accounts | removing {len(accounts) - 30}")
            accounts = accounts[0:30]
    return accounts


def load_accounts():
    accounts = []
    for acc in load_accounts_file():
        acc = acc.rstrip().split(":")
        if acc == ['']:
            continue
        try:
            accounts.append(Account(acc[0], acc[1], [acc[2], acc[3], acc[4]]))
        except IndexError:
            accounts.append(Account(acc[0], acc[1]))
    return accounts


class session:
    block_snipe = ["Snipe", "block"]

    def __init__(self, target_username, accounts, block_snipe, snipe_delay):
        self.target_username = target_username
        self.accounts = accounts
        self.block_snipe = block_snipe
        self.snipe_delay = snipe_delay
        loop = asyncio.get_event_loop()
        self.drop_time = loop.run_until_complete(time_snipe(self.target_username, self.block_snipe))
        self.setup_time = self.drop_time - timedelta(seconds=55)
        self.setup = False
        self.ran = False
        self.drop_time = self.drop_time - timedelta(milliseconds=self.snipe_delay)

    def run(self):
        loop = asyncio.get_event_loop()
        while True:
            now = datetime.utcnow()
            if now >= self.drop_time and not self.ran:
                try:
                    start = time.time()
                    loop.run_until_complete(self.send_requests())
                except RuntimeError:
                    pass
                end = time.time()
                elapsed_time = end - start
                for acc in self.accounts:
                    if acc.got_name:
                        asyncio.get_event_loop().run_until_complete(self.webhook_skin_file(acc))
                rq_sec = self.num_reqs * len(accounts) / elapsed_time
                times.append(rq_sec)
                logging.info(f"{Fore.GREEN}{str(sum(times))[0:13]}{Fore.CYAN} rqs/sec (ESTIMATE) {Fore.WHITE}|{Fore.CYAN} Took {Fore.WHITE}{str(elapsed_time)[0:8]}{Fore.CYAN} seconds{Fore.RESET} | {self.num_reqs * len(accounts)} requests")
                if len(sys.argv) < 3:
                    custom_input("press enter to quit: ")
                quit()
            elif now >= self.setup_time and not self.setup:
                loop.run_until_complete(self.run_auth())
                for acc in accounts:
                    if acc.failed_auth:
                        logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] Removing account: {acc.email} | auth failed")
                        accounts.remove(acc)
                if len(accounts) == 0:
                    logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] you have 0 accounts available to snipe on! | quitting program...")
                    quit()
                custom_info("setup complete")
                self.setup = True
            time.sleep(.00001)

    async def webhook_skin_file(self, acc):
        await acc.webhook_skin_write_file()

    async def send_requests(self):
        async with aiohttp.ClientSession() as session:
            if self.block_snipe == 0:
                self.num_reqs = 8
                self.coros = [
                    acc.snipe_req(session, self.target_username) for acc in self.accounts for _ in range(self.num_reqs)
                ]
            elif self.block_snipe == 1:
                self.num_reqs = 3
                self.coros = [
                    acc.block_req(session, self.target_username) for acc in self.accounts for _ in range(self.num_reqs)
                ]
            await asyncio.wait(self.coros)

    async def run_auth(self):
        async with aiohttp.ClientSession() as session:
            coros = [
                acc.authenticate(session, self.accounts.index(acc) * .5) for acc in self.accounts
            ]
            await asyncio.wait(coros)


print_title()
accounts = load_accounts()
try:
    target_username = sys.argv[1]
    block_snipe = sys.argv[2]
    if str(block_snipe).lower() == "snipe" or str(block_snipe) == "0":
        block_snipe = 0
    if str(block_snipe).lower() == "block" or str(block_snipe) == "1":
        block_snipe = 1
    try:
        snipe_delay = int(sys.argv[3])
    except IndexError:
        if block_snipe == 0:
            snipe_delay = 900
        else:
            snipe_delay = 200
except IndexError:
    block_snipe, target_username, snipe_delay = gather_info()

session = session(target_username, accounts, block_snipe, snipe_delay)
session.run()

