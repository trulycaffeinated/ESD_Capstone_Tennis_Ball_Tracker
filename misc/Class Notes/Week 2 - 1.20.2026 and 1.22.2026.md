# Matlab Intro, Image Generation, Plotting, and Stereo Imaging

Matlab environment is inherently interpretive
- Commands are entered, interpreted and operations are performed immediately

By default everything is a **double** (64 bits)

---
**Perfect Number Example**
```Vectorized_C
function [Result] = Perfect(candidate)
% Determine whether the number passed in is a perfect number or not

% Calculate the sum of the Candidates divisors
Sum = 0;
for Divisor = (Candidate-1):-1:1
	if(rem(Candidate, Divisor) == 0)
		Sum = Sum + Divisor;
	end
end

%
if (Sum == Divisor)
	Result = 1;
else
	Result = 0;
end
```
---

Images don't contain floating point numbers, they are 16 bit (or 8 bit) integers. 
Everything in Matlab is an array or matrixed stored as \[Row Col\]

Because everything is a matrix, multiplication is by default matrix multiplication
- Element by element multiplication is ".\*"
- Matrix multiplication is "\*"

# Peter Corke's Spatial Math Toolbox
Stereo imaging we focus on a point (P), with two cameras a left ($P_L$) and right ($P_R$)
From those cameras we an triangulate $Z_P$ using $X_L$ and $X_R$ 
What happens if $Y_L \neq Y_R$ ? Math gets a lot harder
- This may happen with cameras outside in the wind
- **Specifications should include how accurate our system is to *x* amount of wind 
  (Changes in $\Delta Y$)**

Need to install Peter Corke's...
- Robotics Toolbox
- Machine Vision Toolbox