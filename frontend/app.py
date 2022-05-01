import streamlit as st
import cv2 as cv
from PIL import Image, ImageEnhance
import numpy as np
import os

st.title("ทดลองใช้งาน")
st.write("ffffff")
st.write("fffffdddddf")
@st.cache
def load_image(img):
	im = Image.open(img)
	return im

def main():
	""" Face Detection App """

	st.title(" Face Detection and Editing App")

	activities = ["Detection","About"]
	choice = st.sidebar.selectbox("Select Activity",activities)

	if choice== 'Detection':
		st.subheader("Face Detection")

		image_file = st.file_uploader("Upload Image",type=['jpg','png','jpeg'])

		if image_file is not None:
			our_image = Image.open(image_file)
			st.text("Original Image")
			st.image(our_image)

		enhance_type = st.sidebar.radio("Enhance Type",["Original","Gray-Scale",
			"Contrast","Brightness","Blurring"])

		if enhance_type== 'Gray-Scale':
			new_img = np.array(our_image.convert('RGB'))
			img = cv.cvtColor(new_img,1)
			img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
			st.image(img)

		if enhance_type== 'Contrast':
			c_rate = st.sidebar.slider("Contrast",0.5,3.5)
			enhancer = ImageEnhance.Contrast(our_image)
			img_output = enhancer.enhance(c_rate)
			st.image(img_output)

		if enhance_type== 'Brightness':
			c_rate = st.sidebar.slider("Brightness",0.5,3.5)
			enhancer = ImageEnhance.Brightness(our_image)
			img_output = enhancer.enhance(c_rate)
			st.image(img_output)

		if enhance_type== 'Blurring':
			new_img = np.array(our_image.convert('RGB'))
			blur_rate = st.sidebar.slider("Blur Rate",0.5,3.5)
			img = cv.cvtColor(new_img,1)
			img = cv.GaussianBlur(img,(5,5),blur_rate)
			st.image(img)

		"""Face Detection"""

		task = ["Faces","Smiles","Eyes","Cannize","Cartoonize"]
		feature_choice = st.sidebar.selectbox("Find Features",task)
		if st.button("Process"):


if __name__ == '__main__':
	main()
 