# Python / Anaconda

**This is basically the foundation of lab 4 (Group lab)**

Python is an interpreted language
- Being executed line-by-line similar to matlab - no compilation phase

Embedded systems typically use older versions of tools
The snickerdoodle hardware does not support the latest version of Python

Python does not use typical beginning and end identifiers, so python doesnt have ``{}`` or ``begin end``

```python
# functions begin with def
def functionHello():
	print("Hello from a function\n")
	
# main
def main():
	print("Hello from main")
	functionHello()
	
# ... except that you have to tell the python interpreter the name of 
# the "main" function to call
if __name__ == '__main__'
	main()
```

If there were no functions it would consider it a script and run it top to bottom
- Very similar to powershell scripts or bash scripts

## class example
```Python
import math

# Class to support complex numbers
class Complex:
	def __init(self, Real, Imag):
		self.real = Real
		self.imag = Imag
		
	def Magnitude(self):
		return math.sqrt(self.real * self.real + self.image * self.imag)
		
# Excercises complex class
def main():
	MyComplex - Complex(6.2, -3.14)
	print("Real Values={0}\n".format(MyComplex.real))
	print("Imaginary Value={0}\n".format(MyComplex.imag))
	print("Magnitude={0}\n".format(MyComplex.Magnitude()))
	
if __name__ == '__main__'
	main()
```

