import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json
import game_gomoku
import ai_bot
import sentiment_bot
import aipic_bot
from tkinter import messagebox
class GUI:

    def __init__(self, send, recv, sm, s):
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_ai = ai_bot.AIBot(model="phi3:mini")
        self.chat_logs = []
        self.senti_bot = sentiment_bot.SentimentBot()
        self.my_msg = ""
        self.system_msg = ""
        self.senti_bot = sentiment_bot.SentimentBot()
        self.pic_bot = aipic_bot.AIPicBot()
        self.image_refs = []

    def login(self):
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")
        self.lable_pass = Label(self.login, text="password:",font="Helvetica 12")
        self.lable_pass.place(relheight = 0.2,
                             relx = 0.1,
                             rely = 0.35)
        self.pls.place(relheight = 0.15,
                       relx = 0.2, 
                       rely = 0.07)
        self.entryPass = Entry(self.login,
                               font="Helvetica 14",
                               show="*")
        self.entryPass.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.35)
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 12")
        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.2)
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
        self.entryName.focus()
        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get(), self.entryPass.get()))
        self.go.place(relx = 0.4,
                      rely = 0.55)
        self.Window.mainloop()

    def goAhead(self, name, password):
        if len(name) > 0 and len(password) > 0:

            msg = json.dumps({"action": "login", "name": name, "password": password})
            self.send(msg)
            response = json.loads(self.recv())

            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, menu + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)

                process = threading.Thread(target=self.proc)  ##############
                process.daemon = True
                process.start()

            elif response["status"] == 'wrong password':
                self.pls.config(text="Wrong Password!")
            elif response["status"] == 'duplicate':
                self.pls.config(text="User already logged in!")
    def layout(self,name):
        
        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))


        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.10)

        self.buttonGame = Button(self.labelBottom,
                                 text="Game",
                                 font="Helvetica 10 bold",
                                 width=10,
                                 bg="#ABB2B9",
                                 command=self.request_game)

        self.buttonGame.place(relx=0.88,
                              rely=0.008,
                              relheight=0.06,
                              relwidth=0.10)

        self.buttonAI = Button(self.labelBottom,
                               text="AI Chat",
                               font="Helvetica 10 bold",
                               width=10,
                               bg="#ABB2B9",
                               command=self.open_ai_window)

        self.buttonAI.place(relx=0.66,
                            rely=0.008,
                            relheight=0.06,
                            relwidth=0.10)
        self.textCons.config(cursor = "arrow")

        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
    def proc(self):
        while True:
            read, write, error = select.select([self.socket], [], [], 0)        #########
            peer_msg = []
            if self.socket in read:
                peer_msg = self.recv()

            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                current_text = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""

                if current_text.startswith("[GAME]"):                          ###############
                    game_json_str = current_text[7:]
                    game_data = json.loads(game_json_str)

                    if game_data["data"] == "START":
                        self.start_game_window(i_go_first=False)
                    else:
                        if hasattr(self, 'game_window'):
                            self.game_window.on_peer_move(game_data["data"])

                elif len(current_text.strip()) > 0:
                    self.chat_logs.append(current_text.strip())
                    if len(self.chat_logs) > 50: self.chat_logs.pop(0)

                    if "[IMAGE]:" in current_text:
                        parts = current_text.split("[IMAGE]:")
                        sender_info = parts[0]
                        url = parts[1].strip()

                        self.textCons.config(state=NORMAL)
                        self.textCons.insert(END, sender_info + "\n")

                        photo = self.pic_bot.fetch_image(url)

                        if photo:
                            self.image_refs.append(photo)
                            self.textCons.image_create(END, image=photo)
                            self.textCons.insert(END, "\n")
                        else:
                            self.textCons.insert(END, "[Image Load Failed]\n")

                        self.textCons.config(state=DISABLED)
                        self.textCons.see(END)
                    else:
                        label, emoji = self.senti_bot.get_sentiment(current_text)
                        display_text = f"{current_text}  {emoji}"
                        self.textCons.config(state=NORMAL)
                        self.textCons.insert(END, display_text + "\n")
                        self.textCons.config(state=DISABLED)
                        self.textCons.see(END)

    def request_game(self):
        if self.sm.peer != "":
            self.start_game_window(i_go_first=True)
            msg = json.dumps({"action": "game", "from": self.name, "to": self.sm.peer, "data": "START"})
            self.send(msg)
        else:
            self.textCons.config(state=NORMAL)
            self.textCons.insert(END, "Please connect to someone first!\n")
            self.textCons.config(state=DISABLED)

    def start_game_window(self, i_go_first):
        self.game_window = game_gomoku.GomokuWindow(
            self.name, self.sm.peer, self.send, i_go_first
        )

    def open_ai_window(self):
        self.ai_win = Toplevel()
        self.ai_win.title("Chat with AI Assistant")
        self.ai_win.geometry("450x600")
        setting_frame = Frame(self.ai_win, bg="#EEE", pady=5)
        setting_frame.place(relwidth=1, relheight=0.15)

        Label(setting_frame, text="Set AI Personality:", bg="#EEE").pack(side=TOP, anchor=W, padx=5)

        self.ai_persona_entry = Entry(setting_frame, font="Helvetica 10")
        self.ai_persona_entry.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.ai_persona_entry.insert(0, "You are a helpful assistant.")
        btn_set = Button(setting_frame, text="Set / Reset", command=self.set_ai_persona)
        btn_set.pack(side=RIGHT, padx=5)
        self.ai_text = Text(self.ai_win, font="Helvetica 12", state=DISABLED)
        self.ai_text.place(relheight=0.73, relwidth=1, rely=0.15)
        self.ai_entry = Entry(self.ai_win, font="Helvetica 12")
        self.ai_entry.place(relheight=0.1, relwidth=0.75, rely=0.88, relx=0.02)
        self.ai_entry.bind("<Return>", lambda event: self.send_to_ai())

        btn_send = Button(self.ai_win, text="Ask", command=self.send_to_ai)
        btn_send.place(relheight=0.1, relwidth=0.2, rely=0.88, relx=0.78)

        self.update_ai_display("System", "You can set my personality above. Chat with me privately here.")

    def set_ai_persona(self):
        prompt = self.ai_persona_entry.get()
        msg = self.my_ai.set_personality(prompt)
        self.ai_text.config(state=NORMAL)
        self.ai_text.delete(1.0, END)
        self.ai_text.config(state=DISABLED)
        self.update_ai_display("System", msg)

    def send_to_ai(self):
        msg = self.ai_entry.get()
        if not msg: return
        self.ai_entry.delete(0, END)

        self.update_ai_display("Me", msg)
        response = self.my_ai.ask(msg)
        self.update_ai_display("AI", response)

    def update_ai_display(self, role, content):
        self.ai_text.config(state=NORMAL)
        self.ai_text.insert(END, f"[{role}]: {content}\n\n")
        self.ai_text.see(END)
        self.ai_text.config(state=DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.my_msg = msg
        self.entryMsg.delete(0, END)
        if msg == "/summary":
            history = "\n".join(self.chat_logs)

            if len(history) < 10:
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, "System: Not enough chat history to summarize.\n")
                self.textCons.config(state=DISABLED)
                return
            ai_reply = self.my_ai.analyze_chat(history, "Summarize the discussion in 1-2 sentences.")

            self.my_msg = f"[Summary]: {ai_reply}"                                                              ###############

        elif msg == "/keywords":
            history = "\n".join(self.chat_logs)

            if len(history) < 10:
                return

            ai_reply = self.my_ai.analyze_chat(history,
                                               "List top 5 keywords or topics from the chat, separated by commas.")

            self.my_msg = f"[Keywords]: {ai_reply}"
        elif msg.startswith("@ai"):
            content = msg[3:].strip().lower()

            if "summary" in content or "summarize" in content:
                history_text = "\n".join(self.chat_logs)
                ai_reply = self.my_ai.analyze_chat(history_text, "Summarize the discussion briefly.")
                self.my_msg = f"[AI_Analysis]: {ai_reply}"

            elif "comment" in content or "opinion" in content:
                history_text = "\n".join(self.chat_logs)
                ai_reply = self.my_ai.analyze_chat(history_text, "Give a comment or advice on this conversation.")
                self.my_msg = f"[AI_Comment]: {ai_reply}"

            else:
                ai_reply = self.my_ai.ask(content)
                self.my_msg = f"[AI_Auto]: {ai_reply}"
    def run(self):
        self.login()
if __name__ == "__main__": 
    g = GUI()