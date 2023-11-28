# PowerShell script

# Activate the virtual environment
. C:/Users/admin/.virtualenvs/Mahle-Dashboard-8zo5tHkF/Scripts/Activate.ps1

# Wait for the Streamlit app to start (you may need to adjust this time)
Start-Sleep -Seconds 2

# Run the Streamlit app in the background
streamlit run "C:/Users/admin/Documents/GitHub/mahle_dashboard/App.py"

# Open the app in Chrome
# Replace "http://localhost:7070" with the actual address where your Streamlit app is running
Start-Process "chrome.exe" "http://localhost:7070"

# Close the PowerShell session
Exit