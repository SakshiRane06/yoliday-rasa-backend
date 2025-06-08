# Use the official Rasa image as a base
FROM rasa/rasa:3.6.10-full

# Set the working directory for our application
WORKDIR /app

# Temporarily switch to the root user to gain permissions for installation
USER root

# Copy only the requirements file first (this helps with Docker's build cache)
COPY ./requirements.txt ./

# Now, as root, run pip install. It has permission to write to the main venv.
RUN pip install -r requirements.txt

# Copy the rest of your bot's code into the container.
# The --chown flag ensures the 'rasa' user will own these files, not root.
COPY --chown=rasa:rasa . .

# CRITICAL: Switch back to the non-privileged 'rasa' user for security before running the application.
USER rasa

# Set the default command, which will now be run as the 'rasa' user.
CMD ["run", "actions"]