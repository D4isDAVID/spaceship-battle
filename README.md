## Note

Spaceship Battle was created for a programming festival. \
Due to that, updates are unlikely to happen unless I decide to continue the project.

[Issues](https://github.com/D4isDAVID/Spaceship-Battle/issues/) and [pull requests](https://github.com/D4isDAVID/Spaceship-Battle/pulls) are still much appreciated though! 🙂

# Spaceship Battle

A Multiplayer Top-down Space Shooter game made with Python 3 (PyGame). (not sure if it works on all Python 3 versions)

[Game Trailer](https://www.youtube.com/watch?v=hjskJzHCGd8)

## Opening The Game

To play, you must either launch `client/client.py` inside of the source code with Python, or open the client executable which you can get either by [downloading one](https://github.com/D4isDAVID/Spaceship-Battle/releases) or [building one yourself](#building-an-executable).

In order to play you'll need a server to join. Unfortunately I don't have the funds to run a server for an always dead game, so either somehow find one or [open one yourself](#opening-a-server).

### Controls

`W` and `S` - Move forwards and backwards (respectively) \
`A` and `D` - Rotate left and right (respectively) \
`LShift` - Boost \
Any Mouse Button - Shoot (bullet is shot towards your mouse) \
`M` - Mute music \
Equals (`=`) or Plus (`+`) - Music volume up \
Minus (`-`) or Underscore (`_`) - Music volume down

## Opening a Server

To open your own server you must either launch `server/server.py` inside of the source code with Python, or open the server executable which you can get by either [downloading one](https://github.com/D4isDAVID/Spaceship-Battle/releases) or [building one yourself](#building-an-executable).

Upon opening a server, you can either choose a custom `IP:port` or stick with the default `0.0.0.0:7723` (recommended).
It is possible to play with people outside of your local network (LAN) using port forwarding.

### Server Lobbies

Upon opening a server, a lobby will automatically be created in that same server.

Each lobby supports up to 6 players. When a 7th player joins while the lobby is full, a new lobby is automatically created.
Upon everyone leaving a lobby, it is automatically closed.

## Building an Executable

Spaceship Battle uses PyInstaller for building.
* Run `pip install -r requirements.txt` to install the dependencies
* Launch `build_server.py` with Python to build the server
* Launch `build_client.py` with Python to build the client
