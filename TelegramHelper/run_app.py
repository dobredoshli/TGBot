import subprocess
import os
import sys

def run_app_server():
    """Run the Flask application server using Gunicorn"""
    print("========================================")
    print("= Starting Studio Hours Web Server     =")
    print("========================================")
    
    try:
        # Stop any existing Gunicorn processes
        subprocess.run("pkill -f gunicorn || true", shell=True)
        
        # Run Gunicorn serving the app module
        server_process = subprocess.run(
            "gunicorn --bind 0.0.0.0:5000 --reuse-port --reload app:app",
            shell=True,
            check=True
        )
        
        print("Web server process completed with exit code:", server_process.returncode)
        return server_process.returncode
        
    except subprocess.CalledProcessError as e:
        print(f"Error starting web server: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_app_server())