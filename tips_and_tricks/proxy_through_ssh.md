#Setting up a Proxy to work comfortably from home

The idea is to have an ssh-tunnel to a machine at work, which will then be your proxy
so that you to the rest of the web will apppear as if you are surfing from within the
univeristy. This has among other things the benefit of getting access to articles.

## What you need

* An account at a computer at work that you can ssh to
* Permission to use that computer as a proxy

## How to set it up

1. **Creating the script**

  We need a script to set up the proxy, it's just one line, but it's easier to
  have it in a file on your local machine.
  I call mine ```worksshtunnel``` and I placed it in ```$HOME/bin```:
  
  ```
  #!/usr/bin/bash
  ssh -C2qTnN -D 8080 user@remotemachine
  ```
  And of course, you need to fill in your ```user```-name and the address to the ```remotemachine```.
  
  
2. **Run the script**

  It will request your password as you log on to the remote machine. Then nothing more will happen. This is good.
  All is working.
  If you want to continue using the terminal you can just pause the process and send it to the background.

  *If someone has a nice idea of the script doing this automatically, please update here*

3. **Changing proxy settings in the webbrowser**

  In Firefox (should be similar to all) go to:
  
  1. **Preferences**
  2. **Advanced**
  3. The **Network** tab
  4. Click on **Settings...** for the section "Configure how Firefor connects to the internet"
  5. Select **Manual proxy configuration**
  6. Make sure only the **SOCKS Host** address is filled in as ```127.0.0.1``` and **Port** ```8080```
  7. Press *OK*
  
4. **(Optional) Installing add-on to make it easy**

  Search for and install the add-on **Toggle Proxy** and set it to toggle between **No Proxy** and **Manual proxy configuration**.
  Then place the add-on's button somewhere nice in your browser and now all you have to do is activate it to be surfing through
  work.
  
5. **(Optional) Test that it works**

  Go to ```http://www.whatsmyip.org/``` and make sure it is the IP of your remote machine and not your local machine that is displaying.
  
6. **Remember to turn the proxy off**

  When you are done with your work-stuff, either click the **Toggle Proxy** button
  or go into the **Preferences** as in *Step 2*,
  but change the proxy-settings to **No proxy**.

  You can now also terminate the ssh-tunnel in your terminal.

## How to use it after initial setup

To reuse the solution you just start by running your ```worksshtunnel``` command and then either activate the proxy via the **Toggle Proxy** button or change the settings in **Preferences**.
Remember to turn the proxy off after work is done.
