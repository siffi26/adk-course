---------------
Option 1: Vertex AI
---------------

This is common in the Google ADK course. You authenticate with:

gcloud auth application-default login

and use your Google Cloud project. In that case, you do not need a GOOGLE_API_KEY.

If that's how your previous agents worked, continue using Vertex AI.

Run:

export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=siffifirstagent
export GOOGLE_CLOUD_LOCATION=us-central1

Then run:

adk web

---------------
Option 2: Gemini Developer API
---------------

This uses an API key.

You would get it here:

https://aistudio.google.com/app/apikey

Then:

export GOOGLE_API_KEY=AIza....

You do not need this if you're using Vertex AI.