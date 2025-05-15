
import pandas as pd
import random
import streamlit as st

# Load the data
df = pd.read_csv("Top_20_Golfers_March_2025_with_Wins_and_Majors.txt")

# Initialize session state
if "target_player" not in st.session_state:
    st.session_state.target_player = df.sample(1).iloc[0]
    st.session_state.attempts = 0

target = st.session_state.target_player

st.title("🏌️ PGA Weddle Game")
st.markdown("Guess the PGA Tour player! After each guess, you'll get hints based on stats like age, wins, college, and more.")

guess = st.text_input("🔎 Enter a player name:")

if guess:
    guessed_row = df[df['Name'].str.lower() == guess.lower()]
    st.session_state.attempts += 1

    if guessed_row.empty:
        st.error("Player not found. Make sure the name is spelled correctly.")
    else:
        guessed = guessed_row.iloc[0]

        if guess.lower() == target['Name'].lower():
            st.success(f"🎉 Correct! It was {target['Name']}. Guessed in {st.session_state.attempts} attempts.")
            if st.button("🔁 Play Again"):
                st.session_state.target_player = df.sample(1).iloc[0]
                st.session_state.attempts = 0
        else:
            st.markdown(f"**Guess:** {guessed['Name']}")

            if guessed['Nationality'].lower() == target['Nationality'].lower():
                st.write("🌎 Country: ✅ Correct!")
            else:
                st.write("🌎 Country: ❌ Incorrect")

            if guessed['College'].lower() == target['College'].lower():
                st.write("🎓 College: ✅ Correct!")
            else:
                st.write("🎓 College: ❌ Incorrect")

            def hint(stat, label):
                if guessed[stat] < target[stat]:
                    return f"{label}: ⬆️ Higher"
                elif guessed[stat] > target[stat]:
                    return f"{label}: ⬇️ Lower"
                else:
                    return f"{label}: ✅ Correct!"

            st.write(hint("Age", "🎂 Age"))
            st.write(hint("PGA Card Year", "📅 PGA Tour Card Year"))
            st.write(hint("PGA Tour Wins", "🏆 PGA Tour Wins"))
            st.write(hint("Major Wins", "🏅 Major Wins"))
