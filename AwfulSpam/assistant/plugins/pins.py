from telethon import events, Button, types
from AwfulSpam.event import *


@Rood.on(events.NewMessage(pattern="^[?!/]pinned"))
async def get_pinned(event):
  if event.is_group:
     chat_id = (str(event.chat_id)).replace("-100", "")
     Ok = await Rood.get_messages(event.chat_id, ids=types.InputMessagePinned()) 
     tem = f"The pinned message in {event.chat.title} is <a href=https://t.me/c/{chat_id}/{Ok.id}>here</a>."
     await event.reply(tem, parse_mode="html", link_preview=False)

@Rood.on(events.NewMessage(pattern="^[!?/]pin ?(.*)"))
@is_admin
async def pin(event, perm):
   if event.is_group:
       if not perm.pin_messages:
          await event.reply("You are missing the following rights to use this command:CanPinMsgs.")
          return
       msg = await event.get_reply_message()
       if not msg:
          await event.reply("Reply To Msg")
          return
       input_str = event.pattern_match.group(1)
       if "notify" in input_str:
          await Rood.pin_message(event.chat_id, msg, notify=True)
          return
       await Rood.pin_message(event.chat_id, msg)   

@Rood.on(events.NewMessage(pattern="^[!?/]unpin ?(.*)"))
@is_admin
async def unpin(event, perm):
   if event.is_group:
       if not perm.pin_messages:
          await event.reply("You are missing the following rights to use this command:CanPinMsgs.")
          return
       chat_id = (str(event.chat_id)).replace("-100", "")
       ok = await Rood.get_messages(event.chat_id, ids=types.InputMessagePinned())
       await Rood.unpin_message(event.chat_id, ok)
       await event.reply(f"Successfully Un-Pinned [this](t.me/{event.chat.username}/{ok.id}) message.", link_preview=False)

@Rood.on(events.NewMessage(pattern="^[!?/]permapin"))
@is_admin
async def permapin(event, perm):
   if event.is_group:
       if not perm.pin_messages:
          await event.reply("You are missing the following rights to use this command:CanPinMsgs.")
          return
       msg = await event.get_reply_message()
       if not msg:
          await event.reply("Reply To Msg To Permapin it.")
          return
       hn = await Rood.send_message(event.chat_id, msg.message)
       await Rood.pin_message(event.chat_id, hn, notify=True)


@Rood.on(events.NewMessage(pattern="^[!?/]unpinall"))
async def unpinall(event, perm):
   if event.is_group:
       if not perm.pin_messages:
          await event.reply("You are missing the following rights to use this command:CanPinMsgs!")
          return
       UNPINALL = """
Are you sure you want to 
unpin all msgs?
This action can't be undone!
"""

       await Rood.send_message(event.chat_id, UNPINALL, buttons=[
       [Button.inline("Confirm", data="unpin")], 
       [Button.inline("Cancel", data="cancel")]])


@Rood.on(events.callbackquery.CallbackQuery(data="unpin"))
async def confirm(event):
    check = await event.client.get_permissions(event.chat_id, event.sender_id)
    if check.is_creator:
        await Rood.unpin_message(event.chat_id)
        await event.edit("Unpinned All Msgs!")
        return 

    await event.answer("Group Creator Required!")

@Rood.on(events.callbackquery.CallbackQuery(data="cancel"))
async def cancel(event):

    check = await event.client.get_permissions(event.chat_id, event.sender_id)
    if check.is_creator:
        await event.edit("Un-Pinning All Msgs Has Been Cancelled!")
        return 

    await event.answer("Group Creator Required!")

