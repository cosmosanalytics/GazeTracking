import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from gaze_tracking import GazeTracking

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.gaze = GazeTracking()

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        self.gaze.refresh(img)
        new_frame = self.gaze.annotated_frame()
        text = ""

        if self.gaze.is_right():
            text = "Looking right"
        elif self.gaze.is_left():
            text = "Looking left"
        elif self.gaze.is_center():
            text = "Looking center"

        cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
        
        return av.VideoFrame.from_ndarray(new_frame, format="bgr24")

def main():
    st.title("Gaze Tracking App")

    # webrtc_streamer(
    #     key="gaze_tracking",
    #     video_transformer_factory=VideoTransformer,
    #     async_transform=True,
    # )

    webrtc_streamer(
        key="example",
        video_processor_factory=VideoTransformer,
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        }
    )


if __name__ == "__main__":
    main()
