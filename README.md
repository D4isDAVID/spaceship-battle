## Note
This project was created for a programming festival.  
As such, updates which include big features are unlikely to happen unless I decide to continue the project.

[Issues](https://github.com/D4isDAVID/Spaceship-Battle/issues/) and [pull requests](https://github.com/D4isDAVID/Spaceship-Battle/pulls) are still much appreciated though. 

# Spaceship-Battle
Multiplayer Top-down Space Shooter game made with Python (PyGame).

[Game Trailer](https://www.youtube.com/watch?v=hjskJzHCGd8)


## Opening The Game
To play, you must open either the client.py which is located in the client folder, or the client executable which you can get by either [downloading one](https://github.com/D4isDAVID/Spaceship-Battle/releases) or building one yourself.

In order to play you'll need a server to join.

When opening a server, by default it is bound to IP 0.0.0.0 with the port 7723.  
It's possible to play with people outside of your local network by using port forwarding.

## Server Lobbies
Upon opening a server, a lobby will be created in that same server.

Each lobby supports up to 6 players. When an 7th player joins while the lobby is full, a new lobby is created.  
Upon everyone leaving a lobby, it is closed.

## Building a Executable
This requires PyInstaller.
* Run `python build_server.py` to build the server
* Run `python build_client.py` to build the client
