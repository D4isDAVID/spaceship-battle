## Note
Spaceship-Battle was created for a programming festival.  
As such, major updates are unlikely to happen unless I decide to continue the project.

[Issues](https://github.com/D4isDAVID/Spaceship-Battle/issues/) and [pull requests](https://github.com/D4isDAVID/Spaceship-Battle/pulls) are still much appreciated though. 

# Spaceship-Battle
Multiplayer Top-down Space Shooter game made with Python 3 (PyGame).

[Game Trailer](https://www.youtube.com/watch?v=hjskJzHCGd8)

## Opening The Game
To play, you must open either the client.py which is located in the client folder (inside of the source code), or the client executable which you can get by either [downloading one](https://github.com/D4isDAVID/Spaceship-Battle/releases) or building one yourself.

In order to play you'll need a server to join.

### Controls

W & S - Move forwards and backwards  
A & D - Rotate left and right  
Left Shift - Boost  
Any Mouse Button - Shoot (bullet is shot towards your mouse)  
M - Mute music  
Equals/Plus - Music volume up  
Minus/Underscore - Music volume down

## Opening a Server
It is possible to open your own server by, once again, opening either the server.py which is located in the server folder (inside of the source code), or the server executable which you can get by either [downloading one](https://github.com/D4isDAVID/Spaceship-Battle/releases) or building one yourself.

When opening a server, you can either choose a custom IP:port or just stick with the default 0.0.0.0:7723.  
It's possible to play with people outside of your local network by using port forwarding.

### Server Lobbies
Upon opening a server, a lobby will be created in that same server.

Each lobby supports up to 6 players. When a 7th player joins while the lobby is full, a new lobby is created.  
Upon everyone leaving a lobby, it is closed.

## Building an Executable
Spaceship-Battle uses PyInstaller for building.
* Run `pip install -r requirements.txt` in order to install the dependencies
* Run `python build_server.py` to build the server
* Run `python build_client.py` to build the client
