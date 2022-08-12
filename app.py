from multiprocessing.sharedctypes import Value
import discord
import sys
from discord.ui import Button, View, Select
from discord.ext import commands
import sys
# Prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=">", help_command=None, intents=intents)


# STATUT
@bot.event
async def on_ready():
    print("Le bot est prêt.")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Bot from discord server Pycringe, by BerretMan"))

list_of_player=[]
@commands.has_permissions(manage_roles=True)
@bot.command()
async def duel(ctx, mention):
    oui_button = ColorButton("oui", "green", ctx)
    non_button = ColorButton("non", "red", ctx)
    view = View()
    view.add_item(oui_button)
    view.add_item(non_button)
    Lamention=mention[2:-1]
    list_of_player= [ctx.author.id,int(Lamention)]
    print(list_of_player)
    await ctx.send(f"{ctx.author.mention} veux te défier au morpion. mention Acceptes tu? {mention}", view=view)
    
def createEmbed(list):
    embed = discord.Embed(title="Morpion", description="Just a basic morpion game, by BerretMan", color=0x72d345)
    for z in range(1):
        embed.add_field(name=f"{list}", value="\n\u200b", inline=False)
    return embed


class ColorButton(Button):
    def __init__(self, label, color, ctx, url=None, emoji=None):
        self.play = True
        self.ctx = ctx
        if color == "red":
            super().__init__(label=label, style=discord.ButtonStyle.red, url=url, emoji=emoji)
        if color == "green":
            super().__init__(label=label, style=discord.ButtonStyle.green, url=url, emoji=emoji)
        if color == "grey":
            super().__init__(label=label, style=discord.ButtonStyle.grey, url=url, emoji=emoji)

    async def callback(self, interaction):
        if self.label == "oui":
            
            await interaction.response.send_message(f"Duel accepté")
            global T
            T = Game(self.ctx)
            await T.gameloop()
        else:
            await interaction.response.send_message(f"Duel refusé")
            
class ChooseButton(Button):
    def __init__(self, label, color, url=None, emoji=None):
        self.condition=False
        if color == "red":
            super().__init__(label=label, style=discord.ButtonStyle.red, url=url, emoji=emoji)
        if color == "green":
            super().__init__(label=label, style=discord.ButtonStyle.green, url=url, emoji=emoji)
        if color == "grey":
            super().__init__(label=label, style=discord.ButtonStyle.grey, url=url, emoji=emoji)
    async def callback(self, interaction):
        ChooseButton.disabled=True
        await interaction.response.defer()
        await T.play(self.label)
        

class Game:
    def __init__(self,ctx):
        self.board = f'[A,B,C]\n[D,E,F]\n[G,H,I]'
        self.discord = self.DiscordEmoji()
        self.p0 = "X"
        self.p1 = "O"
        self.case = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.ctx = ctx
        self.play_c=""
        self.list_player = [self.p0, self.p1]
        self.message = "ta mere la pute"
        self.i = 0
        self.id=[]
    def check(self,msg):
        return msg.author == self.ctx.author and msg.channel == self.ctx.channel and \
        msg.content.lower() in ["y", "n"]
    def DiscordEmoji(self):
        self.discord=self.board
        char_to_replace = {
            "A":"<:zero:1007226065367863296>",
            "B":"<:one:1007226270305747014>",
            "C":"<:two:1007226307622490163>",
            "D":"<:three:1007228548119019520>",
            "E":"<:four:1007228671540600843>",
            "F":"<:five:1007228728172089356>",
            "G":"<:six:1007228772623327313>",
            "H":"<:seven:1007228856127729745>",
            "I":"<:eight:1007229323503226920>",
            "X":"<:x:1007230229619683418>",
            "O":"<:o:1007264839535693895>",
            "[":"",
            "]":"",
            ",":""
        }
        for key, value in char_to_replace.items():
            self.discord = self.discord.replace(key, value)
        print(self.discord)
        return createEmbed(self.discord)
    async def game(self):
        self.i+=1
        global x
        x = self.i % 2
    async def gameloop(self):
        print(self.board)
        self.i+=1
        global x
        x = self.i % 2
        print(x)
        button0 = ChooseButton("0", "grey")
        button1 = ChooseButton("1", "grey")
        button2 = ChooseButton("2", "grey")
        button3 = ChooseButton("3", "grey")
        button4 = ChooseButton("4", "grey")
        button5 = ChooseButton("5", "grey")
        button6 = ChooseButton("6", "grey")
        button7 = ChooseButton("7", "grey")
        button8 = ChooseButton("8", "grey")
        view = View(timeout=None)
        view.add_item(button0)
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        view.add_item(button5)
        view.add_item(button6)
        view.add_item(button7)
        view.add_item(button8)
        self.message = await self.ctx.send(embed=self.discord,view=view)
        
    async def play(self,case):
        convert_list=[(0,"A"),(1,"B"),(2,"C"),(3,"D"),(4,"E"),(5,"F"),(6,"G"),(7,"H"),(8,"I")]
        print(case)
        self.board = self.board.replace(convert_list[int(case)][1], self.list_player[x])
        print(self.board)
        print("he oh")
        self.discord = self.DiscordEmoji()
        await self.message.edit(embed=self.discord)
        if self.WinCondition():           
            await self.game()
        else:
            await self.ctx.send(f"Player {self.list_player[x]} Wins")
            sys.exit()
    def WinCondition(self):
        n_case = [1, 3, 5, 9, 11, 13, 17, 19, 21]
        s = [self.board[n_case[x]] for x in range(9)]
        # ligne
        if s[0] == s[1] == s[2] or s[3] == s[4] == s[5] or s[6] == s[7] == s[8]:
            return False
        # colone
        if s[0] == s[3] == s[6] or s[1] == s[4] == s[7] or s[2] == s[5] == s[8]:
            return False
        # diagonale
        if s[0] == s[4] == s[8] or s[2] == s[4] == s[6]:
            return False
        if not any(str(x) in self.board for x in [str(x) for x in range(9)]):
            print("match nul")
        return True
bot.run(Token)
