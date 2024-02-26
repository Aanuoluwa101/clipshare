# Clipshare
A taste of the hither-thither magic

## Introduction

**Clipshare** is a clipboard sharing application designed to simplify the transfer of clipboard content between two PCs. Imagine effortlessly copying text on one PC and promptly pasting it on another, eliminating the need for intermediary applications like messaging platforms.

This application serves as both a showcase of technical proficiency and a solution to a personal challenge – the need for efficient text sharing between two PCs. While its primary purpose is to demonstrate capabilities, **Clipshare** also addresses a common concern among developers who frequently copy text between multiple machines.

## GUI
![Server](https://i.imgur.com/KuFLZNv.png   )

![Client](https://i.imgur.com/O1Rg4BQ.png)

## Dependencies

**Clipshare** is built entirely using Python, making use of various modules for both functionality and the user interface:

- **Tkinter**: Utilized for creating the graphical user interface (GUI).
- **pyperclip**: Employs clipboard manipulation.
- **socket**: Facilitates communication over the network.

Additionally, the application incorporates other essential modules such as Threading, subprocess, re, and random to enhance its overall functionality.



## Architecture

The application follows a Server-Client architecture, with each component consisting of three major elements:

- **The Main Program**: Acts as the entry point, initializing the state object and running both the UI and the state manager as separate threads.

- **State Manager**: Manages the server or client by monitoring the application state, starting or stopping the server/client thread accordingly.

- **User Interface (UI)**: Dynamically updates based on the application state, presenting information such as connection status, clipboard content, and error messages.

![architecture](https://i.imgur.com/eRmDWV2.png)


## Design Patterns

1. **Reactor Multithreading Design Pattern**

   This pattern involves a reactor thread waiting for events to occur, and dispatching handler threads to handle those events. The state manager acts as the reactor, monitoring and managing the state changes triggered by various events. For example, it handles transitions between server states, such as starting or stopping, based on network availability. Also, when the user clicks the connect button on the client's UI and enters the server details, the state manager detects this event and spins up a client in response.

2. **State Design Pattern**

   A behavioral pattern where an object changes its behavior based on some internal state. This application implements this pattern to some extent by having a State class serves as the central point for managing the state of the application. Both the client and server classes hold references to the state object and can alter their behavior based on the state object.

## Performance Considerations

1. While building this application, I had three threads. The two I have mentioned above and a third thread that monitors the clipboard for changes and this was an added CPU cost. I realized later that I could perform the check for clipboard changes in the UI's update method. This helped me remove an entire thread from the program and save CPU resources.

2. I had to make a trade-off between having an extremely fast UI and memory consumption. At an update interval of 100 or 200 milliseconds, I noticed the memory usage of the app was as high as 30%. I decided to leave it at 500 milliseconds, and this drastically reduced memory usage to less than 1%.

## How to Install

### Requirements
- Python 3
- Windows OS
- Both PCs on thesame local network (connected to thesame wifi device)
#### 1. Clone the Repository

```bash:
git clone https://github.com/Aanuoluwa101/clipshare
```

#### 2. Run Installation Script

```bash
cd clipshare
install.bat
```
- On the server PC, enter 'server' when prompted.
- On the client PC, enter 'client' when prompted.
- Enter your desired server or client name.

#### 3. Start the application 
- **For server installation**
    ```bash
    cd server
    python main.py
    ```
- **For client installation**
    ```bash
    cd client
    python main.py
    ```
    









