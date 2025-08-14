import heapq

# ====================================
# Project: Social Network in TEED_GEN10
# Using Undirected Weighted Graph with Dijkstra, BFS & DFS
# ====================================

# User Class
class User:
    def __init__(self, username, bio=""):
        self.username = username  # username
        self.bio = bio  # Short description
        self.messages = []  # Stores received messages

    def __str__(self):
        return f"User: {self.username}, Bio: {self.bio}"

# SocialNetwork Class
class SocialNetwork:
    def __init__(self):
      # store all users
        self.users = {}
        self.graph = {}  # Changed to dict for weighted undirected graph: user -> {friend: weight}

    # Add a new user
    def add_user(self, username, bio=""):
        if username not in self.users:
            self.users[username] = User(username, bio)
            self.graph[username] = {}  # initialize empty dict for friends with weights
            print(f"User {username:<12} --> added successfully.")
        else:
            print(f"User {username:<12} --> already exists.")

    # Search for a user
    def search_user(self, username):
        if username in self.users:
            print(f"{username:<12} --> Hello I'm here!")
        else:
            print(f"{username:<12} --> Hello I'm not here!!")

    # Remove a user completely
    def remove_user(self, username):
        if username in self.users:
            del self.users[username]
            del self.graph[username]
            for friends in self.graph.values():
                if username in friends:
                    del friends[username]  # remove connections both ways
            print(f"User {username} --> removed successfully.")
        else:
            print(f"User {username} --> does not exist.")

    # Add an undirected connection with optional weight (default 1)
    def add_friendship(self, user1, user2, weight=1):
        if user1 in self.users and user2 in self.users:
            if user2 not in self.graph[user1]:
                self.graph[user1][user2] = weight
                self.graph[user2][user1] = weight  # undirected edge
                print(f"Added connection: {user1:<12} --({weight})-- {user2}")
            else:
                print(f"{user1:<12} already connected to {user2}.")
        else:
            print("One or both users do not exist.")

    # Check if user1 and user2 are friends (undirected)
    def are_friends(self, user1, user2):
          # Check if user1 and user2 are in the same network
        if user1 in self.graph and user2 in self.graph[user1]:
            print(f"Yes, {user1} and {user2} are friends.")
            return True
        else:
          # if there are no connection, print it
            print(f"No, {user1} and {user2} are not friends.")
            return False

    # Remove an undirected connection
    def remove_friendship(self, user1, user2):
        #
        if user2 in self.graph.get(user1, {}) and user1 in self.graph.get(user2, {}):
            del self.graph[user1][user2]
            del self.graph[user2][user1]
            print(f"Removed connection: {user1} -- {user2}")
        else:
            print(f"No connection exists between {user1:<12} and {user2}.")

    # Shortest path using Dijkstra's algorithm (weighted)
    def shortest_path(self, start, target):
        if start not in self.graph or target not in self.graph:
            return None
        # initialize the distance
        distances = {node: float('inf') for node in self.graph}
        previous = {node: None for node in self.graph}
        distances[start] = 0
        pq = [(0, start)]  # priority queue: (distance, node)

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_distance > distances[current_node]:
                continue

            if current_node == target:
                # Reconstruct path
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = previous[current_node]
                return path[::-1]

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        return None

    # Display the full network with weights
    def display_network(self):
        print("\tSocial Network Connections:")
        for user in self.graph:
            if self.graph[user]:
                friends_str = ', '.join(f"{friend}({weight})" for friend, weight in self.graph[user].items())
            else:
                friends_str = 'No one'
            print(f"{user:<12} follows --> {friends_str}")
        print()

    # Display a user's friend list with weights
    def display_friend_list(self, username):
        if username in self.graph:
            if self.graph[username]:
                friends_str = ', '.join(f"{friend}({weight})" for friend, weight in self.graph[username].items())
            else:
                friends_str = 'No one'
            print(f"{username:<12} follows --> {friends_str}")
        else:
            print(f"User '{username:<12}' --> not found.")

    # Get user information
    def get_user_info(self, username):
        if username in self.users:
            print(self.users[username])
            self.display_friend_list(username)
        else:
            print(f"User '{username:<12}' --> not found.")

    # Send a message with checks: sender and receiver must exist, not send to self, must be friends
    def send_message(self, sender, receiver, message):
      if sender in self.users and receiver in self.users:
          if sender == receiver:
              print("You cannot send a message to yourself.")
              return

          # Check if they are friends
          if not self.are_friends(sender, receiver):
              # Automatically add friendship both ways
              self.add_friendship(sender, receiver)
              self.add_friendship(receiver, sender)
              print(f"Friendship automatically added between {sender} and {receiver}.")

          # Now send the message
          self.users[receiver].messages.append(f"From {sender}: {message}")
          print(f"Message sent from {sender} to {receiver}: {message}")
      else:
          print("One or both users do not exist.")

    # BFS Traversal
    def bfs(self, start):
        if start not in self.graph:
            print(f"User '{start:<12}' --> not found.")
            return
        visited = set()
        queue = [start]
        print("BFS traversal:", end=" ")

        while queue:
            current = queue.pop(0)
            if current not in visited:
                print(current, end=" ")
                visited.add(current)
                # Extend queue with neighbors
                queue.extend(n for n in self.graph[current] if n not in visited)
        print()

    # DFS Traversal
    def dfs(self, start):
        if start not in self.graph:
            print(f"User '{start:<12}' --> not found.")
            return
        visited = set()
        # inner-recursive DFS
        def dfs_recursive(node):
            if node not in visited:
                print(node, end=" ")
                visited.add(node)
                for neighbor in self.graph[node]:
                    dfs_recursive(neighbor)

        print("DFS traversal:", end=" ")
        dfs_recursive(start)
        print()

