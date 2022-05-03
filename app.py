import streamlit as st
import cv2 
from PIL import Image, ImageEnhance
import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator
from numpy import expand_dims
from io import BytesIO
import sys
from pathlib import Path
from camera import orchestrator # Local Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

try:
	sys.path.remove(str(parent))
except ValueError:  # Already removed
	pass


VERSION = ".".join(st.__version__.split(".")[:2])

demo_pages = {
	"Take a Photo": orchestrator.show_examples,
}


# Global Variables
width = 700
width_aug = 280

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

def augment_img(input_img,input_rotate,input_w_shift,input_h_shift,input_shear,input_zoom,input_horizon,input_vertical):
	datagen = ImageDataGenerator( 
		rotation_range = input_rotate,
		width_shift_range = input_w_shift,
		height_shift_range = input_h_shift,
		shear_range = input_shear,
		zoom_range = input_zoom,
		horizontal_flip = input_horizon,
		vertical_flip = input_vertical,
		fill_mode = 'nearest')    
		
	img = expand_dims(input_img, axis=0)
	pic = datagen.flow(img, batch_size =1)
 
	batch = pic.next()
	result = batch[0].astype('uint8')
	return result

def draw_main_page():
	st.write(
		f"""
		# Web Application For Image Augmentation! 👋
		"""
	)

def main():
	Npic = 0
	imgs = []
	# btn = []
	isRandom = ''
	# photo = st.camera_input("First, take a picture...")
 	# photo = Image.fromarray(photo,'RGB')
  	# photo.save('./photo.png')
	st.sidebar.title("Image Augmentation")
	with st.sidebar.expander("About the App"):
		st.write("""
			Web Application สำหรับทำ Image Augmentation โดยใช้ Python \n  \n
			This web portal has been developed for educational purposes only. No intention to infringe any copyright or trademark.
		""")
		image = Image.open(r'./assets/logo.png') #Brand logo image (optional)
 #---------------------------------------------------------------------------------------------
	contributors = []

	# Draw sidebar
	pages = list(demo_pages.keys())

	if len(pages):
		pages.insert(0, "Upload ")
		st.sidebar.title(f"📸 BearKS")
		query_params = st.experimental_get_query_params()
		if "page" in query_params and query_params["page"][0] == "headliner":
			index = 1
		else:
			index = 0
		selected_demo = st.sidebar.radio("", pages, index, key="pages")
	else:
		selected_demo = "None"

	# Draw main page
	if selected_demo in demo_pages:
		uploaded_file = st.camera_input("take a picture...")
		# uploaded_file = np.array(uploaded_file).as
		# uploaded_file = Image.fromarray(uploaded_file, 'RGB')
		# uploaded_file.save('./photo.jpg')
	else:
		st.image(image,None,width=100) # Display logo
		st.header("Upload your image here...")
		#file uploader to allow users to upload photos
		uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
  
