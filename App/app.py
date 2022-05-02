import streamlit as st
import cv2 
from PIL import Image, ImageEnhance
import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator
from numpy import expand_dims
@st.cache
def load_image(img):
	im = Image.open(img)
	return im

def augment_img(input_img,slider):
	Npic = slider
	rotation_range = 20
	width_shift_range = 0.2 
	height_shift_range = 0.2
	shear_range = 0.2 
	zoom_range = 0.2 
	horizontal_flip = True 
	datagen = ImageDataGenerator( 
		rotation_range = rotation_range,
		width_shift_range = width_shift_range,
		height_shift_range = height_shift_range,
		shear_range = shear_range,
		zoom_range = zoom_range,
		horizontal_flip = horizontal_flip,
		fill_mode = 'nearest')    
		
	img = expand_dims(input_img, axis=0)
	pic = datagen.flow(img, batch_size =1)

	batch = pic.next()
	result = batch[0].astype('uint8')
	
	return result

def main():
    #Add a header and expander in side bar
	imgs = []
	isRandom = ''
	st.sidebar.markdown('<p class="font">My Photo Converter App</p>', unsafe_allow_html=True)
	with st.sidebar.expander("About the App"):
		st.write("""
			Use this simple app to convert your favorite photo to a pencil sketch, a grayscale image or an image with blurring effect.  \n  \nThis app was created by Sharone Li as a side project to learn Streamlit and computer vision. Hope you enjoy!
		""")
		image = Image.open(r'./assets/logo.jpg') #Brand logo image (optional)
	width = 500
	#Create two columns with different width
	col1, col2 = st.columns( [0.8, 0.2])
	with col1:               # To display the header text using css style
		st.markdown(""" <style> .font {
		font-size:35px ; font-family: 'fantasy'; color: #FF9633;} 
		</style> """, unsafe_allow_html=True)
		st.markdown('<p class="font">Upload your photo here...</p>', unsafe_allow_html=True)
		
	with col2:               # To display brand logo
		st.image(image,  width)
	#Add file uploader to allow users to upload photos
	uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
 
	#Add 'before' and 'after' columns
	if uploaded_file is not None:
		image = Image.open(uploaded_file)
		
		col1, col2 = st.columns( [0.5, 0.5])
		with col1:
			st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
			st.image(image,width)  
	
		#Add conditional statements to take the user input values
		with col2:
			st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
			filter = st.sidebar.radio('Covert your photo to:', ['Original','Gray Image','Black and White', 'Pencil Sketch', 'Blur Effect', 'Generate Dataset'])
			if filter == 'Gray Image':
					converted_img = np.array(image.convert('RGB'))
					gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
					st.image(gray_scale, width)
     
			elif filter == 'Black and White':
					converted_img = np.array(image.convert('RGB'))
					gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
					slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
					(thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
					st.image(blackAndWhiteImage, width)
     
			elif filter == 'Pencil Sketch':
					converted_img = np.array(image.convert('RGB')) 
					gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
					inv_gray = 255 - gray_scale
					slider = st.sidebar.slider('Adjust the intensity', 25, 255, 125, step=2)
					blur_image = cv2.GaussianBlur(inv_gray, (slider,slider), 0, 0)
					sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
					st.image(sketch, width) 
     
			elif filter == 'Blur Effect':
					converted_img = np.array(image.convert('RGB'))
					slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2) 
					converted_img = cv2.cvtColor(converted_img, cv2.COLOR_RGB2BGR)
					blur_image = cv2.GaussianBlur(converted_img, (slider,slider), 0, 0)
					st.image(blur_image, channels='BGR', width=500) 
			elif filter == 'Generate Dataset':
					isRandom = 'Generate Dataset'
					converted_img = np.array(image.convert('RGB'))
					slider = st.sidebar.slider('Random Pics', 1, 100, 1, step=1)
					for i in range(0, slider) :
						img_result = augment_img(converted_img,slider)
						imgs.append(img_result)
					# st.markdown('<p style="text-align: center;">Results Below</p>',unsafe_allow_html=True)
			else: 
					st.image(image, width)

		if isRandom == 'Generate Dataset':
			col1, col2, col3, col4 = st.columns( [2, 2, 2, 2]) 
			with col1:
				for i in range(0,len(imgs),4):
					st.image(imgs[i], channels='RGB', width=180)
			with col2:
				for i in range(1,len(imgs),4):
					st.image(imgs[i], channels='RGB', width=180) 
			with col3:
				for i in range(2,len(imgs),4):
					st.image(imgs[i], channels='RGB', width=180) 
			with col4:
				for i in range(3,len(imgs),4):
					st.image(imgs[i], channels='RGB', width=180)			

#Run code 
if __name__ == '__main__':
	main()