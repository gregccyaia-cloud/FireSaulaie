def cp_steel(t):
 if t<600:return 425+.773*t-.00169*t*t+2.22e-6*t**3
 if t<735:return 666+13002/(738-t)
 if t<900:return 545+17820/(t-731)
 return 650.
