import streamlit as st 
from astropy.coordinates import SkyCoord 
import numpy as np 
import pandas as pd 
from PIL import Image
from urllib.request import urlopen
from datetime import datetime 

dates  =np.array(['2022-04-22',
 '2022-04-23',
 '2022-04-24',
 '2022-04-25',
 '2022-04-26',
 '2022-04-27',
 '2022-04-28',
 '2022-04-29',
 '2022-04-30',
 '2022-05-01',
 '2022-05-02',
 '2022-05-03',
 '2022-05-04',
 '2022-05-05',
 '2022-05-06',
 '2022-05-07',
 '2022-05-08',
 '2022-05-09',
 '2022-05-10',
 '2022-05-11',
 '2022-05-12',
 '2022-05-13',
 '2022-05-14',
 '2022-05-15',
 '2022-05-16',
 '2022-05-17',
 '2022-05-18',
 '2022-05-19',
 '2022-05-20',
 '2022-05-21',
 '2022-05-22',
 '2022-05-23',
 '2022-05-24',
 '2022-05-25',
 '2022-05-26',
 '2022-05-27',
 '2022-05-28',
 '2022-05-29',
 '2022-05-30',
 '2022-05-31',
 '2022-06-01',
 '2022-06-02'])

today = datetime.today().strftime('%Y-%m-%d')
ind, = np.where(dates==today)[0]
m_list  = pd.read_csv('galaxies/m_list.txt',names=['gal name']).values
m_list = np.concatenate(m_list)

if 'correct' not in st.session_state.keys():
    st.session_state.correct = False
if 'num_guesses' not in st.session_state.keys():
    st.session_state.num_guesses = 0
if 'galaxy' not in st.session_state.keys():
    st.session_state.galaxy = m_list[ind]
if 'obj' not in st.session_state.keys():
    st.session_state.obj = SkyCoord.from_name(st.session_state.galaxy)
if 'url' not in st.session_state.keys():
    st.session_state.url = f"https://www.legacysurvey.org/viewer/cutout.jpg?ra={st.session_state.obj.ra.value}&dec={st.session_state.obj.dec.value}&layer=sdss&pixscale=1.5&size=700"
if 'viewer' not in st.session_state.keys():
    st.session_state.viewer = f"https://www.legacysurvey.org/viewer?ra={st.session_state.obj.ra.value:.4f}&dec={st.session_state.obj.dec.value:.4f}&layer=sdss&zoom=11"
if 'img' not in st.session_state.keys():
    st.session_state.img = Image.open(urlopen(st.session_state.url))

if 'guesses' not in st.session_state.keys():
    st.session_state.guesses = []
st.title(f'Galaxdle | {today}')
st.subheader(f'Remaining Guesses: {6-st.session_state.num_guesses}')
    
with st.form('submit guess form'):
    if st.session_state.num_guesses == 6:
        st.write('Out of guesses!')
        st.write(f"[View in LegacySurvey]({st.session_state.viewer})")
        st.stop()
        
    text = st.text_input(label='Guess Galaxy')
    s = st.form_submit_button('Submit Guess')
    if s:
        if text == st.session_state.galaxy:
            st.header('Correct!')
            st.session_state.correct = True
            st.balloons()
            st.write(f"[View in LegacySurvey]({st.session_state.viewer})")
        else:
            st.header('Incorrect.')
            st.session_state.guesses.append(text)
            st.write(f"You've Guessed: {st.session_state.guesses}")
            try:
                guess_obs = SkyCoord.from_name(text)
                offset = guess_obs.spherical_offsets_to(st.session_state.obj)
                os_e = offset[0]
                os_n = offset[1]
                st.write(f'<-- {os_e:.2f}, ^ {os_n:.2f}')
            except:
                st.write('Galaxy Name Not Recognized')
            st.session_state.num_guesses += 1


st.image(st.session_state.img)

