<img src="https://github.com/Gariscat/EMInf/blob/main/logo.png" alt="logo" width="384"/>

# loopy
An infrastructure for music information retrieval focusing on electronic music, especially for data synthesis and annotation. Our home page is [here](https://loopy4edm.com/). The paper is now under review by a multimedia venue. Essential components of this project (presets, samples) are available on [Google Drive](https://drive.google.com/drive/folders/1X-jArl_6DsBxZdXGL7wzgaVI4m6f8wiy)

P.S. Since the home page has expired, some demo are available on [SoundCloud](https://soundcloud.com/ca7ax-81464132/loopy-edm-data-generator-demo?si=491f9c07bdd14593a6b92405cc1dcb1d&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)

## Important facts

1. To maintain the quality of sounds, we use high sample rate 44100 instead of 22050.
2. For the same reason, we recommend using stereo wave (2D np.ndarray) instead of mono wave (1D).
3. The mel-spectrogram should be rendered with sr=44100 instead of 22050 (the current version didn't specify this argument). This should be fixed asap.
