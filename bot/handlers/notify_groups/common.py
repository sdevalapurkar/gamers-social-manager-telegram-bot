from telegram import Bot, ChatMember
from telegram.utils.helpers import escape_markdown
from handlers.common import get_one_mention, get_many_mentions


def stringify_notify_group(bot: Bot, notify_group: dict):
    """
    Given a dictionary that contains fields of a notify group, this function
    will return a formatted string message that displays this notify group.
    """
    # Set up all the string vars for the notify group info
    notify_group_name = escape_markdown(notify_group["name"], 2)
    creator_mention = get_one_mention(
        bot, notify_group['creator_id'], notify_group['chat_id']
    )
    creator_status = bot.get_chat_member(notify_group["chat_id"],
                                         notify_group['creator_id']).status
    if creator_status in [ChatMember.KICKED, ChatMember.LEFT]:
        creator_mention += f" *\[Left the group\]*"

    notify_group_description = (escape_markdown(notify_group["description"], 2)
                                if notify_group["description"] else "None")

    # Add current members
    if notify_group["members"]:
        left_members_mentions = []
        members_str = ""
        for member_id in notify_group["members"]:
            member_status = bot.get_chat_member(notify_group["chat_id"],
                                                member_id).status
            user_mention = get_one_mention(bot, member_id,
                                           notify_group['chat_id'])
            if member_status in [ChatMember.KICKED, ChatMember.LEFT]:
                # Store a list of the mentions of members who are left so we
                # can add them at the end
                left_members_mentions.append(f"{user_mention} *\(Left the group\)*\n")
            else:
                members_str += f"{user_mention}\n"

        # Append the members who have left at the end of the members list
        for mention in left_members_mentions:
            members_str += f"{mention}\n"
    else:
        members_str = "`None`"


    invited_str = ""
    if notify_group["invited"]:
        invited_users_identifiers = [user_identifier for user_identifier
                                     in notify_group["invited"]]
        invited_str += get_many_mentions(bot, notify_group["chat_id"],
                                         invited_users_identifiers)
    else:
        invited_str = "`None`"

    return (
        f"`{notify_group_name}` _\(Created by {creator_mention}\)_\n"
        "__Group Description__\n"
        f"`{notify_group_description}`\n"
        "__Current Members__\n"
        f"{members_str}"
        "__Invited Users__\n"
        f"{invited_str}"
    )
