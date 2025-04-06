import os
import time
import subprocess

def banner(message):
    """Print a banner message"""
    length = len(message) + 4
    print("=" * length)
    print(f"= {message} =")
    print("=" * length)

def restart_workflows():
    """Restart our application workflows"""
    banner("Restarting workflows")
    print("This script will restart both the web application and the Telegram bot.")
    
    # Kill any existing Gunicorn processes
    try:
        subprocess.run("pkill -f gunicorn", shell=True)
        print("Stopped any running Gunicorn processes")
    except Exception as e:
        print(f"Error stopping Gunicorn: {e}")
    
    # Kill any existing Python processes for the bot
    try:
        subprocess.run("pkill -f 'python main.py'", shell=True)
        print("Stopped any running Telegram bot processes")
    except Exception as e:
        print(f"Error stopping Telegram bot: {e}")
    
    time.sleep(1)  # Give processes time to terminate
    
    # Start the web application
    try:
        banner("Starting web application")
        web_process = subprocess.Popen(
            "gunicorn --bind 0.0.0.0:5000 --reuse-port --reload app:app",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        print(f"Web application started with PID: {web_process.pid}")
    except Exception as e:
        print(f"Error starting web application: {e}")
    
    time.sleep(2)  # Give web app time to start
    
    # Start the Telegram bot
    try:
        banner("Starting Telegram bot")
        bot_process = subprocess.Popen(
            "python main.py",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        print(f"Telegram bot started with PID: {bot_process.pid}")
    except Exception as e:
        print(f"Error starting Telegram bot: {e}")
    
    banner("Services started")
    print("Web application: http://0.0.0.0:5000")
    print("Telegram bot: Running in background")
    print("\nPress Ctrl+C to exit")
    
    try:
        # Keep the script running and monitor the processes
        while True:
            web_output = web_process.stdout.readline()
            if web_output:
                print(f"[WEB] {web_output.strip()}")
            
            bot_output = bot_process.stdout.readline()
            if bot_output:
                print(f"[BOT] {bot_output.strip()}")
            
            # Check if processes are still running
            if web_process.poll() is not None:
                print("Web application stopped. Restarting...")
                web_process = subprocess.Popen(
                    "gunicorn --bind 0.0.0.0:5000 --reuse-port --reload app:app",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                print(f"Web application restarted with PID: {web_process.pid}")
            
            if bot_process.poll() is not None:
                print("Telegram bot stopped. Restarting...")
                bot_process = subprocess.Popen(
                    "python main.py",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                print(f"Telegram bot restarted with PID: {bot_process.pid}")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down services...")
        web_process.terminate()
        bot_process.terminate()
        print("Services stopped")

if __name__ == "__main__":
    restart_workflows()