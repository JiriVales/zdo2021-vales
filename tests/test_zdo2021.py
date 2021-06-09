import pytest
import os
import skimage.io
from skimage.draw import polygon
import glob
import numpy as np
from pathlib import Path
import zdo2021.main
import sklearn.metrics

# cd ZDO2021
# python -m pytest

def test_run_random():
    vdd = zdo2021.main.VarroaDetector()

    # Nastavte si v operačním systém proměnnou prostředí 'VARROA_DATA_PATH' s cestou k datasetu.
    # Pokud není nastavena, využívá se testovací dataset tests/test_dataset
    dataset_path = os.getenv('VARROA_DATA_PATH_', default=Path(__file__).parent / 'test_dataset/')
    # dataset_path = Path(r"H:\biology\orig\zdo_varroa_detection_coco_001")

    # print(f'dataset_path = {dataset_path}')
    files = glob.glob(f'{dataset_path}/images/*.jpg')
    cislo_obrazku = np.random.randint(0, len(files))
    filename = files[cislo_obrazku]

    im = skimage.io.imread(filename)
    imgs = np.expand_dims(im, axis=0)
    # print(f"imgs.shape={imgs.shape}")
    prediction = vdd.predict(imgs)


    assert prediction.shape[0] == imgs.shape[0]


    # Toto se bude spouštět všude mimo GitHub
    if not os.getenv('CI'):
        import matplotlib.pyplot as plt
        plt.imshow(prediction[0])
        plt.show()

def test_run_all():
    vdd = zdo2021.main.VarroaDetector()

    # Nastavte si v operačním systém proměnnou prostředí 'VARROA_DATA_PATH' s cestou k datasetu.
    # Pokud není nastavena, využívá se testovací dataset tests/test_dataset
    dataset_path = os.getenv('VARROA_DATA_PATH_', default=Path(__file__).parent / 'test_dataset/')
    # dataset_path = Path(r"H:\biology\orig\zdo_varroa_detection_coco_001")

    # print(f'dataset_path = {dataset_path}')
    files = glob.glob(f'{dataset_path}/images/*.jpg')
    f1s = []
    for filename in files:
        im = skimage.io.imread(filename)
        imgs = np.expand_dims(im, axis=0)
        # print(f"imgs.shape={imgs.shape}")
        prediction = vdd.predict(imgs)

        import json
        ann_pth = Path(dataset_path)/"annotations/instances_default.json"
        assert ann_pth.exists()
        # gt_ann = json.loads(str(ann_pth))
        with open(ann_pth, 'r') as infile:
            gt_ann = json.load(infile)
        ground_true_mask = prepare_ground_true_mask(gt_ann, filename, dataset=True)
        f1i = f1score(ground_true_mask, prediction, im, show=True)
        # assert f1i > 0.55
        f1s.append(f1i)

    f1 = np.mean(f1s)
    print(f"f1score={f1}")
    # assert f1 > 0.55


def f1score(ground_true_mask:np.ndarray, prediction:np.ndarray, image=None, show=False):
    """
    Measure f1 score for one image
    :param ground_true_mask:
    :param prediction:
    :return:
    """
    if (ground_true_mask.shape[-1] == prediction.shape[-2]) and (ground_true_mask.shape[-2] == prediction.shape[-1]):
        print(f"Warning: Prediction shape [{ground_true_mask.shape}] does not fit ground true shape [{prediction.shape}]. Tansposition applied.")
        ground_true_mask=np.rot90(ground_true_mask, k=1)

    if ground_true_mask.shape[-1] != prediction.shape[-1]:
        raise ValueError(f"Prediction shape [{ground_true_mask.shape}] does not fit ground true shape [{prediction.shape}]")
    if ground_true_mask.shape[-2] != prediction.shape[-2]:
        raise ValueError(f"Prediction shape [{ground_true_mask.shape}] does not fit ground true shape [{prediction.shape}]")
    f1 = sklearn.metrics.f1_score(ground_true_mask.astype(bool).flatten(), prediction.astype(bool).flatten(), average="macro")

    if (image is not None) and show:
        from matplotlib import pyplot as plt
        plt.imshow(image)
        plt.contour(prediction[0,:,:], colors=['red'])
        plt.contour(ground_true_mask, color=['green'])
        plt.suptitle(f"f1score={f1}")
        plt.show()
    return f1


def prepare_ground_true_mask(gt_ann, filename, dataset=True):
    name = None
    for ann_im in gt_ann['images']:
        if  ann_im["file_name"] == Path(filename).name:
            # mask = np.zeros([], dtype=bool)
            M = np.zeros((ann_im["height"], ann_im["width"]), dtype=bool)
            immage_id = ann_im["id"]
            for ann in gt_ann['annotations']:
                if ann["image_id"] == immage_id:
                    S = ann['segmentation']
                    for s in S:
                        N = len(s)
                        rr, cc = polygon(np.array(s[1:N:2]), np.array(s[0:N:2]))  # (y, x)
                        M[rr, cc] = True

    if dataset:
        # M=M.transpose()
        M=np.rot90(M, k=3)
    return M
