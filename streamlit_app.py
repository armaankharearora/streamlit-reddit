import streamlit as st
from google.cloud import firestore
import json
from google.oauth2 import service_account
import firebase_admin
from firebase_admin import credentials

json_acct_info = json.loads(st.secrets["textkey"])
cred = service_account.Credentials.from_service_account_info(json_acct_info)

#db = firestore.Client(credentials=creds, project="streamlit-reddit")

#db = firestore.Client.from_service_account_json("firestore-key.json")
#db = firestore.Client(credentials=credentials, project="streamlit-reddit")

#cred = credentials.Certificate(json_acct_info)
db = firestore.Client(credentials=cred)


# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
submit = st.button("Submit new post")

# Once the user has submitted, upload it to the database
if title and url and submit:
	doc_ref = db.collection("posts").document(title)
	doc_ref.set({
		"title": title,
		"url": url
	})

# And then render each post, using some light Markdown
posts_ref = db.collection("posts")
for doc in posts_ref.stream():
	post = doc.to_dict()
	title = post["title"]
	url = post["url"]

	st.subheader(f"Post: {title}")
	st.write(f":link: [{url}]({url})")