# Example Usage
if __name__ == "__main__":
    TEED_GEN10 = SocialNetwork()

    # Adding users
    print("===================== Add user ====================")
    Add_user = [
        ("Lymeng", "Hello I'm Lymeng!"), ("Thina", "Hello I'm Thina!"),
        ("Khim", "Hello I'm Khim!"), ("Vimean", "Hello I'm Vimean!"),
        ("Hong", "Hello I'm Hong!"), ("Srun", "Hello I'm Srun!"),
        ("Vin", "Hello I'm Vin!"), ("Lida", "Hello I'm Lida!"),
        ("Chamrong", "Hello I'm Chamrong!"), ("Sambat", "Hello I'm Sambat!"),
        ("Lita", "Hello I'm Lita!"), ("Chinmi", "Hello I'm Chinmi!"),
        ("Nika", "Hello I'm Nika!"), ("Keam", "Hello I'm keam!"),
        ("Nut", "Hello I'm Nut!"), ("Leakena", "Hello I'm Leakena!"),
        ("Panhavorn", "Hello I'm Panhavorn!"), ("Raksa", "Hello I'm Raksa!"),
        ("Sokmeng", "Hello I'm Sokmeng")
    ]
    for username, bio in Add_user:
        TEED_GEN10.add_user(username, bio)

    # Adding friendships with default weight=1
    print("\n================== Add friendships =================")
    friendships = [
        ("Lymeng", "Khim", 4), ("Khim", "Vin", 4), ("Vimean", "Lida", 5),
        ("Chamrong", "Vin", 3), ("Chamrong", "Thina", 5), ("Chinmi", "Khim", 2),
        ("Thina", "Chinmi", 2), ("Khim", "Hong", 4), ("Hong", "Srun", 2),
        ("Srun", "Sambat", 2), ("Sambat", "Lita", 1), ("Chinmi", "Hong", 2),
        ("Vin", "Lymeng", 5), ("Lida", "Khim", 5), ("Lita", "Hong", 1),
        ("Lida", "Lymeng", 3), ("Hong", "Vimean", 1), ("Lymeng", "Thina", 5),
        ("Lida", "Hong", 3), ("Chamrong", "Hong", 2), ("Chinmi", "Vin", 4),
        ("Lymeng", "Chinmi", 3), ("Lymeng", "Chamrong", 3), ("Thina", "Hong", 4),
        ("Keam", "Nika", 1), ("Raksa", "Srun", 3), ("Sokmeng", "Chamrong", 4),
        ("Panhavorn", "Vimean", 3), ("Leakena", "Lida", 2), ("Sokmeng", "Nika", 2),
        ("Lymeng", "Nut", 2)
    ]
    for user1, user2, weight in friendships:
        TEED_GEN10.add_friendship(user1, user2, weight)  # weight=1 default

    # Display network
    print("\n================== Display network =================")
    TEED_GEN10.display_network()

    # Shortest path from start to target
    print("\n================== Shortest path ===================")
    print("Shortest path Lymeng --> Srun:", TEED_GEN10.shortest_path("Lymeng", "Srun"))

    # Search a user
    print("\n=================== Search a user ==================")
    TEED_GEN10.search_user("Hong")
    TEED_GEN10.search_user("Panha")

    # BFS & DFS
    print("\n==================== BFS & DFS =====================")
    TEED_GEN10.bfs("Lymeng")
    TEED_GEN10.dfs("Lida")

    # Send message
    print("\n==================== Send message ==================")
    TEED_GEN10.send_message("Lida", "Sambat", "Hi, CEO handsome boys & beautiful girls")

    # Get user info
    print("\n================== User information ================")
    TEED_GEN10.get_user_info("Lymeng")
    TEED_GEN10.get_user_info("Thina")
    print("\n====================================================")

    # Remove user
    print("\n================== Remove user =====================")
    TEED_GEN10.remove_user("Thina")

    # Remove friendship
    print("\n================= Remove friendship ================")
    TEED_GEN10.remove_friendship("Lymeng", "Khim")
    print("====================================================")

    # Display network
    print("\n================= Display Network ================")
    TEED_GEN10.display_network()
    print("====================================================")