# Stego Whiff
This is a simple program written in Python which allows you to hide and find a text message in a PNG image file. This is done by appending and searching the text after the [IEND chunk](http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html) in the PNG. <br />
You can add a password so the message will be encrypted. Hence you will need such password in case you want to find and unencrypt the message.
***
### Running the program
> Hide a message:
```
> stego-whiff -hide "this is the secret message" my-image.png
```
> Hide a message encrypted with a password:
```
> stego-whiff -hide "this is the secret message" -passwd "super secure pass" my-image.png
```
> Find a message:
```
> stego-whiff -find my-image.png
```
> Find an encrypted message
```
> stego-whiff -find -passwd "super secure passw" my-image.png
``` 
***
### Requirements
```
[cryptography] -> pip install cryptography
```