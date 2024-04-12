import os
from pyrogram import Client, filters
from main.utils import progress_message, humanbytes

# Initialize the Pyrogram client
app = Client("file_renamer_bot")

# Define the admin user ID (replace with your admin user ID)
ADMIN = "your_admin_user_id"

# Command handler to rename files
@app.on_message(filters.private & filters.command("rename") & filters.user(ADMIN))             
async def rename_file(bot, msg):
    # Check if the command is accompanied by a reply to a message
    if len(msg.command) < 2 or not msg.reply_to_message:
        return await msg.reply_text("Please reply to a file with the desired new filename.")
    
    # Extract the replied message
    reply = msg.reply_to_message
    
    # Check if the replied message contains a document, audio, or video
    media = reply.document or reply.audio or reply.video
    if not media:
        return await msg.reply_text("Please reply to a file with the desired new filename.")
    
    # Get the original media file and the new filename from the command
    og_media = getattr(reply, reply.media.value)
    new_name = msg.text.split(" ", 1)[1]
    
    # Download the file and rename it
    downloaded = await reply.download(file_name=new_name, progress=progress_message, progress_args=("Downloading...",))
    
    # Prepare the caption for the renamed file
    filesize = humanbytes(og_media.file_size)
    cap = f"{new_name}\n\n💽 Size: {filesize}"
    
    # Send the renamed file with the original caption
    await bot.send_document(
        chat_id=msg.chat.id,
        document=downloaded,
        caption=cap,
        progress=progress_message,
        progress_args=("Uploading...",)
    )
    
    # Clean up: remove the downloaded file
    os.remove(downloaded)

# Run the bot
app.run()
