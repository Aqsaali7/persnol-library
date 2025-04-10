import streamlit as st
import pandas as pd

st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# Initialize session state
if 'library' not in st.session_state:
    st.session_state.library = pd.DataFrame(columns=["Title", "Author", "Genre", "Read"])

st.title("📚 Personal Library Manager")

# --- Book Entry Form ---
st.subheader("➕ Add a New Book")
with st.form("add_book_form", clear_on_submit=True):
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.selectbox("Genre", ["Fiction", "Non-fiction", "Mystery", "Fantasy", "Science Fiction", "Biography", "Other"])
    read = st.checkbox("Have you read it?")
    submitted = st.form_submit_button("Add Book")

    if submitted:
        if title and author:
            new_book = {
                "Title": title,
                "Author": author,
                "Genre": genre,
                "Read": "Yes" if read else "No"
            }
            st.session_state.library = pd.concat(
                [st.session_state.library, pd.DataFrame([new_book])], ignore_index=True
            )
            st.success(f"Added '{title}' by {author}")
        else:
            st.warning("Please enter both title and author.")

# --- Book Filter ---
st.subheader("🔍 View Your Library")
filter_option = st.radio("Filter by:", ["All", "Read", "Unread"], horizontal=True)

# Apply filter
if filter_option == "Read":
    filtered_books = st.session_state.library[st.session_state.library["Read"] == "Yes"]
elif filter_option == "Unread":
    filtered_books = st.session_state.library[st.session_state.library["Read"] == "No"]
else:
    filtered_books = st.session_state.library

st.dataframe(filtered_books, use_container_width=True)

# --- Delete Book ---
st.subheader("🗑️ Delete a Book")
if not st.session_state.library.empty:
    titles = st.session_state.library["Title"].tolist()
    book_to_delete = st.selectbox("Select a book to delete", titles)
    if st.button("Delete Selected Book"):
        st.session_state.library = st.session_state.library[st.session_state.library["Title"] != book_to_delete]
        st.success(f"Deleted '{book_to_delete}'")
else:
    st.info("Your library is currently empty.")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
