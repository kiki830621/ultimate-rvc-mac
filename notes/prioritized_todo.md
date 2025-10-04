# TODO list for the project

* implement a one-click training tab
  
* rework other settings tab
  * this should also contain other settings such as the ability to change the theme of the app
    * Add Support for changing theme in app?
  * there should be a button to apply settings which will reload the app with the new settings

* move all post processing from vocal conversion step to postprocessing step
  * this includes all the post-processing pedal effects from pedalboard but also the autotune effect that is implemented as part of vocal converson currently

* instead of having custom embedder models, just allow users to upload new embedder models which will be shown in the main embedder models dropdown (and perhaps also saved in the main embedder models dir?)

* linting with Ruff
* typechecking with Pyright
* running all tests
* automatic building and publishing of project to pypi
  * includes automatic update of project version number
* or use pre-commit?

* Could also include pypi package as a release on github

* need to make project version (in `pyproject.toml`) dynamic so that it is updated automatically when a new release is made

* add support for python 3.13.

* Add note about not using with VPN to README.md?

* application of different f0 extraction methods should also be done in parallel.

* The two pitch shifts operations that are currently executed sequentially should be executed in parallel because they are done on cpu

* need to fix issue with ports when using training:
  """
  torch.distributed.DistNetworkError: The server socket has failed to listen on any local network address. The server socket has failed to bind to [Christians-Desktop]:50376 (system error: 10013 - An attempt was made to access a socket in a way forbidden by its access permissions.). The server socket has failed to bind to Christians-Desktop:50376 (system error: 10013 - An attempt was made to access a socket in a way forbidden by its access permissions.).
  * other port when error occurs: 49865
  """
  * seems to be due to us choosing a port that is protected by windows when using torch.distributed for training. should figure out which port it is

* fix error on exiting server on linux after interrupting training:
  "/usr/lib/python3.12/multiprocessing/resource_tracker.py:254: UserWarning: resource_tracker: There appear to be 210 leaked semaphore objects to clean up at shutdown" warnings.warn('resource_tracker: There appear to be %d '

* optimize training pipeline steps for speed
  * dataset preprocessing and feature extraction is 10 sec faster for applio
  * training startup is 30 sec slower
* figure out way of making ./urvc commands execute faster
  * when ultimate rvc is downloaded as a pypi package the exposed commands are much faster so investigate this

* Add example audio files to use for testing
  * Should be located in `audio/examples`
  * could have sub-folders `input` and `output`
    * in `output` folder we have `output_audio.ext` files each with a corresponding `input_audio.json` file containing metadata explaining arguments used to generate output
    * We can then test that actual output is close enough to expected output using audio similarity metric.
* Setup unit testing framework using pytest