#---------------------------------------------------------------------------------------------

	# with Image.open('./assets/logo.png',"rb") as file:
	# 	btn = st.sidebar.download_button(
	# 			label="Download",data=file,file_name="flower.png",mime="image/png")
	#Header!
 
	if uploaded_file is not None:
		image = Image.open(uploaded_file)
		converted_img = rgb_img(image)
		col1, col2 = st.columns( [1, 1])
		with col1:
			st.subheader("Before")
			st.image(image,None,width)  
	
		#Add conditional statements to take the user input values
		with col2:
			st.subheader("After")
			filter = st.sidebar.radio('Covert your photo to:', ['Original','Gray Image','Black and White', 'Pencil Sketch', 'Blur Effect', 'Generate Dataset'])
			if filter == 'Gray Image':
					gray_scale = gray_img(converted_img)
					st.image(gray_scale,None, width)
					if st.button('Save Image'):
							gray_scale2 = Image.fromarray(gray_scale)
							gray_scale2.save('./result_dataset/gray_image.png') 
	 
			elif filter == 'Black and White':
					gray_scale = gray_img(converted_img)
					slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
					(thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
					st.image(blackAndWhiteImage,None, width)
					if st.button('Save Image'):
							blackAndWhiteImage2 = Image.fromarray(blackAndWhiteImage)
							blackAndWhiteImage2.save('./result_dataset/bw_image.png') 
	 
			elif filter == 'Pencil Sketch':
					gray_scale = gray_img(converted_img)
					inv_gray = 255 - gray_scale
					slider = st.sidebar.slider('Adjust the intensity', 25, 255, 125, step=2)
					blur_image = cv2.GaussianBlur(inv_gray, (slider,slider), 0, 0)
					sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
					st.image(sketch,None, width)
					if st.button('Save Image'):
							sketch2 = Image.fromarray(sketch)
							sketch2.save('./result_dataset/sketch_image.png') 
	 
			elif filter == 'Blur Effect':
					slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2) 
					converted_imgb = cv2.cvtColor(converted_img, cv2.COLOR_BGR2RGB)
					blur_image = cv2.GaussianBlur(converted_imgb, (slider,slider), 0, 0)
					blur_image2 = cv2.cvtColor(blur_image, cv2.COLOR_RGB2BGR)
					st.image(blur_image, channels='BGR', width = width) 
					if st.button('Save Image'):
							blur = Image.fromarray(blur_image2)
							blur.save('./result_dataset/blur_image.png')

	 
			elif filter == 'Generate Dataset':
					isRandom = 'Generate Dataset'
					Npic = st.sidebar.slider('Random Pics', 1, 100, 1, step=1)
					agree = st.sidebar.checkbox('Custom Random')
					if agree:
							st.sidebar.write('Edit Data Genarator!')
							rotate_int = st.sidebar.slider('Random Rotation', 1.0, 20.0, 1.0)
							wshift_int = st.sidebar.slider('Random Width Shift', 0.0, 0.2, 0.05)
							hshift_int = st.sidebar.slider('Random Height Shift', 0.0, 0.2, 0.05) 
							shear_int = st.sidebar.slider('Random Shear', 0.0, 0.2, 0.05)  
							zoom_int = st.sidebar.slider('Random Zoom', 0.0, 0.2, 0.05)
							htrue = st.sidebar.selectbox('Horizontal Flip',('True','False'))
							if htrue == 'True' :
								horizon = True     
							else :
								horizon = False    
							vtrue = st.sidebar.selectbox('Vertical Flip',('True','False'))
							if vtrue == 'True' :
								vertical = True     
							else :
								vertical = False  

					elif not agree: 
							rotate_int = 20
							wshift_int = 0.2 
							hshift_int = 0.2
							shear_int = 0.2 
							zoom_int = 0.2 
							horizon = True
							vertical = True 
					for i in range(0, Npic) :
						img_result = augment_img(converted_img,rotate_int,wshift_int,hshift_int,shear_int,zoom_int,horizon,vertical)
						imgs.append(img_result)
						# img_dataset = Image.fromarray(imgs[i], 'RGB')
						# img_dataset.save('./result_dataset/img'+ str(i) +'.jpg')
					st.image(imgs[0],None, width) 
					if st.button('Save Image'):
						for i in range(0, Npic):
							img_dataset = Image.fromarray(imgs[i], 'RGB')
							img_dataset.save('./result_dataset/img'+ str(i) +'.jpg')
					# img = Image.fromarray(imgs[0], 'RGB')
					# img.save('./result_dataset/my.png')
					# image2 = Image.open(r'./result_dataset/my.png')
					# buf = BytesIO()
					# image2.save(buf, format="png")
					# byte_im = buf.getvalue()
					# btn = st.sidebar.download_button(
					# 	label="Download Image",
					# 	data=byte_im,
					# 	file_name="img.jpeg",
					# 	mime="image/png",
					# 	)
	 
			#Default Original Image
			else: 
					st.image(image,None, width)
		# image = Image.open(r'./assets/logo.png')
		# buf = BytesIO()
		# image.save(buf, format="jpg")
		# byte_im = buf.getvalue()
		# btn = st.sidebar.download_button(
		# 	label="Download Image",
		# 	data=byte_im,
		# 	file_name="imagename.jpg",
		# 	mime="image/jpg",
		# 	)
		if isRandom == 'Generate Dataset':
			st.subheader("Other Results :")
			col1, col2, col3, col4, col5 = st.columns( [1, 1, 1, 1, 1]) 
			with col1:
				for i in range(1,len(imgs),5):
					st.image(imgs[i],None, width_aug)
			with col2:
				for i in range(2,len(imgs),5):
					st.image(imgs[i],None, width_aug) 
			with col3:
				for i in range(3,len(imgs),5):
					st.image(imgs[i],None, width_aug) 
			with col4:
				for i in range(4,len(imgs),5):
					st.image(imgs[i],None, width_aug)	
			with col5:
				for i in range(5,len(imgs),5):
					st.image(imgs[i],None, width_aug)     		
	
  
  
# !!!!!!!!Page Config!!!!!!!!!!!
st.set_page_config(
	layout="wide",
	page_title='เสี่ยโบ๊ตสั่งลุย',
	page_icon='./assets/logo.png'
)


#Run code 
if __name__ == '__main__':
	main()