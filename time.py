from time import gmtime, strftime
import time
print("\nGMT: "+time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime()))
print("Local: "+strftime("%a, %d %b %Y %H:%M:%S %Z\n"))