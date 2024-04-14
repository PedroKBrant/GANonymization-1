from main import custom_preprocess, anonymize_directory
from lib.transform.facial_landmarks_478_transformer import FacialLandmarks478
from tqdm import tqdm
import os.path
import cv2
import numpy as np

def anon(model_path):
    model = model_path
    print(model)
    mesh_congiguration = model.split('/')[-1].split('.ckpt')[0]
    output = 'relatorio/02_experiment/results/'+ mesh_congiguration
    anonymize_directory(model, 'relatorio/02_experiment/original', output, mesh_congiguration)

def mesh(input, output):
    for file in tqdm(os.listdir(input), desc=f"Anonymizing from {input}"):
        file_path = os.path.join(input, file)
        img = cv2.imread(file_path)
        img = FacialLandmarks478()(img)
        os.makedirs(os.path.dirname(output), exist_ok=True)
        output_file = os.path.join(output, file)
        cv2.imwrite(output_file, img)

def concat(input_folder, mesh_folder, results_folder, parameter, output_folder):
    input_files = sorted(os.listdir(input_folder))
    mesh_files = sorted(os.listdir(os.path.join(mesh_folder, parameter)))
    results_files = sorted(os.listdir(os.path.join(results_folder, parameter)))

    for input_file, mesh_file, results_file in zip(input_files, mesh_files, results_files):
        input_img = cv2.imread(os.path.join(input_folder, input_file))
        mesh_img = cv2.imread(os.path.join(mesh_folder, parameter, mesh_file))
        results_img = cv2.imread(os.path.join(results_folder, parameter, results_file))

        # Resize images if needed to have the same dimensions
        input_img = cv2.resize(input_img, (mesh_img.shape[1], mesh_img.shape[0]))
        results_img = cv2.resize(results_img, (mesh_img.shape[1], mesh_img.shape[0]))

        # Concatenate images horizontally
        concatenated_img = np.concatenate((input_img, mesh_img, results_img), axis=1)

        # Save the concatenated image to the output folder
        output_file = os.path.join(output_folder, f"{input_file.split('.')[0]}.jpg")
        cv2.imwrite(output_file, concatenated_img)

def concat_vertically(input_folder1, input_folder2, input_folder3, output_folder):
    # Get a list of image filenames from each input folder
    filenames1 = os.listdir(input_folder1)
    filenames2 = os.listdir(input_folder2)
    filenames3 = os.listdir(input_folder3)

    # Iterate over the filenames in the first folder
    for filename1 in filenames1:
        # Check if the filename exists in the other two folders
        if filename1 in filenames2 and filename1 in filenames3:
            # Load images from all three folders
            image1 = cv2.imread(os.path.join(input_folder1, filename1))
            image2 = cv2.imread(os.path.join(input_folder2, filename1))
            image3 = cv2.imread(os.path.join(input_folder3, filename1))

            # Stack the images vertically
            result_image = cv2.vconcat([image1, image2, image3])

            # Save the concatenated image to the output folder
            cv2.imwrite(os.path.join(output_folder, filename1), result_image)
            print(f"Concatenated and saved {filename1} to {output_folder}")

def main(experiment):
    #models_name = ['00_pkb','02_iris_tesselation', '03_iris_no_tesselation']
    models_name = ['02_iris_tesselation']
    for model in models_name:
        anon(f'relatorio/{experiment}/models/{model}.ckpt')
        #mesh('relatorio/input', 'relatorio/02_mesh')
main('02_experiment')
#parameter = model_name[0]
#output_folder = f'relatorio/concat/{parameter}'
#concat('relatorio/input', 'relatorio/mesh', 'relatorio/results', parameter, output_folder)

#input_folder1 = f'relatorio/concat/{model_name[0]}'
#input_folder2 = f'relatorio/concat/{model_name[1]}'
#input_folder3 = f'relatorio/concat/{model_name[2]}'
#output_folder = f'relatorio/concat/final'


#concat_vertically(input_folder1, input_folder2, input_folder3, output_folder)


#TO DO automatize all methods based on the moedl_name array
#TO DO make FacialLandmarks mesh options as an hiperparameter


#anon('relatorio/models/03_iris_no_tesselation.ckpt')
#mesh('relatorio/input', 'relatorio/02_mesh')
