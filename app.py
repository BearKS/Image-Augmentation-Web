import streamlit as st
import cv2 
from PIL import Image, ImageEnhance
import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator
from numpy import expand_dims

# Global Variables
width = 500
width_aug = 170


@st.cache
def load_image(img):
	im = Image.open(img)
	return im

def rgb_img(input_img):
    rgb_image = np.array(input_img.convert('RGB'))
    return rgb_image

def gray_img(input_img):
    gray_image = cv2.cvtColor(input_img, cv2.COLOR_RGB2GRAY)
    return gray_image

def augment_img(input_img):
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
		converted_img = rgb_img(image)
		col1, col2 = st.columns( [0.5, 0.5])
		with col1:
			st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
			st.image(image,width)  
	
		#Add conditional statements to take the user input values
		with col2:
			st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
			filter = st.sidebar.radio('Covert your photo to:', ['Original','Gray Image','Black and White', 'Pencil Sketch', 'Blur Effect', 'Generate Dataset'])
			if filter == 'Gray Image':
					gray_scale = gray_img(converted_img)
					st.image(gray_scale, width)
     
			elif filter == 'Black and White':
					gray_scale = gray_img(converted_img)
					slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
					(thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
					st.image(blackAndWhiteImage, width)
     
			elif filter == 'Pencil Sketch':
					gray_scale = gray_img(converted_img)
					inv_gray = 255 - gray_scale
					slider = st.sidebar.slider('Adjust the intensity', 25, 255, 125, step=2)
					blur_image = cv2.GaussianBlur(inv_gray, (slider,slider), 0, 0)
					sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
					st.image(sketch, width) 
     
			elif filter == 'Blur Effect':
					slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2) 
					converted_imgb = cv2.cvtColor(converted_img, cv2.COLOR_BGR2RGB)
					blur_image = cv2.GaussianBlur(converted_imgb, (slider,slider), 0, 0)
					st.image(blur_image, channels='BGR', width = width) 
     
			elif filter == 'Generate Dataset':
					isRandom = 'Generate Dataset'
					slider = st.sidebar.slider('Random Pics', 1, 100, 1, step=1)
					Npic = slider
					for i in range(0, Npic) :
						img_result = augment_img(converted_img)
						imgs.append(img_result)
					# st.markdown('<p style="text-align: center;">Results Below</p>',unsafe_allow_html=True)
			#Default Original Image
			else: 
					st.image(image, width)

		if isRandom == 'Generate Dataset':
			col1, col2, col3, col4 = st.columns( [3, 3, 3, 3]) 
			with col1:
				for i in range(0,len(imgs),4):
					st.image(imgs[i], channels='RGB', width=width_aug)
			with col2:
				for i in range(1,len(imgs),4):
					st.image(imgs[i], channels='RGB', width=width_aug) 
			with col3:
				for i in range(2,len(imgs),4):
					st.image(imgs[i], channels='RGB', width=width_aug) 
			with col4:
				for i in range(3,len(imgs),4):
					st.image(imgs[i], channels='RGB', width=width_aug)			

#Run code 
if __name__ == '__main__':
	main()