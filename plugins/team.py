from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template
import pprint


class TeamPlugin(WillPlugin):

    @hear("(?P<before>.*)@team(?P<after>.*)")
    def send_to_team(self, message,before,after):
        channel = self.get_room_from_message(message)['name']
        notification_list = self.load("team_" + channel, None)
        if notification_list:
            self.say("{} said: {}team{} ({})".format(message.sender.nick, before, after, ' '.join('@'+user for user in notification_list)), room=self.get_room_from_message(message), notify=True)

    @respond_to("^add (@?)(?P<user>\S+) to (?:this) team")
    def add_to_team(self, message, user):
        """
        add [user] to this team: request to be notified when someone mentions team
        """
        if user == "me":
            user = message.sender.nick
        channel = self.get_room_from_message(message)['name']
        notification_list = self.load("team_" + channel, None)
        if not notification_list:
            notification_list = []
        notification_list.append(user)
        notification_list = list(set(notification_list))
        self.save('team_' + channel, notification_list)
        self.reply(message, "team for {} is now: {}".format(channel, ', '.join(user for user in notification_list)))

    @respond_to("^remove (@?)(?P<user>\S+) from this team")
    def remove_from_team(self, message, user):
        """
        remove [user] from this team: remove a person from this team
        """
        if user == "me":
            user = message.sender.nick
        channel = self.get_room_from_message(message)['name']
        notification_list = self.load("team_" + channel, None)
        if not notification_list:
            notification_list = []
        notification_list.remove(user)
        notification_list = list(set(notification_list))
        self.save('team_' + channel, notification_list)
        self.reply(message, "team for {} is now: {}".format(channel, ', '.join(user for user in notification_list)))

    @respond_to("^who is on this team")
    def check_team(self, message):
        """
        who is on this team: see the notification list for a token
        """
        channel = self.get_room_from_message(message)['name']
        notification_list = self.load("team_" + channel, None)
        self.reply(message, "Team for {}:  {}".format(channel, ', '.join(notification_list)))


