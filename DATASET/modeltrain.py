import tensorflow as tf
import os
from tensorflow.python.tools import freeze_graph

# Define the paths to the training and validation datasets
TRAIN_DIR = 'train'
VAL_DIR = 'val'

# Define the number of classes
NUM_CLASSES = 3

# Define the batch size and number of epochs
BATCH_SIZE = 32
NUM_EPOCHS = 10

# Define the input image size
IMAGE_SIZE = 200

# Define the paths to the label map and output model
LABEL_MAP_PATH = 'label_map.pbtxt'
OUTPUT_MODEL_PATH = 'exercise_detection_model'

# Load the label map
label_map = {'pushup': 1, 'squat': 2}
with open(LABEL_MAP_PATH, 'w') as f:
    for name, id in label_map.items():
        f.write('item {\n')
        f.write('  id: {}\n'.format(id))
        f.write('  name: \'{}\'\n'.format(name))
        f.write('}\n')

# Define the input pipeline for the training and validation datasets
train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE)

val_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    VAL_DIR,
    image_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE)

# Define the model architecture
model = tf.keras.applications.MobileNetV2(
    input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
    include_top=False,
    weights='imagenet')

x = model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dense(1024, activation='relu')(x)
x = tf.keras.layers.Dropout(0.5)(x)
x = tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')(x)

model = tf.keras.models.Model(inputs=model.input, outputs=x)

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(train_dataset,
          epochs=NUM_EPOCHS,
          validation_data=val_dataset)

# Save the model
tf.keras.models.save_model(model, OUTPUT_MODEL_PATH)

# Freeze the model
input_node_names = ['input_1']
output_node_names = ['dense_1/Softmax']
input_graph_path = os.path.join(OUTPUT_MODEL_PATH, 'saved_model.pb')
output_graph_path = os.path.join(OUTPUT_MODEL_PATH, 'frozen_inference_graph.pb')

input_saver_def_path = ""
input_binary = False
output_node_names = ",".join(output_node_names)
restore_op_name = "save/restore_all"
filename_tensor_name = "save/Const:0"
clear_devices = True

freeze_graph.freeze_graph(input_graph_path, input_saver_def_path,
                          input_binary, "", output_node_names,
                          restore_op_name, filename_tensor_name,
                          output_graph_path, clear_devices, "")