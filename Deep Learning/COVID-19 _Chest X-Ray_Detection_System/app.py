import  tensorflow as tf 
from keras.utils import load_img,img_to_array
import numpy as np

from flask import Flask,render_template,request

app=Flask(__name__)

# load Model 
model=tf.keras.models.load_model('deploy_chest_test.h5')

def predict_image(img_path):
    image=load_img(img_path,target_size=(64,64))
    image=img_to_array(image)
    image=np.expand_dims(image,axis=0)

    result=model.predict(image)

    for i in range(len(result)):
        if result[i]>=0.5:
            return 'PNEUMONIA'
        else:
            return "NORMAL"
@app.route('/',methods=['GET','POST'])

def home():
    if request.method=='POST':
        file=request.files['image']

        img_path='static/'+file.filename
        file.save(img_path)

        prediction=predict_image(img_path)

        return render_template('index.html',prediction=prediction,img_path=img_path)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(
        debug=False,
        use_reloader=False,
        port=5001
    )
