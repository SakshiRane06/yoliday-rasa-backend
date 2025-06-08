# Use the official Rasa image as a base
FROM rasa/rasa:3.6.10-full

# Set the working directory inside the container
WORKDIR /app

# Copy the essential files and folders from your repository into the container's working directory
COPY ./requirements.txt ./

# Fix: Use the --user flag to install packages in a user-writable directory.
# This solves the "Permission denied" error.
RUN pip install --user -r requirements.txt

# Add the local user's binary path to the system's PATH.
# This ensures that commands from the installed packages (like gunicorn) can be found.
ENV PATH="/home/rasa/.local/bin:${PATH}"

COPY . .

# The port Rasa's action server runs on
EXPOSE 5055

# The default command to run when the container starts.
CMD ["run", "actions"]