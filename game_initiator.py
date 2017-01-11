from twilio.rest import TwilioRestClient
import json
import pprint
from random import randint
import random


class SHGameInitiator(object):

    account_sid = "REDACTED"
    auth_token = "REDACTED"

    sample_file = [
        {"Player": {
            "Name": "Yaz",
            "Phone": "917-963-7705"
        }},
        {"Player": {
                    "Name": "Yaz",
                    "Phone": "917-963-7705"
        }},
        {"Player": {
                    "Name": "Yaz",
                    "Phone": "917-963-7705"
        }},
        {"Player": {
                    "Name": "Yaz",
                    "Phone": "917-963-7705"
        }},
        {"Player": {
                    "Name": "Yaz",
                    "Phone": "917-963-7705"
        }},
        {"Player": {
                     "Name": "Yaz",
                    "Phone": "917-963-7705"
        }},
        {"Player": {
                    "Name": "Yaz",
                    "Phone": "917-963-7705"
        }},
        {"Player": {
                     "Name": "Yaz",
                    "Phone": "917-963-7705"
        }}
    ]

    roles_dict = {
        1: "SH",
        2: "Fascist",
        3: "Liberal"
    }

    player_number_to_role_dict = {
        5: [1, 1, 3],
        6: [1, 1, 4],
        7: [1, 2, 4],
        8: [1, 2, 5],
        9: [1, 3, 5],
        10: [1, 3, 6]
    }

    def __init__(self):
        self.game_id_to_player_name_dict = {}
        self.game_id_to_player_number_dict = {}
        self.game_id_to_player_role_dict = {}
        self.player_name = None
        self.player_phone_number = None
        self.gamer_id = None
        self.player_number = None
        self.sh_name = None
        self.twilio_phone = None

    def generate_game(self):
        #self._get_player_input()
        self._build_random_values()
        #self._get_player_number()
        player_spread = self._get_player_role()
        self._assign_roles(player_spread)
        #pprint.pprint(player_spread)
        self._send_roles()

    def _send_roles(self):
        sh_id = None
        fascist_list_id = []
        liberal_list_id = []
        for key, value in self.game_id_to_player_role_dict.iteritems():
            if value == "SH":
                self.sh_id = key
                self._message_sh(key)
            elif value == "Fascists":
                self._message_fascists(key)
            else:
                self._message_liberals(sh_id, "Liberals")
    def _message_sh(self, key):
        self.sh_name = self.game_id_to_player_name_dict.get(key)
        sh_phone = self.game_id_to_player_number_dict.get(key)
        sh_message = "You are SH"
        self._message_phone(sh_phone, sh_message)

    def _message_fascists(self, key):
        fascist_name = self.game_id_to_player_name_dict.get(key)
        fascist_phone = self.game_id_to_player_number_dict.get(key)
        fascist_message = "You are a Fascist. SH is " + str(self.sh_name)
        self._message_phone(fascist_phone, fascist_message)

    def _message_liberals(self, key):
        liberal_name = self.game_id_to_player_name_dict.get(key)
        liberal_phone = self.game_id_to_player_number_dict.get(key)
        liberal_message = "You are a Liberal"
        self._message_phone(liberal_phone, liberal_message)

    def _message_phone(self, phone, message):
        account_sid = SHGameInitiator.account_sid
        auth_token = SHGameInitiator.auth_token
        client = TwilioRestClient(account_sid, auth_token)
        message = client.message.create(to=phone, from_=self.twilio_phone, body=message)


    def _build_random_values(self):
        self.player_number = 8
        for key in SHGameInitiator.sample_file:
            print key
            name = key.get("Player").get("Name")
            phone = key.get("Player").get("Phone")
            self.gamer_id = randint(0, 99)
            self.game_id_to_player_name_dict[self.gamer_id] = name
            self.game_id_to_player_number_dict[self.gamer_id] = phone
        pprint.pprint(self.game_id_to_player_name_dict)
        pprint.pprint(self.game_id_to_player_number_dict)


    def _assign_roles(self, player_list):
        gamer_id_list = self.game_id_to_player_name_dict.keys()
        print gamer_id_list
        print player_list
        for role_index in range(self.player_number):
            #self._shuffle_player_spread(player_list)
            print role_index
            #role = player_list[role_index]
            role = random.choice(player_list)
            random_id = random.choice(gamer_id_list)
            self.game_id_to_player_role_dict[random_id] = role
            print self.game_id_to_player_role_dict
            player_list.remove(role)
            gamer_id_list.remove(random_id)
        pprint.pprint(self.game_id_to_player_role_dict)


    def _shuffle_player_spread(self, player_list):
        return random.shuffle(player_list)

    def _get_player_role(self):
        game_id_to_player_role_dict = {}
        game_spread_list = []
        player_spread_list = SHGameInitiator.player_number_to_role_dict.get(self.player_number)
        for spread in range(3):
            key_lookup = spread + 1
            role = SHGameInitiator.roles_dict[key_lookup]
            role_amount = player_spread_list[spread]
            role_begin = 0
            while role_begin < role_amount:
                game_spread_list.append(role)
                role_begin += 1

        pprint.pprint(game_spread_list)
        return game_spread_list

    def _get_player_input(self):

        player_number = self._get_player_number()
        for player in range(player_number):
            self.gamer_id = randint(0, 99)
            self.player_name = raw_input("Enter Your First Name: ")
            self.player_phone_number = raw_input("Enter Your Phone Number: ")
            self.game_id_to_player_name_dict[self.gamer_id] = self.player_name
            self.game_id_to_player_number_dict[self.gamer_id] = self.player_phone_number

        pprint.pprint(self.game_id_to_player_name_dict)
        pprint.pprint(self.game_id_to_player_number_dict)


    def _get_player_number(self):
        self.player_number = int(raw_input("Enter a Number between 5-10: "))
        player_normalized = self.player_number - 1
        return player_normalized

if __name__  == "__main__":
    print "game init"
    game_start = SHGameInitiator()
    game_start.generate_game()
