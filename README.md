# Stego Whiff
This is a simple program written in Python which allows you to hide or find text message in a PNG image file.<br/>
This is done by appending or searching the text after the IEND chunk in the PNG.

#### Running the program:
Hide a message:
```
stego-whiff.py -hide "this is the secret message" my-image.png
```
Find a message:
```
stego-whiff.py -find my-image.png
```

> To do: *add some encryption process into so the text message can't be seen easily* 