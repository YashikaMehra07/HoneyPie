import cv2
from deepface import DeepFace
from PIL import Image

import matplotlib.pyplot as plt
# import pandas as pd 
# from datetime import datetime
from dbfunc import store_user_mood_data
    
def analyze_mood_deepface(vdo):
    try:
        # DeepFace emotion analysis
        print("Running DeepFace on frame")
        cv2.imwrite("debug_frame.jpg", vdo)
        analysis = DeepFace.analyze(vdo, actions=['emotion'], enforce_detection=False)
        print(f"DeepFace result: {analysis}")
        
        emotion= analysis[0]['emotion'] #dic {emotion{}, dom_emo{}} choosing emo dict 
        sort_emo= sorted(emotion.items(), key= lambda x: x[1], reverse=True) # sorting on basis of items that has (angry, rate) n choosing rate

        dominant_emotion = analysis[0]['dominant_emotion']
        sec_emo= sort_emo[1][0] if len(sort_emo) > 1 else None # the second emo's name 
        cv2.putText(vdo, f'Feeling: {dominant_emotion} and {sec_emo}', (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2) #img, text, origin, font, fontsize, BRGcolor, thickness
        
        return dominant_emotion, sec_emo 
    except Exception as e:
        print(f"Error during emotion analysis: {e}")
        return None, None

def detect_mood(username, frame):
        print(f"Detecting mood for: {username}")
        # Detect emotion
        emo1, emo2 = analyze_mood_deepface(frame)        
        if emo1 and emo2:
            store_user_mood_data(username, emo1, emo2)
            
        return emo1, emo2

# if __name__== '__main__':
    # vdo_cap= cv2.VideoCapture(0)
    # while True:
    #         ret, vdo= vdo_cap.read()
    #         analyze_mood_deepface(vdo)

    #     # Show the frame
            
    #         cv2.imshow('Mood Recognition', vdo)
    #         if cv2.waitKey(10) & 0xFF== ord('q'):
    #                 break
    # vdo_cap.release()
    # cv2.destroyAllWindows()