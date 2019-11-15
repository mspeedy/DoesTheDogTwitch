# -*- coding: utf8 -*-
from apis.doesthedogdie import get_info_for_movie
import json
import requests
import sys

from dtdd_api import shorten
from twitchio.ext import commands
import config
try:
    from config import only_show_yes
except:
    print("⚠ Please set only_show_yes in your config.py")
    only_show_yes = False
try:
    from config import use_memcache
except:
    use_memcache = False
try:
    from config import use_dtdd_web_api
    if use_dtdd_web_api:
        try:
            from config import dtdd_web_api_address
        except ImportError:
            print("⚠ Please set dtdd_web_api_address in your config.py")
            use_dtdd_web_api = False
except:
    print("⚠ Please set use_dtdd_web_api in your config.py")
    use_dtdd_web_api = False

try:
    from config import use_short_names
except:
    print("⚠ Please set use_short_names in your config.py")
    use_short_names = False


def yes_or_no_formatter(topic):
    action = "Unsure"
    
    if topic['yes_votes'] > topic['no_votes']:
        action = "Yes"
    elif topic['no_votes'] > topic['yes_votes']:
        action = "No"
    return "{topic} : {action} (Yes: {yes_votes} | No : {no_votes})\n".format(topic=topic['topic'], yes_votes=topic['yes_votes'], no_votes=topic['no_votes'], action=action), action, topic['topic_short']

def generate_warning(movie):
    # movie1 = dict(title=movie)
    #
    # to_write = []
    if use_dtdd_web_api:
        print("⏩ Getting data from faster web API")
    else:
        print("🐶 Getting data from DoesTheDogDie.com")
        if not use_memcache:
            print("⚠ You aren't using a memcache or an external API for DTDD - this will take a while")

    topics = get_info_for_movie(movie)

    if topics == None:
        return {"error": "cannot find movie"}, 404
    for status in topics:
        if status.get('topic_short', None) is None:
            status['topic_short'] = shorten(status['topic'])

    topic_list = 'This game may contain: '

    for topic in topics:
        if topic['yes_votes'] > topic['no_votes']:
            topic_list = topic_list + topic['topic_short'] + ', '

    topic_list = topic_list[:len(topic_list) - 1]

    return topic_list



class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=config.oauth_token, client_id='NotSoSpeedRuns', nick='NotSoSpeedBot', prefix='!',
                         initial_channels=['NotSoSpeedRuns'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    # Commands use a decorator...
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

def main():
    bot = Bot()
    bot.run()
    pass

if __name__ == "__main__":
    main()
