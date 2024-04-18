import pyodbc as db 


class Db_driver():
    def __init__(self, db_location = r"D:\testbereich\discordbot\W4tcher\watcher.accdb"): 
        con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + f'{db_location}'
        conn = db.connect(con_string)
        self.cur = conn.cursor() 


    def search_for_author(self,data, value = ""):
        try:
            command_search_for_author = f'SELECT * FROM Author Where DiscordID  = {data["id"]};'
            self.cur.execute(command_search_for_author)
            Name =  self.cur.fetchall()[0]
            return_tuple = ""
            if value == "id":
                 return_tuple = Name[0]
            
            elif value == "DID":
                 return_tuple = Name[1]

            elif value == "Name":
                 return_tuple = Name[2]
            
            elif value == "Disk":
                 return_tuple = Name[3]
            
            if (Name[2] == data["name"]):
                return (True , return_tuple)
            else: 
                return (False, "None")

        except IndexError as e:
                return False


    def search_for_channel(self,data, value = ""):
        try:
            command_search_for_channel = f'SELECT * FROM Kanal WHERE DiscordID  = {data["id"]};'
            self.cur.execute(command_search_for_channel)
            Channel = self.cur.fetchall()[0]
            return_tuple = ""
            if value == "id":
                 return_tuple = Channel[0]
            
            elif value == "DID":
                 return_tuple = Channel[1]

            elif value == "Name":
                 return_tuple =  Channel[2]

            else:
                 return_tuple = "None"

            if (Channel[2] == data["name"]):
                return (True , return_tuple)
            else: 
                return (False, "None")

        except IndexError as e:
                return False


    def insert_author(self, data):
        command_insert_into_Author = f"INSERT INTO Author (DiscordID, Name, Discriminator) VALUES ({data['id']}, '{data['name']}', '{data['discriminator']}');"
        #return command_insert_into_Author
        self.cur.execute(command_insert_into_Author)
        self.cur.commit()
        return True


    def insert_channel(self,data):
        command_insert_into_Channel = f"INSERT INTO Kanal (DiscordID, KanalName) VALUES ({data['id']}, '{data['name']}');"
        #return command_insert_into_Author
        self.cur.execute(command_insert_into_Channel)
        self.cur.commit()
        return True


    def save_message(self, message):
        
        author_exists = self.search_for_author(data=message["author"], value="id")
        channel_exists =  self.search_for_channel(data=message["channel"], value="id")
        
        if not(author_exists[0]):
            self.insert_author(data=message["author"] )
            
        if not(channel_exists[0]):
            self.insert_channel(data=message["author"])

        command_insert_into_message = f"INSERT INTO Nachrichten (Nachricht, Author, Datum, Kanal) VALUES ('{message['content']}',{author_exists[1]},{message['timestamp']}, {channel_exists[1]});"
        if channel_exists[0] and author_exists[0]:
            self.cur.execute(command_insert_into_message)
            self.cur.commit()
             

# p1 = Db_driver()
# p1.save_message(message=message)
pass