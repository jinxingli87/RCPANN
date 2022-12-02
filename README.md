# RCPANN
Modeling ring current proton distribution using artificial neural network.
This model is based on RBSP/RBSPICE measurements from 2013-2018. The RBSPICE measures proton flux at 14 energy channels from 45 keV to 598 keV, and this model provides proton spin-averaged flux in those 14 energy channels.
The 'lws_training_display_v4.1.ipynb' demonstrates the training of the model, as well as the illustration of comparision between test dataset and predictions over long-term. The processed data are stored in 'rcpann_data_v1.0.zip'. Two additional subprograms are needed: 'time_double.string.py' which converts time formats and 'test_correlation.py' which plot comparison between test data and predictions.
To use this model, the users basically use 'rcpann_model_v1.0.ipynb', which load the model stored in 'rcpann_model_files.zip', and output the results (the log10 of flux in units of keV^-1c m^-2 s^-1). We also shows 4 examples of how to use this model. To simulate proton flux in a specific event, the uses also need the geomagnetic data stored in 'geomag_2012_2018.csv'.
Please contact jinxing.li.87@gmail.com for support.
