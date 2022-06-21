# Stego Whiff
This is a simple program written in Python which allows you to hide and find a text message in a PNG image file.<br/>
This is done by appending and searching the text after the IEND chunk in the PNG.

#### Running the program:
Hide a message:
```
stego-whiff -hide "this is the secret message" my-image.png
```
Find a message:
```
stego-whiff -find my-image.png
```
