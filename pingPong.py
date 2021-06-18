import sqlite3
conn = sqlite3.connect('players.db')
cur = conn.cursor()


# clear database
def delete_all():
    cur.execute("DELETE from players")
    conn.commit()


# function to setup database during the first run
def first_run():
    cur.execute("""CREATE TABLE players(
            name text,
            wins integer,
            score integer
            )""")
    conn.commit()


# ScoreBord Object that keeps track of the score and winning condition
class ScoreBoard:
    # Assume state is 2d array already
    def __init__(self):
        self.player1 = 0
        self.player2 = 0

    def addScore(self, pNum):
        if pNum == 1:
            self.player1 += 1
        else:
            self.player2 += 1

    def getScore(self, pNum):
        if pNum == 1:
            return self.player1
        else:
            return self.player2

    def printScore(self):
        print("Player 1 Score: ", self.player1)
        print("Player 2 Score: ", self.player2)

    def checkEnd(self):
        if self.player1 > 10 or self.player2 > 10:
            if self.player1-self.player2 >= 2:
                print("Player 1 Wins!")
                return 1
            if self.player2 - self.player1 >= 2:
                print("Player 2 Wins!")
                return 2
        return 0


# add user with name: name into database
# wins and scores value automatically default to 0
def add_user(name):
    print("Adding User", name)
    cur.execute("INSERT INTO players VALUES (?, 0, 0)", (name,))
    conn.commit()


# checks if username name has been registered or not
# return False if name is in database True otherwise
def check_user(name):
    print("Checking User")
    cur.execute('SELECT * FROM players')
    arr = cur.fetchall()
    print(arr)
    if len(arr) < 1:
        return True
    for i in arr:
        print(i)
        na, wins, score = i
        if na == name:
            return False
    return True


# adds score to username name
# properties wins will increase by 1. score will be added to score
def add_result(name, score):
    cur.execute('SELECT * FROM players WHERE name = ?', (name,))
    print("Adding Result")
    player = cur.fetchone()
    print(player)
    n, w, s = player
    print(n, w, s)
    w += 1
    s += score
    cur.execute("""UPDATE players SET wins = ? WHERE name = ?""",
                (w, name)
                )
    cur.execute("""UPDATE players SET score = ? WHERE name = ?""",
                (s, name)
                )
    conn.commit()


# displays the leaderboard in order
# Priority wins(decreasing) and then score(increasing)
def display_leaders():
    print("LeaderBoard")
    cur.execute('SELECT * FROM players ORDER BY wins DESC, score ASC;')
    print(cur.fetchall())


# main function that starts the code
# will create a ScoreBoard object to keep track of score
def start():
    cur.execute('SELECT * FROM players')
    display_leaders()
    user1 = input("Enter Player1 Username: ")
    if check_user(user1):
        add_user(user1)
    print("Welcome", user1)
    user2 = input("Enter Player2 Username: ")
    if check_user(user2):
        add_user(user2)
    print("Welcome", user2)
    counter = 0  # counter that will reset to 0 every 2 turns to keep track of server
    rounds = 1  # counter to display the rounds
    currentP = 0  # track current server 1 = player 1 serve 2 = player 2 serve
    scores = ScoreBoard()  # initiate scoreboard
    # create infinite loop to keep seeking input until winning or quitting conditions are fulfilled
    while True:
        try:
            if rounds == 1:
                currentP = int(input("Starting Player (1 or 2): "))
                print("--------------------------")
        except ValueError:
            print("please enter 1 or 2")
            continue
        if currentP == 1:
            server = user1
        else:
            server = user2
        scores.printScore()
        results = scores.checkEnd()
        if results > 0:
            if results == 1:
                add_result(user1, scores.getScore(1))
            else:
                add_result(user2, scores.getScore(2))
            display_leaders()
            return
        print("Round ", rounds)
        print("Server: ", server)
        print("Player ", )
        qu = input("Do you want to quit? (enter y to quit)")
        if qu == "y":
            print("Goodbye!")
            return
        try:
            result = int(input("Which player Score: "))
        except ValueError:
            print("please enter 1 or 2")
            continue
        if result != 1 and result != 2:
            print("Please enter valid player number 1 or 2")
            continue
        scores.addScore(result)
        rounds += 1
        counter += 1
        if counter == 2:
            counter = 0
            if currentP == 1:
                currentP = 2
            else:
                currentP = 1
        print("--------------------------")


if __name__ == '__main__':
    first_run()  # Run this function to set up database in you first run
    # please delete or comment out above function after initial setup
    start()
    conn.close()

