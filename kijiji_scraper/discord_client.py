#!/bin/usr/env python3
import discord
import requests

class DiscordClient():

    def __init__(self, discord_config):
        with requests.Session() as session:
            self.webhook = discord.SyncWebhook.from_url(discord_config.get("webhook"), session=session)
            self.bot_name = discord_config.get("bot name")

            url_params = discord_config.get("webhook").split('?')
            if (len(url_params) > 1):
                if (url_params[1][0:9]=="thread_id"):
                    self.thread_id = discord.Object(url_params[1].split('=')[1], type=discord.abc.Snowflake)

    # Sends a Discord message with links and info of new ads
    def send_ads(self, ad_dict, discord_title):
        title = self.__create_discord_title(discord_title, len(ad_dict))

        if hasattr(self,'thread_id'):
            result = self.webhook.send(content=f"**{title}**", username=self.bot_name, thread=self.thread_id)
        else:
            result = self.webhook.send(content=f"**{title}**", username=self.bot_name)

        for ad_id in ad_dict:
            embed = self.__create_discord_embed(ad_dict, ad_id)
            
            if hasattr(self,'thread_id'):
                result = self.webhook.send(embed=embed, username=self.bot_name, thread=self.thread_id)
            else:
                result = self.webhook.send(embed=embed, username=self.bot_name)

    def __create_discord_title(self, discord_title, ad_count):
        if ad_count > 1:
            return str(ad_count) + ' New ' + discord_title + ' Ads Found!'

        return 'One New ' + discord_title + ' Ad Found!'

    def __create_discord_embed(self, ad_dict, ad_id):

        embed = discord.Embed()
        embed.colour = discord.Colour.green()
        embed.url=ad_dict[ad_id]['Url']

        try:
            embed.title = f"{ad_dict[ad_id]['Title']}"

            if ad_dict[ad_id]['Location'] != "":
                embed.add_field(name="Location", value=ad_dict[ad_id]['Location'])

            if ad_dict[ad_id]['Date'] != "":
                embed.add_field(name="Date", value=ad_dict[ad_id]['Date'])
            
            if ad_dict[ad_id]['Price'] != "":
                embed.add_field(name="Price", value=ad_dict[ad_id]['Price'])

            if ad_dict[ad_id]['Description'] != "":
                embed.add_field(name="Description", value=ad_dict[ad_id]['Description'], inline=False)

            if ad_dict[ad_id]['Details'] != "":
                embed.add_field(name="Details", value=ad_dict[ad_id]['Details'], inline=False)
            
        except KeyError:
            embed.title = f"{ad_dict[ad_id]['Title']}"

        return embed