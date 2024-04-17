import pyodbc as db 
db_location = r"D:\testbereich\discordbot\W4tcher\watcher.accdb"
con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + f'{db_location}'
conn = db.connect(con_string)
cur = conn.cursor() 

# data = {
#         "author": {
#             "id": str(author.id),
#             "name": author.name,
#             "discriminator": author.discriminator,
#         },
#         "content": message.content,
#         "timestamp": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
#         "channel": {
#             "id": str(message.channel.id),
#             "name": message.channel.name
#         }
#     }







# def save_message(message):
#     author_exists = search_for_author(data=data["author"], cur=cur)
#     channel_exists =  search_for_channel(data=data["channel"],  cur=cur)
#     if not(author_exists):
#         insert_author(data=data["author"], cur=cur)




def search_for_author(data, cur):
    try:
        command_search_for_author = f'SELECT * FROM Author Where DiscordID  = {data["id"]};'
        author = cur.execute(command_search_for_author)
        #print(cur.fetchall())
        Name =  cur.fetchall()[0][2] 
        if not(Name == ''):
            return True

    except IndexError as e:
            return False

def search_for_channel(data, cur):
    command_search_for_author = f'SELECT * FROM Kanal WERE DiscordID  = {data["id"]};'
    author = cur.execute(command_search_for_author)
    
    if author:
        return True
    else:
        return False

def insert_author(data, cur):
    command_insert_into_Author = f"INSERT INTO Author (ID, DiscordID, Name, Discriminator) VALUES (NULL, {data['id']}, {data['name']}, {data['discriminator']});"
    cur.execute(command_insert_into_Author)
    return True

command = 'create table if NOT EXIST Messages(ID INT not null auto_increment unique key primary key ,vorname varchar(32) )'