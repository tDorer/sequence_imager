README.md
##########################################################################################################################

--Guide--


This file contains all important information for the use of the sequence imager.

To use the program a working python version with numpy and matplotlib needs to be installed.
Then create a text file containing nothing but the sequence as a one letter code and name it "YourName.seq".
I added an "example.seq" and the resulting image.
Finally, simply extract the files, open a command prompt and execute the python script by navigating into the folder which contains the files and type:

	python3 plot.py

The program asks for some options to customize. Just enter the values without the '.

If your sequence does not work, please first try the example.seq. Is that works normally, please report the error.

There is also a notebook added to try around or track errors.


#############################################################################################################################


--example--

The example.seq file is plotted by open the command prompt and typing:

	python3 plot.py

The program will then ask:
"Please enter the name of your sequence file.
Do not enter the .seq ending."

Therefore just type:

	example
	
If you have stored a "parameter.csv" file in your folder the program will use that file. Otherwise you will be asked, which file to use. Here you need to enter the full file name, including the ending.

The program will then ask:
"Please enter here a number to decide the distance between the amino acids in the plot. The Default use is 0.06.
Just press Enter to use the default."

You can type any number or simply press Enter to use 0.06. I recommend to use numbers only between 0.04 and 0.08.

The program will then ask:
"Do you want to start your plot in the left corner? Please press Enter for that case, please type 'MIDDLE' if you want to start in the center."

Therefore type

	MIDDLE

if you want to start in the center. Any other action will start the plot in the left corner.

The program will then need some time to calculate and will finally ask if you want to see the plot directly. There will be a png file saved into the used folder in any case.






###############################################################################################################################


More information about the parameter file:


The parameter file contains the sizes of the spheres and their colors. The last line in the file is used to shift the letters to the middle of the spheres, it does sometimes not work perfectly if the sequence is very long. 
My parameter file is included in the archive it could be modified as wished, in general it should have the format:
	   
Aminoacid one letter code,size of the sphere (number between 0 and 1),hexadecimal color code for the amino acid,shift of the letter
	   
example:
R,0.656,#003050,0.101 
	   
I recommend to call this file parameter.csv otherwise you need to recall the filename later.
	
