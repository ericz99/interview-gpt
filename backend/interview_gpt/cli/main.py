# from interview_gpt.core.recorder import recorder
import time

class Recorder:
   def __init__(self):
       self.is_active = True

   def something(self):
       while self.is_active:
           print("Doing something...")
           time.sleep(1)

   def stop(self):
       print('stopping')
       self.is_active = False

recorder = Recorder()
recorder.something()  # This will run the while loop until it's stopped
# Now, if you want to stop the loop from the outside, you can call
recorder.stop()