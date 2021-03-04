import time

import ewcfg
import ewutils
import ewstats
from ew import EwPlayer

# Returns a user's life state/gang color as a discord.Colour object
def get_tweet_color(user_data):
    if user_data.life_state < 2:
        color = ewcfg.tweet_color_by_lifestate.get(user_data.life_state)
    else:
        color = ewcfg.tweet_color_by_faction.get(user_data.faction)

    if color is None:   
        color = ewutils.discord.Embed.Empty
    else:
        color = ewutils.discord.Colour(int(color, 16))

    return color

async def tweet(cmd):
    
    user_data = EwPlayer(id_user=cmd.message.author.id, id_server=cmd.guild.id)
    
    if user_data.has_gellphone():

        if cmd.tokens_count < 2:
            response = "Tweet what?"
            return await ewutils.send_response(response, cmd)

        tweet_content = ' '.join("`{}`".format(token) if token.startswith("#") else token for token in cmd.tokens[1:])
        # embed limits
        if len(tweet_content) > 280:
            response = "Alright there bud, slow down a bit. No one's gonna read all that ({}/280).".format(len(tweet_content))
            return await ewutils.send_response(response, cmd)

        tweet = ewutils.discord.Embed()

        tweet.set_thumbnail(url = cmd.message.author.avatar_url)
        # we use the description to set the author since members cannot be mentioned from the author field
        checkmark = ewcfg.emote_verified if user_data.verified else ""
        tweet.description="<@!{}>{}".format(cmd.message.author.id, checkmark)
        tweet.color = get_tweet_color(user_data)

        # \u200b is a whitespace character, since we cannot leave field names empty
        tweet.add_field(name='\u200b', value = tweet_content)

        # works as long as the first attachment is an image
        # other file types are ignored
        if len(cmd.message.attachments) > 0:
            tweet.set_image(url=cmd.message.attachments[0].url)

        channel = ewutils.get_channel(server=cmd.guild, channel_name=ewcfg.channel_slimetwitter)

        await ewutils.send_message(cmd.client, channel, embed=tweet)

    else:
        response = "You need to have a gellphone to !tweet."
        return await ewutils.send_response(response, cmd)

async def verification(cmd):

    user_data = EwPlayer(member=cmd.message.author)
    
    if user_data.poi == ewcfg.poi_id_slimecorphq:

        if user_data.verified:
            response = "*Huh? You're already verified! Get outta here you goofster!*"
            return await ewutils.send_response(response, cmd)

        time_now = int(time.time())
        time_in_server = time_now - user_data.time_joined

        if time_in_server >= 60 * 60 * 24 * 180: # 6 months

            lifetime_slime = user_data.get_stat(metric=ewcfg.stat_lifetime_slimes)
            # you can use haunted slimes too cause we're nicer to ghosts than we should be
            lifetime_haunted = user_data.get_stat(metric=ewcfg.stat_lifetime_slimeshaunted)

            if lifetime_slime > 1000000000 or lifetime_haunted > 100000000:

                user_data.verified = True
                user_data.persist()
                response = "*Alright, everything checks out. Congratulations, you're #verified now.*"#TODO emote

            else:
                response = "*Yeah, sorry, looks but it like you don't love slime enough. Try getting some more slime, then come back. Freak.*"
                
                if user_data.life_state != ewcfg.life_state_corpse:
                    response += " ({current:,}/{needed:,} lifetime slime)".format(current=lifetime_slime, needed=1000000000)
                else:
                    response += " ({current:,}/{needed:,} lifetime slime haunted)".format(current=lifetime_haunted, needed=100000000)
        else:
            response = "*We can't just verify any random schmuck who wanders into our city, it'd be a bad look. Stick around for a while, then we'll consider verifying you.*"
    else:
        if user_data.poi == ewcfg.poi_id_stockexchange:
            response = "*Hey buddy, I think you got the wrong door, the HQ's two blocks down.*"
        else:
            response = "Only the Slimecorp employees at the HQ can get you verified on Slime Twitter."

    return await ewutils.send_response(response, cmd)