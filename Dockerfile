# Use the official Rasa image as a base
FROM rasa/rasa:3.6.10-full

# Set the working directory inside the container
WORKDIR /app

# Copy the essential files and folders from your repository into the container's working directory
# Note: We copy credentials.yml, endpoints.yml etc. first.
# This takes advantage of Docker's layer caching. If you only change your NLU data,
# Docker won't need to re-install the python packages, making builds much faster.
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# The port Rasa's action server runs on
EXPOSE 5055

# The default command to run when the container starts.
# We'll make this the action server command, as it's the most common.
# We will override this for the main Rasa server in the Railway settings.
CMD ["run", "actions"]